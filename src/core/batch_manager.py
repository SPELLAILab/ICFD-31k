"""
Batch management system for isolating dataset generations.
"""

import os
import json
from datetime import datetime
from typing import Dict, List, Any, Optional
from pathlib import Path
import yaml
from rich.console import Console


class BatchManager:
    """
    Manages batch isolation, metadata, and folder structure.
    Ensures each generation creates a new timestamped folder.
    """
    
    def __init__(self, console: Console, config_path: str = "config/batch_config.yaml"):
        self.console = console
        self.config_path = config_path
        self.batch_id: Optional[str] = None
        self.batch_config: Dict[str, Any] = {}
        self.batch_metadata: Dict[str, Any] = {}
        
    def load_batch_config(self) -> Dict[str, Any]:
        """
        Load batch configuration from YAML file.
        
        Returns:
            Dictionary containing batch configuration
        """
        try:
            with open(self.config_path, 'r') as f:
                self.batch_config = yaml.safe_load(f)
            
            self.console.print(f"[green]✓[/green] Loaded batch configuration: {self.batch_config['batch']['name']}")
            return self.batch_config
            
        except FileNotFoundError:
            self.console.print(f"[red]Error:[/red] Batch config file not found: {self.config_path}")
            self.console.print("[yellow]Creating default config file...[/yellow]")
            self._create_default_config()
            return self.load_batch_config()
            
        except yaml.YAMLError as e:
            self.console.print(f"[red]Error parsing YAML config:[/red] {e}")
            raise
    
    def _create_default_config(self):
        """Create a default batch configuration file if it doesn't exist."""
        default_config = {
            'batch': {
                'name': 'Default Batch',
                'description': 'Default dataset generation batch',
                'scenario_type': 'general'
            },
            'entities': {
                'organizations': ['HDFC Bank', 'State Bank of India', 'ICICI Bank', 'Axis Bank']
            },
            'generation': {
                'multiplier': 1,
                'max_workers': 50,
                'rate_limit_per_minute': 500,
                'enable_adaptive_scaling': True
            },
            'recovery': {
                'enabled': True,
                'checkpoint_interval': 50,
                'auto_resume': True,
                'retry_failed_sessions': True,
                'max_retries': 3
            },
            'output': {
                'create_batch_folder': True,
                'save_batch_metadata': True
            }
        }
        
        os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
        with open(self.config_path, 'w') as f:
            yaml.dump(default_config, f, default_flow_style=False, sort_keys=False)
        
        self.console.print(f"[green]✓[/green] Created default config at {self.config_path}")
    
    def create_batch_id(self) -> str:
        """
        Generate a unique batch ID from timestamp.
        
        Format: batch_YYYY-MM-DD_HH-MM-SS
        
        Returns:
            Batch ID string
        """
        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        self.batch_id = f"batch_{timestamp}"
        return self.batch_id
    
    def create_batch_folders(self, output_dir: str = "output") -> tuple[str, str]:
        """
        Create timestamped batch folders for source conversations and training data.
        
        Args:
            output_dir: Base output directory
            
        Returns:
            Tuple of (source_folder_path, training_folder_path)
        """
        if not self.batch_id:
            self.create_batch_id()
        
        # Create folder paths
        source_folder = os.path.join(output_dir, "source_conversations", self.batch_id)
        training_folder = os.path.join(output_dir, "training_data", self.batch_id)
        recovery_folder = os.path.join(output_dir, "recovery")
        
        # Create directories
        Path(source_folder).mkdir(parents=True, exist_ok=True)
        Path(training_folder).mkdir(parents=True, exist_ok=True)
        Path(recovery_folder).mkdir(parents=True, exist_ok=True)
        
        self.console.print(f"\n[bold blue]📁 Batch Folders Created:[/bold blue]")
        self.console.print(f"   Source: {source_folder}")
        self.console.print(f"   Training: {training_folder}")
        self.console.print(f"   Recovery: {recovery_folder}")
        
        return source_folder, training_folder
    
    def initialize_batch_metadata(self, 
                                  scenarios: List[Dict], 
                                  agents: List[str], 
                                  customers: List[str],
                                  multiplier: int) -> Dict[str, Any]:
        """
        Initialize batch metadata with generation information.
        
        Args:
            scenarios: List of scenario dictionaries
            agents: List of agent personas
            customers: List of customer personas
            multiplier: Combination multiplier
            
        Returns:
            Batch metadata dictionary
        """
        total_combinations = len(agents) * len(customers) * len(scenarios) * multiplier
        
        self.batch_metadata = {
            "batch_id": self.batch_id,
            "batch_name": self.batch_config['batch']['name'],
            "batch_description": self.batch_config['batch']['description'],
            "scenario_type": self.batch_config['batch']['scenario_type'],
            "start_time": datetime.now().isoformat(),
            "end_time": None,
            "status": "in_progress",
            
            # Generation configuration
            "total_scenarios": len(scenarios),
            "total_agents": len(agents),
            "total_customers": len(customers),
            "multiplier": multiplier,
            "total_expected": total_combinations,
            "total_generated": 0,
            "total_failed": 0,
            
            # Schema and version info
            "schema_version": "2.0",
            "generator_version": "2.0.0",
            
            # Configuration snapshot
            "config_snapshot": self.batch_config,
            
            # Scenario snapshot (prevents loss if file changes)
            "scenarios_snapshot": scenarios,
            
            # Statistics (updated during generation)
            "statistics": {
                "average_duration_seconds": 0,
                "total_training_chunks": 0,
                "success_rate": 0.0
            }
        }
        
        return self.batch_metadata
    
    def save_batch_metadata(self, output_dir: str = "output"):
        """
        Save batch metadata to JSON file in the batch folder.
        
        Args:
            output_dir: Base output directory
        """
        if not self.batch_id:
            self.console.print("[yellow]Warning: No batch ID set, skipping metadata save[/yellow]")
            return
        
        metadata_path = os.path.join(
            output_dir, 
            "source_conversations", 
            self.batch_id, 
            "batch_metadata.json"
        )
        
        with open(metadata_path, 'w') as f:
            json.dump(self.batch_metadata, f, indent=2)
        
        self.console.print(f"[green]✓[/green] Saved batch metadata: {metadata_path}")
    
    def update_batch_statistics(self, 
                                completed: int, 
                                failed: int, 
                                total_chunks: int = 0):
        """
        Update batch statistics during generation.
        
        Args:
            completed: Number of completed conversations
            failed: Number of failed conversations
            total_chunks: Total training chunks generated
        """
        self.batch_metadata["total_generated"] = completed
        self.batch_metadata["total_failed"] = failed
        self.batch_metadata["statistics"]["total_training_chunks"] = total_chunks
        
        if self.batch_metadata["total_expected"] > 0:
            success_rate = (completed / self.batch_metadata["total_expected"]) * 100
            self.batch_metadata["statistics"]["success_rate"] = round(success_rate, 2)
    
    def finalize_batch(self, output_dir: str = "output"):
        """
        Finalize batch metadata when generation completes.
        
        Args:
            output_dir: Base output directory
        """
        self.batch_metadata["end_time"] = datetime.now().isoformat()
        self.batch_metadata["status"] = "completed"
        
        # Calculate duration
        start = datetime.fromisoformat(self.batch_metadata["start_time"])
        end = datetime.fromisoformat(self.batch_metadata["end_time"])
        duration = (end - start).total_seconds()
        self.batch_metadata["statistics"]["duration_seconds"] = duration
        self.batch_metadata["statistics"]["duration_minutes"] = round(duration / 60, 2)
        
        # Save final metadata
        self.save_batch_metadata(output_dir)
        
        self.console.print(f"\n[bold green]✓ Batch finalized:[/bold green] {self.batch_id}")
        self.console.print(f"   Duration: {self.batch_metadata['statistics']['duration_minutes']} minutes")
    
    def get_batch_config_value(self, *keys, default=None):
        """
        Get a value from batch configuration using dot notation.
        
        Args:
            *keys: Configuration keys (e.g., 'generation', 'max_workers')
            default: Default value if key not found
            
        Returns:
            Configuration value or default
        """
        value = self.batch_config
        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                return default
        return value
    
    def get_organizations(self) -> List[str]:
        """Get list of organizations from batch configuration."""
        return self.get_batch_config_value('entities', 'organizations', default=[])
    
    def get_max_workers(self) -> int:
        """Get max workers setting from batch configuration."""
        return self.get_batch_config_value('generation', 'max_workers', default=50)
    
    def get_checkpoint_interval(self) -> int:
        """Get checkpoint interval from batch configuration."""
        return self.get_batch_config_value('recovery', 'checkpoint_interval', default=50)
    
    def is_recovery_enabled(self) -> bool:
        """Check if recovery is enabled in batch configuration."""
        return self.get_batch_config_value('recovery', 'enabled', default=True)
    
    def get_batch_type(self) -> str:
        """Get the batch type/scenario type from configuration."""
        return self.get_batch_config_value('batch', 'scenario_type', default='unknown')
    
    def get_description(self) -> str:
        """Get the batch description from configuration."""
        return self.get_batch_config_value('batch', 'description', default='No description')
    
    def initialize_batch_metadata_simple(self, total_conversations: int, multiplier: int) -> Dict[str, Any]:
        """
        Simplified batch metadata initialization (for DatasetGenerator integration).
        
        Args:
            total_conversations: Total number of conversations to generate
            multiplier: Combination multiplier
            
        Returns:
            Batch metadata dictionary
        """
        self.batch_metadata = {
            "batch_id": self.batch_id,
            "batch_name": self.batch_config.get('batch', {}).get('name', 'Unnamed Batch'),
            "batch_description": self.batch_config.get('batch', {}).get('description', ''),
            "scenario_type": self.batch_config.get('batch', {}).get('scenario_type', 'mixed'),
            "start_time": datetime.now().isoformat(),
            "end_time": None,
            "status": "in_progress",
            
            # Generation configuration
            "multiplier": multiplier,
            "total_expected": total_conversations,
            "total_generated": 0,
            "total_failed": 0,
            
            # Schema and version info
            "schema_version": "2.0",
            "generator_version": "2.0.0",
            
            # Statistics (updated during generation)
            "statistics": {
                "average_duration_seconds": 0,
                "total_training_chunks": 0,
                "success_rate": 0.0
            }
        }
        
        return self.batch_metadata
    
    def finalize_batch_metadata(self, 
                                completed_conversations: int,
                                total_chunks: int,
                                batch_folder: str = None,
                                status: str = "completed",
                                error_message: str = None) -> None:
        """
        Finalize batch metadata when generation completes, is interrupted, or fails.
        
        Args:
            completed_conversations: Number of successfully completed conversations
            total_chunks: Total training chunks generated
            batch_folder: Batch folder name (for reference)
            status: Final status ('completed', 'interrupted', 'failed')
            error_message: Optional error message if status is 'failed'
        """
        if not self.batch_metadata:
            self.console.print("[yellow]Warning: No batch metadata to finalize[/yellow]")
            return
        
        self.batch_metadata["end_time"] = datetime.now().isoformat()
        self.batch_metadata["status"] = status
        self.batch_metadata["total_generated"] = completed_conversations
        self.batch_metadata["statistics"]["total_training_chunks"] = total_chunks
        
        # Calculate success rate
        if self.batch_metadata["total_expected"] > 0:
            success_rate = (completed_conversations / self.batch_metadata["total_expected"]) * 100
            self.batch_metadata["statistics"]["success_rate"] = round(success_rate, 2)
        
        # Calculate duration
        try:
            start = datetime.fromisoformat(self.batch_metadata["start_time"])
            end = datetime.fromisoformat(self.batch_metadata["end_time"])
            duration = (end - start).total_seconds()
            self.batch_metadata["statistics"]["duration_seconds"] = duration
            self.batch_metadata["statistics"]["duration_minutes"] = round(duration / 60, 2)
        except Exception as e:
            self.console.print(f"[yellow]Warning: Could not calculate duration: {e}[/yellow]")
        
        # Add error message if provided
        if error_message:
            self.batch_metadata["error_message"] = error_message
        
        self.console.print(f"\n[bold {'green' if status == 'completed' else 'yellow'}]Batch {status}: {self.batch_id}[/bold {'green' if status == 'completed' else 'yellow'}]")
