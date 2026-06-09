"""
Main dataset generator class that orchestrates the entire pipeline.
"""

import os
import asyncio
from typing import Dict, List, Any
import groq
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, TaskID

from config.settings import (
    PERSONAS_FILE, SCENARIOS_FILE, BATCH_CONFIG_FILE,
    MAX_WORKERS, ENABLE_BATCH_FOLDERS, SAVE_BATCH_METADATA
)
from src.utils.data_loader import DataLoader
from src.core.combination_generator import CombinationGenerator
from src.generators.conversation_generator import ConversationGenerator
from src.generators.chunk_expander import ChunkExpander
from src.utils.file_manager import FileManager
from src.core.batch_manager import BatchManager
from src.core.worker_pool import WorkerPool


class DatasetGenerator:
    """Main orchestrator for the synthetic fraud detection dataset generation."""
    
    def __init__(self, scenarios_file: str = None, personas_file: str = None):
        """
        Initialize the dataset generator with all necessary components.
        
        Args:
            scenarios_file: Optional path to scenarios file. If None, uses default from settings.
            personas_file: Optional path to personas file. If None, uses default from settings.
        """
        self.console = Console()
        
        # Store scenarios file path (use provided or default from settings)
        self.scenarios_file = scenarios_file if scenarios_file else SCENARIOS_FILE
        self.personas_file = personas_file if personas_file else PERSONAS_FILE
        
        # Initialize batch manager (will be configured in main())
        self.batch_manager = None
        self.batch_id = None
        
        # Initialize all components (FileManager will be recreated with batch folder)
        self.data_loader = DataLoader(self.console)
        self.combination_generator = CombinationGenerator(self.console)
        self.chunk_expander = ChunkExpander(self.console)
        self.file_manager = None  # Will be initialized after batch folder is created
        
        # Data storage
        self.agent_personas = []
        self.customer_personas = []
        self.scenarios = []
        self.combinations = []
        self.groq_client = None
        self.conversation_generator = None
        
        # Statistics tracking
        self.total_source_conversations = 0
        self.total_training_chunks = 0
    
    def initialize_groq_client(self) -> groq.AsyncGroq:
        """
        Initialize the Groq API client using environment variable for API key.
        
        Returns:
            Configured Groq async client
        """
        api_key = os.getenv('GROQ_API_KEY')
        if not api_key:
            raise ValueError("GROQ_API_KEY environment variable not found. Please set it before running the script.")
        
        self.console.print("\n[bold blue]Initializing Groq API client...[/bold blue]")
        client = groq.AsyncGroq(api_key=api_key)
        self.console.print("Groq client initialized successfully")
        
        return client
    
    def load_input_data(self) -> None:
        """Load all input data (personas and scenarios)."""
        self.agent_personas, self.customer_personas = self.data_loader.load_personas(self.personas_file)
        self.scenarios = self.data_loader.load_scenarios(self.scenarios_file)
        
        # Print which files are being used
        self.console.print(f"[cyan]Loading personas from: {self.personas_file}[/cyan]")
        self.console.print(f"[cyan]Loading scenarios from: {self.scenarios_file}[/cyan]")
    
    def generate_combinations(self, multiplier: int) -> None:
        """Generate systematic combinations of all inputs."""
        unique_combinations, total_conversations = self.combination_generator.calculate_total_conversations(
            self.agent_personas, self.customer_personas, self.scenarios, multiplier
        )
        
        self.combinations = self.combination_generator.generate_combination_list(
            self.agent_personas, self.customer_personas, self.scenarios, multiplier
        )
        
        self.console.print(f"\n[bold green]Generated {len(self.combinations):,} systematic combinations![/bold green]")
    
    async def run_generation_pipeline(self) -> None:
        """Run the complete generation pipeline using WorkerPool for high performance."""
        
        total_combinations = len(self.combinations)
        self.console.print(f"\n[bold green]Starting generation of {total_combinations:,} conversations...[/bold green]")
        self.console.print(f"[cyan]Using WorkerPool with up to {MAX_WORKERS} concurrent workers[/cyan]")
        
        # Create worker pool
        worker_pool = WorkerPool(
            console=self.console,
            max_workers=MAX_WORKERS,
            rate_limit_per_minute=500,
            enable_adaptive_scaling=True
        )
        
        # Run the worker pool with all combinations
        try:
            results, errors = await worker_pool.run(
                tasks=self.combinations,
                process_func=self._worker_generate_conversation
            )
            
            # Update final statistics
            self.total_source_conversations = len(results)
            # total_training_chunks is updated by workers
            
            if errors:
                self.console.print(f"\n[yellow]Warning: {len(errors)} conversations failed[/yellow]")
            
        except KeyboardInterrupt:
            self.console.print("\n[yellow]Generation interrupted by user. Stopping workers...[/yellow]")
            raise
    
    async def _worker_generate_conversation(self, combination: Dict[str, Any]) -> None:
        """
        Worker function for generating a single conversation.
        
        This is called by WorkerPool workers and handles the complete generation
        and saving of a single conversation plus its training chunks.
        
        Args:
            combination: Dictionary with agent, customer, scenario, and metadata
        """
        
        session_id = combination['session_id']
        scenario = combination['scenario']
        
        try:
            # Stage 1: Generate source conversation
            source_conversation = await self.conversation_generator.generate_source_conversation(combination)
            
            # Save source conversation
            self.file_manager.save_source_conversation(source_conversation)
            
            # Stage 2: Expand into training chunks
            training_chunks = self.chunk_expander.expand_conversation_into_chunks(source_conversation)
            
            # Save training chunks
            self.file_manager.save_training_chunks(training_chunks)
            
            # Update chunk count (thread-safe increment)
            self.total_training_chunks += len(training_chunks)
            
        except Exception as e:
            self.console.print(f"[red]Session {session_id} failed: {str(e)}[/red]")
            raise  # Re-raise to let WorkerPool handle retries
    
    def print_final_summary(self) -> None:
        """Print the final generation summary with statistics."""
        
        # Get final file statistics
        stats = self.file_manager.get_statistics()
        
        summary_text = f"""
[bold green]Dataset Generation Complete![/bold green]

[cyan]Source Conversations:[/cyan] {stats['source_conversations']:,}
[cyan]Training Data Points:[/cyan] {stats['training_chunks']:,}
[cyan]Source Files Directory:[/cyan] {stats['source_dir']}
[cyan]Training Files Directory:[/cyan] {stats['training_dir']}

[bold]Success![/bold] Your systematic fraud detection dataset is ready for training.

[yellow]Key Improvements:[/yellow]
- Systematic generation (no random bias)
- Perfect combination coverage
- Configurable multiplier for variations
- Modular, maintainable architecture
        """.strip()
        
        self.console.print(Panel(summary_text, title="Generation Summary", border_style="green"))
    
    async def main(self, multiplier: int = 2) -> None:
        """
        Main execution function that orchestrates the entire dataset generation process.
        
        Args:
            multiplier: Number of variations to generate for each unique combination
        """
        
        # Print welcome banner
        from config.settings import GROQ_MODEL, CHUNK_INTERVAL_SECONDS
        
        welcome_text = f"""
[bold blue]Systematic Dataset Generator for Fraud Detection[/bold blue]

Generation Strategy: Systematic combinations (not random)
Model: {GROQ_MODEL}
Chunk interval: {CHUNK_INTERVAL_SECONDS} seconds
Combination multiplier: {multiplier}x
Max concurrent workers: {MAX_WORKERS}

This will generate EVERY possible agent-customer-scenario combination!
        """.strip()
        
        self.console.print(Panel(welcome_text, title="Dataset Generation Starting", border_style="blue"))
        
        try:
            # Initialize batch management if enabled
            if ENABLE_BATCH_FOLDERS:
                self.batch_manager = BatchManager(self.console, BATCH_CONFIG_FILE)
                self.batch_manager.load_batch_config()
                
                # Create batch ID and folders
                self.batch_id = self.batch_manager.create_batch_id()
                batch_folders = self.batch_manager.create_batch_folders(self.batch_id)
                
                # Initialize file manager with batch folder
                self.file_manager = FileManager(self.console, batch_folder=self.batch_id)
                
                # Display batch info
                batch_info = f"""
[cyan]Batch ID:[/cyan] {self.batch_id}
[cyan]Batch Type:[/cyan] {self.batch_manager.get_batch_type()}
[cyan]Description:[/cyan] {self.batch_manager.get_description()}
[cyan]Organizations:[/cyan] {len(self.batch_manager.get_organizations())} configured
                """.strip()
                self.console.print(Panel(batch_info, title="Batch Configuration", border_style="cyan"))
            else:
                # Use default file manager without batch folders
                self.file_manager = FileManager(self.console)
            
            # Setup phase
            self.file_manager.setup_directories()
            
            # Load input data
            self.load_input_data()
            
            # Generate systematic combinations
            self.generate_combinations(multiplier)
            
            # Initialize API client and conversation generator
            self.groq_client = self.initialize_groq_client()
            self.conversation_generator = ConversationGenerator(self.console, self.groq_client)
            
            # Initialize batch metadata if batch mode is enabled
            if ENABLE_BATCH_FOLDERS and SAVE_BATCH_METADATA:
                self.batch_manager.initialize_batch_metadata_simple(
                    total_conversations=len(self.combinations),
                    multiplier=multiplier
                )
            
            # Run the generation pipeline
            await self.run_generation_pipeline()
            
            # Save batch metadata if enabled
            if ENABLE_BATCH_FOLDERS and SAVE_BATCH_METADATA:
                self.batch_manager.finalize_batch_metadata(
                    completed_conversations=self.total_source_conversations,
                    total_chunks=self.total_training_chunks,
                    batch_folder=self.batch_id
                )
                self.batch_manager.save_batch_metadata(self.batch_id)
            
            # Final summary
            self.print_final_summary()
            
        except KeyboardInterrupt:
            self.console.print("\n[yellow]Generation interrupted by user.[/yellow]")
            
            # Save partial metadata if batch mode is enabled
            if ENABLE_BATCH_FOLDERS and SAVE_BATCH_METADATA and self.batch_manager:
                self.batch_manager.finalize_batch_metadata(
                    completed_conversations=self.total_source_conversations,
                    total_chunks=self.total_training_chunks,
                    batch_folder=self.batch_id,
                    status="interrupted"
                )
                self.batch_manager.save_batch_metadata(self.batch_id)
            
            self.print_final_summary()
        except Exception as e:
            self.console.print(f"\n[red]Fatal error: {e}[/red]")
            
            # Save error metadata if batch mode is enabled
            if ENABLE_BATCH_FOLDERS and SAVE_BATCH_METADATA and self.batch_manager:
                self.batch_manager.finalize_batch_metadata(
                    completed_conversations=self.total_source_conversations,
                    total_chunks=self.total_training_chunks,
                    batch_folder=self.batch_id,
                    status="failed",
                    error_message=str(e)
                )
                self.batch_manager.save_batch_metadata(self.batch_id)
            
            raise
