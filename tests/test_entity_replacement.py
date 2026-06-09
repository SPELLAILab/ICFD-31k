#!/usr/bin/env python3
"""
Test script to verify entity replacement is working correctly.
This will catch placeholder replacement issues BEFORE running generation.
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

from src.generators.conversation_generator import replace_placeholders

def test_ecommerce_placeholders():
    """Test e-commerce entity replacements."""
    print("\n" + "="*80)
    print("TESTING E-COMMERCE PLACEHOLDER REPLACEMENT")
    print("="*80)
    
    test_cases = [
        "[MARKETPLACE_PLATFORM]",
        "[ECOMMERCE_PLATFORM]",
        "[ELECTRONICS_ITEM]",
        "[UPI_APP]",
        "[ITEM_CATEGORY]",
    ]
    
    passed = 0
    failed = 0
    
    for placeholder in test_cases:
        text = f"Test with {placeholder} placeholder"
        result = replace_placeholders(text)
        
        if placeholder in result:
            print(f"FAILED: {placeholder} NOT replaced")
            print(f"   Input:  {text}")
            print(f"   Output: {result}")
            failed += 1
        else:
            print(f"PASSED: {placeholder} → {result.replace('Test with ', '').replace(' placeholder', '')}")
            passed += 1
    
    print(f"\nE-commerce Results: {passed} passed, {failed} failed")
    return failed == 0


def test_utility_placeholders():
    """Test utility entity replacements."""
    print("\n" + "="*80)
    print("TESTING UTILITY PLACEHOLDER REPLACEMENT")
    print("="*80)
    
    test_cases = [
        "[STATE_ELECTRICITY_BOARD]",
        "[MOBILE_CARRIER]",
        "[INTERNET_PROVIDER]",
        "[GAS_AGENCY]",
        "[DTH_PROVIDER]",
        "[WATER_SUPPLY_DEPARTMENT]",
        "[GOVERNMENT_SCHEME]",
        "[UPI_APP]",
    ]
    
    passed = 0
    failed = 0
    
    for placeholder in test_cases:
        text = f"Test with {placeholder} placeholder"
        result = replace_placeholders(text)
        
        if placeholder in result:
            print(f"FAILED: {placeholder} NOT replaced")
            print(f"   Input:  {text}")
            print(f"   Output: {result}")
            failed += 1
        else:
            print(f"PASSED: {placeholder} → {result.replace('Test with ', '').replace(' placeholder', '')}")
            passed += 1
    
    print(f"\nUtility Results: {passed} passed, {failed} failed")
    return failed == 0


def test_real_scenario():
    """Test with actual scenario text."""
    print("\n" + "="*80)
    print("TESTING REAL SCENARIO TEXT")
    print("="*80)
    
    # E-commerce scenario
    ecommerce_scenario = "A user receives a call from someone claiming to be from [MARKETPLACE_PLATFORM]. The agent states there's an issue with their [ELECTRONICS_ITEM] order."
    
    result = replace_placeholders(ecommerce_scenario)
    
    if "[" in result and "]" in result:
        print("FAILED: E-commerce scenario still has placeholders")
        print(f"   Input:  {ecommerce_scenario}")
        print(f"   Output: {result}")
        ecommerce_ok = False
    else:
        print("PASSED: E-commerce scenario")
        print(f"   Input:  {ecommerce_scenario}")
        print(f"   Output: {result}")
        ecommerce_ok = True
    
    # Utility scenario
    utility_scenario = "An agent claiming to be from [MOBILE_CARRIER] calls stating the user's SIM card will be blocked. They ask the user to install an app."
    
    result = replace_placeholders(utility_scenario)
    
    if "[" in result and "]" in result:
        print("\nFAILED: Utility scenario still has placeholders")
        print(f"   Input:  {utility_scenario}")
        print(f"   Output: {result}")
        utility_ok = False
    else:
        print("\nPASSED: Utility scenario")
        print(f"   Input:  {utility_scenario}")
        print(f"   Output: {result}")
        utility_ok = True
    
    return ecommerce_ok and utility_ok


def main():
    """Run all tests."""
    print("\n" + "="*80)
    print("ENTITY REPLACEMENT TEST SUITE")
    print("="*80)
    print("\nThis test verifies that placeholders are replaced BEFORE API calls.")
    print("If this fails, you'll waste API credits generating conversations with")
    print("literal [PLACEHOLDER] text instead of real entity names.")
    print("="*80)
    
    ecommerce_ok = test_ecommerce_placeholders()
    utility_ok = test_utility_placeholders()
    scenario_ok = test_real_scenario()
    
    print("\n" + "="*80)
    print("FINAL RESULTS")
    print("="*80)
    
    if ecommerce_ok and utility_ok and scenario_ok:
        print("PASS: ALL TESTS PASSED - Entity replacement working correctly!")
        print("PASS: Safe to generate conversations - API calls will use real entities")
        sys.exit(0)
    else:
        print("FAIL: Entity replacement tests failed.")
        print("Fix placeholder replacement issues before running generation.")
        print("\nIssues found:")
        if not ecommerce_ok:
            print("  - E-commerce placeholders not working")
        if not utility_ok:
            print("  - Utility placeholders not working (CRITICAL - currently generating)")
        if not scenario_ok:
            print("  - Real scenario text replacement failing")
        sys.exit(1)


if __name__ == "__main__":
    main()
