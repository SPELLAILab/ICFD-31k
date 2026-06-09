"""
RoBERTa Streaming Baseline Training Script

Trains RoBERTa-base on chunk-level data for streaming fraud detection.

Usage:
    python train_roberta_streaming.py --data_dir ../../output/training_data \\
                                       --output_dir ./models \\
                                       --results_dir ./results \\
                                       --batch_size 4 \\
                                       --epochs 5
"""

import json
import os
import sys
from pathlib import Path
from typing import Dict, List, Tuple, Any
from datetime import datetime
from collections import defaultdict
import argparse
import logging

import numpy as np
import pandas as pd
from tqdm import tqdm
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score, precision_recall_fscore_support,
    confusion_matrix, classification_report
)

import torch
from torch.utils.data import Dataset
import transformers
from transformers import (
    RobertaTokenizer, RobertaForSequenceClassification,
    TrainingArguments, Trainer, EarlyStoppingCallback
)

# Set up detailed logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/training.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)


class FraudChunkDataset(Dataset):
    """
    PyTorch Dataset for fraud detection from conversation chunks.
    
    Each sample is a cumulative transcript up to a specific timestamp
    with a binary fraud label (YES=1, NO=0).
    """
    
    def __init__(self, chunks: List[Dict], tokenizer: RobertaTokenizer, max_length: int = 512):
        """
        Args:
            chunks: List of chunk dictionaries with 'text' and 'label' keys
            tokenizer: RoBERTa tokenizer for text encoding
            max_length: Maximum sequence length for truncation
        """
        self.chunks = chunks
        self.tokenizer = tokenizer
        self.max_length = max_length
        
        logger.info(f"Created dataset with {len(chunks)} chunks")
        logger.info(f"Max sequence length: {max_length}")
    
    def __len__(self):
        return len(self.chunks)
    
    def __getitem__(self, idx):
        chunk = self.chunks[idx]
        
        # Tokenize text
        encoding = self.tokenizer(
            chunk['text'],
            truncation=True,
            padding='max_length',
            max_length=self.max_length,
            return_tensors='pt'
        )
        
        return {
            'input_ids': encoding['input_ids'].squeeze(),
            'attention_mask': encoding['attention_mask'].squeeze(),
            'labels': torch.tensor(chunk['label'], dtype=torch.long)
        }


def format_transcript(transcript: List[Dict]) -> str:
    """
    Convert cumulative transcript list to formatted string.
    
    Args:
        transcript: List of utterances with speaker, text, timestamp_end
        
    Returns:
        Formatted string: "Agent: ... Customer: ... Agent: ..."
    """
    formatted_parts = []
    for utterance in transcript:
        speaker = utterance.get('speaker', 'Unknown')
        text = utterance.get('text', '')
        formatted_parts.append(f"{speaker}: {text}")
    
    return " ".join(formatted_parts)


def load_chunk_data(data_dir: str, max_samples: int = None) -> List[Dict]:
    """
    Load all pre-chunked data from training_data directory.
    
    Args:
        data_dir: Path to training_data directory with batch folders
        max_samples: Optional limit on total samples (for testing)
        
    Returns:
        List of chunk dictionaries with keys:
            - text: Formatted cumulative transcript
            - label: Binary label (1=fraud, 0=legit)
            - timestamp: Chunk timestamp in seconds
            - session_id: Conversation identifier
            - batch: Batch folder name
    """
    logger.info(f"Loading chunk data from: {data_dir}")
    
    data_path = Path(data_dir)
    if not data_path.exists():
        raise FileNotFoundError(f"Data directory not found: {data_dir}")
    
    all_chunks = []
    batch_dirs = sorted([d for d in data_path.iterdir() if d.is_dir() and d.name.startswith('batch_')])
    
    logger.info(f"Found {len(batch_dirs)} batch directories")
    
    for batch_dir in tqdm(batch_dirs, desc="Loading batches"):
        chunk_files = list(batch_dir.glob("*.json"))
        
        for chunk_file in tqdm(chunk_files, desc=f"Loading {batch_dir.name}", leave=False):
            try:
                with open(chunk_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                # Extract features
                transcript_text = format_transcript(data.get('cumulative_transcript', []))
                label = 1 if data.get('final_verdict') == 'YES' else 0
                timestamp = data.get('chunk_timestamp', 0)
                session_id = data.get('session_id', 0)
                
                # Create unique session identifier including batch name
                unique_session_id = f"{batch_dir.name}_{session_id}"
                
                all_chunks.append({
                    'text': transcript_text,
                    'label': label,
                    'timestamp': timestamp,
                    'session_id': unique_session_id,
                    'batch': batch_dir.name
                })
                
                # Stop if reached max_samples
                if max_samples and len(all_chunks) >= max_samples:
                    logger.info(f"Reached max_samples limit: {max_samples}")
                    return all_chunks
                    
            except Exception as e:
                logger.warning(f"Error loading {chunk_file}: {e}")
                continue
    
    logger.info(f"Loaded {len(all_chunks)} chunks successfully")
    
    # Log class distribution
    fraud_count = sum(1 for c in all_chunks if c['label'] == 1)
    legit_count = len(all_chunks) - fraud_count
    logger.info(f"Class distribution:")
    logger.info(f"  Fraud (YES): {fraud_count} ({fraud_count/len(all_chunks)*100:.2f}%)")
    logger.info(f"  Legit (NO):  {legit_count} ({legit_count/len(all_chunks)*100:.2f}%)")
    
    return all_chunks


def create_session_based_splits(
    all_chunks: List[Dict],
    train_ratio: float = 0.7,
    val_ratio: float = 0.15,
    test_ratio: float = 0.15,
    random_seed: int = 42
) -> Tuple[List[Dict], List[Dict], List[Dict]]:
    """
    Split data by session_id to prevent data leakage.
    
    CRITICAL: All chunks from the same conversation must stay in the same split
    to prevent the model from seeing the same conversation at different timestamps
    during training and testing.
    
    Args:
        all_chunks: List of all chunk dictionaries
        train_ratio: Proportion for training (default 0.7)
        val_ratio: Proportion for validation (default 0.15)
        test_ratio: Proportion for testing (default 0.15)
        random_seed: Random seed for reproducibility
        
    Returns:
        Tuple of (train_chunks, val_chunks, test_chunks)
    """
    logger.info("Creating session-based data splits")
    logger.info(f"Split ratios - Train: {train_ratio}, Val: {val_ratio}, Test: {test_ratio}")
    
    # Group chunks by session
    sessions = defaultdict(list)
    for chunk in all_chunks:
        sessions[chunk['session_id']].append(chunk)
    
    session_ids = list(sessions.keys())
    logger.info(f"Total unique sessions: {len(session_ids)}")
    
    # Calculate labels per session (use majority vote for stratification)
    session_labels = []
    for sid in session_ids:
        chunks_in_session = sessions[sid]
        fraud_count = sum(1 for c in chunks_in_session if c['label'] == 1)
        session_label = 1 if fraud_count > len(chunks_in_session) / 2 else 0
        session_labels.append(session_label)
    
    # Stratified split by session
    train_sessions, temp_sessions, train_labels, temp_labels = train_test_split(
        session_ids, session_labels,
        test_size=(val_ratio + test_ratio),
        random_state=random_seed,
        stratify=session_labels
    )
    
    val_sessions, test_sessions, _, _ = train_test_split(
        temp_sessions, temp_labels,
        test_size=test_ratio / (val_ratio + test_ratio),
        random_state=random_seed,
        stratify=temp_labels
    )
    
    # Flatten chunks from selected sessions
    train_chunks = [chunk for sid in train_sessions for chunk in sessions[sid]]
    val_chunks = [chunk for sid in val_sessions for chunk in sessions[sid]]
    test_chunks = [chunk for sid in test_sessions for chunk in sessions[sid]]
    
    # Log split statistics
    logger.info(f"\n{'='*60}")
    logger.info("Session-based split statistics:")
    logger.info(f"{'='*60}")
    
    for split_name, chunks, session_list in [
        ("Train", train_chunks, train_sessions),
        ("Validation", val_chunks, val_sessions),
        ("Test", test_chunks, test_sessions)
    ]:
        fraud = sum(1 for c in chunks if c['label'] == 1)
        legit = len(chunks) - fraud
        logger.info(f"\n{split_name}:")
        logger.info(f"  Sessions: {len(session_list):,}")
        logger.info(f"  Chunks: {len(chunks):,}")
        logger.info(f"  Fraud: {fraud:,} ({fraud/len(chunks)*100:.2f}%)")
        logger.info(f"  Legit: {legit:,} ({legit/len(chunks)*100:.2f}%)")
    
    logger.info(f"{'='*60}\n")
    
    return train_chunks, val_chunks, test_chunks


def compute_metrics(pred) -> Dict[str, float]:
    """
    Compute evaluation metrics for Trainer.
    
    Args:
        pred: Predictions object from Trainer
        
    Returns:
        Dictionary with accuracy, precision, recall, f1
    """
    labels = pred.label_ids
    preds = pred.predictions.argmax(-1)
    
    precision, recall, f1, _ = precision_recall_fscore_support(
        labels, preds, average='binary', zero_division=0
    )
    acc = accuracy_score(labels, preds)
    
    return {
        'accuracy': acc,
        'precision': precision,
        'recall': recall,
        'f1': f1,
    }


def evaluate_model(
    model: RobertaForSequenceClassification,
    test_dataset: FraudChunkDataset,
    test_chunks: List[Dict],
    tokenizer: RobertaTokenizer,
    device: str = 'cuda'
) -> Dict[str, Any]:
    """
    Comprehensive evaluation with streaming-specific metrics.
    
    Args:
        model: Trained RoBERTa model
        test_dataset: PyTorch dataset for testing
        test_chunks: Original chunk data with metadata
        tokenizer: RoBERTa tokenizer
        device: Device for inference
        
    Returns:
        Dictionary with all evaluation results
    """
    logger.info("Running comprehensive evaluation...")
    
    model.eval()
    model.to(device)
    
    predictions = []
    true_labels = []
    
    # Get predictions
    with torch.no_grad():
        for i in tqdm(range(len(test_dataset)), desc="Evaluating"):
            inputs = test_dataset[i]
            input_ids = inputs['input_ids'].unsqueeze(0).to(device)
            attention_mask = inputs['attention_mask'].unsqueeze(0).to(device)
            
            outputs = model(input_ids=input_ids, attention_mask=attention_mask)
            logits = outputs.logits
            pred = torch.argmax(logits, dim=1).item()
            
            predictions.append(pred)
            true_labels.append(inputs['labels'].item())
    
    # Overall metrics
    precision, recall, f1, _ = precision_recall_fscore_support(
        true_labels, predictions, average='binary', zero_division=0
    )
    accuracy = accuracy_score(true_labels, predictions)
    cm = confusion_matrix(true_labels, predictions)
    
    results = {
        'overall_metrics': {
            'accuracy': float(accuracy),
            'precision': float(precision),
            'recall': float(recall),
            'f1': float(f1),
            'total_samples': len(predictions),
            'confusion_matrix': cm.tolist()
        }
    }
    
    logger.info(f"\n{'='*60}")
    logger.info("Overall Test Results:")
    logger.info(f"{'='*60}")
    logger.info(f"Accuracy:  {accuracy*100:.2f}%")
    logger.info(f"Precision: {precision*100:.2f}%")
    logger.info(f"Recall:    {recall*100:.2f}%")
    logger.info(f"F1-Score:  {f1*100:.2f}%")
    logger.info(f"{'='*60}\n")
    
    # Performance by timestamp range
    logger.info("Analyzing performance by timestamp...")
    timestamp_ranges = [
        (0, 30, "0-30s (Early)"),
        (30, 60, "30-60s (Mid)"),
        (60, 120, "60-120s (Late)"),
        (120, float('inf'), "120s+ (Very Late)")
    ]
    
    timestamp_results = {}
    for start, end, label in timestamp_ranges:
        mask = [(start <= chunk['timestamp'] < end) for chunk in test_chunks]
        if sum(mask) == 0:
            continue
            
        range_preds = [p for p, m in zip(predictions, mask) if m]
        range_labels = [l for l, m in zip(true_labels, mask) if m]
        
        if len(range_labels) > 0:
            range_acc = accuracy_score(range_labels, range_preds)
            range_p, range_r, range_f1, _ = precision_recall_fscore_support(
                range_labels, range_preds, average='binary', zero_division=0
            )
            
            timestamp_results[label] = {
                'accuracy': float(range_acc),
                'precision': float(range_p),
                'recall': float(range_r),
                'f1': float(range_f1),
                'sample_count': len(range_labels)
            }
            
            logger.info(f"{label:20s}: F1={range_f1*100:.2f}%, "
                       f"Acc={range_acc*100:.2f}%, Samples={len(range_labels):,}")
    
    results['performance_by_timestamp'] = timestamp_results
    
    # Early detection analysis
    logger.info("\nAnalyzing early detection rate...")
    
    # Group by session
    session_predictions = defaultdict(list)
    for chunk, pred, label in zip(test_chunks, predictions, true_labels):
        session_predictions[chunk['session_id']].append({
            'timestamp': chunk['timestamp'],
            'prediction': pred,
            'true_label': label
        })
    
    early_detection_times = []
    total_fraud_sessions = 0
    detected_fraud_sessions = 0
    
    for session_id, preds in session_predictions.items():
        # Check if this is a fraud session (majority vote)
        true_labels_session = [p['true_label'] for p in preds]
        if sum(true_labels_session) > len(true_labels_session) / 2:
            total_fraud_sessions += 1
            
            # Find first detection
            sorted_preds = sorted(preds, key=lambda x: x['timestamp'])
            for pred_info in sorted_preds:
                if pred_info['prediction'] == 1:  # Detected as fraud
                    early_detection_times.append(pred_info['timestamp'])
                    detected_fraud_sessions += 1
                    break
    
    if early_detection_times:
        results['early_detection'] = {
            'total_fraud_sessions': total_fraud_sessions,
            'detected_fraud_sessions': detected_fraud_sessions,
            'detection_rate': float(detected_fraud_sessions / total_fraud_sessions),
            'avg_detection_time': float(np.mean(early_detection_times)),
            'median_detection_time': float(np.median(early_detection_times)),
            'min_detection_time': float(np.min(early_detection_times)),
            'max_detection_time': float(np.max(early_detection_times))
        }
        
        logger.info(f"\nEarly Detection Analysis:")
        logger.info(f"  Total fraud sessions: {total_fraud_sessions}")
        logger.info(f"  Detected: {detected_fraud_sessions} ({detected_fraud_sessions/total_fraud_sessions*100:.2f}%)")
        logger.info(f"  Avg detection time: {np.mean(early_detection_times):.1f}s")
        logger.info(f"  Median detection time: {np.median(early_detection_times):.1f}s")
    
    # Per-conversation accuracy
    logger.info("\nAnalyzing per-conversation accuracy...")
    
    correct_sessions = 0
    for session_id, preds in session_predictions.items():
        # Use majority vote for both prediction and ground truth
        pred_votes = [p['prediction'] for p in preds]
        true_votes = [p['true_label'] for p in preds]
        
        pred_label = 1 if sum(pred_votes) > len(pred_votes) / 2 else 0
        true_label = 1 if sum(true_votes) > len(true_votes) / 2 else 0
        
        if pred_label == true_label:
            correct_sessions += 1
    
    conversation_accuracy = correct_sessions / len(session_predictions)
    results['per_conversation_accuracy'] = float(conversation_accuracy)
    
    logger.info(f"Per-conversation accuracy (majority vote): {conversation_accuracy*100:.2f}%")
    logger.info(f"Total test sessions: {len(session_predictions)}")
    
    return results


def save_predictions(
    predictions: List[int],
    true_labels: List[int],
    test_chunks: List[Dict],
    output_path: str
):
    """
    Save detailed predictions to CSV for analysis.
    
    Args:
        predictions: Model predictions
        true_labels: Ground truth labels
        test_chunks: Original chunk data with metadata
        output_path: Path to save CSV file
    """
    logger.info(f"Saving predictions to {output_path}")
    
    df = pd.DataFrame({
        'session_id': [c['session_id'] for c in test_chunks],
        'timestamp': [c['timestamp'] for c in test_chunks],
        'batch': [c['batch'] for c in test_chunks],
        'true_label': true_labels,
        'predicted_label': predictions,
        'correct': [p == t for p, t in zip(predictions, true_labels)],
        'transcript_preview': [c['text'][:200] + '...' if len(c['text']) > 200 else c['text'] 
                               for c in test_chunks]
    })
    
    df.to_csv(output_path, index=False)
    logger.info(f"Saved {len(df)} predictions")


class DetailedLoggingCallback(transformers.TrainerCallback):
    """Custom callback for detailed logging during training."""
    
    def __init__(self, log_file: str):
        self.log_file = log_file
        self.epoch_start_time = None
        
    def on_epoch_begin(self, args, state, control, **kwargs):
        self.epoch_start_time = datetime.now()
        logger.info(f"\n{'='*60}")
        logger.info(f"Epoch {state.epoch:.0f} started at {self.epoch_start_time.strftime('%H:%M:%S')}")
        logger.info(f"{'='*60}")
        
    def on_epoch_end(self, args, state, control, **kwargs):
        epoch_time = (datetime.now() - self.epoch_start_time).total_seconds()
        logger.info(f"\n{'='*60}")
        logger.info(f"Epoch {state.epoch:.0f} completed in {epoch_time:.2f}s ({epoch_time/60:.2f}m)")
        logger.info(f"{'='*60}\n")
        
    def on_evaluate(self, args, state, control, metrics=None, **kwargs):
        if metrics:
            logger.info(f"\n{'='*60}")
            logger.info(f"Evaluation at step {state.global_step}")
            logger.info(f"{'='*60}")
            for key, value in metrics.items():
                if isinstance(value, float):
                    logger.info(f"  {key}: {value:.4f}")
                else:
                    logger.info(f"  {key}: {value}")
            logger.info(f"{'='*60}\n")


def main():
    parser = argparse.ArgumentParser(description='Train RoBERTa streaming baseline')
    
    # Data arguments
    parser.add_argument('--data_dir', type=str, 
                       default='../../output/training_data',
                       help='Path to training_data directory')
    parser.add_argument('--max_samples', type=int, default=None,
                       help='Maximum number of samples to load (for testing)')
    
    # Model arguments
    parser.add_argument('--model_name', type=str, 
                       default='roberta-base',
                       help='HuggingFace model name')
    parser.add_argument('--max_length', type=int, default=512,
                       help='Maximum sequence length')
    
    # Training arguments
    parser.add_argument('--output_dir', type=str, default='./models',
                       help='Output directory for model checkpoints')
    parser.add_argument('--results_dir', type=str, default='./results',
                       help='Output directory for results')
    parser.add_argument('--batch_size', type=int, default=4,
                       help='Training batch size per device')
    parser.add_argument('--gradient_accumulation_steps', type=int, default=4,
                       help='Gradient accumulation steps')
    parser.add_argument('--epochs', type=int, default=5,
                       help='Number of training epochs')
    parser.add_argument('--learning_rate', type=float, default=2e-5,
                       help='Learning rate')
    parser.add_argument('--warmup_ratio', type=float, default=0.1,
                       help='Warmup ratio')
    parser.add_argument('--weight_decay', type=float, default=0.01,
                       help='Weight decay')
    parser.add_argument('--seed', type=int, default=42,
                       help='Random seed')
    parser.add_argument('--eval_steps', type=int, default=5000,
                       help='Evaluation frequency (steps)')
    parser.add_argument('--save_steps', type=int, default=5000,
                       help='Save checkpoint frequency (steps)')
    parser.add_argument('--early_stopping_patience', type=int, default=3,
                       help='Early stopping patience')
    
    args = parser.parse_args()
    
    # Create output directories
    os.makedirs(args.output_dir, exist_ok=True)
    os.makedirs(args.results_dir, exist_ok=True)
    os.makedirs('logs', exist_ok=True)
    
    # Log configuration
    logger.info(f"\n{'='*60}")
    logger.info("RoBERTa Streaming Baseline Training")
    logger.info(f"{'='*60}")
    logger.info(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info(f"\nConfiguration:")
    for key, value in vars(args).items():
        logger.info(f"  {key}: {value}")
    logger.info(f"{'='*60}\n")
    
    # Set random seed
    transformers.set_seed(args.seed)
    
    # Check device
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    logger.info(f"Using device: {device}")
    if device == 'cuda':
        logger.info(f"GPU: {torch.cuda.get_device_name(0)}")
        logger.info(f"GPU Memory: {torch.cuda.get_device_properties(0).total_memory / 1e9:.2f} GB")
    
    # Load data
    logger.info("\n" + "="*60)
    logger.info("Loading data...")
    logger.info("="*60)
    all_chunks = load_chunk_data(args.data_dir, max_samples=args.max_samples)
    
    # Create splits
    train_chunks, val_chunks, test_chunks = create_session_based_splits(
        all_chunks,
        random_seed=args.seed
    )
    
    # Save split information
    split_info = {
        'train_sessions': len(set(c['session_id'] for c in train_chunks)),
        'train_chunks': len(train_chunks),
        'val_sessions': len(set(c['session_id'] for c in val_chunks)),
        'val_chunks': len(val_chunks),
        'test_sessions': len(set(c['session_id'] for c in test_chunks)),
        'test_chunks': len(test_chunks),
        'split_timestamp': datetime.now().isoformat()
    }
    
    with open(os.path.join(args.results_dir, 'data_splits.json'), 'w') as f:
        json.dump(split_info, f, indent=2)
    
    # Load tokenizer and model
    logger.info(f"\nLoading model: {args.model_name}")
    tokenizer = RobertaTokenizer.from_pretrained(args.model_name)
    model = RobertaForSequenceClassification.from_pretrained(
        args.model_name,
        num_labels=2
    )
    
    # Create datasets
    logger.info("\nCreating PyTorch datasets...")
    train_dataset = FraudChunkDataset(train_chunks, tokenizer, args.max_length)
    val_dataset = FraudChunkDataset(val_chunks, tokenizer, args.max_length)
    test_dataset = FraudChunkDataset(test_chunks, tokenizer, args.max_length)
    
    # Training arguments
    training_args = TrainingArguments(
        output_dir=args.output_dir,
        num_train_epochs=args.epochs,
        per_device_train_batch_size=args.batch_size,
        per_device_eval_batch_size=args.batch_size * 2,
        gradient_accumulation_steps=args.gradient_accumulation_steps,
        learning_rate=args.learning_rate,
        warmup_ratio=args.warmup_ratio,
        weight_decay=args.weight_decay,
        logging_dir=os.path.join(args.output_dir, 'logs'),
        logging_steps=100,
        eval_strategy='steps',
        eval_steps=args.eval_steps,
        save_strategy='steps',
        save_steps=args.save_steps,
        save_total_limit=3,
        load_best_model_at_end=True,
        metric_for_best_model='f1',
        greater_is_better=True,
        report_to=['tensorboard'],
        seed=args.seed,
        fp16=torch.cuda.is_available(),  # Use mixed precision if available
    )
    
    # Callbacks
    callbacks = [
        EarlyStoppingCallback(early_stopping_patience=args.early_stopping_patience),
        DetailedLoggingCallback(log_file='logs/training.log')
    ]
    
    # Create trainer
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=val_dataset,
        compute_metrics=compute_metrics,
        callbacks=callbacks,
    )
    
    # Train
    logger.info("\n" + "="*60)
    logger.info("Starting training...")
    logger.info("="*60 + "\n")
    
    train_result = trainer.train()
    
    # Save final model
    logger.info("\nSaving final model...")
    trainer.save_model(os.path.join(args.output_dir, 'final_model'))
    tokenizer.save_pretrained(os.path.join(args.output_dir, 'final_model'))
    
    # Save training metrics
    train_metrics = {
        'train_runtime': train_result.metrics['train_runtime'],
        'train_samples_per_second': train_result.metrics['train_samples_per_second'],
        'train_loss': train_result.metrics['train_loss'],
        'epoch': train_result.metrics['epoch'],
    }
    
    with open(os.path.join(args.results_dir, 'training_metrics.json'), 'w') as f:
        json.dump(train_metrics, f, indent=2)
    
    logger.info(f"\nTraining completed in {train_metrics['train_runtime']:.2f}s")
    logger.info(f"Final training loss: {train_metrics['train_loss']:.4f}")
    
    # Evaluate on test set
    logger.info("\n" + "="*60)
    logger.info("Evaluating on test set...")
    logger.info("="*60 + "\n")
    
    # Get predictions for detailed analysis
    predictions_output = trainer.predict(test_dataset)
    predictions = predictions_output.predictions.argmax(-1).tolist()
    true_labels = predictions_output.label_ids.tolist()
    
    # Comprehensive evaluation
    eval_results = evaluate_model(
        model=model,
        test_dataset=test_dataset,
        test_chunks=test_chunks,
        tokenizer=tokenizer,
        device=device
    )
    
    # Save results
    with open(os.path.join(args.results_dir, 'test_results.json'), 'w') as f:
        json.dump(eval_results, f, indent=2)
    
    # Save predictions
    save_predictions(
        predictions=predictions,
        true_labels=true_labels,
        test_chunks=test_chunks,
        output_path=os.path.join(args.results_dir, 'predictions.csv')
    )
    
    # Final summary
    logger.info(f"\n{'='*60}")
    logger.info("Training Complete!")
    logger.info(f"{'='*60}")
    logger.info(f"Model saved to: {os.path.join(args.output_dir, 'final_model')}")
    logger.info(f"Results saved to: {args.results_dir}")
    logger.info(f"Final F1-Score: {eval_results['overall_metrics']['f1']*100:.2f}%")
    logger.info(f"Final Accuracy: {eval_results['overall_metrics']['accuracy']*100:.2f}%")
    logger.info(f"Completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info(f"{'='*60}\n")


if __name__ == '__main__':
    main()
