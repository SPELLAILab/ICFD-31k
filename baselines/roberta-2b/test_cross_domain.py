"""
Cross-Domain Generalization Test for RoBERTa 2b (Streaming)
=============================================================

Tests the streaming model on completely unseen fraud domains to evaluate:
1. Real-world generalization and robustness
2. Early detection performance on new fraud types
3. Temporal detection patterns across domains

This is a critical test for deployment readiness:
- Training: Banking, Tech, Healthcare, Govt, Jobs, etc.
- Testing: Crypto, Romance, Charity, Investment, Tax (NEW)

Key Differences from RoBERTa 2a:
- Uses chunk-level analysis for streaming detection
- Measures detection time for each fraud case
- Evaluates early detection rate on unseen domains

Usage:
    python test_cross_domain.py --test_data ../../output/source_conversations/testing_batch

"""

import json
import os
from pathlib import Path
from collections import defaultdict
import argparse

import pandas as pd
import numpy as np
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


def format_transcript_until_timestamp(transcript, end_time):
    """Format transcript up to a specific timestamp for streaming simulation"""
    formatted_parts = []
    for utterance in transcript:
        timestamp = utterance.get('timestamp_end', 0)
        if timestamp <= end_time:
            speaker = utterance.get('speaker', 'Unknown')
            text = utterance.get('text', '')
            formatted_parts.append(f"{speaker}: {text}")
        else:
            break
    return " ".join(formatted_parts)


def format_transcript(transcript):
    """Format full transcript to string"""
    formatted_parts = []
    for utterance in transcript:
        speaker = utterance.get('speaker', 'Unknown')
        text = utterance.get('text', '')
        formatted_parts.append(f"{speaker}: {text}")
    return " ".join(formatted_parts)


def load_cross_domain_data(data_dir):
    """Load cross-domain test conversations with chunk-level analysis"""
    print(f"\n{'='*60}")
    print("Loading Cross-Domain Test Data (Streaming Mode)")
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
            
            transcript = data.get('transcript', [])
            transcript_text = format_transcript(transcript)
            label = 1 if data.get('final_verdict') == 'YES' else 0
            
            # Get chunk-level analysis for streaming detection
            chunk_analysis = data.get('chunk_level_analysis', [])
            
            # Calculate actual fraud detection point (when verdict flips to YES)
            fraud_detection_time = None
            if label == 1:  # If it's fraud
                for chunk in chunk_analysis:
                    if chunk.get('verdict_at_chunk') == 'YES':
                        fraud_detection_time = chunk.get('timestamp', 0)
                        break
            
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
                'scenario_id': scenario_info.get('scenario_id', 0),
                'transcript': transcript,
                'chunk_analysis': chunk_analysis,
                'fraud_detection_time': fraud_detection_time,
                'conversation_duration': transcript[-1].get('timestamp_end', 0) if transcript else 0
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


def evaluate_streaming_detection(model, tokenizer, conversations, device='cuda', chunk_interval=10.0):
    """
    Evaluate model with streaming detection simulation.
    
    Tests model at regular intervals (e.g., every 10 seconds) to measure:
    - When fraud is first detected
    - Early detection rate (detected before fraud occurs)
    - Detection time statistics
    """
    model.eval()
    model.to(device)
    
    results = []
    
    print(f"\nSimulating streaming detection (every {chunk_interval}s)...")
    
    for conv in tqdm(conversations, desc="Evaluating streaming"):
        transcript = conv['transcript']
        true_label = conv['label']
        fraud_detection_time = conv['fraud_detection_time']
        conversation_duration = conv['conversation_duration']
        
        # Skip if no transcript
        if not transcript:
            continue
        
        # Generate timestamps to test (every chunk_interval seconds)
        test_timestamps = []
        current_time = chunk_interval
        while current_time <= conversation_duration:
            test_timestamps.append(current_time)
            current_time += chunk_interval
        
        # Add final timestamp if not already included
        if conversation_duration not in test_timestamps:
            test_timestamps.append(conversation_duration)
        
        # Track when model first detects fraud
        model_detection_time = None
        final_prediction = 0
        
        with torch.no_grad():
            for timestamp in test_timestamps:
                # Get transcript up to this timestamp
                partial_transcript = format_transcript_until_timestamp(transcript, timestamp)
                
                # Skip if empty
                if not partial_transcript.strip():
                    continue
                
                # Tokenize and predict
                encoding = tokenizer(
                    partial_transcript,
                    truncation=True,
                    padding='max_length',
                    max_length=512,
                    return_tensors='pt'
                )
                
                input_ids = encoding['input_ids'].to(device)
                attention_mask = encoding['attention_mask'].to(device)
                
                outputs = model(input_ids=input_ids, attention_mask=attention_mask)
                logits = outputs.logits
                pred = torch.argmax(logits, dim=1).item()
                
                # Record when model first predicts fraud
                if pred == 1 and model_detection_time is None:
                    model_detection_time = timestamp
                
                # Update final prediction
                final_prediction = pred
        
        # Calculate detection metrics
        detected_early = False
        detection_latency = None
        
        if true_label == 1 and fraud_detection_time is not None:
            if model_detection_time is not None:
                detection_latency = model_detection_time - fraud_detection_time
                detected_early = detection_latency <= 0  # Detected at or before fraud occurs
        
        results.append({
            'file': conv['file'],
            'domain': conv['domain'],
            'scenario_id': conv['scenario_id'],
            'true_label': true_label,
            'final_prediction': final_prediction,
            'correct': final_prediction == true_label,
            'fraud_detection_time': fraud_detection_time,
            'model_detection_time': model_detection_time,
            'detection_latency': detection_latency,
            'detected_early': detected_early,
            'conversation_duration': conversation_duration
        })
    
    return results


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


def calculate_early_detection_metrics(results):
    """Calculate early detection metrics for fraud cases"""
    fraud_cases = [r for r in results if r['true_label'] == 1]
    
    if not fraud_cases:
        return {}
    
    # Cases where fraud was detected
    detected_cases = [r for r in fraud_cases if r['model_detection_time'] is not None]
    
    # Early detection (detected at or before fraud occurs)
    early_detected = [r for r in detected_cases if r['detected_early']]
    
    # Calculate statistics
    detection_times = [r['detection_latency'] for r in detected_cases if r['detection_latency'] is not None]
    
    return {
        'total_fraud_cases': len(fraud_cases),
        'detected_fraud_cases': len(detected_cases),
        'early_detected_cases': len(early_detected),
        'early_detection_rate': len(early_detected) / len(fraud_cases) * 100 if fraud_cases else 0,
        'mean_detection_time': float(np.mean([r['model_detection_time'] for r in detected_cases])) if detected_cases else None,
        'median_detection_time': float(np.median([r['model_detection_time'] for r in detected_cases])) if detected_cases else None,
        'mean_detection_latency': float(np.mean(detection_times)) if detection_times else None,
        'median_detection_latency': float(np.median(detection_times)) if detection_times else None,
    }


def main():
    parser = argparse.ArgumentParser(description='Cross-domain generalization test (streaming)')
    parser.add_argument('--model_dir', type=str, 
                       default='./final_model',
                       help='Path to saved model')
    parser.add_argument('--test_data', type=str,
                       required=True,
                       help='Path to cross-domain test data')
    parser.add_argument('--output_dir', type=str,
                       default='./cross_domain_results',
                       help='Output directory for results')
    parser.add_argument('--chunk_interval', type=float,
                       default=10.0,
                       help='Chunk interval for streaming simulation (seconds)')
    
    args = parser.parse_args()
    
    print("\n" + "="*60)
    print("Cross-Domain Generalization Test (Streaming)")
    print("="*60)
    
    # Check device (with MPS support for Apple Silicon)
    if torch.cuda.is_available():
        device = 'cuda'
    elif torch.backends.mps.is_available():
        device = 'mps'
        print("Using Apple Silicon GPU (MPS) - This will be MUCH faster than CPU!")
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
    
    # Evaluate with streaming detection
    print(f"\n{'='*60}")
    print("Overall Cross-Domain Evaluation (Streaming)")
    print(f"{'='*60}")
    
    results = evaluate_streaming_detection(
        model, tokenizer, all_conversations, device, args.chunk_interval
    )
    
    # Calculate overall metrics
    true_labels = [r['true_label'] for r in results]
    predictions = [r['final_prediction'] for r in results]
    overall_metrics = calculate_metrics(true_labels, predictions)
    
    print(f"\n{'='*60}")
    print("Standard Classification Metrics")
    print(f"{'='*60}")
    print(f"  Accuracy:  {overall_metrics['accuracy']*100:.2f}%")
    print(f"  Precision: {overall_metrics['precision']*100:.2f}%")
    print(f"  Recall:    {overall_metrics['recall']*100:.2f}%")
    print(f"  F1-Score:  {overall_metrics['f1']*100:.2f}%")
    
    cm = overall_metrics['confusion_matrix']
    print(f"\nConfusion Matrix:")
    print(f"  TN: {cm[0][0]:4d}  FP: {cm[0][1]:4d}")
    print(f"  FN: {cm[1][0]:4d}  TP: {cm[1][1]:4d}")
    
    # Calculate early detection metrics
    early_detection_metrics = calculate_early_detection_metrics(results)
    
    print(f"\n{'='*60}")
    print("Early Detection Metrics (Streaming)")
    print(f"{'='*60}")
    print(f"  Total Fraud Cases:      {early_detection_metrics['total_fraud_cases']}")
    print(f"  Detected:               {early_detection_metrics['detected_fraud_cases']}")
    print(f"  Early Detected:         {early_detection_metrics['early_detected_cases']}")
    print(f"  Early Detection Rate:   {early_detection_metrics['early_detection_rate']:.2f}%")
    
    if early_detection_metrics['mean_detection_time']:
        print(f"\n  Mean Detection Time:    {early_detection_metrics['mean_detection_time']:.1f}s")
        print(f"  Median Detection Time:  {early_detection_metrics['median_detection_time']:.1f}s")
    
    if early_detection_metrics['mean_detection_latency']:
        print(f"\n  Mean Detection Latency: {early_detection_metrics['mean_detection_latency']:+.1f}s")
        print(f"  Median Detection Latency: {early_detection_metrics['median_detection_latency']:+.1f}s")
        print(f"  (Negative = detected before fraud, Positive = detected after fraud)")
    
    # Compare with original and RoBERTa 2a
    print(f"\n{'='*60}")
    print("Comparison with Other Models")
    print(f"{'='*60}")
    print(f"  RoBERTa 2a (In-Domain):     F1 = 98.45%")
    print(f"  RoBERTa 2a (Cross-Domain):  F1 = 92.97%")
    print(f"  RoBERTa 2b (In-Domain):     F1 = 95.59%")
    print(f"  RoBERTa 2b (Cross-Domain):  F1 = {overall_metrics['f1']*100:.2f}%")
    
    diff_from_2a = overall_metrics['f1']*100 - 92.97
    print(f"\n  Δ vs RoBERTa 2a (Cross):    {diff_from_2a:+.2f}%")
    
    diff_from_indomain = overall_metrics['f1']*100 - 95.59
    print(f"  Generalization Gap (2b):    ΔF1 = {diff_from_indomain:+.2f}%")
    
    if abs(diff_from_indomain) < 3:
        print("\n  Pass Strong generalization (< 3% drop)")
    elif abs(diff_from_indomain) < 8:
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
        
        # Get results for this domain
        domain_results_list = [r for r in results if r['domain'] == domain]
        domain_labels = [r['true_label'] for r in domain_results_list]
        domain_preds = [r['final_prediction'] for r in domain_results_list]
        
        if len(domain_labels) > 0:
            domain_metrics = calculate_metrics(domain_labels, domain_preds)
            domain_early_detection = calculate_early_detection_metrics(domain_results_list)
            
            domain_results[domain] = {
                'classification': domain_metrics,
                'early_detection': domain_early_detection
            }
            
            print(f"\n{domain.upper()}:")
            print(f"  Samples:   {len(domain_labels)}")
            print(f"  Accuracy:  {domain_metrics['accuracy']*100:.2f}%")
            print(f"  Precision: {domain_metrics['precision']*100:.2f}%")
            print(f"  Recall:    {domain_metrics['recall']*100:.2f}%")
            print(f"  F1-Score:  {domain_metrics['f1']*100:.2f}%")
            
            if domain_early_detection['total_fraud_cases'] > 0:
                print(f"  Early Detection Rate: {domain_early_detection['early_detection_rate']:.1f}%")
    
    # Save results
    results_summary = {
        'overall': {
            'classification': overall_metrics,
            'early_detection': early_detection_metrics
        },
        'per_domain': domain_results,
        'comparison': {
            '2a_in_domain_f1': 98.45,
            '2a_cross_domain_f1': 92.97,
            '2b_in_domain_f1': 95.59,
            '2b_cross_domain_f1': overall_metrics['f1'] * 100,
            'generalization_gap_2b': diff_from_indomain,
            'delta_vs_2a_cross': diff_from_2a
        },
        'total_samples': len(all_conversations)
    }
    
    with open(output_dir / 'cross_domain_results.json', 'w') as f:
        json.dump(results_summary, f, indent=2)
    
    # Save detailed predictions
    pred_df = pd.DataFrame(results)
    pred_df.to_csv(output_dir / 'cross_domain_predictions.csv', index=False)
    
    print(f"\n{'='*60}")
    print("Results saved to:")
    print(f"  {output_dir}/cross_domain_results.json")
    print(f"  {output_dir}/cross_domain_predictions.csv")
    print(f"{'='*60}\n")
    
    return 0


if __name__ == '__main__':
    exit(main())
