"""
Gemma Zero-Shot Results Analysis
==============================

Analyze and visualize results from Gemma zero-shot evaluation.
"""

import json
import argparse
from pathlib import Path
import pandas as pd
import numpy as np
from typing import Dict, Any


def load_results(results_dir: str) -> tuple[pd.DataFrame, Dict[str, Any]]:
    """Load results from evaluation."""
    results_path = Path(results_dir)
    
    # Load detailed results
    df = pd.read_csv(results_path / 'detailed_results.csv')
    
    # Load metrics
    with open(results_path / 'metrics.json', 'r') as f:
        metrics = json.load(f)
    
    return df, metrics


def analyze_errors(df: pd.DataFrame):
    """Analyze error patterns."""
    print(f"\n{'='*60}")
    print("ERROR ANALYSIS")
    print(f"{'='*60}")
    
    # Overall error rate
    total_samples = len(df)
    error_samples = df['error'].notna().sum()
    success_samples = total_samples - error_samples
    
    print(f"Total samples: {total_samples}")
    print(f"Successful: {success_samples} ({success_samples/total_samples*100:.2f}%)")
    print(f"Errors: {error_samples} ({error_samples/total_samples*100:.2f}%)")
    
    if error_samples > 0:
        print(f"\nError examples:")
        error_df = df[df['error'].notna()].head(5)
        for _, row in error_df.iterrows():
            print(f"  Sample {row['sample_id']}: {row['error'][:100]}...")


def analyze_predictions(df: pd.DataFrame):
    """Analyze prediction patterns."""
    print(f"\n{'='*60}")
    print("PREDICTION ANALYSIS")
    print(f"{'='*60}")
    
    # Filter successful predictions
    success_df = df[df['error'].isna()].copy()
    
    if len(success_df) == 0:
        print("No successful predictions to analyze.")
        return
    
    # Prediction distribution
    pred_counts = success_df['predicted_label'].value_counts()
    print(f"\nPrediction distribution:")
    for label, count in pred_counts.items():
        print(f"  {label}: {count} ({count/len(success_df)*100:.2f}%)")
    
    # Confidence analysis
    print(f"\nConfidence statistics:")
    print(f"  Mean: {success_df['confidence'].mean():.3f}")
    print(f"  Median: {success_df['confidence'].median():.3f}")
    print(f"  Std: {success_df['confidence'].std():.3f}")
    print(f"  Min: {success_df['confidence'].min():.3f}")
    print(f"  Max: {success_df['confidence'].max():.3f}")
    
    # Confidence by prediction
    for label in success_df['predicted_label'].unique():
        label_df = success_df[success_df['predicted_label'] == label]
        print(f"  {label} confidence: {label_df['confidence'].mean():.3f} ± {label_df['confidence'].std():.3f}")


def analyze_performance_by_label(df: pd.DataFrame):
    """Analyze performance by true label."""
    print(f"\n{'='*60}")
    print("PERFORMANCE BY TRUE LABEL")
    print(f"{'='*60}")
    
    # Filter successful predictions
    success_df = df[df['error'].isna()].copy()
    
    if len(success_df) == 0:
        return
    
    for true_label in success_df['true_label'].unique():
        label_df = success_df[success_df['true_label'] == true_label]
        
        correct = label_df['correct'].sum()
        total = len(label_df)
        accuracy = correct / total * 100
        
        print(f"\nTrue Label: {true_label}")
        print(f"  Samples: {total}")
        print(f"  Correct: {correct}")
        print(f"  Accuracy: {accuracy:.2f}%")
        
        # Prediction breakdown
        pred_counts = label_df['predicted_label'].value_counts()
        for pred, count in pred_counts.items():
            print(f"    Predicted {pred}: {count} ({count/total*100:.2f}%)")


def analyze_timing(df: pd.DataFrame):
    """Analyze processing time patterns."""
    print(f"\n{'='*60}")
    print("TIMING ANALYSIS")
    print(f"{'='*60}")
    
    # Filter successful predictions
    success_df = df[df['error'].isna()].copy()
    
    if len(success_df) == 0:
        return
    
    times = success_df['processing_time']
    
    print(f"Processing time statistics:")
    print(f"  Mean: {times.mean():.2f}s")
    print(f"  Median: {times.median():.2f}s")
    print(f"  Std: {times.std():.2f}s")
    print(f"  Min: {times.min():.2f}s")
    print(f"  Max: {times.max():.2f}s")
    print(f"  Total: {times.sum():.2f}s ({times.sum()/60:.1f}m)")
    
    # Timing by prediction
    for label in success_df['predicted_label'].unique():
        label_times = success_df[success_df['predicted_label'] == label]['processing_time']
        print(f"  {label} avg time: {label_times.mean():.2f}s")


def compare_with_baselines(metrics: Dict[str, Any]):
    """Compare with baseline models."""
    print(f"\n{'='*60}")
    print("COMPARISON WITH TRAINED MODELS")
    print(f"{'='*60}")
    
    overall = metrics['overall_metrics']
    
    # Baseline performance (from previous results)
    baselines = {
        'RoBERTa 2a (In-Domain)': {'f1': 98.45, 'accuracy': 99.63},
        'RoBERTa 2a (Cross-Domain)': {'f1': 92.97, 'accuracy': 87.20},
        'RoBERTa 2b (In-Domain)': {'f1': 95.59, 'accuracy': 95.40},
        'RoBERTa 2b (Cross-Domain)': {'f1': 88.56, 'accuracy': 79.90},
    }
    
    gemma_f1 = overall['f1'] * 100
    gemma_acc = overall['accuracy'] * 100
    
    print(f"{'Model':<30} {'F1-Score':<10} {'Accuracy':<10} {'F1 Gap':<10}")
    print(f"{'-'*65}")
    
    print(f"{'Gemma Zero-Shot':<30} {gemma_f1:<10.2f} {gemma_acc:<10.2f} {'--':<10}")
    
    for name, scores in baselines.items():
        f1_gap = gemma_f1 - scores['f1']
        print(f"{name:<30} {scores['f1']:<10.2f} {scores['accuracy']:<10.2f} {f1_gap:<10.2f}")
    
    print(f"\nKey Insights:")
    
    # Performance gaps
    gaps = {name: gemma_f1 - scores['f1'] for name, scores in baselines.items()}
    
    best_gap = max(gaps.values())
    worst_gap = min(gaps.values())
    
    if best_gap > -5:
        print(f"   Strong zero-shot performance. Gap to best trained model: {worst_gap:.2f}%")
    elif best_gap > -15:
        print(f"   Moderate zero-shot performance. Gap to best trained model: {worst_gap:.2f}%")
    else:
        print(f"   Weak zero-shot performance. Gap to best trained model: {worst_gap:.2f}%")
    
    # Compare with cross-domain
    cross_domain_gap = gemma_f1 - baselines['RoBERTa 2a (Cross-Domain)']['f1']
    if cross_domain_gap > -5:
        print(f"   Competitive with cross-domain performance. Gap: {cross_domain_gap:.2f}%")
    else:
        print(f"   Below cross-domain performance. Gap: {cross_domain_gap:.2f}%")


def show_sample_responses(df: pd.DataFrame, n_samples: int = 5):
    """Show sample responses for analysis."""
    print(f"\n{'='*60}")
    print(f"SAMPLE RESPONSES (First {n_samples})")
    print(f"{'='*60}")
    
    # Filter successful predictions
    success_df = df[df['error'].isna()].copy()
    
    if len(success_df) == 0:
        print("No successful predictions to show.")
        return
    
    sample_df = success_df.head(n_samples)
    
    for i, (_, row) in enumerate(sample_df.iterrows(), 1):
        status = "CORRECT" if row['correct'] else "INCORRECT"
        
        print(f"\n--- Sample {i} ({row['sample_id']}) ---")
        print(f"True: {row['true_label']} | Predicted: {row['predicted_label']} | {status}")
        print(f"Confidence: {row['confidence']:.3f} | Time: {row['processing_time']:.2f}s")
        print(f"Response: {row['response_preview']}")


def main():
    parser = argparse.ArgumentParser(description='Analyze Gemma zero-shot results')
    parser.add_argument('--results_dir', type=str, default='./results',
                       help='Directory containing results')
    parser.add_argument('--show_samples', type=int, default=5,
                       help='Number of sample responses to show')
    
    args = parser.parse_args()
    
    results_path = Path(args.results_dir)
    if not results_path.exists():
        print(f"Results directory not found: {args.results_dir}")
        return 1
    
    print(f"Loading results from: {args.results_dir}")
    
    try:
        df, metrics = load_results(args.results_dir)
        
        print(f"\n{'='*60}")
        print("GEMMA ZERO-SHOT EVALUATION ANALYSIS")
        print(f"{'='*60}")
        print(f"Total samples: {len(df)}")
        
        # Run analyses
        analyze_errors(df)
        analyze_predictions(df)
        analyze_performance_by_label(df)
        analyze_timing(df)
        compare_with_baselines(metrics)
        show_sample_responses(df, args.show_samples)
        
        print(f"\n{'='*60}")
        print("Analysis complete")
        print(f"{'='*60}")
        
    except Exception as e:
        print(f"Error during analysis: {e}")
        return 1
    
    return 0


if __name__ == '__main__':
    exit(main())