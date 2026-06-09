"""
File I/O utilities for saving conversations and training chunks.
"""

import json
from pathlib import Path
from typing import Dict, List, Any
from rich.console import Console

from config.settings import OUTPUT_DIR, SOURCE_CONVERSATIONS_DIR, TRAINING_DATA_DIR, CHUNK_INTERVAL_SECONDS


class FileManager:
    """Handles all file operations for saving conversations and chunks."""
    
    def __init__(self, console: Console, batch_folder: str = None):
        """
        Initialize FileManager.
        
        Args:
            console: Rich console for output
            batch_folder: Optional batch folder name (e.g., 'batch_2025-10-11_14-30-45')
                         If provided, files will be saved in batch-specific subdirectories
        """
        self.console = console
        self.output_dir = Path(OUTPUT_DIR)
        self.batch_folder = batch_folder
        
        # Use batch-specific folders if batch_folder is provided
        if batch_folder:
            self.source_conversations_dir = self.output_dir / SOURCE_CONVERSATIONS_DIR / batch_folder
            self.training_data_dir = self.output_dir / TRAINING_DATA_DIR / batch_folder
        else:
            self.source_conversations_dir = self.output_dir / SOURCE_CONVERSATIONS_DIR
            self.training_data_dir = self.output_dir / TRAINING_DATA_DIR
    
    def setup_directories(self) -> None:
        """Create the required output directory structure."""
        if self.batch_folder:
            self.console.print(f"\n[bold blue]Setting up batch directory structure for: {self.batch_folder}[/bold blue]")
        else:
            self.console.print("\n[bold blue]Setting up directory structure...[/bold blue]")
        
        directories = [self.output_dir, self.source_conversations_dir, self.training_data_dir]
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
            self.console.print(f"✓ Created directory: {directory}")
    
    def save_source_conversation(self, conversation: Dict[str, Any]) -> str:
        """
        Save a complete source conversation to the output directory.
        
        Args:
            conversation: Complete conversation data
            
        Returns:
            Path where the file was saved
        """
        
        # Extract metadata for filename generation
        session_id = conversation.get("session_id", 0)
        scenario = conversation.get("scenario", {})
        case_type_clean = scenario.get("case_type", "Unknown").replace(" ", "_")
        scenario_id = scenario.get("scenario_id", 0)
        multiplier_round = conversation.get("multiplier_round", 1)
        
        # Create descriptive filename
        filename = f"SCENARIO_{scenario_id}_{case_type_clean}_{session_id:04d}_r{multiplier_round}.json"
        
        filepath = self.source_conversations_dir / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(conversation, f, indent=2, ensure_ascii=False)
        
        return str(filepath)
    
    def save_training_chunks(self, chunks: List[Dict[str, Any]]) -> List[str]:
        """
        Save individual training chunks to the training data directory.
        
        Args:
            chunks: List of training data chunks
            
        Returns:
            List of file paths where chunks were saved
        """
        
        saved_paths = []
        
        for chunk in chunks:
            # Extract metadata for filename generation
            session_id = chunk.get("session_id", 0)
            scenario_info = chunk.get("scenario_info", {})
            case_type_clean = scenario_info.get("case_type", "Unknown").replace(" ", "_")
            scenario_id = scenario_info.get("scenario_id", 0)
            chunk_time = chunk.get("chunk_timestamp", 0)
            multiplier_round = chunk.get("multiplier_round", 1)
            
            # Create descriptive filename
            filename = f"SCENARIO_{scenario_id}_{case_type_clean}_{session_id:04d}_r{multiplier_round}_chunk_{chunk_time}s.json"
            
            filepath = self.training_data_dir / filename
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(chunk, f, indent=2, ensure_ascii=False)
            
            saved_paths.append(str(filepath))
        
        return saved_paths
    
    def get_statistics(self) -> Dict[str, int]:
        """Get current file statistics from output directories."""
        
        source_files = list(self.source_conversations_dir.glob("*.json"))
        training_files = list(self.training_data_dir.glob("*.json"))
        
        return {
            "source_conversations": len(source_files),
            "training_chunks": len(training_files),
            "source_dir": str(self.source_conversations_dir),
            "training_dir": str(self.training_data_dir)
        }
