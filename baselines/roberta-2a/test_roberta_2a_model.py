"""
Test RoBERTa 2a Model - Verify Saved Model Performance
======================================================

This script loads the saved RoBERTa static-classification model and evaluates it on
the test set to verify its performance matches the original training results.

Expected F1-score: 98.45%
Expected Accuracy: 98.40%

Usage:
    python test_roberta_2a_model.py

"""

import json
import os
from pathlib import Path
from typing import Dict, List
import argparse

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
print("RoBERTa Static Classification Model Testing")
print("="*60)


class FraudDataset(Dataset):
    """PyTorch Dataset for fraud detection"""
    
    def __init__(self, conversations: List[Dict], tokenizer: RobertaTokenizer, max_length: int = 512):
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


def format_transcript(transcript: List[Dict]) -> str:
    """Format transcript list to string"""
    formatted_parts = []
    for utterance in transcript:
        speaker = utterance.get('speaker', 'Unknown')
        text = utterance.get('text', '')
        formatted_parts.append(f"{speaker}: {text}")
    return " ".join(formatted_parts)


def load_conversation_data(data_dir: str) -> List[Dict]:
    """Load all conversations from source_conversations directory"""
    print(f"\nLoading conversations from: {data_dir}")
    
    data_path = Path(data_dir)
    if not data_path.exists():
        raise FileNotFoundError(f"Data directory not found: {data_dir}")
    
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
                    'file': conv_file.name
                })
                
            except Exception as e:
                print(f"Warning: Error loading {conv_file}: {e}")
                continue
    
    print(f"Loaded {len(all_conversations)} conversations")
    
    # Log class distribution
    fraud_count = sum(1 for c in all_conversations if c['label'] == 1)
    legit_count = len(all_conversations) - fraud_count
    print(f"\nClass distribution:")
    print(f"  Fraud (YES): {fraud_count} ({fraud_count/len(all_conversations)*100:.2f}%)")
    print(f"  Legit (NO):  {legit_count} ({legit_count/len(all_conversations)*100:.2f}%)")
    
    return all_conversations


def load_test_split(results_dir: str) -> List[str]:
    """Load test conversation filenames from previous split"""
    predictions_path = Path(results_dir) / 'predictions.csv'
    
    if predictions_path.exists():
        print(f"\nLoading test split from: {predictions_path}")
        df = pd.read_csv(predictions_path)
        test_files = df['conversation_file'].unique().tolist()
        print(f"Found {len(test_files)} test conversations from original split")
        return test_files
    else:
        print(f"\nWarning: predictions.csv not found at {predictions_path}")
        print("Will use random 15% split for testing")
        return None


def evaluate_model(model, dataset, conversations, device='cuda'):
    """Comprehensive evaluation"""
    print("\n" + "="*60)
    print("Evaluating model...")
    print("="*60)
    
    model.eval()
    model.to(device)
    
    predictions = []
    true_labels = []
    
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
        'total_samples': len(predictions)
    }
    
    # Print results
    print(f"\n{'='*60}")
    print("Test Results:")
    print(f"{'='*60}")
    print(f"Accuracy:  {accuracy*100:.2f}%")
    print(f"Precision: {precision*100:.2f}%")
    print(f"Recall:    {recall*100:.2f}%")
    print(f"F1-Score:  {f1*100:.2f}%")
    print(f"\nTotal samples: {len(predictions)}")
    print(f"\nConfusion Matrix:")
    print(f"  True Negatives:  {cm[0][0]:,}")
    print(f"  False Positives: {cm[0][1]:,}")
    print(f"  False Negatives: {cm[1][0]:,}")
    print(f"  True Positives:  {cm[1][1]:,}")
    
    errors = cm[0][1] + cm[1][0]
    print(f"\nTotal errors: {errors} ({errors/len(predictions)*100:.2f}%)")
    print(f"{'='*60}\n")
    
    # Compare with expected
    print("Comparison with Original Training:")
    print(f"  Expected F1: 98.45%")
    print(f"  Current F1:  {f1*100:.2f}%")
    diff = f1*100 - 98.45
    if abs(diff) < 0.5:
        print(f"  Difference:  {diff:+.2f}% Pass (within 0.5% tolerance)")
    else:
        print(f"  Difference:  {diff:+.2f}% (unexpected difference)")
    
    return results, predictions, true_labels


def main():
    parser = argparse.ArgumentParser(description='Test saved RoBERTa 2a model')
    parser.add_argument('--model_dir', type=str, 
                       default='./roberta_final_results',
                       help='Path to saved model directory')
    parser.add_argument('--data_dir', type=str,
                       default='../../output/source_conversations',
                       help='Path to source_conversations directory')
    parser.add_argument('--results_dir', type=str,
                       default='../roberta-2a/results',
                       help='Path to original results (for test split)')
    parser.add_argument('--max_length', type=int, default=512,
                       help='Maximum sequence length')
    
    args = parser.parse_args()
    
    # Check device (prioritize: CUDA > MPS > CPU)
    if torch.cuda.is_available():
        device = 'cuda'
        print(f"\nUsing device: {device}")
        print(f"GPU: {torch.cuda.get_device_name(0)}")
    elif torch.backends.mps.is_available():
        device = 'mps'
        print(f"\nUsing device: {device} (Apple Silicon GPU)")
        print(f"This will be MUCH faster than CPU!")
    else:
        device = 'cpu'
        print(f"\nUsing device: {device}")
    
    # Load model and tokenizer
    print(f"\nLoading model from: {args.model_dir}")
    
    if not Path(args.model_dir).exists():
        print(f"Error: Model directory not found: {args.model_dir}")
        return 1
    
    try:
        tokenizer = RobertaTokenizer.from_pretrained(args.model_dir)
        model = RobertaForSequenceClassification.from_pretrained(args.model_dir)
        print("Pass Model and tokenizer loaded successfully")
    except Exception as e:
        print(f"✗ Error loading model: {e}")
        return 1
    
    # Load all conversations
    all_conversations = load_conversation_data(args.data_dir)
    
    # Get test split
    test_files = load_test_split(args.results_dir)
    
    if test_files:
        # Use original test split
        test_conversations = [c for c in all_conversations if c['file'] in test_files]
        print(f"\nUsing original test split: {len(test_conversations)} conversations")
    else:
        # Random split (15%)
        from sklearn.model_selection import train_test_split
        labels = [c['label'] for c in all_conversations]
        _, test_conversations = train_test_split(
            all_conversations, test_size=0.15, random_state=42, stratify=labels
        )
        print(f"\nUsing random 15% split: {len(test_conversations)} conversations")
    
    # Create dataset
    print("\nCreating PyTorch dataset...")
    test_dataset = FraudDataset(test_conversations, tokenizer, args.max_length)
    
    # Evaluate
    results, predictions, true_labels = evaluate_model(
        model, test_dataset, test_conversations, device
    )
    
    # Save results
    output_dir = Path('test_results')
    output_dir.mkdir(exist_ok=True)
    
    with open(output_dir / 'retest_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    # Save predictions
    pred_df = pd.DataFrame({
        'conversation_file': [c['file'] for c in test_conversations],
        'true_label': true_labels,
        'predicted_label': predictions,
        'correct': [p == t for p, t in zip(predictions, true_labels)],
        'transcript_preview': [c['text'][:200] + '...' for c in test_conversations]
    })
    pred_df.to_csv(output_dir / 'retest_predictions.csv', index=False)
    
    print(f"\nResults saved to: {output_dir}/")
    print(f"  - retest_results.json")
    print(f"  - retest_predictions.csv")
    
    print("\n" + "="*60)
    print("Testing complete!")
    print("="*60)
    
    return 0


if __name__ == '__main__':
    exit(main())
