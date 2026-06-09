"""
Terminal UI Display for Gemma Zero-Shot Evaluation
=================================================

Simple, clean TUI showing worker progress and system stats.
"""

import time
import threading
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from rich.console import Console
from rich.live import Live
from rich.table import Table
from rich.progress import Progress, BarColumn, TextColumn, TimeRemainingColumn
from rich.panel import Panel
from rich.layout import Layout
from rich.text import Text
import psutil


class WorkerTUI:
    """Clean TUI for monitoring parallel Gemma workers."""
    
    def __init__(self, num_workers: int, total_samples: int):
        self.console = Console()
        self.num_workers = num_workers
        self.total_samples = total_samples
        self.start_time = datetime.now()
        
        # Worker stats
        self.worker_stats = {
            i: {
                'status': 'Starting',
                'processed': 0,
                'current_batch': 0,
                'errors': 0,
                'avg_time_per_sample': 0.0,
                'gpu_id': None
            }
            for i in range(num_workers)
        }
        
        self.total_processed = 0
        self.total_errors = 0
        self.is_running = True
        
        # Progress tracking
        self.progress = Progress(
            TextColumn("[bold blue]Overall Progress"),
            BarColumn(bar_width=40),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            TextColumn("•"),
            TextColumn("{task.completed}/{task.total}"),
            TimeRemainingColumn(),
        )
        self.overall_task = self.progress.add_task("Processing", total=total_samples)
    
    def update_worker(self, worker_id: int, status: str = None, processed: int = None, 
                     current_batch: int = None, errors: int = None, 
                     avg_time: float = None, gpu_id: int = None):
        """Update worker statistics."""
        worker = self.worker_stats[worker_id]
        
        if status is not None:
            worker['status'] = status
        if processed is not None:
            worker['processed'] = processed
        if current_batch is not None:
            worker['current_batch'] = current_batch
        if errors is not None:
            worker['errors'] = errors
        if avg_time is not None:
            worker['avg_time_per_sample'] = avg_time
        if gpu_id is not None:
            worker['gpu_id'] = gpu_id
    
    def update_totals(self):
        """Update total statistics."""
        self.total_processed = sum(w['processed'] for w in self.worker_stats.values())
        self.total_errors = sum(w['errors'] for w in self.worker_stats.values())
        self.progress.update(self.overall_task, completed=self.total_processed)
    
    def get_system_stats(self) -> Dict:
        """Get current system statistics."""
        cpu_percent = psutil.cpu_percent(interval=None)
        memory = psutil.virtual_memory()
        
        stats = {
            'cpu_percent': cpu_percent,
            'memory_percent': memory.percent,
            'memory_available_gb': memory.available / (1024**3),
        }
        
        # GPU stats if available
        try:
            import torch
            if torch.cuda.is_available():
                stats['gpu_count'] = torch.cuda.device_count()
                stats['gpu_memory'] = []
                for i in range(torch.cuda.device_count()):
                    mem_allocated = torch.cuda.memory_allocated(i) / (1024**3)
                    mem_reserved = torch.cuda.memory_reserved(i) / (1024**3)
                    stats['gpu_memory'].append({
                        'allocated_gb': mem_allocated,
                        'reserved_gb': mem_reserved
                    })
        except:
            pass
        
        return stats
    
    def create_worker_table(self) -> Table:
        """Create worker status table."""
        table = Table(title="Worker Status", show_header=True, header_style="bold magenta")
        
        table.add_column("Worker", style="cyan", width=8)
        table.add_column("GPU", style="green", width=6)
        table.add_column("Status", style="yellow", width=12)
        table.add_column("Processed", style="blue", width=10)
        table.add_column("Batch", style="magenta", width=8)
        table.add_column("Errors", style="red", width=8)
        table.add_column("Avg Time/Sample", style="cyan", width=15)
        
        for worker_id, stats in self.worker_stats.items():
            gpu_str = f"GPU {stats['gpu_id']}" if stats['gpu_id'] is not None else "N/A"
            status_color = {
                'Starting': 'yellow',
                'Running': 'green',
                'Waiting': 'blue',
                'Error': 'red',
                'Completed': 'green bold'
            }.get(stats['status'], 'white')
            
            table.add_row(
                f"W-{worker_id}",
                gpu_str,
                f"[{status_color}]{stats['status']}[/{status_color}]",
                str(stats['processed']),
                str(stats['current_batch']),
                str(stats['errors']),
                f"{stats['avg_time_per_sample']:.2f}s"
            )
        
        return table
    
    def create_summary_panel(self) -> Panel:
        """Create summary statistics panel."""
        elapsed = datetime.now() - self.start_time
        
        # Calculate rates
        samples_per_second = self.total_processed / max(elapsed.total_seconds(), 1)
        
        # ETA calculation
        remaining = self.total_samples - self.total_processed
        eta_seconds = remaining / max(samples_per_second, 0.001)
        eta = timedelta(seconds=int(eta_seconds))
        
        # Accuracy (if we have labels)
        accuracy_str = "N/A"
        if hasattr(self, 'correct_predictions') and self.total_processed > 0:
            accuracy = self.correct_predictions / self.total_processed * 100
            accuracy_str = f"{accuracy:.2f}%"
        
        summary_text = f"""
[bold cyan] Overall Progress[/bold cyan]
Total Processed: [bold]{self.total_processed:,}[/bold] / {self.total_samples:,}
Completion: [bold]{self.total_processed/self.total_samples*100:.1f}%[/bold]

[bold yellow] Timing[/bold yellow]  
Elapsed: [bold]{str(elapsed).split('.')[0]}[/bold]
Rate: [bold]{samples_per_second:.1f} samples/sec[/bold]
ETA: [bold]{str(eta)}[/bold]

[bold red]Errors[/bold red]
Total Errors: [bold]{self.total_errors}[/bold]
Error Rate: [bold]{self.total_errors/max(self.total_processed,1)*100:.2f}%[/bold]

[bold green] Performance[/bold green]
Accuracy: [bold]{accuracy_str}[/bold]
        """.strip()
        
        return Panel(summary_text, title="[bold blue]Gemma Zero-Shot Evaluation[/bold blue]", 
                    border_style="blue")
    
    def create_system_panel(self) -> Panel:
        """Create system resource panel."""
        stats = self.get_system_stats()
        
        system_text = f"""
[bold cyan]System Resources[/bold cyan]
CPU Usage: [bold]{stats['cpu_percent']:.1f}%[/bold]
Memory: [bold]{stats['memory_percent']:.1f}%[/bold] ([bold]{stats['memory_available_gb']:.1f}GB available[/bold])
"""
        
        if 'gpu_count' in stats:
            system_text += f"\n[bold green]GPU Status[/bold green]\n"
            for i, gpu_mem in enumerate(stats['gpu_memory']):
                system_text += f"GPU {i}: [bold]{gpu_mem['allocated_gb']:.1f}GB[/bold] / [bold]{gpu_mem['reserved_gb']:.1f}GB[/bold] reserved\n"
        
        return Panel(system_text.strip(), title="[bold green]System[/bold green]", 
                    border_style="green")
    
    def create_layout(self) -> Layout:
        """Create the main layout."""
        layout = Layout()
        
        layout.split_column(
            Layout(name="header", size=8),
            Layout(name="main", ratio=2),
            Layout(name="progress", size=3)
        )
        
        layout["main"].split_row(
            Layout(name="workers", ratio=2),
            Layout(name="sidebar")
        )
        
        layout["sidebar"].split_column(
            Layout(name="summary"),
            Layout(name="system")
        )
        
        return layout
    
    def render(self) -> Layout:
        """Render the complete UI."""
        layout = self.create_layout()
        
        # Update layout components
        layout["header"].update(Panel(
            f"[bold blue]Gemma 1.1 2B Zero-Shot Fraud Detection[/bold blue]\n"
            f"Workers: {self.num_workers} | Total Samples: {self.total_samples:,} | "
            f"Started: {self.start_time.strftime('%H:%M:%S')}",
            border_style="blue"
        ))
        
        layout["workers"].update(self.create_worker_table())
        layout["summary"].update(self.create_summary_panel())
        layout["system"].update(self.create_system_panel())
        layout["progress"].update(self.progress)
        
        return layout
    
    def display_live(self):
        """Start live display in a separate thread."""
        with Live(self.render(), refresh_per_second=2, console=self.console) as live:
            while self.is_running:
                self.update_totals()
                live.update(self.render())
                time.sleep(0.5)
    
    def start_display_thread(self):
        """Start the display in a background thread."""
        self.display_thread = threading.Thread(target=self.display_live, daemon=True)
        self.display_thread.start()
        return self.display_thread
    
    def stop(self):
        """Stop the display."""
        self.is_running = False
        if hasattr(self, 'display_thread'):
            self.display_thread.join(timeout=1.0)
    
    def update_accuracy(self, correct: int, total: int):
        """Update accuracy statistics."""
        self.correct_predictions = correct
        self.total_predictions = total