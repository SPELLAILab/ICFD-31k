"""
Cross-Domain Generalization Test for RoBERTa 2a
================================================

Tests the model on completely unseen fraud domains to evaluate
real-world generalization and robustness.

This is a critical test for deployment readiness:
- Training: Banking, Tech, Healthcare, Govt, Jobs, etc.
- Testing: Crypto, Romance, Charity, Investment, Tax (NEW)

Usage:
    python test_cross_domain.py --test_data ../../output/cross_domain_test/source_conversations

"""

import json
import os
from pathlib import Path
from collections import defaultdict
import argparse

import pandas as pd
from tqdm import tqdm
from sklearn.metrics import (
    accuracy_score, precision_recall_fscore_support,
    confusion_matrix, classification_report
)

import torch
from torch.utils.data import Dataset
from transformers import RobertaTokenizer, RobertaForSequenceClassification


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


def load_cross_domain_data(data_dir):
    """Load cross-domain test conversations"""
    print(f"\n{'='*60}")
    print("Loading Cross-Domain Test Data")
    print(f"{'='*60}")
    print(f"From: {data_dir}")
    
    data_path = Path(data_dir)
    if not data_path.exists():
        raise FileNotFoundError(f"Data directory not found: {data_dir}")
    
    conversations_by_domain = defaultdict(list)
    all_conversations = []
    
    # Load from batch directories
    batch_dirs = sorted([d for d in data_path.iterdir() if d.is_dir() and d.name.startswith('batch_')])
    
    if not batch_dirs:
        # Try loading directly from directory
        conv_files = list(data_path.glob("*.json"))
    else:
        conv_files = []
        for batch_dir in batch_dirs:
            conv_files.extend(batch_dir.glob("*.json"))
    
    print(f"Found {len(conv_files)} conversation files")
    
    for conv_file in tqdm(conv_files, desc="Loading conversations"):
        try:
            with open(conv_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            transcript_text = format_transcript(data.get('transcript', []))
            label = 1 if data.get('final_verdict') == 'YES' else 0
            
            # Extract domain from scenario
            scenario_info = data.get('scenario', {})
            scenario_desc = scenario_info.get('description', '')
            
            # Determine domain based on keywords
            domain = 'unknown'
            if 'crypto' in scenario_desc.lower() or 'nft' in scenario_desc.lower() or 'blockchain' in scenario_desc.lower():
                domain = 'crypto'
            elif 'romance' in scenario_desc.lower() or 'dating' in scenario_desc.lower() or 'relationship' in scenario_desc.lower():
                domain = 'romance'
            elif 'charity' in scenario_desc.lower() or 'donation' in scenario_desc.lower():
                domain = 'charity'
            elif 'investment' in scenario_desc.lower() or 'real estate' in scenario_desc.lower() or 'ponzi' in scenario_desc.lower():
                domain = 'investment'
            elif 'tax' in scenario_desc.lower() or 'irs' in scenario_desc.lower() or 'social security' in scenario_desc.lower():
                domain = 'tax'
            
            conv_data = {
                'text': transcript_text,
                'label': label,
                'file': conv_file.name,
                'domain': domain,
                'scenario_id': scenario_info.get('scenario_id', 0)
            }
            
            all_conversations.append(conv_data)
            conversations_by_domain[domain].append(conv_data)
            
        except Exception as e:
            print(f"Warning: Error loading {conv_file}: {e}")
            continue
    
    print(f"\nLoaded {len(all_conversations)} conversations")
    print(f"\nDomain distribution:")
    for domain, convs in sorted(conversations_by_domain.items()):
        fraud_count = sum(1 for c in convs if c['label'] == 1)
        print(f"  {domain:15s}: {len(convs):3d} conversations ({fraud_count} fraud)")
    
    return all_conversations, conversations_by_domain


def evaluate_model(model, dataset, conversations, device='cuda'):
    """Evaluate model and return predictions"""
    model.eval()
    model.to(device)
    
    predictions = []
    true_labels = []
    
    with torch.no_grad():
        for i in tqdm(range(len(dataset)), desc="Evaluating"):
            inputs = dataset[i]
            input_ids = inputs['input_ids'].unsqueeze(0).to(device)
            attention_mask = inputs['attention_mask'].unsqueeze(0).to(device)
            
            outputs = model(input_ids=input_ids, attention_mask=attention_mask)
            logits = outputs.logits
            pred = torch.argmax(logits, dim=1).item()
            
            predictions.append(pred)
            true_labels.append(inputs['labels'].item())
    
    return predictions, true_labels


def calculate_metrics(true_labels, predictions):
    """Calculate standard metrics"""
    precision, recall, f1, _ = precision_recall_fscore_support(
        true_labels, predictions, average='binary', zero_division=0
    )
    accuracy = accuracy_score(true_labels, predictions)
    cm = confusion_matrix(true_labels, predictions)
    
    return {
        'accuracy': float(accuracy),
        'precision': float(precision),
        'recall': float(recall),
        'f1': float(f1),
        'confusion_matrix': cm.tolist()
    }


def main():
    parser = argparse.ArgumentParser(description='Cross-domain generalization test')
    parser.add_argument('--model_dir', type=str, 
                       default='./roberta_final_results',
                       help='Path to saved model')
    parser.add_argument('--test_data', type=str,
                       required=True,
                       help='Path to cross-domain test data')
    parser.add_argument('--output_dir', type=str,
                       default='./cross_domain_results',
                       help='Output directory for results')
    
    args = parser.parse_args()
    
    print("\n" + "="*60)
    print("Cross-Domain Generalization Test")
    print("="*60)
    
    # Check device (with MPS support for Apple Silicon)
    if torch.cuda.is_available():
        device = 'cuda'
    elif torch.backends.mps.is_available():
        device = 'mps'
        print("Using Apple Silicon GPU (MPS)")
    else:
        device = 'cpu'
    print(f"\nUsing device: {device}")
    
    # Create output directory
    output_dir = Path(args.output_dir)
    output_dir.mkdir(exist_ok=True)
    
    # Load model
    print(f"\nLoading model from: {args.model_dir}")
    tokenizer = RobertaTokenizer.from_pretrained(args.model_dir)
    model = RobertaForSequenceClassification.from_pretrained(args.model_dir)
    print("Pass Model loaded")
    
    # Load cross-domain data
    all_conversations, conversations_by_domain = load_cross_domain_data(args.test_data)
    
    # Create dataset
    print("\nCreating dataset...")
    test_dataset = FraudDataset(all_conversations, tokenizer)
    
    # Evaluate overall
    print(f"\n{'='*60}")
    print("Overall Cross-Domain Evaluation")
    print(f"{'='*60}")
    
    predictions, true_labels = evaluate_model(model, test_dataset, all_conversations, device)
    overall_metrics = calculate_metrics(true_labels, predictions)
    
    print(f"\nOverall Results:")
    print(f"  Accuracy:  {overall_metrics['accuracy']*100:.2f}%")
    print(f"  Precision: {overall_metrics['precision']*100:.2f}%")
    print(f"  Recall:    {overall_metrics['recall']*100:.2f}%")
    print(f"  F1-Score:  {overall_metrics['f1']*100:.2f}%")
    
    cm = overall_metrics['confusion_matrix']
    print(f"\nConfusion Matrix:")
    print(f"  TN: {cm[0][0]:4d}  FP: {cm[0][1]:4d}")
    print(f"  FN: {cm[1][0]:4d}  TP: {cm[1][1]:4d}")
    
    # Compare with original
    print(f"\n{'='*60}")
    print("Comparison with Original Test (In-Domain)")
    print(f"{'='*60}")
    print(f"  Original (In-Domain):  F1 = 98.45%")
    print(f"  Cross-Domain:          F1 = {overall_metrics['f1']*100:.2f}%")
    diff = overall_metrics['f1']*100 - 98.45
    print(f"  Generalization Gap:    ΔF1 = {diff:+.2f}%")
    
    if diff > -3:
        print("\n  Pass Strong generalization (< 3% drop)")
    elif diff > -8:
        print("\n  Moderate generalization (3-8% drop)")
    else:
        print("\n  ✗ Poor generalization (> 8% drop)")
    
    # Per-domain analysis
    print(f"\n{'='*60}")
    print("Per-Domain Performance")
    print(f"{'='*60}")
    
    domain_results = {}
    
    for domain, convs in sorted(conversations_by_domain.items()):
        if len(convs) == 0:
            continue
        
        # Get predictions for this domain
        domain_indices = [i for i, c in enumerate(all_conversations) if c['domain'] == domain]
        domain_preds = [predictions[i] for i in domain_indices]
        domain_labels = [true_labels[i] for i in domain_indices]
        
        if len(domain_labels) > 0:
            domain_metrics = calculate_metrics(domain_labels, domain_preds)
            domain_results[domain] = domain_metrics
            
            print(f"\n{domain.upper()}:")
            print(f"  Samples:   {len(domain_labels)}")
            print(f"  Accuracy:  {domain_metrics['accuracy']*100:.2f}%")
            print(f"  Precision: {domain_metrics['precision']*100:.2f}%")
            print(f"  Recall:    {domain_metrics['recall']*100:.2f}%")
            print(f"  F1-Score:  {domain_metrics['f1']*100:.2f}%")
    
    # Save results
    results = {
        'overall': overall_metrics,
        'per_domain': domain_results,
        'comparison': {
            'original_f1': 98.45,
            'cross_domain_f1': overall_metrics['f1'] * 100,
            'generalization_gap': diff
        },
        'total_samples': len(all_conversations)
    }
    
    with open(output_dir / 'cross_domain_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    # Save predictions
    pred_df = pd.DataFrame({
        'file': [c['file'] for c in all_conversations],
        'domain': [c['domain'] for c in all_conversations],
        'scenario_id': [c['scenario_id'] for c in all_conversations],
        'true_label': true_labels,
        'predicted_label': predictions,
        'correct': [p == t for p, t in zip(predictions, true_labels)],
        'transcript_preview': [c['text'][:200] + '...' for c in all_conversations]
    })
    pred_df.to_csv(output_dir / 'cross_domain_predictions.csv', index=False)
    
    print(f"\n{'='*60}")
    print("Results saved to:")
    print(f"  {output_dir}/cross_domain_results.json")
    print(f"  {output_dir}/cross_domain_predictions.csv")
    print(f"{'='*60}\n")
    
    return 0


if __name__ == '__main__':
    exit(main())
