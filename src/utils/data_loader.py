"""
Data loading and parsing utilities for personas and scenarios.
"""

import re
from typing import Dict, List, Tuple, Any
from rich.console import Console
from rich.table import Table


class DataLoader:
    """Handles loading and parsing of input data files."""
    
    def __init__(self, console: Console):
        self.console = console
    
    def load_personas(self, filepath: str) -> Tuple[List[str], List[str]]:
        """
        Parse personas.txt file into agent and customer persona lists.
        
        Args:
            filepath: Path to the personas.txt file
            
        Returns:
            Tuple of (agent_personas, customer_personas) lists
        """
        self.console.print(f"\n[bold blue]Loading personas from {filepath}...[/bold blue]")
        
        with open(filepath, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Split content into sections
        sections = content.split('[')
        agent_personas = []
        customer_personas = []
        
        current_section = None
        
        for section in sections:
            if section.startswith('AGENT PERSONAS]'):
                current_section = 'agent'
                lines = section.split('\n')[1:]  # Skip the header line
            elif section.startswith('CUSTOMER PERSONAS]'):
                current_section = 'customer'
                lines = section.split('\n')[1:]  # Skip the header line
            else:
                continue
                
            # Parse personas from lines
            for line in lines:
                line = line.strip()
                # Skip empty lines, section headers, and delimiter markers
                if line and not line.startswith('[') and not line.startswith('---'):
                    if current_section == 'agent':
                        agent_personas.append(line)
                    elif current_section == 'customer':
                        customer_personas.append(line)
        
        self.console.print(f"✓ Loaded {len(agent_personas)} agent personas")
        self.console.print(f"✓ Loaded {len(customer_personas)} customer personas")
        
        return agent_personas, customer_personas
    
    def load_scenarios(self, filepath: str) -> List[Dict[str, Any]]:
        """
        Parse scenarios.txt file into a list of scenario dictionaries.
        
        Args:
            filepath: Path to the scenarios.txt file
            
        Returns:
            List of scenario dictionaries with keys: scenario_id, description, case_type, policy
        """
        self.console.print(f"\n[bold blue]Loading scenarios from {filepath}...[/bold blue]")
        
        with open(filepath, 'r', encoding='utf-8') as file:
            content = file.read()
        
        scenarios = []
        # Split by scenario headers
        scenario_sections = re.split(r'\[SCENARIO (\d+)\]', content)[1:]  # Remove empty first element
        
        # Process pairs of (scenario_number, scenario_content)
        for i in range(0, len(scenario_sections), 2):
            if i + 1 < len(scenario_sections):
                scenario_id = int(scenario_sections[i])
                scenario_content = scenario_sections[i + 1].strip()
                
                # Parse the scenario content
                lines = scenario_content.split('\n')
                description = ""
                case_type = ""
                platform_type = None
                context = None
                fraud_technique = None
                policy_lines = []
                
                current_section = None
                
                for line in lines:
                    line = line.strip()
                    if line.startswith('description:'):
                        description = line[12:].strip()  # Remove 'description: '
                    elif line.startswith('case_type:'):
                        case_type = line[10:].strip()  # Remove 'case_type: '
                    elif line.startswith('platform_type:'):
                        platform_type = line[14:].strip()  # Remove 'platform_type: '
                    elif line.startswith('context:'):
                        context = line[8:].strip()  # Remove 'context: '
                    elif line.startswith('fraud_technique:'):
                        fraud_technique = line[16:].strip()  # Remove 'fraud_technique: '
                    elif line.startswith('policy:'):
                        current_section = 'policy'
                    elif current_section == 'policy' and line:
                        policy_lines.append(line)
                
                scenario = {
                    'scenario_id': scenario_id,
                    'description': description,
                    'case_type': case_type,
                    'policy': '\n'.join(policy_lines)
                }
                
                # Add optional metadata fields if present
                if platform_type:
                    scenario['platform_type'] = platform_type
                if context:
                    scenario['context'] = context
                if fraud_technique:
                    scenario['fraud_technique'] = fraud_technique
                
                scenarios.append(scenario)
        
        self.console.print(f"✓ Loaded {len(scenarios)} scenarios")
        
        # Display scenario distribution
        self._display_scenario_distribution(scenarios)
        
        return scenarios
    
    def _display_scenario_distribution(self, scenarios: List[Dict[str, Any]]) -> None:
        """Display a table showing the distribution of scenario types."""
        case_types = {}
        for scenario in scenarios:
            case_type = scenario['case_type']
            case_types[case_type] = case_types.get(case_type, 0) + 1
        
        table = Table(title="Scenario Distribution")
        table.add_column("Case Type", style="cyan")
        table.add_column("Count", style="green")
        
        for case_type, count in case_types.items():
            table.add_row(case_type, str(count))
        
        self.console.print(table)
