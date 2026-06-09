"""
t-SNE Visualization Test

Creates 2D visualization of conversation embeddings to show clustering patterns.
"""

from typing import Dict, Any
import random
import numpy as np
import matplotlib.pyplot as plt
from rich.console import Console
from .base_test import BaseEvaluationTest

console = Console()


class TSNEVisualizationTest(BaseEvaluationTest):
    """
    t-SNE Visualization: High-dimensional embedding projection to 2D
    
    Visualizes:
    - Fraud vs Normal separation
    - Case type clustering
    - Domain clustering
    - Outlier detection
    
    Expected patterns:
    - Moderate separation (not perfect, not random)
    - Subtle Fraud between Clear Fraud and Normal
    - Some overlap (reflects real-world ambiguity)
    """
    
    def __init__(self, conversations, labels, case_types, output_dir,
                 max_samples: int = 2000):
        super().__init__(conversations, labels, case_types, output_dir)
        self.max_samples = max_samples
    
    def get_test_name(self) -> str:
        return "t-SNE Visualization"
    
    def run(self) -> Dict[str, Any]:
        """Run t-SNE visualization"""
        console.print("\n[bold blue]Test: t-SNE Visualization[/bold blue]")
        
        try:
            from sentence_transformers import SentenceTransformer
            from sklearn.manifold import TSNE
        except ImportError:
            console.print("[red]⚠ Skipping: sentence-transformers not installed[/red]")
            console.print("[yellow]Install with: pip install sentence-transformers scikit-learn[/yellow]")
            return None
        
        console.print("Loading sentence transformer model...")
        model = SentenceTransformer('all-MiniLM-L6-v2')
        
        # Sample for visualization
        sample_size = min(self.max_samples, len(self.conversations))
        indices = random.sample(range(len(self.conversations)), sample_size)
        
        sample_convs = [self.conversations[i] for i in indices]
        sample_labels = [self.labels[i] for i in indices]
        sample_case_types = [self.case_types[i] for i in indices]
        
        console.print(f"Encoding {len(sample_convs)} conversations...")
        embeddings = model.encode(sample_convs, show_progress_bar=True, batch_size=32)
        
        console.print("Computing t-SNE projection...")
        tsne = TSNE(n_components=2, random_state=42, perplexity=30, max_iter=1000)
        embeddings_2d = tsne.fit_transform(embeddings)
        
        # Create visualizations
        fig, axes = plt.subplots(1, 2, figsize=(16, 6))
        
        # Plot 1: By Label (Fraud vs Normal)
        ax1 = axes[0]
        for label, color, marker in [('YES', 'red', 'o'), ('NO', 'green', 's')]:
            mask = np.array([l == label for l in sample_labels])
            label_name = 'Fraud' if label == 'YES' else 'Normal'
            count = np.sum(mask)
            ax1.scatter(
                embeddings_2d[mask, 0],
                embeddings_2d[mask, 1],
                c=color,
                label=f'{label_name} (n={count})',
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
            count = np.sum(mask)
            if count > 0:
                ax2.scatter(
                    embeddings_2d[mask, 0],
                    embeddings_2d[mask, 1],
                    c=color,
                    label=f'{case_type} (n={count})',
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
        
        output_path = self.output_dir / 'tsne_visualization.pdf'
        plt.savefig(output_path, format='pdf', bbox_inches='tight')
        plt.close()
        
        console.print(f"[green]✓ Plot saved: {output_path}[/green]")
        
        # Store results
        self.results = {
            'samples': len(sample_convs),
            'plot_saved': str(output_path),
            'fraud_count': int(np.sum([l == 'YES' for l in sample_labels])),
            'normal_count': int(np.sum([l == 'NO' for l in sample_labels]))
        }
        
        self.save_results()
        return self.results
