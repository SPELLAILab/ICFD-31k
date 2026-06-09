#!/usr/bin/env python3
"""
Synthetic Dataset Generator for ICFD-31k.

Generates source conversations and streaming training chunks from the
persona, scenario, and entity libraries in ``data/``.

Architecture:
1. Stage 1: generate_source_conversation() - Creates complete conversations via Groq API
2. Stage 2: expand_conversation_into_chunks() - Expands conversations into training chunks
"""

import asyncio
import argparse
from dotenv import load_dotenv

from src.core.dataset_generator import DatasetGenerator
from config.settings import COMBINATION_MULTIPLIER

# Load environment variables from .env file
load_dotenv()


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Generate systematic synthetic dataset for fraud detection",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Banking fraud (default)
  python generate_dataset.py --multiplier 1
  
  # E-commerce fraud
  python generate_dataset.py --scenarios data/scenarios/scenarios_ecommerce.txt --multiplier 1
  
  # Custom scenarios with higher multiplier
  python generate_dataset.py --scenarios data/scenarios/scenarios_bank.txt --multiplier 3
  
  # Dry run to see what would be generated
  python generate_dataset.py --scenarios data/scenarios/scenarios_ecommerce.txt --dry-run

With 10 agents × 10 customers × 30 scenarios:
  Multiplier 1: 3,000 conversations
  Multiplier 2: 6,000 conversations  
  Multiplier 3: 9,000 conversations
        """
    )
    
    parser.add_argument(
        '--multiplier', 
        type=int, 
        default=COMBINATION_MULTIPLIER,
        help=f'Number of variations per unique combination (default: {COMBINATION_MULTIPLIER})'
    )
    
    parser.add_argument(
        '--scenarios',
        type=str,
        default=None,
        help='Path to scenarios file (e.g., data/scenarios/scenarios_ecommerce.txt). Default: data/scenarios/scenarios.txt'
    )
    
    parser.add_argument(
        '--personas',
        type=str,
        default=None,
        help='Path to personas file (e.g., data/testing/personas_cross_domain.txt). Default: data/personas.txt'
    )
    
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Show generation plan without actually running it'
    )
    
    return parser.parse_args()


async def main():
    """Main entry point for the dataset generator."""
    
    args = parse_arguments()
    
    # Create and run the dataset generator
    generator = DatasetGenerator(
        scenarios_file=args.scenarios,
        personas_file=args.personas
    )
    
    if args.dry_run:
        # Load data and show plan without generating
        generator.load_input_data()
        generator.generate_combinations(args.multiplier)
        generator.console.print("\n[yellow]Dry run complete. Use without --dry-run to generate the dataset.[/yellow]")
    else:
        # Run the full generation pipeline
        await generator.main(multiplier=args.multiplier)


if __name__ == "__main__":
    asyncio.run(main())
