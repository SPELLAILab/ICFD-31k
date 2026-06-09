#!/usr/bin/env python3
"""
Dataset Statistics Calculator
==============================

Calculates comprehensive statistics for the fraud detection dataset:
1. Average conversation length from source conversations
2. Chunk timestamp intervals from training data
3. Total chunk counts from valid batches only

Usage:
    python calculate_dataset_stats.py
    python calculate_dataset_stats.py --detailed  # Show per-batch breakdown
"""

import json
import argparse
from pathlib import Path
from collections import defaultdict
import statistics

# Valid batch directories (exclude bad batches)
VALID_BATCHES = [
    'batch_2025-10-11_21-42-13',
    'batch_2025-10-12_19-54-00',
    'batch_2025-10-12_22-36-40',
    'batch_2025-10-12_23-39-07',
    'batch_2025-10-13_00-20-15',
    'batch_2025-10-13_01-02-16',
    'batch_2025-10-13_01-36-50',
    'batch_2025-10-13_02-01-52',
    'batch_2025-10-13_02-35-27',
    'batch_2025-10-13_02-53-33',
    'testing_batch'
]


def calculate_conversation_stats(source_dir):
    """Calculate average conversation length from source conversations."""
    print("\n" + "="*70)
    print("CONVERSATION LENGTH ANALYSIS")
    print("="*70)
    
    source_path = Path(source_dir)
    conversation_lengths = []
    batch_stats = defaultdict(list)
    
    for batch_name in VALID_BATCHES:
        batch_dir = source_path / batch_name
        if not batch_dir.exists():
            print(f"WARN: Batch not found: {batch_name}")
            continue
        
        json_files = list(batch_dir.glob("*.json"))
        
        for json_file in json_files:
            try:
                with open(json_file, 'r') as f:
                    data = json.load(f)
                
                # Get the last timestamp from transcript
                transcript = data.get('transcript', [])
                if transcript:
                    last_timestamp = transcript[-1].get('timestamp_end', 0)
                    # Ensure it's a float
                    last_timestamp = float(last_timestamp) if last_timestamp else 0
                    if last_timestamp > 0:
                        conversation_lengths.append(last_timestamp)
                        batch_stats[batch_name].append(last_timestamp)
                    
            except Exception as e:
                print(f"WARN: Error reading {json_file.name}: {e}")
                continue
    
    if not conversation_lengths:
        print("FAIL: No conversations found!")
        return None
    
    # Calculate overall statistics
    avg_length = statistics.mean(conversation_lengths)
    median_length = statistics.median(conversation_lengths)
    min_length = min(conversation_lengths)
    max_length = max(conversation_lengths)
    stdev_length = statistics.stdev(conversation_lengths) if len(conversation_lengths) > 1 else 0
    
    print(f"\n📊 Overall Statistics:")
    print(f"   Total Conversations: {len(conversation_lengths):,}")
    print(f"   Average Length:      {avg_length:.2f} seconds")
    print(f"   Median Length:       {median_length:.2f} seconds")
    print(f"   Min Length:          {min_length:.2f} seconds")
    print(f"   Max Length:          {max_length:.2f} seconds")
    print(f"   Std Deviation:       {stdev_length:.2f} seconds")
    
    # Distribution analysis
    ranges = {
        '< 60s': sum(1 for l in conversation_lengths if l < 60),
        '60-120s': sum(1 for l in conversation_lengths if 60 <= l < 120),
        '120-180s': sum(1 for l in conversation_lengths if 120 <= l < 180),
        '180-240s': sum(1 for l in conversation_lengths if 180 <= l < 240),
        '240-300s': sum(1 for l in conversation_lengths if 240 <= l < 300),
        '300-360s': sum(1 for l in conversation_lengths if 300 <= l < 360),
        '> 360s': sum(1 for l in conversation_lengths if l >= 360),
    }
    
    print(f"\n📈 Length Distribution:")
    for range_name, count in ranges.items():
        percentage = (count / len(conversation_lengths)) * 100
        bar = '█' * int(percentage / 2)
        print(f"   {range_name:>10s}: {count:5,} ({percentage:5.1f}%) {bar}")
    
    return {
        'batch_stats': batch_stats,
        'overall_stats': {
            'count': len(conversation_lengths),
            'mean': avg_length,
            'median': median_length,
            'min': min_length,
            'max': max_length,
            'stdev': stdev_length
        }
    }


def calculate_chunk_intervals(training_dir):
    """Analyze chunk timestamp intervals from training data."""
    print("\n" + "="*70)
    print("CHUNK INTERVAL ANALYSIS")
    print("="*70)
    
    training_path = Path(training_dir)
    chunk_timestamps_by_conv = defaultdict(list)
    
    # Sample from first valid batch
    for batch_name in VALID_BATCHES:
        batch_dir = training_path / batch_name
        if not batch_dir.exists():
            continue
        
        # Get files from a few conversations
        json_files = sorted(list(batch_dir.glob("*.json")))[:200]  # Sample more files
        
        for json_file in json_files:
            # Parse timestamp from filename: *_chunk_XXs.json
            if '_chunk_' in json_file.name:
                try:
                    timestamp_str = json_file.name.split('_chunk_')[1].replace('s.json', '')
                    timestamp = int(timestamp_str)
                    
                    # Group by base conversation name
                    base_name = json_file.name.split('_chunk_')[0]
                    chunk_timestamps_by_conv[base_name].append(timestamp)
                    
                except (ValueError, IndexError):
                    continue
        
        if chunk_timestamps_by_conv:
            break
    
    if not chunk_timestamps_by_conv:
        print("FAIL: No chunk data found!")
        return None
    
    # Calculate intervals for each conversation
    all_intervals = []
    for base_name, timestamps in chunk_timestamps_by_conv.items():
        sorted_timestamps = sorted(timestamps)
        if len(sorted_timestamps) > 1:
            intervals = [sorted_timestamps[i+1] - sorted_timestamps[i] 
                        for i in range(len(sorted_timestamps)-1)]
            all_intervals.extend(intervals)
    
    if all_intervals:
        avg_interval = statistics.mean(all_intervals)
        mode_interval = statistics.mode(all_intervals)
        unique_intervals = sorted(set(all_intervals))
        
        print(f"\n📊 Chunk Interval Statistics:")
        print(f"   Conversations Analyzed: {len(chunk_timestamps_by_conv)}")
        print(f"   Total Intervals Found:  {len(all_intervals)}")
        print(f"   Average Interval:       {avg_interval:.2f} seconds")
        print(f"   Most Common Interval:   {mode_interval} seconds")
        print(f"   Unique Intervals:       {unique_intervals}")
        
        # Count frequency of each interval
        interval_counts = defaultdict(int)
        for interval in all_intervals:
            interval_counts[interval] += 1
        
        print(f"\n📈 Interval Distribution:")
        for interval in sorted(interval_counts.keys())[:10]:  # Show top 10
            count = interval_counts[interval]
            percentage = (count / len(all_intervals)) * 100
            bar = '█' * int(percentage / 2)
            print(f"   {interval:3d}s: {count:4,} ({percentage:5.1f}%) {bar}")
        
        return {
            'average_interval': avg_interval,
            'mode_interval': mode_interval,
            'unique_intervals': unique_intervals,
            'conversations_analyzed': len(chunk_timestamps_by_conv)
        }
    else:
        print("WARN: Could not determine chunk intervals from sample")
        return None


def calculate_chunk_counts(training_dir):
    """Calculate total chunk counts from valid batches only."""
    print("\n" + "="*70)
    print("TRAINING CHUNKS COUNT (Valid Batches Only)")
    print("="*70)
    
    training_path = Path(training_dir)
    batch_counts = {}
    total_chunks = 0
    
    for batch_name in VALID_BATCHES:
        batch_dir = training_path / batch_name
        if not batch_dir.exists():
            print(f"WARN: Batch not found: {batch_name}")
            continue
        
        json_files = list(batch_dir.glob("*.json"))
        count = len(json_files)
        batch_counts[batch_name] = count
        total_chunks += count
    
    print(f"\n📦 Per-Batch Chunk Counts:")
    for batch_name in VALID_BATCHES:
        if batch_name in batch_counts:
            count = batch_counts[batch_name]
            percentage = (count / total_chunks * 100) if total_chunks > 0 else 0
            print(f"   {batch_name:30s}: {count:7,} ({percentage:5.1f}%)")
    
    print(f"\n{'='*70}")
    print(f"   {'TOTAL TRAINING CHUNKS':30s}: {total_chunks:7,}")
    print(f"{'='*70}")
    
    return {
        'batch_counts': batch_counts,
        'total_chunks': total_chunks
    }


def main():
    parser = argparse.ArgumentParser(
        description='Calculate comprehensive dataset statistics',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument('--detailed', action='store_true',
                       help='Show detailed per-batch breakdown')
    parser.add_argument('--source-dir', type=str,
                       default='output/source_conversations',
                       help='Path to source conversations directory')
    parser.add_argument('--training-dir', type=str,
                       default='output/training_data',
                       help='Path to training data directory')
    
    args = parser.parse_args()
    
    print("\n" + "="*70)
    print("FRAUD DETECTION DATASET STATISTICS CALCULATOR")
    print("="*70)
    print(f"Valid Batches: {len(VALID_BATCHES)}")
    print(f"Source Dir:    {args.source_dir}")
    print(f"Training Dir:  {args.training_dir}")
    
    # Calculate conversation statistics
    conv_stats = calculate_conversation_stats(args.source_dir)
    
    # Calculate chunk intervals
    chunk_intervals = calculate_chunk_intervals(args.training_dir)
    
    # Calculate chunk counts
    chunk_counts = calculate_chunk_counts(args.training_dir)
    
    # Summary for research paper
    print("\n" + "="*70)
    print("SUMMARY FOR RESEARCH PAPER")
    print("="*70)
    
    if conv_stats:
        print(f"\n📄 Source Conversations:")
        print(f"   Total:              {conv_stats['overall_stats']['count']:,}")
        print(f"   Avg Length:         {conv_stats['overall_stats']['mean']:.1f} seconds")
        print(f"   Range:              {conv_stats['overall_stats']['min']:.0f}-{conv_stats['overall_stats']['max']:.0f} seconds")
    
    if chunk_intervals:
        print(f"\n⏱️  Chunk Intervals:")
        print(f"   Primary Interval:   {chunk_intervals['mode_interval']} seconds")
        print(f"   All Intervals:      {chunk_intervals['unique_intervals']}")
    
    if chunk_counts:
        print(f"\n📊 Training Chunks:")
        print(f"   Total:              {chunk_counts['total_chunks']:,}")
        print(f"   Valid Batches:      {len(chunk_counts['batch_counts'])}")
    
    if conv_stats and chunk_counts:
        chunks_per_conv = chunk_counts['total_chunks'] / conv_stats['overall_stats']['count']
        print(f"   Avg Chunks/Conv:    {chunks_per_conv:.1f}")
    
    print("\n" + "="*70)
    print("PASS: Analysis Complete!")
    print("="*70 + "\n")


if __name__ == '__main__':
    main()
