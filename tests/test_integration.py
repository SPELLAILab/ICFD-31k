#!/usr/bin/env python3
"""
Integration test to verify placeholder replacement in the ACTUAL generation flow.
This tests the construct_meta_prompt method to ensure placeholders are replaced.
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

from src.generators.conversation_generator import ConversationGenerator
from rich.console import Console
import groq

def test_prompt_generation():
    """Test that placeholders are replaced in actual prompt generation."""
    
    print("\n" + "="*80)
    print("INTEGRATION TEST: Prompt Generation with Placeholder Replacement")
    print("="*80)
    
    # Create a mock generator (we won't actually call the API)
    console = Console()
    # Create a dummy client (we won't use it)
    generator = ConversationGenerator(console, None)
    
    # Test utility scenario (the failing case)
    utility_scenario = {
        'scenario_id': 2,
        'description': 'A user receives a call from someone claiming to be from their mobile carrier ([MOBILE_CARRIER]). The agent states the user\'s SIM card will be blocked.',
        'case_type': 'Clear Fraud',
        'policy': 'Rule A: Mobile carriers never ask customers to install third-party apps.',
        'platform_type': 'telecom_provider'
    }
    
    agent_persona = "Aggressive Scammer"
    customer_persona = "Cautious Customer"
    duration = 120
    customer_name = "Rohan Sharma"
    bank_name = "HDFC Bank"
    
    # Call the actual method that's used in generation
    system_prompt, user_prompt = generator.construct_meta_prompt(
        agent_persona, customer_persona, utility_scenario, 
        duration, customer_name, bank_name
    )
    
    print("\n📋 Generated User Prompt:")
    print("-" * 80)
    print(user_prompt)
    print("-" * 80)
    
    # Check if placeholder still exists
    if "[MOBILE_CARRIER]" in user_prompt:
        print("\nFAILED: [MOBILE_CARRIER] placeholder NOT replaced in prompt!")
        print("   This is the EXACT prompt that would be sent to Groq API.")
        print("   The API would generate conversations with literal [MOBILE_CARRIER].")
        return False
    else:
        print("\nPASSED: [MOBILE_CARRIER] placeholder replaced successfully!")
        
        # Extract what it was replaced with
        import re
        match = re.search(r'mobile carrier \(([^)]+)\)', user_prompt)
        if match:
            replacement = match.group(1)
            print(f"   Replaced with: {replacement}")
        
        return True


def test_ecommerce_prompt():
    """Test e-commerce scenario in prompt generation."""
    
    print("\n" + "="*80)
    print("INTEGRATION TEST: E-commerce Prompt Generation")
    print("="*80)
    
    console = Console()
    generator = ConversationGenerator(console, None)
    
    ecommerce_scenario = {
        'scenario_id': 1,
        'description': 'A user receives a call about an order from [MARKETPLACE_PLATFORM] for a [ELECTRONICS_ITEM].',
        'case_type': 'Clear Fraud',
        'policy': 'Rule: Never share OTP',
        'platform_type': 'marketplace'
    }
    
    agent_persona = "Friendly Agent"
    customer_persona = "Trusting Customer"
    duration = 90
    customer_name = "Priya Patel"
    bank_name = "SBI"
    
    system_prompt, user_prompt = generator.construct_meta_prompt(
        agent_persona, customer_persona, ecommerce_scenario, 
        duration, customer_name, bank_name
    )
    
    print("\n📋 Generated User Prompt:")
    print("-" * 80)
    print(user_prompt)
    print("-" * 80)
    
    # Check for placeholders
    has_placeholders = "[MARKETPLACE_PLATFORM]" in user_prompt or "[ELECTRONICS_ITEM]" in user_prompt
    
    if has_placeholders:
        print("\nFAILED: E-commerce placeholders NOT replaced!")
        return False
    else:
        print("\nPASSED: E-commerce placeholders replaced successfully!")
        return True


def test_multiple_placeholders():
    """Test scenario with multiple placeholders."""
    
    print("\n" + "="*80)
    print("INTEGRATION TEST: Multiple Placeholders")
    print("="*80)
    
    console = Console()
    generator = ConversationGenerator(console, None)
    
    complex_scenario = {
        'scenario_id': 3,
        'description': 'Agent from [STATE_ELECTRICITY_BOARD] asks for payment via [UPI_APP] for urgent bill.',
        'case_type': 'Clear Fraud',
        'policy': 'Rule: Never pay to personal UPI',
        'platform_type': 'utility_provider'
    }
    
    agent_persona = "Urgent Agent"
    customer_persona = "Worried Customer"
    duration = 100
    customer_name = "Vikram Singh"
    bank_name = "ICICI Bank"
    
    system_prompt, user_prompt = generator.construct_meta_prompt(
        agent_persona, customer_persona, complex_scenario, 
        duration, customer_name, bank_name
    )
    
    print("\n📋 Generated User Prompt:")
    print("-" * 80)
    print(user_prompt)
    print("-" * 80)
    
    # Check for any placeholders
    has_placeholders = "[" in user_prompt and "]" in user_prompt
    
    if has_placeholders:
        print("\nFAILED: Some placeholders NOT replaced!")
        print(f"   Prompt still contains: {[word for word in user_prompt.split() if '[' in word]}")
        return False
    else:
        print("\nPASSED: All placeholders replaced successfully!")
        return True


def main():
    """Run all integration tests."""
    
    print("\n" + "="*80)
    print("PLACEHOLDER REPLACEMENT INTEGRATION TEST SUITE")
    print("="*80)
    print("\nThis tests the ACTUAL prompt generation flow used by the API.")
    print("If these tests pass, the generated conversations will have real entities.")
    print("="*80)
    
    utility_ok = test_prompt_generation()
    ecommerce_ok = test_ecommerce_prompt()
    multiple_ok = test_multiple_placeholders()
    
    print("\n" + "="*80)
    print("FINAL RESULTS")
    print("="*80)
    
    if utility_ok and ecommerce_ok and multiple_ok:
        print("PASS: ALL INTEGRATION TESTS PASSED!")
        print("PASS: Placeholder replacement working in actual generation flow")
        print("PASS: Safe to generate conversations - prompts will use real entities")
        sys.exit(0)
    else:
        print("FAIL: Integration tests failed.")
        print("\nIssues:")
        if not utility_ok:
            print("  - Utility placeholders failing in prompt generation")
        if not ecommerce_ok:
            print("  - E-commerce placeholders failing in prompt generation")
        if not multiple_ok:
            print("  - Multiple placeholders not handled correctly")
        sys.exit(1)


if __name__ == "__main__":
    main()
