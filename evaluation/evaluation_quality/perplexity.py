"""
Perplexity Test

Measures text naturalness using a language model (GPT-2).
Lower perplexity = more natural/fluent text.
"""

from typing import Dict, Any
import random
import numpy as np
import matplotlib.pyplot as plt
from rich.console import Console
from rich.table import Table
from rich.progress import Progress
from .base_test import BaseEvaluationTest

console = Console()


class PerplexityTest(BaseEvaluationTest):
    """
    Perplexity Test: Measures how "surprised" GPT-2 is by the text
    
    Lower perplexity = more natural text
    
    Thresholds (using GPT-2):
    - < 50: Excellent (very natural)
    - 50-80: Good (natural)
    - 80-150: Acceptable
    - > 150: Poor (unnatural)
    """
    
    def __init__(self, conversations, labels, case_types, output_dir, 
                 max_samples: int = 500):
        super().__init__(conversations, labels, case_types, output_dir)
        self.max_samples = max_samples
    
    def get_test_name(self) -> str:
        return "Perplexity Analysis"
    
    def run(self) -> Dict[str, Any]:
        """Run Perplexity test"""
        console.print("\n[bold blue]Test: Perplexity Analysis[/bold blue]")
        
        try:
            import torch
            from transformers import GPT2LMHeadModel, GPT2TokenizerFast
        except ImportError:
            console.print("[red]⚠ Skipping: transformers library not installed[/red]")
            console.print("[yellow]Install with: pip install transformers torch[/yellow]")
            return None
        
        console.print("Loading GPT-2 model...")
        device = 'cuda' if torch.cuda.is_available() else 'cpu'
        console.print(f"Using device: {device}")
        
        model = GPT2LMHeadModel.from_pretrained('gpt2').to(device)
        tokenizer = GPT2TokenizerFast.from_pretrained('gpt2')
        model.eval()
        
        # Sample conversations for faster computation
        sample_size = min(self.max_samples, len(self.conversations))
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
                    encodings = tokenizer(text[:1000], return_tensors='pt', 
                                        truncation=True, max_length=512)
                    input_ids = encodings.input_ids.to(device)
                    
                    with torch.no_grad():
                        outputs = model(input_ids, labels=input_ids)
                        loss = outputs.loss
                        ppl = torch.exp(loss).item()
                    
                    # Filter out extreme values
                    if ppl < 1000:
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
        fraud_median = np.median(fraud_ppls) if fraud_ppls else 0
        
        normal_mean = np.mean(normal_ppls) if normal_ppls else 0
        normal_std = np.std(normal_ppls) if normal_ppls else 0
        normal_median = np.median(normal_ppls) if normal_ppls else 0
        
        # Display results
        table = Table(title="Perplexity Statistics (GPT-2)")
        table.add_column("Label", style="cyan")
        table.add_column("Mean", style="white")
        table.add_column("Median", style="white")
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
        
        table.add_row(
            "Fraud", 
            f"{fraud_mean:.2f}", 
            f"{fraud_median:.2f}",
            f"{fraud_std:.2f}", 
            str(len(fraud_ppls)), 
            status(fraud_mean)
        )
        table.add_row(
            "Normal", 
            f"{normal_mean:.2f}",
            f"{normal_median:.2f}",
            f"{normal_std:.2f}", 
            str(len(normal_ppls)), 
            status(normal_mean)
        )
        
        console.print(table)
        
        # Create visualization
        plt.figure(figsize=(10, 6))
        if fraud_ppls:
            plt.hist(fraud_ppls, bins=30, alpha=0.6, label=f'Fraud (n={len(fraud_ppls)})', 
                    color='red', edgecolor='black')
        if normal_ppls:
            plt.hist(normal_ppls, bins=30, alpha=0.6, label=f'Normal (n={len(normal_ppls)})', 
                    color='green', edgecolor='black')
        plt.xlabel('Perplexity', fontsize=12)
        plt.ylabel('Frequency', fontsize=12)
        plt.title('Perplexity Distribution (GPT-2)', fontsize=14, fontweight='bold')
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        
        output_path = self.output_dir / 'perplexity_distribution.png'
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        console.print(f"[green]✓ Plot saved: {output_path}[/green]")
        
        # Store results
        self.results = {
            'fraud_mean': float(fraud_mean),
            'fraud_median': float(fraud_median),
            'fraud_std': float(fraud_std),
            'normal_mean': float(normal_mean),
            'normal_median': float(normal_median),
            'normal_std': float(normal_std),
            'fraud_samples': len(fraud_ppls),
            'normal_samples': len(normal_ppls),
            'pass': fraud_mean < 150 and normal_mean < 150
        }
        
        self.save_results()
        return self.results
