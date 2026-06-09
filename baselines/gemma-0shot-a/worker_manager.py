"""
Worker Manager for Parallel Gemma Evaluation
===========================================

Manages multiple GPU workers for efficient parallel processing.
"""

import json
import time
import queue
import threading
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from pathlib import Path
import torch
import torch.multiprocessing as mp
from transformers import AutoTokenizer, AutoModelForCausalLM


@dataclass
class EvaluationTask:
    """Single evaluation task for a worker."""
    sample_id: str
    conversation: Dict[str, Any]
    policy_text: str
    
    
@dataclass 
class EvaluationResult:
    """Result from processing a single sample."""
    sample_id: str
    prediction: str  # "YES" or "NO"
    confidence: float
    response_text: str
    processing_time: float
    error: Optional[str] = None


class GemmaWorker:
    """Single worker process for Gemma evaluation."""
    
    def __init__(self, worker_id: int, gpu_id: int, model_name: str = "google/gemma-1.1-2b-it"):
        self.worker_id = worker_id
        self.gpu_id = gpu_id
        self.model_name = model_name
        self.device = f"cuda:{gpu_id}"
        
        # Load model and tokenizer
        self.tokenizer = None
        self.model = None
        self._load_model()
    
    def _load_model(self):
        """Load Gemma model on assigned GPU."""
        try:
            torch.cuda.set_device(self.gpu_id)
            
            # Get HuggingFace token from environment
            import os
            hf_token = os.environ.get('HF_TOKEN') or os.environ.get('HUGGING_FACE_HUB_TOKEN')
            
            self.tokenizer = AutoTokenizer.from_pretrained(
                self.model_name,
                token=hf_token
            )
            self.model = AutoModelForCausalLM.from_pretrained(
                self.model_name,
                torch_dtype=torch.float16,
                device_map={"": self.device},
                low_cpu_mem_usage=True,
                token=hf_token
            )
            
            # Add pad token if missing
            if self.tokenizer.pad_token is None:
                self.tokenizer.pad_token = self.tokenizer.eos_token
                
        except Exception as e:
            raise RuntimeError(f"Worker {self.worker_id} failed to load model on GPU {self.gpu_id}: {e}")
    
    def format_transcript(self, transcript: List[Dict]) -> str:
        """Format transcript to readable text."""
        formatted_parts = []
        for utterance in transcript:
            speaker = utterance.get('speaker', 'Unknown')
            text = utterance.get('text', '')
            formatted_parts.append(f"{speaker}: {text}")
        return "\n".join(formatted_parts)
    
    def create_prompt(self, conversation: Dict[str, Any], policy_text: str) -> str:
        """Create zero-shot evaluation prompt."""
        transcript_text = self.format_transcript(conversation.get('cumulative_transcript', []))
        
        prompt = f"""You are a fraud detection expert. Analyze the following phone conversation against the given policies to determine if it contains fraudulent activity.

POLICIES:
{policy_text}

CONVERSATION:
{transcript_text}

TASK: Based on the policies above, is this conversation fraudulent?

Think step by step:
1. Identify any policy violations in the conversation
2. Look for pressure tactics, urgency, or requests for sensitive information
3. Consider if the agent is following legitimate procedures

Answer with only YES (fraudulent) or NO (legitimate), followed by a brief explanation.

ANSWER:"""
        
        return prompt
    
    def evaluate_sample(self, task: EvaluationTask) -> EvaluationResult:
        """Evaluate a single conversation sample."""
        start_time = time.time()
        
        try:
            # Create prompt
            prompt = self.create_prompt(task.conversation, task.policy_text)
            
            # Tokenize
            inputs = self.tokenizer(
                prompt,
                return_tensors="pt",
                max_length=2048,
                truncation=True,
                padding=True
            ).to(self.device)
            
            # Generate response
            with torch.no_grad():
                outputs = self.model.generate(
                    **inputs,
                    max_new_tokens=150,
                    do_sample=True,
                    temperature=0.1,
                    pad_token_id=self.tokenizer.eos_token_id,
                    eos_token_id=self.tokenizer.eos_token_id
                )
            
            # Decode response
            response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            
            # Extract the answer part (after "ANSWER:")
            if "ANSWER:" in response:
                answer_part = response.split("ANSWER:")[-1].strip()
            else:
                answer_part = response.strip()
            
            # Parse prediction
            prediction = "NO"  # Default to legitimate
            confidence = 0.5
            
            if answer_part.upper().startswith("YES"):
                prediction = "YES"
                confidence = 0.8
            elif answer_part.upper().startswith("NO"):
                prediction = "NO"
                confidence = 0.8
            else:
                # Try to find YES/NO in the response
                answer_upper = answer_part.upper()
                if "YES" in answer_upper and "NO" not in answer_upper:
                    prediction = "YES"
                    confidence = 0.6
                elif "NO" in answer_upper and "YES" not in answer_upper:
                    prediction = "NO"
                    confidence = 0.6
                else:
                    # Ambiguous - default to NO with low confidence
                    prediction = "NO"
                    confidence = 0.3
            
            processing_time = time.time() - start_time
            
            return EvaluationResult(
                sample_id=task.sample_id,
                prediction=prediction,
                confidence=confidence,
                response_text=answer_part[:500],  # Limit response length
                processing_time=processing_time
            )
            
        except Exception as e:
            processing_time = time.time() - start_time
            return EvaluationResult(
                sample_id=task.sample_id,
                prediction="NO",
                confidence=0.0,
                response_text="",
                processing_time=processing_time,
                error=str(e)
            )


def worker_process(worker_id: int, gpu_id: int, task_queue: mp.Queue, 
                  result_queue: mp.Queue, tui_queue: mp.Queue, model_name: str):
    """Worker process function for multiprocessing."""
    try:
        # Initialize worker
        worker = GemmaWorker(worker_id, gpu_id, model_name)
        
        # Notify TUI of successful initialization
        tui_queue.put({
            'type': 'worker_update',
            'worker_id': worker_id,
            'status': 'Running',
            'gpu_id': gpu_id
        })
        
        processed_count = 0
        error_count = 0
        total_time = 0.0
        
        while True:
            try:
                # Get task with timeout
                task = task_queue.get(timeout=1.0)
                
                if task is None:  # Shutdown signal
                    break
                
                # Process task
                result = worker.evaluate_sample(task)
                result_queue.put(result)
                
                # Update statistics
                processed_count += 1
                total_time += result.processing_time
                if result.error:
                    error_count += 1
                
                avg_time = total_time / processed_count
                
                # Update TUI
                tui_queue.put({
                    'type': 'worker_update',
                    'worker_id': worker_id,
                    'processed': processed_count,
                    'errors': error_count,
                    'avg_time': avg_time
                })
                
            except queue.Empty:
                # Timeout - check if we should continue
                continue
            except Exception as e:
                error_count += 1
                tui_queue.put({
                    'type': 'worker_update',
                    'worker_id': worker_id,
                    'status': 'Error',
                    'errors': error_count
                })
                # Continue processing other tasks
                continue
        
        # Worker finished
        tui_queue.put({
            'type': 'worker_update',
            'worker_id': worker_id,
            'status': 'Completed'
        })
        
    except Exception as e:
        tui_queue.put({
            'type': 'worker_update',
            'worker_id': worker_id,
            'status': 'Error'
        })
        raise


class WorkerManager:
    """Manages multiple worker processes for parallel evaluation."""
    
    def __init__(self, num_workers: int, model_name: str = "google/gemma-1.1-2b-it"):
        self.num_workers = num_workers
        self.model_name = model_name
        
        # Check GPU availability
        if not torch.cuda.is_available():
            raise RuntimeError("CUDA not available. GPU required for Gemma evaluation.")
        
        self.num_gpus = torch.cuda.device_count()
        if self.num_gpus == 0:
            raise RuntimeError("No CUDA GPUs detected.")
        
        print(f"Detected {self.num_gpus} GPU(s), using {min(num_workers, self.num_gpus)} workers")
        
        # Adjust workers to available GPUs
        self.num_workers = min(num_workers, self.num_gpus)
        
        # Multiprocessing queues
        self.task_queue = mp.Queue()
        self.result_queue = mp.Queue()
        self.tui_queue = mp.Queue()
        
        # Worker processes
        self.workers = []
        self.running = False
    
    def start_workers(self):
        """Start all worker processes."""
        self.running = True
        
        for worker_id in range(self.num_workers):
            gpu_id = worker_id % self.num_gpus
            
            process = mp.Process(
                target=worker_process,
                args=(worker_id, gpu_id, self.task_queue, self.result_queue, 
                      self.tui_queue, self.model_name),
                daemon=True
            )
            
            self.workers.append(process)
            process.start()
        
        # Wait a moment for workers to initialize
        time.sleep(2)
    
    def add_tasks(self, tasks: List[EvaluationTask]):
        """Add tasks to the queue."""
        for task in tasks:
            self.task_queue.put(task)
    
    def get_results(self, timeout: float = 1.0) -> List[EvaluationResult]:
        """Get all available results."""
        results = []
        
        while True:
            try:
                result = self.result_queue.get(timeout=timeout)
                results.append(result)
            except queue.Empty:
                break
        
        return results
    
    def get_tui_updates(self) -> List[Dict]:
        """Get TUI updates from workers."""
        updates = []
        
        while True:
            try:
                update = self.tui_queue.get_nowait()
                updates.append(update)
            except queue.Empty:
                break
        
        return updates
    
    def shutdown(self):
        """Shutdown all workers."""
        self.running = False
        
        # Send shutdown signals
        for _ in range(self.num_workers):
            self.task_queue.put(None)
        
        # Wait for workers to finish
        for worker in self.workers:
            worker.join(timeout=5.0)
            if worker.is_alive():
                worker.terminate()
        
        # Clear queues
        while not self.task_queue.empty():
            try:
                self.task_queue.get_nowait()
            except:
                break
        
        while not self.result_queue.empty():
            try:
                self.result_queue.get_nowait()
            except:
                break
    
    def is_finished(self) -> bool:
        """Check if all workers are finished processing."""
        return self.task_queue.empty() and all(not w.is_alive() for w in self.workers)