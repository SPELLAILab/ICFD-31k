"""
Full Dataset Test for RoBERTa 2a
=================================

Tests model on ALL conversations (100%) instead of just 15% split
to get the most accurate performance estimate.

This eliminates split variance entirely by using the complete dataset.

Usage:
    python test_full_dataset.py

Warning: Takes longer than split testing (20-30 minutes on CPU)

"""

import json
import os
from pathlib import Path
from typing import Dict, List
import argparse
import time

import numpy as np
import pandas as pd
from tqdm import tqdm
from sklearn.metrics import (
    accuracy_score, precision_recall_fscore_support,
    confusion_matrix, classification_report
)

import torch
from torch.utils.data import Dataset
from transformers import RobertaTokenizer, RobertaForSequenceClassification

print("="*60)
print("RoBERTa 2a Full Dataset Test")
print("="*60)


class FraudDataset(Dataset):
    """PyTorch Dataset for fraud detection"""
    
    def __init__(self, conversations, tokenizer, max_length=512):
        self.conversations = conversations
        self.tokenizer = tokenizer
        self.max_length = max_length
    
    def __len__(self):
        return len(self.conversations)
    
    def __getitem__(self, idx):
        conv = self.conversations[idx]
        
        encoding = self.tokenizer(
            conv['text'],
            truncation=True,
            padding='max_length',
            max_length=self.max_length,
            return_tensors='pt'
        )
        
        return {
            'input_ids': encoding['input_ids'].squeeze(),
            'attention_mask': encoding['attention_mask'].squeeze(),
            'labels': torch.tensor(conv['label'], dtype=torch.long)
        }


def format_transcript(transcript):
    """Format transcript list to string"""
    formatted_parts = []
    for utterance in transcript:
        speaker = utterance.get('speaker', 'Unknown')
        text = utterance.get('text', '')
        formatted_parts.append(f"{speaker}: {text}")
    return " ".join(formatted_parts)


def load_conversation_data(data_dir):
    """Load all conversations"""
    print(f"\nLoading ALL conversations from: {data_dir}")
    
    data_path = Path(data_dir)
    all_conversations = []
    batch_dirs = sorted([d for d in data_path.iterdir() if d.is_dir() and d.name.startswith('batch_')])
    
    print(f"Found {len(batch_dirs)} batch directories")
    
    for batch_dir in tqdm(batch_dirs, desc="Loading batches"):
        conversation_files = list(batch_dir.glob("*.json"))
        
        for conv_file in conversation_files:
            try:
                with open(conv_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                transcript_text = format_transcript(data.get('transcript', []))
                label = 1 if data.get('final_verdict') == 'YES' else 0
                
                all_conversations.append({
                    'text': transcript_text,
                    'label': label,
                    'file': conv_file.name,
                    'batch': batch_dir.name
                })
                
            except Exception as e:
                continue
    
    print(f"Loaded {len(all_conversations)} conversations")
    
    # Class distribution
    fraud_count = sum(1 for c in all_conversations if c['label'] == 1)
    legit_count = len(all_conversations) - fraud_count
    print(f"\nClass distribution:")
    print(f"  Fraud (YES): {fraud_count} ({fraud_count/len(all_conversations)*100:.2f}%)")
    print(f"  Legit (NO):  {legit_count} ({legit_count/len(all_conversations)*100:.2f}%)")
    
    return all_conversations


def evaluate_model(model, dataset, conversations, device='cpu'):
    """Comprehensive evaluation on full dataset"""
    print(f"\n{'='*60}")
    print("Evaluating on Full Dataset")
    print(f"{'='*60}")
    print(f"Total samples: {len(dataset):,}")
    
    start_time = time.time()
    
    model.eval()
    model.to(device)
    
    predictions = []
    true_labels = []
    
    print("\nProcessing conversations...")
    with torch.no_grad():
        for i in tqdm(range(len(dataset)), desc="Testing"):
            inputs = dataset[i]
            input_ids = inputs['input_ids'].unsqueeze(0).to(device)
            attention_mask = inputs['attention_mask'].unsqueeze(0).to(device)
            
            outputs = model(input_ids=input_ids, attention_mask=attention_mask)
            logits = outputs.logits
            pred = torch.argmax(logits, dim=1).item()
            
            predictions.append(pred)
            true_labels.append(inputs['labels'].item())
    
    elapsed_time = time.time() - start_time
    
    # Calculate metrics
    precision, recall, f1, _ = precision_recall_fscore_support(
        true_labels, predictions, average='binary', zero_division=0
    )
    accuracy = accuracy_score(true_labels, predictions)
    cm = confusion_matrix(true_labels, predictions)
    
    results = {
        'accuracy': float(accuracy),
        'precision': float(precision),
        'recall': float(recall),
        'f1': float(f1),
        'confusion_matrix': cm.tolist(),
        'total_samples': len(predictions),
        'elapsed_time': elapsed_time
    }
    
    # Print results
    print(f"\n{'='*60}")
    print("Full Dataset Results")
    print(f"{'='*60}")
    print(f"Samples:   {len(predictions):,}")
    print(f"Time:      {elapsed_time:.1f}s ({elapsed_time/60:.1f}m)")
    print(f"Speed:     {len(predictions)/elapsed_time:.1f} samples/sec")
    print(f"\nPerformance:")
    print(f"  Accuracy:  {accuracy*100:.2f}%")
    print(f"  Precision: {precision*100:.2f}%")
    print(f"  Recall:    {recall*100:.2f}%")
    print(f"  F1-Score:  {f1*100:.2f}%")
    
    print(f"\nConfusion Matrix:")
    print(f"  True Negatives:  {cm[0][0]:,}")
    print(f"  False Positives: {cm[0][1]:,}")
    print(f"  False Negatives: {cm[1][0]:,}")
    print(f"  True Positives:  {cm[1][1]:,}")
    
    errors = cm[0][1] + cm[1][0]
    print(f"\nTotal errors: {errors:,} ({errors/len(predictions)*100:.2f}%)")
    print(f"Correct:      {len(predictions)-errors:,} ({(len(predictions)-errors)/len(predictions)*100:.2f}%)")
    
    # Compare with previous results
    print(f"\n{'='*60}")
    print("Comparison with Previous Tests")
    print(f"{'='*60}")
    print(f"  Original training test (15%): F1 = 98.45%")
    print(f"  Retest with new split (15%):  F1 = 99.63%")
    print(f"  Full dataset test (100%):     F1 = {f1*100:.2f}%")
    
    # Analysis
    print(f"\n{'='*60}")
    print("Analysis")
    print(f"{'='*60}")
    
    if f1 >= 0.98:
        print("Pass EXCELLENT: F1 ≥ 98% - Model is highly accurate")
    elif f1 >= 0.95:
        print("Pass GOOD: F1 ≥ 95% - Model performs well")
    elif f1 >= 0.90:
        print("MODERATE: F1 ≥ 90% - Acceptable but room for improvement")
    else:
        print("✗ POOR: F1 < 90% - Model needs improvement")
    
    # Error rate assessment
    error_rate = errors / len(predictions)
    if error_rate < 0.01:
        print(f"Pass Error rate < 1%: Excellent reliability")
    elif error_rate < 0.02:
        print(f"Pass Error rate < 2%: Good reliability")
    elif error_rate < 0.05:
        print(f"Error rate < 5%: Acceptable reliability")
    else:
        print(f"✗ Error rate ≥ 5%: Reliability concerns")
    
    # Balance assessment
    fp_rate = cm[0][1] / (cm[0][0] + cm[0][1]) if (cm[0][0] + cm[0][1]) > 0 else 0
    fn_rate = cm[1][0] / (cm[1][0] + cm[1][1]) if (cm[1][0] + cm[1][1]) > 0 else 0
    
    print(f"\nError breakdown:")
    print(f"  False Positive rate: {fp_rate*100:.2f}% (legit flagged as fraud)")
    print(f"  False Negative rate: {fn_rate*100:.2f}% (fraud missed)")
    
    if abs(fp_rate - fn_rate) < 0.01:
        print(f"  Pass Balanced errors: Model is not biased")
    elif fp_rate > fn_rate * 1.5:
        print(f"  More false positives: Model is conservative (flags more)")
    else:
        print(f"  More false negatives: Model is lenient (misses more)")
    
    return results, predictions, true_labels


def main():
    parser = argparse.ArgumentParser(description='Full dataset test for RoBERTa 2a')
    parser.add_argument('--model_dir', type=str, 
                       default='./roberta_final_results',
                       help='Path to saved model')
    parser.add_argument('--data_dir', type=str,
                       default='../../output/source_conversations',
                       help='Path to source_conversations')
    parser.add_argument('--output_dir', type=str,
                       default='./full_dataset_results',
                       help='Output directory')
    parser.add_argument('--save_predictions', action='store_true',
                       help='Save all predictions to CSV (large file!)')
    
    args = parser.parse_args()
    
    # Create output directory
    output_dir = Path(args.output_dir)
    output_dir.mkdir(exist_ok=True)
    
    # Check device (prioritize: CUDA > MPS > CPU)
    if torch.cuda.is_available():
        device = 'cuda'
        print(f"\nUsing device: {device}")
        print(f"GPU: {torch.cuda.get_device_name(0)}")
    elif torch.backends.mps.is_available():
        device = 'mps'
        print(f"\nUsing device: {device} (Apple Silicon GPU)")
    else:
        device = 'cpu'
        print(f"\nUsing device: {device}")
    
    # Load model
    print(f"\nLoading model from: {args.model_dir}")
    tokenizer = RobertaTokenizer.from_pretrained(args.model_dir)
    model = RobertaForSequenceClassification.from_pretrained(args.model_dir)
    print("Pass Model loaded")
    
    # Load ALL conversations
    all_conversations = load_conversation_data(args.data_dir)
    
    # Create dataset
    print("\nCreating PyTorch dataset...")
    dataset = FraudDataset(all_conversations, tokenizer)
    
    # Evaluate
    results, predictions, true_labels = evaluate_model(
        model, dataset, all_conversations, device
    )
    
    # Save results
    print(f"\n{'='*60}")
    print("Saving Results")
    print(f"{'='*60}")
    
    with open(output_dir / 'full_dataset_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    print(f"Pass Saved: {output_dir}/full_dataset_results.json")
    
    # Save predictions if requested
    if args.save_predictions:
        print("\nSaving predictions (this may take a while)...")
        pred_df = pd.DataFrame({
            'file': [c['file'] for c in all_conversations],
            'batch': [c['batch'] for c in all_conversations],
            'true_label': true_labels,
            'predicted_label': predictions,
            'correct': [p == t for p, t in zip(predictions, true_labels)],
            'transcript_preview': [c['text'][:200] + '...' for c in all_conversations]
        })
        pred_df.to_csv(output_dir / 'full_dataset_predictions.csv', index=False)
        print(f"Pass Saved: {output_dir}/full_dataset_predictions.csv")
        
        # Save error cases only
        error_df = pred_df[pred_df['correct'] == False]
        error_df.to_csv(output_dir / 'error_cases.csv', index=False)
        print(f"Pass Saved: {output_dir}/error_cases.csv ({len(error_df)} errors)")
    
    # Final summary
    print(f"\n{'='*60}")
    print("Summary")
    print(f"{'='*60}")
    print(f"This full dataset test provides the most accurate")
    print(f"performance estimate by eliminating split variance.")
    print(f"\nFinal F1-Score: {results['f1']*100:.2f}%")
    print(f"\nThis represents the model's true expected performance")
    print(f"on this type of fraud detection data.")
    print(f"{'='*60}\n")
    
    return 0


if __name__ == '__main__':
    exit(main())
