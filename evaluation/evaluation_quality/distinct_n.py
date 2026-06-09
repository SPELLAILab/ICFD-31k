"""
Linguistic Diversity Test (Distinct-n)

Measures vocabulary richness and detects template reuse.
"""

from typing import Dict, Any, List
from rich.console import Console
from rich.table import Table
from .base_test import BaseEvaluationTest

console = Console()


class DistinctNTest(BaseEvaluationTest):
    """
    Distinct-n Test: Ratio of unique n-grams to total n-grams
    
    Metrics:
    - Distinct-1 (unigrams): unique_words / total_words
    - Distinct-2 (bigrams): unique_bigrams / total_bigrams
    - Distinct-3 (trigrams): unique_trigrams / total_trigrams
    
    Thresholds:
    - Distinct-1: > 0.05 (Good), > 0.10 (Excellent)
    - Distinct-2: > 0.30 (Good), > 0.50 (Excellent)
    - Distinct-3: > 0.50 (Good), > 0.70 (Excellent)
    """
    
    def get_test_name(self) -> str:
        return "Linguistic Diversity (Distinct-n)"
    
    def calculate_distinct_n(self, texts: List[str], n: int = 1) -> float:
        """Calculate Distinct-n score for given texts"""
        all_ngrams = []
        
        for text in texts:
            tokens = text.lower().split()
            ngrams = [tuple(tokens[i:i+n]) for i in range(len(tokens)-n+1)]
            all_ngrams.extend(ngrams)
        
        if not all_ngrams:
            return 0.0
        
        return len(set(all_ngrams)) / len(all_ngrams)
    
    def run(self) -> Dict[str, Any]:
        """Run Distinct-n test"""
        console.print("\n[bold blue]Test: Linguistic Diversity (Distinct-n)[/bold blue]")
        
        # Calculate for full dataset
        distinct_1 = self.calculate_distinct_n(self.conversations, n=1)
        distinct_2 = self.calculate_distinct_n(self.conversations, n=2)
        distinct_3 = self.calculate_distinct_n(self.conversations, n=3)
        
        # Calculate by label
        fraud_convs, normal_convs = self.get_fraud_normal_split()
        
        fraud_d1 = self.calculate_distinct_n(fraud_convs, n=1) if fraud_convs else 0
        fraud_d2 = self.calculate_distinct_n(fraud_convs, n=2) if fraud_convs else 0
        fraud_d3 = self.calculate_distinct_n(fraud_convs, n=3) if fraud_convs else 0
        
        normal_d1 = self.calculate_distinct_n(normal_convs, n=1) if normal_convs else 0
        normal_d2 = self.calculate_distinct_n(normal_convs, n=2) if normal_convs else 0
        normal_d3 = self.calculate_distinct_n(normal_convs, n=3) if normal_convs else 0
        
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
        
        # Store results
        self.results = {
            'distinct_1': distinct_1,
            'distinct_2': distinct_2,
            'distinct_3': distinct_3,
            'fraud': {'d1': fraud_d1, 'd2': fraud_d2, 'd3': fraud_d3},
            'normal': {'d1': normal_d1, 'd2': normal_d2, 'd3': normal_d3},
            'pass': distinct_1 > 0.05 and distinct_2 > 0.30 and distinct_3 > 0.50
        }
        
        self.save_results()
        return self.results
