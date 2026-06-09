"""
Gemma Zero-Shot Fraud Detection Evaluation (Step 0a)
===================================================

Tests Gemma 1.1 2B model on fraud detection using only:
- Policy text from scenarios
- Full conversation transcripts
- Zero-shot reasoning (no training examples)

Features:
- Parallel GPU processing for speed
- Real-time TUI with worker monitoring
- Comprehensive evaluation metrics
- Robust error handling and recovery

Usage:
    python test_gemma_0shot.py --data_dir ../../output/training_data \
                              --num_workers 4 \
                              --batch_size 16 \
                              --max_samples 1000
"""

import json
import os
import sys
import time
import argparse
from pathlib import Path
from typing import List, Dict, Any
from datetime import datetime
from collections import defaultdict

import pandas as pd
import numpy as np
from tqdm import tqdm
from sklearn.metrics import (
    accuracy_score, precision_recall_fscore_support,
    confusion_matrix, classification_report
)

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent.parent))

from worker_manager import WorkerManager, EvaluationTask, EvaluationResult
from tui_display import WorkerTUI


def load_conversation_data(data_dir: str, max_samples: int = None) -> List[Dict[str, Any]]:
    """
    Load conversation data from training_data directory.
    
    Args:
        data_dir: Path to training_data directory
        max_samples: Maximum number of samples to load
        
    Returns:
        List of conversation dictionaries
    """
    print(f"Loading conversation data from: {data_dir}")
    
    data_path = Path(data_dir)
    if not data_path.exists():
        raise FileNotFoundError(f"Data directory not found: {data_dir}")
    
    conversations = []
    batch_dirs = sorted([d for d in data_path.iterdir() if d.is_dir() and d.name.startswith('batch_')])
    
    print(f"Found {len(batch_dirs)} batch directories")
    
    for batch_dir in tqdm(batch_dirs, desc="Loading batches"):
        conv_files = list(batch_dir.glob("*.json"))
        
        for conv_file in conv_files:
            try:
                with open(conv_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                # Skip if missing required fields
                if 'cumulative_transcript' not in data or 'final_verdict' not in data:
                    continue
                
                conversations.append(data)
                
                # Stop if reached max_samples
                if max_samples and len(conversations) >= max_samples:
                    return conversations
                    
            except Exception as e:
                print(f"Warning: Error loading {conv_file}: {e}")
                continue
    
    print(f"Loaded {len(conversations)} conversations")
    
    # Log class distribution only if we have conversations
    if conversations:
        fraud_count = sum(1 for c in conversations if c.get('final_verdict') == 'YES')
        legit_count = len(conversations) - fraud_count
        print(f"Class distribution:")
        print(f"  Fraud (YES): {fraud_count} ({fraud_count/len(conversations)*100:.2f}%)")
        print(f"  Legit (NO):  {legit_count} ({legit_count/len(conversations)*100:.2f}%)")
    else:
        print("Warning: No conversations found")
    
    return conversations


def extract_policy_text(conversation: Dict[str, Any]) -> str:
    """Extract policy text from conversation scenario."""
    scenario = conversation.get('scenario', {})
    policy = scenario.get('policy', '')
    
    if not policy:
        # Fallback to general fraud policies
        policy = """
Rule A: Agents must NEVER ask for passwords, PINs, OTPs, or other sensitive authentication information
Rule B: Agents must NEVER request immediate fund transfers or payments
Rule C: Agents must properly identify themselves and their organization
Rule D: Agents must NOT use high-pressure tactics or create false urgency
Rule E: Agents must NOT make unrealistic promises or guarantees
        """.strip()
    
    return policy


def create_evaluation_tasks(conversations: List[Dict[str, Any]]) -> List[EvaluationTask]:
    """Create evaluation tasks from conversations."""
    tasks = []
    
    for i, conv in enumerate(conversations):
        policy_text = extract_policy_text(conv)
        
        task = EvaluationTask(
            sample_id=f"sample_{i:06d}",
            conversation=conv,
            policy_text=policy_text
        )
        tasks.append(task)
    
    return tasks


def calculate_metrics(results: List[EvaluationResult], conversations: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Calculate comprehensive evaluation metrics."""
    
    # Filter out error results
    valid_results = [r for r in results if r.error is None]
    error_count = len(results) - len(valid_results)
    
    if not valid_results:
        return {'error': 'No valid results to evaluate'}
    
    # Extract predictions and labels
    predictions = []
    true_labels = []
    confidences = []
    processing_times = []
    
    # Create mapping from sample_id to conversation
    conv_map = {f"sample_{i:06d}": conv for i, conv in enumerate(conversations)}
    
    for result in valid_results:
        if result.sample_id in conv_map:
            conv = conv_map[result.sample_id]
            true_label = 1 if conv.get('final_verdict') == 'YES' else 0
            pred_label = 1 if result.prediction == 'YES' else 0
            
            predictions.append(pred_label)
            true_labels.append(true_label)
            confidences.append(result.confidence)
            processing_times.append(result.processing_time)
    
    if not predictions:
        return {'error': 'No valid predictions found'}
    
    # Calculate standard metrics
    accuracy = accuracy_score(true_labels, predictions)
    precision, recall, f1, _ = precision_recall_fscore_support(
        true_labels, predictions, average='binary', zero_division=0
    )
    cm = confusion_matrix(true_labels, predictions)
    
    # Calculate additional metrics
    avg_confidence = np.mean(confidences)
    avg_processing_time = np.mean(processing_times)
    
    # Per-class analysis
    fraud_indices = [i for i, label in enumerate(true_labels) if label == 1]
    legit_indices = [i for i, label in enumerate(true_labels) if label == 0]
    
    fraud_accuracy = accuracy_score(
        [true_labels[i] for i in fraud_indices],
        [predictions[i] for i in fraud_indices]
    ) if fraud_indices else 0.0
    
    legit_accuracy = accuracy_score(
        [true_labels[i] for i in legit_indices],
        [predictions[i] for i in legit_indices]
    ) if legit_indices else 0.0
    
    return {
        'overall_metrics': {
            'accuracy': float(accuracy),
            'precision': float(precision),
            'recall': float(recall),
            'f1': float(f1),
            'total_samples': len(predictions),
            'total_errors': error_count,
            'error_rate': error_count / len(results),
            'confusion_matrix': cm.tolist()
        },
        'class_specific': {
            'fraud_samples': len(fraud_indices),
            'fraud_accuracy': float(fraud_accuracy),
            'legit_samples': len(legit_indices),
            'legit_accuracy': float(legit_accuracy)
        },
        'performance': {
            'avg_confidence': float(avg_confidence),
            'avg_processing_time': float(avg_processing_time),
            'total_processing_time': float(sum(processing_times))
        }
    }


def save_results(results: List[EvaluationResult], conversations: List[Dict[str, Any]], 
                metrics: Dict[str, Any], output_dir: str):
    """Save results to files."""
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)
    
    # Save detailed results
    results_data = []
    conv_map = {f"sample_{i:06d}": conv for i, conv in enumerate(conversations)}
    
    for result in results:
        conv = conv_map.get(result.sample_id, {})
        true_label = conv.get('final_verdict', 'UNKNOWN')
        
        results_data.append({
            'sample_id': result.sample_id,
            'true_label': true_label,
            'predicted_label': result.prediction,
            'confidence': result.confidence,
            'processing_time': result.processing_time,
            'correct': (true_label == result.prediction),
            'error': result.error,
            'response_preview': result.response_text[:200] if result.response_text else ''
        })
    
    # Save to CSV
    df = pd.DataFrame(results_data)
    df.to_csv(output_path / 'detailed_results.csv', index=False)
    
    # Save metrics to JSON
    with open(output_path / 'metrics.json', 'w') as f:
        json.dump(metrics, f, indent=2)
    
    # Save summary
    summary = {
        'model': 'google/gemma-1.1-2b-it',
        'evaluation_type': 'zero_shot',
        'timestamp': datetime.now().isoformat(),
        'total_samples': len(results),
        'successful_predictions': len([r for r in results if r.error is None]),
        'key_metrics': metrics.get('overall_metrics', {})
    }
    
    with open(output_path / 'summary.json', 'w') as f:
        json.dump(summary, f, indent=2)
    
    print(f"\nResults saved to: {output_path}")
    print(f"  - detailed_results.csv: Per-sample predictions")
    print(f"  - metrics.json: Complete evaluation metrics")
    print(f"  - summary.json: High-level summary")


def main():
    parser = argparse.ArgumentParser(description='Gemma Zero-Shot Fraud Detection Evaluation')
    
    # Data arguments
    parser.add_argument('--data_dir', type=str, 
                       default='../../output/training_data',
                       help='Path to training_data directory')
    parser.add_argument('--max_samples', type=int, default=None,
                       help='Maximum number of samples to evaluate')
    
    # Model arguments
    parser.add_argument('--model_name', type=str, 
                       default='google/gemma-1.1-2b-it',
                       help='HuggingFace model name')
    
    # Processing arguments
    parser.add_argument('--num_workers', type=int, default=4,
                       help='Number of parallel workers')
    parser.add_argument('--batch_size', type=int, default=16,
                       help='Batch size for processing')
    
    # Output arguments
    parser.add_argument('--output_dir', type=str, default='./results',
                       help='Output directory for results')
    
    args = parser.parse_args()
    
    print(f"\n{'='*60}")
    print("Gemma Zero-Shot Fraud Detection Evaluation")
    print(f"{'='*60}")
    print(f"Model: {args.model_name}")
    print(f"Workers: {args.num_workers}")
    print(f"Data: {args.data_dir}")
    print(f"Max samples: {args.max_samples or 'All'}")
    print(f"Output: {args.output_dir}")
    print(f"{'='*60}\n")
    
    # Load data
    conversations = load_conversation_data(args.data_dir, args.max_samples)
    
    if not conversations:
        print("No conversations loaded. Exiting.")
        return 1
    
    # Create tasks
    tasks = create_evaluation_tasks(conversations)
    print(f"Created {len(tasks)} evaluation tasks")
    
    # Initialize TUI
    tui = WorkerTUI(args.num_workers, len(tasks))
    tui.start_display_thread()
    
    # Initialize worker manager
    try:
        worker_manager = WorkerManager(args.num_workers, args.model_name)
        worker_manager.start_workers()
        
        # Add all tasks
        worker_manager.add_tasks(tasks)
        
        # Process results
        all_results = []
        processed_count = 0
        
        start_time = time.time()
        
        while processed_count < len(tasks):
            # Get new results
            new_results = worker_manager.get_results(timeout=0.5)
            all_results.extend(new_results)
            processed_count = len(all_results)
            
                # Process TUI updates
            tui_updates = worker_manager.get_tui_updates()
            for update in tui_updates:
                if update['type'] == 'worker_update':
                    tui.update_worker(
                        worker_id=update['worker_id'],
                        status=update.get('status'),
                        processed=update.get('processed'),
                        errors=update.get('errors'),
                        avg_time=update.get('avg_time'),
                        gpu_id=update.get('gpu_id')
                    )
            
            # Update accuracy if we have results
            if all_results:
                valid_results = [r for r in all_results if r.error is None]
                if valid_results:
                    conv_map = {f"sample_{i:06d}": conv for i, conv in enumerate(conversations)}
                    correct = 0
                    total = 0
                    
                    for result in valid_results:
                        if result.sample_id in conv_map:
                            conv = conv_map[result.sample_id]
                            true_label = conv.get('final_verdict', 'NO')
                            if true_label == result.prediction:
                                correct += 1
                            total += 1
                    
                    if total > 0:
                        tui.update_accuracy(correct, total)
            
            time.sleep(0.1)
        
        total_time = time.time() - start_time
        
        # Shutdown workers
        worker_manager.shutdown()
        tui.stop()
        
        print(f"\nEvaluation completed in {total_time:.2f} seconds")
        print(f"Processed {len(all_results)} samples")
        
        # Calculate metrics
        metrics = calculate_metrics(all_results, conversations)
        
        if 'error' in metrics:
            print(f"Error calculating metrics: {metrics['error']}")
            return 1
        
        # Display results
        print(f"\n{'='*60}")
        print("EVALUATION RESULTS")
        print(f"{'='*60}")
        
        overall = metrics['overall_metrics']
        print(f"Overall Performance:")
        print(f"   Accuracy:  {overall['accuracy']*100:.2f}%")
        print(f"   Precision: {overall['precision']*100:.2f}%")
        print(f"   Recall:    {overall['recall']*100:.2f}%")
        print(f"   F1-Score:  {overall['f1']*100:.2f}%")
        
        cm = overall['confusion_matrix']
        print(f"\nConfusion Matrix:")
        print(f"   TN: {cm[0][0]:4d}  FP: {cm[0][1]:4d}")
        print(f"   FN: {cm[1][0]:4d}  TP: {cm[1][1]:4d}")
        
        performance = metrics['performance']
        print(f"\nPerformance:")
        print(f"   Avg processing time: {performance['avg_processing_time']:.2f}s/sample")
        print(f"   Avg confidence:     {performance['avg_confidence']:.3f}")
        print(f"   Error rate:         {overall['error_rate']*100:.2f}%")
        
        # Comparison with trained models (if available)
        print(f"\nComparison with Trained Models:")
        print(f"   Gemma Zero-Shot:    F1 = {overall['f1']*100:.2f}%")
        print(f"   RoBERTa 2a (In):    F1 = 98.45%")
        print(f"   RoBERTa 2b (In):    F1 = 95.59%")
        print(f"   Performance Gap:    {overall['f1']*100 - 98.45:.2f}% vs 2a")
        
        # Save results
        save_results(all_results, conversations, metrics, args.output_dir)
        
        print(f"\n{'='*60}")
        print("Evaluation complete")
        print(f"{'='*60}\n")
        
        return 0
        
    except KeyboardInterrupt:
        print("\n\nEvaluation interrupted by user")
        worker_manager.shutdown()
        tui.stop()
        return 1
        
    except Exception as e:
        print(f"\n\nError during evaluation: {e}")
        if 'worker_manager' in locals():
            worker_manager.shutdown()
        if 'tui' in locals():
            tui.stop()
        return 1


if __name__ == '__main__':
    # Set multiprocessing start method
    import torch.multiprocessing as mp
    mp.set_start_method('spawn', force=True)
    
    exit(main())