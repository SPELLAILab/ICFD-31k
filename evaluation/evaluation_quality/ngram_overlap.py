"""
N-gram Overlap Test

Detects template reuse and memorization by measuring shared n-grams.
"""

from typing import Dict, Any, List, Set, Tuple
from itertools import combinations
import random
import numpy as np
from rich.console import Console
from rich.table import Table
from rich.progress import Progress
from .base_test import BaseEvaluationTest

console = Console()


class NgramOverlapTest(BaseEvaluationTest):
    """
    N-gram Overlap Test: Percentage of shared n-grams between conversation pairs
    
    Thresholds:
    - Unigram overlap: < 40% (common words)
    - Bigram overlap: < 15% (common phrases)
    - Trigram overlap: < 5% (unique constructions)
    """
    
    def __init__(self, conversations: List[str], labels: List[str], 
                 case_types: List[str], output_dir, sample_pairs: int = 1000):
        super().__init__(conversations, labels, case_types, output_dir)
        self.sample_pairs = sample_pairs
    
    def get_test_name(self) -> str:
        return "N-gram Overlap Analysis"
    
    def get_ngrams(self, text: str, n: int) -> Set[Tuple]:
        """Extract n-grams from text"""
        tokens = text.lower().split()
        return set(tuple(tokens[i:i+n]) for i in range(len(tokens)-n+1))
    
    def calculate_overlap(self, n: int, num_pairs: int = None) -> Dict[str, float]:
        """Calculate n-gram overlap for conversation pairs"""
        if num_pairs is None:
            num_pairs = self.sample_pairs
        
        num_convs = len(self.conversations)
        max_pairs = num_convs * (num_convs - 1) // 2
        num_pairs = min(num_pairs, max_pairs)
        
        # Sample conversation pairs
        pairs = random.sample(list(combinations(range(num_convs), 2)), num_pairs)
        
        overlaps = []
        
        for i, j in pairs:
            ngrams_i = self.get_ngrams(self.conversations[i], n)
            ngrams_j = self.get_ngrams(self.conversations[j], n)
            
            if len(ngrams_i) > 0 and len(ngrams_j) > 0:
                overlap = len(ngrams_i & ngrams_j) / min(len(ngrams_i), len(ngrams_j))
                overlaps.append(overlap)
        
        return {
            'mean': np.mean(overlaps) if overlaps else 0,
            'std': np.std(overlaps) if overlaps else 0,
            'max': np.max(overlaps) if overlaps else 0,
            'min': np.min(overlaps) if overlaps else 0
        }
    
    def run(self) -> Dict[str, Any]:
        """Run N-gram Overlap test"""
        console.print("\n[bold blue]Test: N-gram Overlap Analysis[/bold blue]")
        
        num_convs = len(self.conversations)
        max_pairs = num_convs * (num_convs - 1) // 2
        num_pairs = min(self.sample_pairs, max_pairs)
        
        console.print(f"Sampling {num_pairs} conversation pairs...")
        
        results = {}
        
        with Progress() as progress:
            task = progress.add_task("Computing overlaps...", total=3)
            
            for n in [1, 2, 3]:
                stats = self.calculate_overlap(n, num_pairs=min(500, num_pairs))
                results[f'{n}-gram'] = stats
                progress.update(task, advance=1)
        
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
        
        # Store results
        self.results = results
        self.results['pairs_sampled'] = num_pairs
        self.results['pass'] = all(
            results[f'{n}-gram']['mean'] <= thresholds[f'{n}-gram'] 
            for n in [1, 2, 3]
        )
        
        self.save_results()
        return self.results
