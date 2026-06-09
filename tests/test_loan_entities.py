"""
Loan Entity Integration Test
=============================

Tests that loan entities are properly integrated into the conversation generator.

This test verifies:
1. Loan entity file loads correctly
2. All 169 loan entities are accessible
3. Placeholder replacement works for all loan placeholder types
4. Integration with conversation generator is complete

Run this before generating loan fraud conversations.
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

print("=" * 70)
print("LOAN ENTITY INTEGRATION TEST")
print("=" * 70)
print()

# =============================================================================
# TEST 1: LOAN ENTITIES IMPORT
# =============================================================================
print("Test 1: Loan Entity Import")
print("-" * 70)

try:
    from data.entities.loan_entities import (
        PREDATORY_LENDING_APPS, LEGITIMATE_LENDING_APPS,
        NBFC_COMPANIES, MICROFINANCE_INSTITUTIONS, CREDIT_BUREAUS,
        get_all_loan_entities, get_all_lending_apps,
        get_entity_by_category, get_entity_count_by_category
    )
    
    stats = get_entity_count_by_category()
    
    print(f"PASS: Loan entities loaded successfully")
    print(f"   - Predatory apps: {stats['predatory_apps']}")
    print(f"   - Legitimate apps: {stats['legitimate_apps']}")
    print(f"   - NBFC companies: {stats['nbfc_companies']}")
    print(f"   - Microfinance institutions: {stats['microfinance_institutions']}")
    print(f"   - Credit bureaus: {stats['credit_bureaus']}")
    print(f"   - TOTAL: {stats['total']} entities")
    
    import_pass = True
    total_entities = stats['total']
    
except Exception as e:
    print(f"FAILED: {e}")
    import_pass = False
    total_entities = 0

print()

# =============================================================================
# TEST 2: ENTITY DIVERSITY
# =============================================================================
print("Test 2: Entity Diversity Check")
print("-" * 70)

if import_pass:
    try:
        # Check that all categories have entities
        diversity_pass = True
        
        if len(PREDATORY_LENDING_APPS) < 30:
            print(f"WARN: Predatory apps count low: {len(PREDATORY_LENDING_APPS)}")
            diversity_pass = False
        else:
            print(f"PASS: Predatory apps: {len(PREDATORY_LENDING_APPS)} (sufficient)")
        
        if len(LEGITIMATE_LENDING_APPS) < 20:
            print(f"WARN: Legitimate apps count low: {len(LEGITIMATE_LENDING_APPS)}")
            diversity_pass = False
        else:
            print(f"PASS: Legitimate apps: {len(LEGITIMATE_LENDING_APPS)} (sufficient)")
        
        if len(NBFC_COMPANIES) < 30:
            print(f"WARN: NBFC count low: {len(NBFC_COMPANIES)}")
            diversity_pass = False
        else:
            print(f"PASS: NBFC companies: {len(NBFC_COMPANIES)} (sufficient)")
        
        if len(MICROFINANCE_INSTITUTIONS) < 20:
            print(f"WARN: Microfinance count low: {len(MICROFINANCE_INSTITUTIONS)}")
            diversity_pass = False
        else:
            print(f"PASS: Microfinance institutions: {len(MICROFINANCE_INSTITUTIONS)} (sufficient)")
        
        if len(CREDIT_BUREAUS) < 4:
            print(f"WARN: Credit bureaus count low: {len(CREDIT_BUREAUS)}")
            diversity_pass = False
        else:
            print(f"PASS: Credit bureaus: {len(CREDIT_BUREAUS)} (sufficient)")
        
        if diversity_pass:
            print(f"\nPASS: All entity categories have sufficient diversity")
        
    except Exception as e:
        print(f"FAILED: {e}")
        diversity_pass = False
else:
    diversity_pass = False

print()

# =============================================================================
# TEST 3: CONVERSATION GENERATOR INTEGRATION
# =============================================================================
print("Test 3: Conversation Generator Integration")
print("-" * 70)

try:
    from src.generators.conversation_generator import replace_placeholders
    
    test_cases = [
        {
            'name': '[LENDING_APP] replacement',
            'input': 'Loan from [LENDING_APP] is overdue',
            'placeholder': '[LENDING_APP]',
            'platform': 'digital_lending_app'
        },
        {
            'name': '[PREDATORY_APP] replacement',
            'input': 'Scam app [PREDATORY_APP] is harassing',
            'placeholder': '[PREDATORY_APP]',
            'platform': 'digital_lending_app'
        },
        {
            'name': '[LEGITIMATE_APP] replacement',
            'input': 'Apply via [LEGITIMATE_APP] for instant loan',
            'placeholder': '[LEGITIMATE_APP]',
            'platform': 'digital_lending_app'
        },
        {
            'name': '[NBFC] replacement',
            'input': 'Contact [NBFC] for personal loan',
            'placeholder': '[NBFC]',
            'platform': 'legitimate_bank'
        },
        {
            'name': '[MICROFINANCE] replacement',
            'input': 'Small loan from [MICROFINANCE] available',
            'placeholder': '[MICROFINANCE]',
            'platform': 'legitimate_bank'
        },
        {
            'name': '[CREDIT_BUREAU] replacement',
            'input': 'Check [CREDIT_BUREAU] score before applying',
            'placeholder': '[CREDIT_BUREAU]',
            'platform': 'digital_lending_app'
        },
    ]
    
    integration_pass = True
    
    for test in test_cases:
        result = replace_placeholders(test['input'], test['platform'])
        replaced = test['placeholder'] not in result
        
        if replaced:
            print(f"PASS: {test['name']}: WORKING")
            print(f"   Result: {result}")
        else:
            print(f"FAIL: {test['name']}: NOT REPLACED")
            print(f"   Result: {result}")
            integration_pass = False
    
    if integration_pass:
        print(f"\nPASS: All loan placeholders working in conversation generator")
    
except Exception as e:
    print(f"FAIL: Integration test FAILED: {e}")
    integration_pass = False

print()

# =============================================================================
# TEST 4: MIXED PLACEHOLDER TEST
# =============================================================================
print("Test 4: Mixed Domain Placeholder Test")
print("-" * 70)

try:
    from src.generators.conversation_generator import replace_placeholders
    
    # Test scenario with multiple placeholders (loan + e-commerce + utility)
    test_mixed = """Agent from [LENDING_APP] asking to pay via [UPI_APP]. 
Customer used [MOBILE_CARRIER] to receive OTP. 
Check [CREDIT_BUREAU] before taking loan from [NBFC]."""
    
    result_mixed = replace_placeholders(test_mixed, 'digital_lending_app')
    
    # Check that all placeholders are replaced
    placeholders_to_check = [
        '[LENDING_APP]', '[UPI_APP]', '[MOBILE_CARRIER]', 
        '[CREDIT_BUREAU]', '[NBFC]'
    ]
    
    all_replaced = all(ph not in result_mixed for ph in placeholders_to_check)
    
    if all_replaced:
        print(f"PASS: Mixed domain placeholders: ALL REPLACED")
        print(f"   Example output:")
        for line in result_mixed.split('\n'):
            if line.strip():
                print(f"   {line.strip()}")
        mixed_pass = True
    else:
        print(f"FAIL: Mixed domain placeholders: SOME NOT REPLACED")
        remaining = [ph for ph in placeholders_to_check if ph in result_mixed]
        print(f"   Not replaced: {', '.join(remaining)}")
        print(f"   Result: {result_mixed}")
        mixed_pass = False
        
except Exception as e:
    print(f"FAIL: Mixed placeholder test FAILED: {e}")
    mixed_pass = False

print()

# =============================================================================
# TEST 5: SAMPLE ENTITIES
# =============================================================================
print("Test 5: Sample Entities Validation")
print("-" * 70)

if import_pass:
    try:
        print("Sample Predatory Apps (first 5):")
        for app in PREDATORY_LENDING_APPS[:5]:
            print(f"  - {app}")
        
        print("\nSample Legitimate Apps (first 5):")
        for app in LEGITIMATE_LENDING_APPS[:5]:
            print(f"  - {app}")
        
        print("\nSample NBFCs (first 5):")
        for nbfc in NBFC_COMPANIES[:5]:
            print(f"  - {nbfc}")
        
        print("\nSample Microfinance (first 3):")
        for mfi in MICROFINANCE_INSTITUTIONS[:3]:
            print(f"  - {mfi}")
        
        print("\nAll Credit Bureaus:")
        for bureau in CREDIT_BUREAUS:
            print(f"  - {bureau}")
        
        sample_pass = True
        
    except Exception as e:
        print(f"FAIL: Sample validation FAILED: {e}")
        sample_pass = False
else:
    sample_pass = False

print()

# =============================================================================
# FINAL SUMMARY
# =============================================================================
print("=" * 70)
print("FINAL TEST SUMMARY")
print("=" * 70)

test_results = [
    ("Loan Entity Import", import_pass),
    ("Entity Diversity", diversity_pass),
    ("Conversation Generator Integration", integration_pass),
    ("Mixed Domain Placeholders", mixed_pass),
    ("Sample Entities", sample_pass),
]

passed = sum(1 for _, result in test_results if result)
total = len(test_results)

for test_name, result in test_results:
    status = "PASS" if result else "FAIL"
    print(f"{status}: {test_name}")

print()
print(f"Tests Passed: {passed}/{total}")

if passed == total:
    print()
    print("ALL LOAN ENTITY TESTS PASSED")
    print()
    print(f"PASS: {total_entities} loan entities ready for conversation generation")
    print(f"PASS: All 6 placeholder types working correctly")
    print(f"PASS: Integration with conversation generator complete")
    print()
    print("STATUS: READY TO GENERATE LOAN FRAUD CONVERSATIONS")
    sys.exit(0)
else:
    print()
    print("WARN: Some tests failed. Fix issues before generating.")
    sys.exit(1)
