"""
Combination generation utilities for systematic dataset creation.
"""

from typing import Dict, List, Any
from rich.console import Console
from rich.table import Table
from rich.panel import Panel


class CombinationGenerator:
    """Generates systematic combinations of agents, customers, and scenarios."""
    
    def __init__(self, console: Console):
        self.console = console
    
    def calculate_total_conversations(self, agents: List[str], customers: List[str], 
                                    scenarios: List[Dict], multiplier: int) -> tuple[int, int]:
        """
        Calculate the total number of conversations based on input data.
        
        Args:
            agents: List of agent personas
            customers: List of customer personas
            scenarios: List of scenarios
            multiplier: Number of variations per combination
            
        Returns:
            Tuple of (unique_combinations, total_conversations)
        """
        unique_combinations = len(agents) * len(customers) * len(scenarios)
        total_conversations = unique_combinations * multiplier
        
        self.console.print(f"\n[bold blue]Combination Calculation:[/bold blue]")
        self.console.print(f"  Agent Personas: {len(agents)}")
        self.console.print(f"  Customer Personas: {len(customers)}")
        self.console.print(f"  Scenarios: {len(scenarios)}")
        self.console.print(f"  Multiplier: {multiplier}")
        self.console.print(f"  → Unique Combinations: {unique_combinations:,}")
        self.console.print(f"  → Total Conversations: {total_conversations:,}")
        
        return unique_combinations, total_conversations
    
    def generate_combination_list(self, agents: List[str], customers: List[str], 
                                scenarios: List[Dict], multiplier: int) -> List[Dict[str, Any]]:
        """
        Generate systematic combinations ensuring each triplet is covered exactly N times.
        
        Args:
            agents: List of agent personas
            customers: List of customer personas
            scenarios: List of scenarios
            multiplier: Number of variations per combination
            
        Returns:
            List of combination dictionaries with agent, customer, scenario, and metadata
        """
        self.console.print(f"\n[bold blue]Generating systematic combinations...[/bold blue]")
        
        combinations = []
        session_id = 1
        
        for multiplier_round in range(multiplier):
            for scenario in scenarios:
                for agent in agents:
                    for customer in customers:
                        combination = {
                            'session_id': session_id,
                            'agent_persona': agent,
                            'customer_persona': customer,
                            'scenario': scenario,
                            'multiplier_round': multiplier_round + 1,
                            'combination_key': f"{scenario['scenario_id']}_{agents.index(agent)}_{customers.index(customer)}"
                        }
                        combinations.append(combination)
                        session_id += 1
        
        # Display combination statistics
        self._display_combination_statistics(combinations, scenarios)
        
        return combinations
    
    def _display_combination_statistics(self, combinations: List[Dict], scenarios: List[Dict]) -> None:
        """Display statistics about the generated combinations."""
        
        # Count combinations by case type
        case_type_counts = {}
        for combo in combinations:
            case_type = combo['scenario']['case_type']
            case_type_counts[case_type] = case_type_counts.get(case_type, 0) + 1
        
        # Create statistics table
        table = Table(title="Systematic Combination Distribution")
        table.add_column("Case Type", style="cyan")
        table.add_column("Combinations", style="green")
        table.add_column("Percentage", style="yellow")
        
        total_combinations = len(combinations)
        for case_type, count in case_type_counts.items():
            percentage = (count / total_combinations) * 100
            table.add_row(case_type, f"{count:,}", f"{percentage:.1f}%")
        
        self.console.print(table)
        
        # Display summary
        summary_text = f"""
[bold]Systematic Generation Summary:[/bold]

✓ Perfect coverage: Every agent-customer-scenario combination included
✓ Balanced distribution: Equal representation across all scenarios
✓ No random bias: Deterministic, reproducible generation
✓ Complete dataset: {total_combinations:,} conversations planned

This approach ensures comprehensive training data coverage!
        """.strip()
        
        self.console.print(Panel(summary_text, title="Generation Strategy", border_style="green"))
