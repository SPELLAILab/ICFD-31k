#!/usr/bin/env python3
"""
Dataset Quality Evaluation Suite

Performs comprehensive quality evaluation on the fraud detection conversation dataset.
Includes: Distinct-n, Perplexity, Zipf's Law, t-SNE, N-gram Overlap, Semantic Similarity.

Usage:
    python evaluate_dataset_quality.py --source-dir output/source_conversations
"""

import json
import argparse
from pathlib import Path
from collections import Counter
from itertools import combinations
import random
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from typing import List, Dict, Tuple
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn
from rich.table import Table
from rich.panel import Panel
import warnings
warnings.filterwarnings('ignore')

console = Console()


class DatasetEvaluator:
    """Comprehensive dataset quality evaluator"""
    
    def __init__(self, source_dir: Path, output_dir: Path, sample_size: int = None):
        self.source_dir = Path(source_dir)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.sample_size = sample_size
        
        self.conversations = []
        self.labels = []
        self.case_types = []
        self.domains = []
        
        self.results = {}
        
    def load_conversations(self):
        """Load all conversations from source directory"""
        console.print("\n[bold blue]Loading conversations...[/bold blue]")
        
        json_files = list(self.source_dir.rglob("*.json"))
        
        if self.sample_size and len(json_files) > self.sample_size:
            json_files = random.sample(json_files, self.sample_size)
            console.print(f"[yellow]Sampling {self.sample_size} conversations for faster evaluation[/yellow]")
        
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
                    if not conversation_text and 'turns' in data:
                        # Alternative format: build from turns
                        conversation_text = ' '.join([
                            turn.get('content', '') for turn in data['turns']
                        ])
                    
                    if conversation_text:
                        self.conversations.append(conversation_text)
                        self.labels.append(data.get('label', 'UNKNOWN'))
                        self.case_types.append(data.get('case_type', 'UNKNOWN'))
                        
                        # Extract domain from scenario
                        scenario = data.get('scenario', {})
                        if isinstance(scenario, dict):
                            self.domains.append(scenario.get('domain', 'UNKNOWN'))
                        else:
                            self.domains.append('UNKNOWN')
                
                except Exception as e:
                    console.print(f"[red]Error loading {json_file}: {e}[/red]")
                
                progress.update(task, advance=1)
        
        console.print(f"[green]✓ Loaded {len(self.conversations)} conversations[/green]")
        
        # Print distribution
        label_counts = Counter(self.labels)
        console.print(f"  Fraud: {label_counts.get('YES', 0)}, Normal: {label_counts.get('NO', 0)}")
    
    def test_distinct_n(self):
        """Test 1: Linguistic Diversity (Distinct-n)"""
        console.print("\n[bold blue]Test 1: Linguistic Diversity (Distinct-n)[/bold blue]")
        
        def calculate_distinct_n(texts: List[str], n: int = 1) -> float:
            """Calculate Distinct-n score"""
            all_ngrams = []
            for text in texts:
                tokens = text.lower().split()
                ngrams = [tuple(tokens[i:i+n]) for i in range(len(tokens)-n+1)]
                all_ngrams.extend(ngrams)
            
            if not all_ngrams:
                return 0.0
            return len(set(all_ngrams)) / len(all_ngrams)
        
        # Calculate for full dataset
        distinct_1 = calculate_distinct_n(self.conversations, n=1)
        distinct_2 = calculate_distinct_n(self.conversations, n=2)
        distinct_3 = calculate_distinct_n(self.conversations, n=3)
        
        # Calculate by label
        fraud_convs = [c for c, l in zip(self.conversations, self.labels) if l == 'YES']
        normal_convs = [c for c, l in zip(self.conversations, self.labels) if l == 'NO']
        
        fraud_d1 = calculate_distinct_n(fraud_convs, n=1) if fraud_convs else 0
        fraud_d2 = calculate_distinct_n(fraud_convs, n=2) if fraud_convs else 0
        fraud_d3 = calculate_distinct_n(fraud_convs, n=3) if fraud_convs else 0
        
        normal_d1 = calculate_distinct_n(normal_convs, n=1) if normal_convs else 0
        normal_d2 = calculate_distinct_n(normal_convs, n=2) if normal_convs else 0
        normal_d3 = calculate_distinct_n(normal_convs, n=3) if normal_convs else 0
        
        # Display results
        table = Table(title="Distinct-n Scores")
        table.add_column("Metric", style="cyan")
        table.add_column("Full Dataset", style="white")
        table.add_column("Fraud", style="red")
        table.add_column("Normal", style="green")
        table.add_column("Threshold", style="yellow")
        table.add_column("Status", style="bold")
        
        def status(value, threshold):
            return "✓" if value >= threshold else "⚠"
        
        table.add_row(
            "Distinct-1",
            f"{distinct_1:.4f}",
            f"{fraud_d1:.4f}",
            f"{normal_d1:.4f}",
            ">0.05",
            status(distinct_1, 0.05)
        )
        table.add_row(
            "Distinct-2",
            f"{distinct_2:.4f}",
            f"{fraud_d2:.4f}",
            f"{normal_d2:.4f}",
            ">0.30",
            status(distinct_2, 0.30)
        )
        table.add_row(
            "Distinct-3",
            f"{distinct_3:.4f}",
            f"{fraud_d3:.4f}",
            f"{normal_d3:.4f}",
            ">0.50",
            status(distinct_3, 0.50)
        )
        
        console.print(table)
        
        self.results['distinct_n'] = {
            'distinct_1': distinct_1,
            'distinct_2': distinct_2,
            'distinct_3': distinct_3,
            'fraud': {'d1': fraud_d1, 'd2': fraud_d2, 'd3': fraud_d3},
            'normal': {'d1': normal_d1, 'd2': normal_d2, 'd3': normal_d3}
        }
        
        return self.results['distinct_n']
    
    def test_ngram_overlap(self, n: int = 3, sample_pairs: int = 1000):
        """Test 2: N-gram Overlap Analysis"""
        console.print("\n[bold blue]Test 2: N-gram Overlap Analysis[/bold blue]")
        
        def get_ngrams(text: str, n: int) -> set:
            tokens = text.lower().split()
            return set(tuple(tokens[i:i+n]) for i in range(len(tokens)-n+1))
        
        # Sample conversation pairs to avoid O(n^2) computation
        num_convs = len(self.conversations)
        max_pairs = num_convs * (num_convs - 1) // 2
        num_pairs = min(sample_pairs, max_pairs)
        
        console.print(f"Sampling {num_pairs} conversation pairs...")
        
        pairs = random.sample(list(combinations(range(num_convs), 2)), num_pairs)
        
        overlaps = []
        with Progress() as progress:
            task = progress.add_task("Computing overlaps...", total=len(pairs))
            
            for i, j in pairs:
                ngrams_i = get_ngrams(self.conversations[i], n)
                ngrams_j = get_ngrams(self.conversations[j], n)
                
                if len(ngrams_i) > 0 and len(ngrams_j) > 0:
                    overlap = len(ngrams_i & ngrams_j) / min(len(ngrams_i), len(ngrams_j))
                    overlaps.append(overlap)
                
                progress.update(task, advance=1)
        
        mean_overlap = np.mean(overlaps)
        std_overlap = np.std(overlaps)
        
        # Test for different n-gram sizes
        results = {}
        for n_val in [1, 2, 3]:
            overlaps_n = []
            pairs_sample = random.sample(pairs, min(500, len(pairs)))
            
            for i, j in pairs_sample:
                ngrams_i = get_ngrams(self.conversations[i], n_val)
                ngrams_j = get_ngrams(self.conversations[j], n_val)
                
                if len(ngrams_i) > 0 and len(ngrams_j) > 0:
                    overlap = len(ngrams_i & ngrams_j) / min(len(ngrams_i), len(ngrams_j))
                    overlaps_n.append(overlap)
            
            results[f'{n_val}-gram'] = {
                'mean': np.mean(overlaps_n),
                'std': np.std(overlaps_n),
                'max': np.max(overlaps_n)
            }
        
        # Display results
        table = Table(title="N-gram Overlap Statistics")
        table.add_column("N-gram", style="cyan")
        table.add_column("Mean Overlap", style="white")
        table.add_column("Std Dev", style="white")
        table.add_column("Max Overlap", style="yellow")
        table.add_column("Threshold", style="yellow")
        table.add_column("Status", style="bold")
        
        thresholds = {'1-gram': 0.40, '2-gram': 0.15, '3-gram': 0.05}
        
        for n_type, stats in results.items():
            threshold = thresholds[n_type]
            status = "✓" if stats['mean'] <= threshold else "⚠"
            
            table.add_row(
                n_type,
                f"{stats['mean']*100:.2f}%",
                f"{stats['std']*100:.2f}%",
                f"{stats['max']*100:.2f}%",
                f"<{threshold*100:.0f}%",
                status
            )
        
        console.print(table)
        
        self.results['ngram_overlap'] = results
        return results
    
    def test_zipf_law(self):
        """Test 3: Zipf's Law Analysis"""
        console.print("\n[bold blue]Test 3: Zipf's Law Analysis[/bold blue]")
        
        # Tokenize and count all words
        all_words = []
        for text in self.conversations:
            words = text.lower().split()
            all_words.extend(words)
        
        word_counts = Counter(all_words)
        
        # Sort by frequency
        frequencies = sorted(word_counts.values(), reverse=True)
        ranks = np.arange(1, len(frequencies) + 1)
        
        # Calculate deviation from Zipf's Law
        expected = frequencies[0] / ranks
        
        # Use only top 1000 words to avoid log(0) issues
        n_words = min(1000, len(frequencies))
        log_ranks = np.log(ranks[:n_words])
        log_freqs = np.log(frequencies[:n_words])
        log_expected = np.log(expected[:n_words])
        
        mse = np.mean((log_freqs - log_expected)**2)
        
        # Calculate slope (should be close to -1)
        coeffs = np.polyfit(log_ranks, log_freqs, 1)
        slope = coeffs[0]
        
        console.print(f"Zipf's Law MSE: {mse:.4f} (threshold: <0.05)")
        console.print(f"Log-log slope: {slope:.3f} (expected: ≈-1.0)")
        
        status = "✓ PASS" if mse < 0.05 and -1.2 < slope < -0.8 else "⚠ WARNING"
        console.print(f"Status: {status}")
        
        # Create visualization
        plt.figure(figsize=(10, 6))
        plt.loglog(ranks[:n_words], frequencies[:n_words], 'b.', alpha=0.5, label='Actual')
        plt.loglog(ranks[:n_words], expected[:n_words], 'r--', linewidth=2, label="Zipf's Law (slope=-1)")
        plt.xlabel('Rank (log scale)', fontsize=12)
        plt.ylabel('Frequency (log scale)', fontsize=12)
        plt.title("Zipf's Law Analysis", fontsize=14, fontweight='bold')
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        
        output_path = self.output_dir / 'zipf_law_analysis.png'
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        console.print(f"[green]Plot saved: {output_path}[/green]")
        
        self.results['zipf_law'] = {
            'mse': mse,
            'slope': slope,
            'vocabulary_size': len(word_counts),
            'total_words': len(all_words)
        }
        
        return self.results['zipf_law']
    
    def test_perplexity(self, max_samples: int = 500):
        """Test 4: Perplexity Analysis"""
        console.print("\n[bold blue]Test 4: Perplexity Analysis[/bold blue]")
        
        try:
            import torch
            from transformers import GPT2LMHeadModel, GPT2TokenizerFast
        except ImportError:
            console.print("[red]⚠ Skipping perplexity test: transformers library not installed[/red]")
            console.print("[yellow]Install with: pip install transformers torch[/yellow]")
            return None
        
        console.print("Loading GPT-2 model...")
        device = 'cuda' if torch.cuda.is_available() else 'cpu'
        model = GPT2LMHeadModel.from_pretrained('gpt2').to(device)
        tokenizer = GPT2TokenizerFast.from_pretrained('gpt2')
        model.eval()
        
        # Sample conversations for faster computation
        sample_size = min(max_samples, len(self.conversations))
        indices = random.sample(range(len(self.conversations)), sample_size)
        
        fraud_ppls = []
        normal_ppls = []
        
        with Progress() as progress:
            task = progress.add_task("Computing perplexity...", total=len(indices))
            
            for idx in indices:
                text = self.conversations[idx]
                label = self.labels[idx]
                
                try:
                    # Truncate long texts
                    encodings = tokenizer(text[:1000], return_tensors='pt', truncation=True, max_length=512)
                    input_ids = encodings.input_ids.to(device)
                    
                    with torch.no_grad():
                        outputs = model(input_ids, labels=input_ids)
                        loss = outputs.loss
                        ppl = torch.exp(loss).item()
                    
                    if ppl < 1000:  # Filter out extreme values
                        if label == 'YES':
                            fraud_ppls.append(ppl)
                        else:
                            normal_ppls.append(ppl)
                
                except Exception as e:
                    pass  # Skip problematic texts
                
                progress.update(task, advance=1)
        
        # Calculate statistics
        fraud_mean = np.mean(fraud_ppls) if fraud_ppls else 0
        fraud_std = np.std(fraud_ppls) if fraud_ppls else 0
        normal_mean = np.mean(normal_ppls) if normal_ppls else 0
        normal_std = np.std(normal_ppls) if normal_ppls else 0
        
        table = Table(title="Perplexity Statistics")
        table.add_column("Label", style="cyan")
        table.add_column("Mean", style="white")
        table.add_column("Std Dev", style="white")
        table.add_column("Samples", style="yellow")
        table.add_column("Status", style="bold")
        
        def status(mean):
            if mean < 50:
                return "✓ Excellent"
            elif mean < 80:
                return "✓ Good"
            elif mean < 150:
                return "⚠ Acceptable"
            else:
                return "✗ Poor"
        
        table.add_row("Fraud", f"{fraud_mean:.2f}", f"{fraud_std:.2f}", str(len(fraud_ppls)), status(fraud_mean))
        table.add_row("Normal", f"{normal_mean:.2f}", f"{normal_std:.2f}", str(len(normal_ppls)), status(normal_mean))
        
        console.print(table)
        
        # Create visualization
        plt.figure(figsize=(10, 6))
        if fraud_ppls:
            plt.hist(fraud_ppls, bins=30, alpha=0.6, label='Fraud', color='red', edgecolor='black')
        if normal_ppls:
            plt.hist(normal_ppls, bins=30, alpha=0.6, label='Normal', color='green', edgecolor='black')
        plt.xlabel('Perplexity', fontsize=12)
        plt.ylabel('Frequency', fontsize=12)
        plt.title('Perplexity Distribution (GPT-2)', fontsize=14, fontweight='bold')
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        
        output_path = self.output_dir / 'perplexity_distribution.png'
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        console.print(f"[green]Plot saved: {output_path}[/green]")
        
        self.results['perplexity'] = {
            'fraud_mean': fraud_mean,
            'fraud_std': fraud_std,
            'normal_mean': normal_mean,
            'normal_std': normal_std,
            'fraud_samples': len(fraud_ppls),
            'normal_samples': len(normal_ppls)
        }
        
        return self.results['perplexity']
    
    def test_semantic_similarity(self, max_samples: int = 1000):
        """Test 5: Semantic Similarity Analysis"""
        console.print("\n[bold blue]Test 5: Semantic Similarity Analysis[/bold blue]")
        
        try:
            from sentence_transformers import SentenceTransformer
            from sklearn.metrics.pairwise import cosine_similarity
        except ImportError:
            console.print("[red]⚠ Skipping semantic similarity test: sentence-transformers not installed[/red]")
            console.print("[yellow]Install with: pip install sentence-transformers scikit-learn[/yellow]")
            return None
        
        console.print("Loading sentence transformer model...")
        model = SentenceTransformer('all-MiniLM-L6-v2')
        
        # Sample for faster computation
        sample_size = min(max_samples, len(self.conversations))
        indices = random.sample(range(len(self.conversations)), sample_size)
        
        sample_convs = [self.conversations[i] for i in indices]
        sample_labels = [self.labels[i] for i in indices]
        
        console.print(f"Encoding {len(sample_convs)} conversations...")
        embeddings = model.encode(sample_convs, show_progress_bar=True, batch_size=32)
        
        # Separate by label
        fraud_mask = np.array([l == 'YES' for l in sample_labels])
        normal_mask = ~fraud_mask
        
        fraud_embeddings = embeddings[fraud_mask]
        normal_embeddings = embeddings[normal_mask]
        
        console.print("Computing similarity scores...")
        
        # Intra-class similarity
        if len(fraud_embeddings) > 1:
            fraud_sim = cosine_similarity(fraud_embeddings)
            fraud_intra = fraud_sim[np.triu_indices_from(fraud_sim, k=1)]
        else:
            fraud_intra = np.array([0])
        
        if len(normal_embeddings) > 1:
            normal_sim = cosine_similarity(normal_embeddings)
            normal_intra = normal_sim[np.triu_indices_from(normal_sim, k=1)]
        else:
            normal_intra = np.array([0])
        
        # Inter-class similarity
        if len(fraud_embeddings) > 0 and len(normal_embeddings) > 0:
            inter_sim = cosine_similarity(fraud_embeddings, normal_embeddings).flatten()
        else:
            inter_sim = np.array([0])
        
        # Calculate statistics
        fraud_intra_mean = np.mean(fraud_intra)
        normal_intra_mean = np.mean(normal_intra)
        inter_mean = np.mean(inter_sim)
        
        avg_intra = (fraud_intra_mean + normal_intra_mean) / 2
        separation = avg_intra - inter_mean
        
        table = Table(title="Semantic Similarity Analysis")
        table.add_column("Comparison", style="cyan")
        table.add_column("Mean", style="white")
        table.add_column("Std Dev", style="white")
        table.add_column("Expected", style="yellow")
        table.add_column("Status", style="bold")
        
        table.add_row(
            "Fraud-Fraud (intra)",
            f"{fraud_intra_mean:.3f}",
            f"{np.std(fraud_intra):.3f}",
            "0.4-0.6",
            "✓" if 0.3 < fraud_intra_mean < 0.7 else "⚠"
        )
        table.add_row(
            "Normal-Normal (intra)",
            f"{normal_intra_mean:.3f}",
            f"{np.std(normal_intra):.3f}",
            "0.4-0.6",
            "✓" if 0.3 < normal_intra_mean < 0.7 else "⚠"
        )
        table.add_row(
            "Fraud-Normal (inter)",
            f"{inter_mean:.3f}",
            f"{np.std(inter_sim):.3f}",
            "0.2-0.4",
            "✓" if 0.1 < inter_mean < 0.5 else "⚠"
        )
        table.add_row(
            "[bold]Separation Score[/bold]",
            f"[bold]{separation:.3f}[/bold]",
            "",
            ">0.10",
            "✓" if separation > 0.10 else "⚠"
        )
        
        console.print(table)
        
        self.results['semantic_similarity'] = {
            'fraud_intra_mean': fraud_intra_mean,
            'normal_intra_mean': normal_intra_mean,
            'inter_mean': inter_mean,
            'separation_score': separation
        }
        
        return self.results['semantic_similarity']
    
    def generate_tsne_plot(self, max_samples: int = 2000):
        """Test 6: t-SNE Visualization"""
        console.print("\n[bold blue]Test 6: t-SNE Visualization[/bold blue]")
        
        try:
            from sentence_transformers import SentenceTransformer
            from sklearn.manifold import TSNE
        except ImportError:
            console.print("[red]⚠ Skipping t-SNE: sentence-transformers not installed[/red]")
            return None
        
        console.print("Loading sentence transformer model...")
        model = SentenceTransformer('all-MiniLM-L6-v2')
        
        # Sample for visualization
        sample_size = min(max_samples, len(self.conversations))
        indices = random.sample(range(len(self.conversations)), sample_size)
        
        sample_convs = [self.conversations[i] for i in indices]
        sample_labels = [self.labels[i] for i in indices]
        sample_case_types = [self.case_types[i] for i in indices]
        
        console.print(f"Encoding {len(sample_convs)} conversations...")
        embeddings = model.encode(sample_convs, show_progress_bar=True, batch_size=32)
        
        console.print("Computing t-SNE projection...")
        tsne = TSNE(n_components=2, random_state=42, perplexity=30, n_iter=1000)
        embeddings_2d = tsne.fit_transform(embeddings)
        
        # Create visualizations
        fig, axes = plt.subplots(1, 2, figsize=(16, 6))
        
        # Plot 1: By Label (Fraud vs Normal)
        ax1 = axes[0]
        for label, color, marker in [('YES', 'red', 'o'), ('NO', 'green', 's')]:
            mask = np.array([l == label for l in sample_labels])
            label_name = 'Fraud' if label == 'YES' else 'Normal'
            ax1.scatter(
                embeddings_2d[mask, 0],
                embeddings_2d[mask, 1],
                c=color,
                label=label_name,
                alpha=0.6,
                s=30,
                marker=marker,
                edgecolors='black',
                linewidths=0.5
            )
        ax1.set_title('t-SNE: Fraud vs Normal', fontsize=14, fontweight='bold')
        ax1.set_xlabel('t-SNE Component 1')
        ax1.set_ylabel('t-SNE Component 2')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # Plot 2: By Case Type
        ax2 = axes[1]
        case_type_colors = {
            'Clear Fraud': 'darkred',
            'Subtle Fraud': 'orange',
            'Clear Normal': 'darkgreen',
            'Ambiguous but Ultimately Normal': 'lightblue'
        }
        
        for case_type, color in case_type_colors.items():
            mask = np.array([ct == case_type for ct in sample_case_types])
            if np.any(mask):
                ax2.scatter(
                    embeddings_2d[mask, 0],
                    embeddings_2d[mask, 1],
                    c=color,
                    label=case_type,
                    alpha=0.6,
                    s=30,
                    edgecolors='black',
                    linewidths=0.5
                )
        ax2.set_title('t-SNE: By Case Type', fontsize=14, fontweight='bold')
        ax2.set_xlabel('t-SNE Component 1')
        ax2.set_ylabel('t-SNE Component 2')
        ax2.legend(fontsize=8)
        ax2.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        output_path = self.output_dir / 'tsne_visualization.png'
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        console.print(f"[green]✓ Plot saved: {output_path}[/green]")
        
        self.results['tsne'] = {
            'samples': len(sample_convs),
            'plot_saved': str(output_path)
        }
        
        return self.results['tsne']
    
    def generate_report(self):
        """Generate comprehensive evaluation report"""
        console.print("\n[bold blue]Generating Evaluation Report...[/bold blue]")
        
        report_lines = [
            "# Dataset Quality Evaluation Report",
            f"\n**Date**: {np.datetime64('today')}",
            f"**Dataset**: {self.source_dir}",
            f"**Conversations Analyzed**: {len(self.conversations)}",
            f"**Fraud**: {sum(1 for l in self.labels if l == 'YES')}",
            f"**Normal**: {sum(1 for l in self.labels if l == 'NO')}",
            "\n---\n",
            "## Summary of Results\n"
        ]
        
        # Distinct-n
        if 'distinct_n' in self.results:
            dn = self.results['distinct_n']
            report_lines.extend([
                "### 1. Linguistic Diversity (Distinct-n)",
                f"- **Distinct-1**: {dn['distinct_1']:.4f} (threshold: >0.05) {'✓' if dn['distinct_1'] > 0.05 else '⚠'}",
                f"- **Distinct-2**: {dn['distinct_2']:.4f} (threshold: >0.30) {'✓' if dn['distinct_2'] > 0.30 else '⚠'}",
                f"- **Distinct-3**: {dn['distinct_3']:.4f} (threshold: >0.50) {'✓' if dn['distinct_3'] > 0.50 else '⚠'}",
                ""
            ])
        
        # N-gram Overlap
        if 'ngram_overlap' in self.results:
            report_lines.append("### 2. N-gram Overlap")
            for n_type, stats in self.results['ngram_overlap'].items():
                report_lines.append(f"- **{n_type}**: {stats['mean']*100:.2f}% ± {stats['std']*100:.2f}%")
            report_lines.append("")
        
        # Zipf's Law
        if 'zipf_law' in self.results:
            zl = self.results['zipf_law']
            report_lines.extend([
                "### 3. Zipf's Law",
                f"- **MSE**: {zl['mse']:.4f} (threshold: <0.05) {'✓' if zl['mse'] < 0.05 else '⚠'}",
                f"- **Slope**: {zl['slope']:.3f} (expected: ≈-1.0) {'✓' if -1.2 < zl['slope'] < -0.8 else '⚠'}",
                f"- **Vocabulary Size**: {zl['vocabulary_size']:,}",
                ""
            ])
        
        # Perplexity
        if 'perplexity' in self.results:
            pp = self.results['perplexity']
            report_lines.extend([
                "### 4. Perplexity (GPT-2)",
                f"- **Fraud Mean**: {pp['fraud_mean']:.2f} ± {pp['fraud_std']:.2f}",
                f"- **Normal Mean**: {pp['normal_mean']:.2f} ± {pp['normal_std']:.2f}",
                ""
            ])
        
        # Semantic Similarity
        if 'semantic_similarity' in self.results:
            ss = self.results['semantic_similarity']
            report_lines.extend([
                "### 5. Semantic Similarity",
                f"- **Fraud-Fraud (intra-class)**: {ss['fraud_intra_mean']:.3f}",
                f"- **Normal-Normal (intra-class)**: {ss['normal_intra_mean']:.3f}",
                f"- **Fraud-Normal (inter-class)**: {ss['inter_mean']:.3f}",
                f"- **Separation Score**: {ss['separation_score']:.3f} (threshold: >0.10) {'✓' if ss['separation_score'] > 0.10 else '⚠'}",
                ""
            ])
        
        report_lines.extend([
            "---",
            "## Interpretation",
            "",
            "**Overall Assessment**: "
        ])
        
        # Count passes
        passes = 0
        total = 0
        
        if 'distinct_n' in self.results:
            dn = self.results['distinct_n']
            if dn['distinct_1'] > 0.05:
                passes += 1
            if dn['distinct_2'] > 0.30:
                passes += 1
            if dn['distinct_3'] > 0.50:
                passes += 1
            total += 3
        
        if 'zipf_law' in self.results:
            zl = self.results['zipf_law']
            if zl['mse'] < 0.05 and -1.2 < zl['slope'] < -0.8:
                passes += 1
            total += 1
        
        if 'semantic_similarity' in self.results:
            ss = self.results['semantic_similarity']
            if ss['separation_score'] > 0.10:
                passes += 1
            total += 1
        
        if total > 0:
            score = (passes / total) * 100
            if score >= 80:
                assessment = "✓ EXCELLENT - Dataset meets quality standards"
            elif score >= 60:
                assessment = "✓ GOOD - Dataset is acceptable with minor issues"
            else:
                assessment = "⚠ NEEDS IMPROVEMENT - Consider regenerating some conversations"
            
            report_lines.append(f"{assessment} ({passes}/{total} checks passed)")
        
        report_lines.extend([
            "",
            "---",
            "Generated by Dataset Quality Evaluation Suite"
        ])
        
        # Save report
        report_path = self.output_dir / 'evaluation_report.md'
        with open(report_path, 'w') as f:
            f.write('\n'.join(report_lines))
        
        console.print(f"[green]✓ Report saved: {report_path}[/green]")
        
        # Save JSON results
        json_path = self.output_dir / 'evaluation_results.json'
        with open(json_path, 'w') as f:
            json.dump(self.results, f, indent=2)
        
        console.print(f"[green]✓ Results saved: {json_path}[/green]")
    
    def run_all_tests(self, skip_tests: List[str] = None):
        """Run complete evaluation suite"""
        skip_tests = skip_tests or []
        
        console.print(Panel.fit(
            "[bold cyan]Dataset Quality Evaluation Suite[/bold cyan]\n"
            "Comprehensive quality assessment for fraud detection conversations",
            border_style="cyan"
        ))
        
        # Load data
        self.load_conversations()
        
        if len(self.conversations) == 0:
            console.print("[red]Error: No conversations loaded. Check source directory.[/red]")
            return
        
        # Run tests
        if 'distinct_n' not in skip_tests:
            self.test_distinct_n()
        
        if 'ngram_overlap' not in skip_tests:
            self.test_ngram_overlap()
        
        if 'zipf_law' not in skip_tests:
            self.test_zipf_law()
        
        if 'perplexity' not in skip_tests:
            self.test_perplexity()
        
        if 'semantic_similarity' not in skip_tests:
            self.test_semantic_similarity()
        
        if 'tsne' not in skip_tests:
            self.generate_tsne_plot()
        
        # Generate final report
        self.generate_report()
        
        console.print("\n[bold green]✓ Evaluation Complete![/bold green]")
        console.print(f"Results saved in: {self.output_dir}")


def main():
    parser = argparse.ArgumentParser(
        description="Evaluate dataset quality with comprehensive metrics"
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
    
    evaluator = DatasetEvaluator(
        source_dir=args.source_dir,
        output_dir=args.output_dir,
        sample_size=args.sample_size
    )
    
    evaluator.run_all_tests(skip_tests=args.skip_tests)


if __name__ == '__main__':
    main()
