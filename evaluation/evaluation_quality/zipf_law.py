"""
Zipf's Law Test

Validates that word frequency distribution follows natural language patterns.
"""

from typing import Dict, Any
from collections import Counter
import numpy as np
import matplotlib.pyplot as plt
from rich.console import Console
from .base_test import BaseEvaluationTest

console = Console()


class ZipfLawTest(BaseEvaluationTest):
    """
    Zipf's Law Test: Word frequency distribution follows power law
    
    Natural language: frequency ∝ 1/rank
    
    Metrics:
    - MSE: Mean squared error from expected Zipf distribution (< 0.05 is good)
    - Slope: Log-log plot slope (should be ≈ -1.0)
    
    Thresholds:
    - MSE < 0.05: Good adherence to Zipf's Law
    - -1.2 < Slope < -0.8: Natural language distribution
    """
    
    def get_test_name(self) -> str:
        return "Zipf's Law Analysis"
    
    def run(self) -> Dict[str, Any]:
        """Run Zipf's Law test"""
        console.print("\n[bold blue]Test: Zipf's Law Analysis[/bold blue]")
        
        # Tokenize and count all words
        all_words = []
        for text in self.conversations:
            words = text.lower().split()
            all_words.extend(words)
        
        word_counts = Counter(all_words)
        
        # Sort by frequency
        frequencies = sorted(word_counts.values(), reverse=True)
        ranks = np.arange(1, len(frequencies) + 1)
        
        # Calculate expected Zipf distribution
        expected = frequencies[0] / ranks
        
        # Use only top 1000 words to avoid log(0) issues
        n_words = min(1000, len(frequencies))
        log_ranks = np.log(ranks[:n_words])
        log_freqs = np.log(frequencies[:n_words])
        log_expected = np.log(expected[:n_words])
        
        # Calculate MSE
        mse = np.mean((log_freqs - log_expected)**2)
        
        # Calculate slope (should be close to -1)
        coeffs = np.polyfit(log_ranks, log_freqs, 1)
        slope = coeffs[0]
        intercept = coeffs[1]
        
        console.print(f"Zipf's Law MSE: {mse:.4f} (threshold: <0.05)")
        console.print(f"Log-log slope: {slope:.3f} (expected: ≈-1.0)")
        console.print(f"Vocabulary size: {len(word_counts):,}")
        console.print(f"Total words: {len(all_words):,}")
        
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
        
        output_path = self.output_dir / 'zipf_law_analysis.pdf'
        plt.savefig(output_path, format='pdf', bbox_inches='tight')
        plt.close()
        
        console.print(f"[green]✓ Plot saved: {output_path}[/green]")
        
        # Store results
        self.results = {
            'mse': float(mse),
            'slope': float(slope),
            'intercept': float(intercept),
            'vocabulary_size': len(word_counts),
            'total_words': len(all_words),
            'unique_ratio': len(word_counts) / len(all_words),
            'pass': mse < 0.05 and -1.2 < slope < -0.8
        }
        
        self.save_results()
        return self.results
