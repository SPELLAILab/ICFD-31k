#!/usr/bin/env python3
"""
Dataset Quality Evaluation Suite - Main Runner

Runs all evaluation tests and generates comprehensive report.

Usage:
    python run_evaluation.py --source-dir output/source_conversations
    python run_evaluation.py --source-dir output/source_conversations --sample-size 1000
    python run_evaluation.py --source-dir output/source_conversations --skip-tests perplexity tsne
"""

import argparse
import json
from pathlib import Path
from rich.console import Console
from rich.panel import Panel

from evaluation.evaluation_quality.utils import load_conversations, generate_markdown_report
from evaluation.evaluation_quality.distinct_n import DistinctNTest
from evaluation.evaluation_quality.ngram_overlap import NgramOverlapTest
from evaluation.evaluation_quality.zipf_law import ZipfLawTest
from evaluation.evaluation_quality.perplexity import PerplexityTest
from evaluation.evaluation_quality.semantic_similarity import SemanticSimilarityTest
from evaluation.evaluation_quality.tsne_visualization import TSNEVisualizationTest

console = Console()


def main():
    parser = argparse.ArgumentParser(
        description="Comprehensive dataset quality evaluation suite"
    )
    parser.add_argument(
        '--source-dir',
        type=str,
        default='output/source_conversations',
        help='Directory containing source conversations'
    )
    parser.add_argument(
        '--output-dir',
        type=str,
        default='evaluation_results',
        help='Directory to save evaluation results'
    )
    parser.add_argument(
        '--sample-size',
        type=int,
        default=None,
        help='Sample N conversations for faster evaluation (default: use all)'
    )
    parser.add_argument(
        '--skip-tests',
        nargs='+',
        choices=['distinct_n', 'ngram_overlap', 'zipf_law', 'perplexity', 'semantic_similarity', 'tsne'],
        default=[],
        help='Tests to skip'
    )
    
    args = parser.parse_args()
    
    # Print header
    console.print(Panel.fit(
        "[bold cyan]Dataset Quality Evaluation Suite[/bold cyan]\n"
        "Comprehensive quality assessment for fraud detection conversations\n"
        "Version 1.0",
        border_style="cyan"
    ))
    
    # Create output directory
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Load conversations
    conversations, labels, case_types, domains = load_conversations(
        args.source_dir, 
        args.sample_size
    )
    
    if len(conversations) == 0:
        console.print("[red]Error: No conversations loaded. Check source directory.[/red]")
        return
    
    # Store all results
    all_results = {}
    
    # Run tests
    try:
        if 'distinct_n' not in args.skip_tests:
            test = DistinctNTest(conversations, labels, case_types, output_dir)
            result = test.run()
            if result:
                all_results['distinct_n'] = result
        
        if 'ngram_overlap' not in args.skip_tests:
            test = NgramOverlapTest(conversations, labels, case_types, output_dir)
            result = test.run()
            if result:
                all_results['ngram_overlap'] = result
        
        if 'zipf_law' not in args.skip_tests:
            test = ZipfLawTest(conversations, labels, case_types, output_dir)
            result = test.run()
            if result:
                all_results['zipf_law'] = result
        
        if 'perplexity' not in args.skip_tests:
            test = PerplexityTest(conversations, labels, case_types, output_dir)
            result = test.run()
            if result:
                all_results['perplexity'] = result
        
        if 'semantic_similarity' not in args.skip_tests:
            test = SemanticSimilarityTest(conversations, labels, case_types, output_dir)
            result = test.run()
            if result:
                all_results['semantic_similarity'] = result
        
        if 'tsne' not in args.skip_tests:
            test = TSNEVisualizationTest(conversations, labels, case_types, output_dir)
            result = test.run()
            if result:
                all_results['tsne'] = result
    
    except KeyboardInterrupt:
        console.print("\n[yellow]Evaluation interrupted by user[/yellow]")
        return
    except Exception as e:
        console.print(f"\n[red]Error during evaluation: {e}[/red]")
        import traceback
        traceback.print_exc()
        return
    
    # Generate comprehensive report
    console.print("\n[bold blue]Generating Final Report...[/bold blue]")
    
    # Convert numpy types to native Python types for JSON serialization
    def convert_to_native(obj):
        import numpy as np
        if isinstance(obj, (np.integer, np.floating)):
            return float(obj)
        elif isinstance(obj, (np.ndarray,)):
            return obj.tolist()
        elif isinstance(obj, (np.bool_,)):
            return bool(obj)
        elif isinstance(obj, dict):
            return {k: convert_to_native(v) for k, v in obj.items()}
        elif isinstance(obj, (list, tuple)):
            return [convert_to_native(item) for item in obj]
        return obj
    
    # Save combined JSON results
    json_path = output_dir / 'all_results.json'
    with open(json_path, 'w') as f:
        json.dump(convert_to_native(all_results), f, indent=2)
    console.print(f"[green]✓ Combined results saved: {json_path}[/green]")
    
    # Generate markdown report
    report_path = generate_markdown_report(all_results, output_dir)
    
    # Print summary
    console.print("\n[bold green]✓ Evaluation Complete![/bold green]")
    console.print(f"Results saved in: [cyan]{output_dir}[/cyan]")
    console.print(f"Report: [cyan]{report_path}[/cyan]")
    
    # Count test results
    passed = sum(1 for r in all_results.values() if isinstance(r, dict) and r.get('pass', False))
    total = sum(1 for r in all_results.values() if isinstance(r, dict) and 'pass' in r)
    
    if total > 0:
        console.print(f"\nTests passed: [green]{passed}/{total}[/green] ({passed/total*100:.1f}%)")


if __name__ == '__main__':
    main()
