"""
Base class for all evaluation tests
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List
from pathlib import Path
import json
from rich.console import Console

console = Console()


class BaseEvaluationTest(ABC):
    """Abstract base class for dataset evaluation tests"""
    
    def __init__(self, conversations: List[str], labels: List[str], 
                 case_types: List[str], output_dir: Path):
        """
        Initialize test with dataset
        
        Args:
            conversations: List of conversation texts
            labels: List of labels (YES/NO)
            case_types: List of case types
            output_dir: Directory to save results
        """
        self.conversations = conversations
        self.labels = labels
        self.case_types = case_types
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        self.results = {}
    
    @abstractmethod
    def run(self) -> Dict[str, Any]:
        """
        Run the evaluation test
        
        Returns:
            Dictionary containing test results
        """
        pass
    
    @abstractmethod
    def get_test_name(self) -> str:
        """Return the name of the test"""
        pass
    
    def save_results(self, filename: str = None):
        """Save test results to JSON file"""
        if filename is None:
            filename = f"{self.get_test_name().lower().replace(' ', '_')}_results.json"
        
        output_path = self.output_dir / filename
        
        # Convert numpy types to Python native types for JSON serialization
        def convert_to_native(obj):
            import numpy as np
            if isinstance(obj, (np.integer, np.floating)):
                return float(obj)
            elif isinstance(obj, (np.ndarray,)):
                return obj.tolist()
            elif isinstance(obj, (np.bool_,)):
                return bool(obj)
            elif isinstance(obj, dict):
                return {k: convert_to_native(v) for k, v in obj.items()}
            elif isinstance(obj, (list, tuple)):
                return [convert_to_native(item) for item in obj]
            return obj
        
        serializable_results = convert_to_native(self.results)
        
        with open(output_path, 'w') as f:
            json.dump(serializable_results, f, indent=2)
        
        console.print(f"[green]✓ Results saved: {output_path}[/green]")
    
    def get_fraud_normal_split(self):
        """Split conversations by fraud/normal label"""
        fraud_convs = [c for c, l in zip(self.conversations, self.labels) if l == 'YES']
        normal_convs = [c for c, l in zip(self.conversations, self.labels) if l == 'NO']
        return fraud_convs, normal_convs
