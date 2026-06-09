"""
Semantic Similarity Test

Measures semantic separation between fraud and normal conversations.
"""

from typing import Dict, Any
import random
import numpy as np
from rich.console import Console
from rich.table import Table
from .base_test import BaseEvaluationTest

console = Console()


class SemanticSimilarityTest(BaseEvaluationTest):
    """
    Semantic Similarity Test: Cosine similarity between embeddings
    
    Measures:
    - Intra-class similarity (fraud-fraud, normal-normal)
    - Inter-class similarity (fraud-normal)
    - Separation score (intra - inter)
    
    Thresholds:
    - Intra-class: 0.4-0.6 (good clustering)
    - Inter-class: 0.2-0.4 (good separation)
    - Separation score: > 0.10 (meaningful difference)
    """
    
    def __init__(self, conversations, labels, case_types, output_dir,
                 max_samples: int = 1000):
        super().__init__(conversations, labels, case_types, output_dir)
        self.max_samples = max_samples
    
    def get_test_name(self) -> str:
        return "Semantic Similarity Analysis"
    
    def run(self) -> Dict[str, Any]:
        """Run Semantic Similarity test"""
        console.print("\n[bold blue]Test: Semantic Similarity Analysis[/bold blue]")
        
        try:
            from sentence_transformers import SentenceTransformer
            from sklearn.metrics.pairwise import cosine_similarity
        except ImportError:
            console.print("[red]⚠ Skipping: sentence-transformers not installed[/red]")
            console.print("[yellow]Install with: pip install sentence-transformers scikit-learn[/yellow]")
            return None
        
        console.print("Loading sentence transformer model...")
        model = SentenceTransformer('all-MiniLM-L6-v2')
        
        # Sample for faster computation
        sample_size = min(self.max_samples, len(self.conversations))
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
        fraud_intra_mean = float(np.mean(fraud_intra))
        normal_intra_mean = float(np.mean(normal_intra))
        inter_mean = float(np.mean(inter_sim))
        
        avg_intra = (fraud_intra_mean + normal_intra_mean) / 2
        separation = avg_intra - inter_mean
        
        # Display results
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
        
        # Store results
        self.results = {
            'fraud_intra_mean': fraud_intra_mean,
            'fraud_intra_std': float(np.std(fraud_intra)),
            'normal_intra_mean': normal_intra_mean,
            'normal_intra_std': float(np.std(normal_intra)),
            'inter_mean': inter_mean,
            'inter_std': float(np.std(inter_sim)),
            'separation_score': float(separation),
            'samples': sample_size,
            'pass': separation > 0.10
        }
        
        self.save_results()
        return self.results
