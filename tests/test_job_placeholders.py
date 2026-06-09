#!/usr/bin/env python3
"""
Job Entity Placeholder Test - Verify job fraud scenarios work correctly.
"""

import sys
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

from src.generators.conversation_generator import ConversationGenerator
from rich.console import Console

def test_job_placeholders():
    """Test job entity placeholder replacement in actual prompt generation."""
    
    print("\n" + "="*80)
    print("JOB ENTITY PLACEHOLDER INTEGRATION TEST")
    print("="*80)
    
    console = Console()
    generator = ConversationGenerator(console, None)
    
    # Test all job placeholder types
    test_scenarios = [
        {
            'scenario_id': 1,
            'description': 'Agent from [IT_COMPANY] calls about interview on [JOB_PORTAL]. Pay ₹1500 via [UPI_APP].',
            'case_type': 'Clear Fraud',
            'policy': 'Rule: Never pay fees for interviews',
            'platform_type': 'corporate'
        },
        {
            'scenario_id': 2,
            'description': 'Fake offer from [MNC_COMPANY]. Pay for background check.',
            'case_type': 'Clear Fraud',
            'policy': 'Rule: Company pays for background checks',
            'platform_type': 'corporate'
        },
        {
            'scenario_id': 3,
            'description': 'Bribery for job at [GOVERNMENT_DEPT].',
            'case_type': 'Clear Fraud',
            'policy': 'Rule: Government jobs are merit-based',
            'platform_type': 'government'
        },
        {
            'scenario_id': 4,
            'description': 'Fake cabin crew job from [AIRLINE_COMPANY]. Pay medical fee.',
            'case_type': 'Clear Fraud',
            'policy': 'Rule: Company arranges medical exams',
            'platform_type': 'corporate'
        }
    ]
    
    all_passed = True
    
    for i, scenario in enumerate(test_scenarios, 1):
        print(f"\n{'─'*80}")
        print(f"Test {i}: {scenario['description'][:60]}...")
        print(f"{'─'*80}")
        
        system_prompt, user_prompt = generator.construct_meta_prompt(
            "Scammer", "Cautious Customer", scenario,
            90, "Rohan Sharma", "HDFC Bank"
        )
        
        # Check if placeholders still exist
        placeholders_found = []
        for placeholder in ["[IT_COMPANY]", "[MNC_COMPANY]", "[JOB_PORTAL]", 
                          "[GOVERNMENT_DEPT]", "[AIRLINE_COMPANY]", "[UPI_APP]"]:
            if placeholder in user_prompt:
                placeholders_found.append(placeholder)
        
        if placeholders_found:
            print(f"FAILED: Placeholders NOT replaced: {', '.join(placeholders_found)}")
            print(f"\nGenerated prompt:\n{user_prompt}")
            all_passed = False
        else:
            print(f"PASSED: All placeholders replaced")
            # Extract and show what was replaced
            import re
            scenario_line = [line for line in user_prompt.split('\n') if 'Scenario:' in line][0]
            print(f"   {scenario_line}")
    
    print("\n" + "="*80)
    if all_passed:
        print("PASS: ALL JOB PLACEHOLDER TESTS PASSED!")
        print("PASS: Job entity integration working correctly")
        print("PASS: Safe to generate job fraud conversations")
        return True
    else:
        print("FAIL: JOB PLACEHOLDER TESTS FAILED!")
        print("FAIL: Fix issues before generating job conversations")
        return False


if __name__ == "__main__":
    success = test_job_placeholders()
    sys.exit(0 if success else 1)
