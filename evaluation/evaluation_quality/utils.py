"""
Utility functions for evaluation suite
"""

import json
from pathlib import Path
from typing import List, Tuple
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn
from collections import Counter

console = Console()


def load_conversations(source_dir: Path, sample_size: int = None) -> Tuple[List[str], List[str], List[str], List[str]]:
    """
    Load conversations from source directory
    
    Args:
        source_dir: Path to directory containing JSON conversation files
        sample_size: Optional number of conversations to sample
    
    Returns:
        Tuple of (conversations, labels, case_types, domains)
    """
    console.print("\n[bold blue]Loading conversations...[/bold blue]")
    
    source_dir = Path(source_dir)
    json_files = list(source_dir.rglob("*.json"))
    
    if sample_size and len(json_files) > sample_size:
        import random
        json_files = random.sample(json_files, sample_size)
        console.print(f"[yellow]Sampling {sample_size} conversations for faster evaluation[/yellow]")
    
    conversations = []
    labels = []
    case_types = []
    domains = []
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TaskProgressColumn(),
    ) as progress:
        task = progress.add_task("Loading...", total=len(json_files))
        
        for json_file in json_files:
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                # Extract full conversation text
                conversation_text = data.get('conversation', '')
                
                # Try alternative formats
                if not conversation_text and 'transcript' in data:
                    # Format: transcript with speaker/text pairs
                    conversation_text = ' '.join([
                        turn.get('text', '') for turn in data['transcript']
                    ])
                elif not conversation_text and 'turns' in data:
                    # Format: turns with content
                    conversation_text = ' '.join([
                        turn.get('content', '') for turn in data['turns']
                    ])
                
                if conversation_text:
                    conversations.append(conversation_text)
                    
                    # Extract label (try multiple fields)
                    label = (data.get('label') or 
                            data.get('final_verdict') or 
                            data.get('is_fraud') or 
                            'UNKNOWN')
                    labels.append(label)
                    
                    # Extract case type from scenario or top level
                    scenario = data.get('scenario', {})
                    if isinstance(scenario, dict):
                        case_type = scenario.get('case_type', data.get('case_type', 'UNKNOWN'))
                        domain = scenario.get('domain', 'UNKNOWN')
                    else:
                        case_type = data.get('case_type', 'UNKNOWN')
                        domain = 'UNKNOWN'
                    
                    case_types.append(case_type)
                    domains.append(domain)
            
            except Exception as e:
                console.print(f"[red]Error loading {json_file}: {e}[/red]")
            
            progress.update(task, advance=1)
    
    console.print(f"[green]✓ Loaded {len(conversations)} conversations[/green]")
    
    # Print distribution
    label_counts = Counter(labels)
    console.print(f"  Fraud: {label_counts.get('YES', 0)}, Normal: {label_counts.get('NO', 0)}")
    
    return conversations, labels, case_types, domains


def generate_markdown_report(results: dict, output_dir: Path):
    """
    Generate comprehensive markdown report from test results
    
    Args:
        results: Dictionary of test results
        output_dir: Directory to save report
    """
    import numpy as np
    
    report_lines = [
        "# Dataset Quality Evaluation Report",
        f"\n**Date**: {np.datetime64('today')}",
        f"**Tests Run**: {len(results)}",
        "\n---\n",
        "## Summary of Results\n"
    ]
    
    # Count passes
    passes = 0
    total = 0
    
    # Distinct-n
    if 'distinct_n' in results:
        dn = results['distinct_n']
        report_lines.extend([
            "### 1. Linguistic Diversity (Distinct-n)",
            f"- **Distinct-1**: {dn['distinct_1']:.4f} (threshold: >0.05) {'✓' if dn['distinct_1'] > 0.05 else '⚠'}",
            f"- **Distinct-2**: {dn['distinct_2']:.4f} (threshold: >0.30) {'✓' if dn['distinct_2'] > 0.30 else '⚠'}",
            f"- **Distinct-3**: {dn['distinct_3']:.4f} (threshold: >0.50) {'✓' if dn['distinct_3'] > 0.50 else '⚠'}",
            f"- **Status**: {'✓ PASS' if dn.get('pass', False) else '⚠ FAIL'}",
            ""
        ])
        if dn.get('pass', False):
            passes += 1
        total += 1
    
    # N-gram Overlap
    if 'ngram_overlap' in results:
        no = results['ngram_overlap']
        report_lines.append("### 2. N-gram Overlap")
        for n_type in ['1-gram', '2-gram', '3-gram']:
            if n_type in no:
                stats = no[n_type]
                report_lines.append(f"- **{n_type}**: {stats['mean']*100:.2f}% ± {stats['std']*100:.2f}%")
        report_lines.append(f"- **Status**: {'✓ PASS' if no.get('pass', False) else '⚠ FAIL'}")
        report_lines.append("")
        if no.get('pass', False):
            passes += 1
        total += 1
    
    # Zipf's Law
    if 'zipf_law' in results:
        zl = results['zipf_law']
        report_lines.extend([
            "### 3. Zipf's Law",
            f"- **MSE**: {zl['mse']:.4f} (threshold: <0.05) {'✓' if zl['mse'] < 0.05 else '⚠'}",
            f"- **Slope**: {zl['slope']:.3f} (expected: ≈-1.0) {'✓' if -1.2 < zl['slope'] < -0.8 else '⚠'}",
            f"- **Vocabulary Size**: {zl['vocabulary_size']:,}",
            f"- **Status**: {'✓ PASS' if zl.get('pass', False) else '⚠ FAIL'}",
            ""
        ])
        if zl.get('pass', False):
            passes += 1
        total += 1
    
    # Perplexity
    if 'perplexity' in results:
        pp = results['perplexity']
        report_lines.extend([
            "### 4. Perplexity (GPT-2)",
            f"- **Fraud Mean**: {pp['fraud_mean']:.2f} ± {pp['fraud_std']:.2f}",
            f"- **Normal Mean**: {pp['normal_mean']:.2f} ± {pp['normal_std']:.2f}",
            f"- **Status**: {'✓ PASS' if pp.get('pass', False) else '⚠ FAIL'}",
            ""
        ])
        if pp.get('pass', False):
            passes += 1
        total += 1
    
    # Semantic Similarity
    if 'semantic_similarity' in results:
        ss = results['semantic_similarity']
        report_lines.extend([
            "### 5. Semantic Similarity",
            f"- **Fraud-Fraud (intra-class)**: {ss['fraud_intra_mean']:.3f}",
            f"- **Normal-Normal (intra-class)**: {ss['normal_intra_mean']:.3f}",
            f"- **Fraud-Normal (inter-class)**: {ss['inter_mean']:.3f}",
            f"- **Separation Score**: {ss['separation_score']:.3f} (threshold: >0.10) {'✓' if ss['separation_score'] > 0.10 else '⚠'}",
            f"- **Status**: {'✓ PASS' if ss.get('pass', False) else '⚠ FAIL'}",
            ""
        ])
        if ss.get('pass', False):
            passes += 1
        total += 1
    
    # t-SNE
    if 'tsne' in results:
        tsne = results['tsne']
        report_lines.extend([
            "### 6. t-SNE Visualization",
            f"- **Samples Visualized**: {tsne['samples']}",
            f"- **Fraud Count**: {tsne['fraud_count']}",
            f"- **Normal Count**: {tsne['normal_count']}",
            f"- **Plot**: {tsne['plot_saved']}",
            ""
        ])
    
    # Overall assessment
    report_lines.extend([
        "---",
        "## Overall Assessment",
        ""
    ])
    
    if total > 0:
        score = (passes / total) * 100
        if score >= 80:
            assessment = "✓ EXCELLENT - Dataset meets quality standards"
        elif score >= 60:
            assessment = "✓ GOOD - Dataset is acceptable with minor issues"
        else:
            assessment = "⚠ NEEDS IMPROVEMENT - Consider regenerating some conversations"
        
        report_lines.append(f"**{assessment}** ({passes}/{total} tests passed, {score:.1f}%)")
    
    report_lines.extend([
        "",
        "---",
        "Generated by Dataset Quality Evaluation Suite v1.0"
    ])
    
    # Save report
    report_path = output_dir / 'evaluation_report.md'
    with open(report_path, 'w') as f:
        f.write('\n'.join(report_lines))
    
    console.print(f"[green]✓ Report saved: {report_path}[/green]")
    
    return report_path
