"""
MASTER ENTITY INTEGRATION TEST
==============================

Comprehensive test for ALL entity domains in the fraud detection pipeline.
This test validates that all 5 entity domains are properly loaded and integrated:

1. E-commerce Entities (851 entities)
2. Utility Entities (137 entities)  
3. Job Entities (228 entities)
4. Loan Entities (169 entities)
5. Tech Entities (152 entities)

TOTAL: 1,537 entities across 5 domains

Run this test before generating conversations for ANY domain to ensure
the entire entity system is working correctly.
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

print("=" * 80)
print(" " * 20 + "MASTER ENTITY INTEGRATION TEST")
print("=" * 80)
print()

all_tests_passed = True
domain_stats = {}

# =============================================================================
# TEST 1: E-COMMERCE ENTITIES
# =============================================================================
print("Test 1: E-commerce Entities")
print("-" * 80)

try:
    from data.entities.ecommerce_entities import (
        INDIAN_MARKETPLACES, INDIAN_ECOMMERCE_RETAIL, INDIAN_UPI_APPS,
        ELECTRONICS_ITEMS, get_all_platforms, get_all_products
    )
    
    ecommerce_count = len(get_all_platforms()) + len(get_all_products())
    domain_stats['ecommerce'] = ecommerce_count
    print(f"PASS: E-commerce entities loaded: {ecommerce_count} entities")
    ecommerce_pass = True
except Exception as e:
    print(f"FAILED: {e}")
    ecommerce_pass = False
    all_tests_passed = False

print()

# =============================================================================
# TEST 2: UTILITY ENTITIES
# =============================================================================
print("Test 2: Utility Entities")
print("-" * 80)

try:
    from data.entities.utility_entities import (
        STATE_ELECTRICITY_BOARDS, MOBILE_CARRIERS,
        get_all_utility_providers
    )
    
    utility_count = len(get_all_utility_providers())
    domain_stats['utility'] = utility_count
    print(f"PASS: Utility entities loaded: {utility_count} entities")
    utility_pass = True
except Exception as e:
    print(f"FAILED: {e}")
    utility_pass = False
    all_tests_passed = False

print()

# =============================================================================
# TEST 3: JOB ENTITIES
# =============================================================================
print("Test 3: Job Entities")
print("-" * 80)

try:
    from data.entities.job_entities import (
        IT_COMPANIES, MNC_COMPANIES, JOB_PORTALS,
        get_all_job_entities
    )
    
    job_count = len(get_all_job_entities())
    domain_stats['job'] = job_count
    print(f"PASS: Job entities loaded: {job_count} entities")
    job_pass = True
except Exception as e:
    print(f"FAILED: {e}")
    job_pass = False
    all_tests_passed = False

print()

# =============================================================================
# TEST 4: LOAN ENTITIES
# =============================================================================
print("Test 4: Loan Entities")
print("-" * 80)

try:
    from data.entities.loan_entities import (
        PREDATORY_LENDING_APPS, LEGITIMATE_LENDING_APPS,
        NBFC_COMPANIES, get_all_loan_entities
    )
    
    loan_count = len(get_all_loan_entities())
    domain_stats['loan'] = loan_count
    print(f"PASS: Loan entities loaded: {loan_count} entities")
    loan_pass = True
except Exception as e:
    print(f"FAILED: {e}")
    loan_pass = False
    all_tests_passed = False

print()

# =============================================================================
# TEST 5: TECH ENTITIES
# =============================================================================
print("Test 5: Tech Entities")
print("-" * 80)

try:
    from data.entities.tech_entities import (
        TECH_COMPANIES, SOCIAL_MEDIA_PLATFORMS, EMAIL_PROVIDERS,
        get_all_tech_entities
    )
    
    tech_count = len(get_all_tech_entities())
    domain_stats['tech'] = tech_count
    print(f"PASS: Tech entities loaded: {tech_count} entities")
    tech_pass = True
except Exception as e:
    print(f"FAILED: {e}")
    tech_pass = False
    all_tests_passed = False

print()

# =============================================================================
# TEST 6: CONVERSATION GENERATOR INTEGRATION
# =============================================================================
print("Test 6: Conversation Generator Integration - All Domains")
print("-" * 80)

try:
    from src.generators.conversation_generator import replace_placeholders
    
    # Test critical placeholders from each domain
    test_scenarios = [
        # E-commerce
        ("E-commerce", "[MARKETPLACE_PLATFORM] + [UPI_APP]", 
         "Order from [MARKETPLACE_PLATFORM] paid via [UPI_APP]", "ecommerce"),
        
        # Utility  
        ("Utility", "[STATE_ELECTRICITY_BOARD] + [MOBILE_CARRIER]",
         "Bill from [STATE_ELECTRICITY_BOARD] via [MOBILE_CARRIER]", "utility"),
        
        # Job
        ("Job", "[IT_COMPANY] + [JOB_PORTAL]",
         "Job at [IT_COMPANY] posted on [JOB_PORTAL]", "job"),
        
        # Loan
        ("Loan", "[LENDING_APP] + [CREDIT_BUREAU]",
         "Loan from [LENDING_APP] verified by [CREDIT_BUREAU]", "digital_lending_app"),
        
        # Tech (including critical [FOOD_DELIVERY_APP])
        ("Tech", "[TECH_COMPANY] + [SOCIAL_MEDIA_APP]",
         "Support from [TECH_COMPANY] for [SOCIAL_MEDIA_APP] account", "tech_support"),
        
        # Tech FOOD_DELIVERY_APP (CRITICAL TEST)
        ("Tech Food", "[FOOD_DELIVERY_APP]",
         "Refund from [FOOD_DELIVERY_APP] processing", "app_support"),
    ]
    
    integration_pass = True
    
    for domain, placeholders, test_text, platform in test_scenarios:
        result = replace_placeholders(test_text, platform)
        
        # Check if any placeholder remains
        has_placeholder = '[' in result and ']' in result
        
        if not has_placeholder:
            print(f"PASS: {domain:12} placeholders ({placeholders}): WORKING")
            print(f"   Result: {result}")
        else:
            print(f"FAIL: {domain:12} placeholders ({placeholders}): FAILED")
            print(f"   Result: {result}")
            integration_pass = False
            all_tests_passed = False
    
    if integration_pass:
        print(f"\nPASS: All domain placeholders integrated successfully")
    
except Exception as e:
    print(f"FAIL: Integration test FAILED: {e}")
    integration_pass = False
    all_tests_passed = False

print()

# =============================================================================
# TEST 7: CROSS-DOMAIN PLACEHOLDER TEST
# =============================================================================
print("Test 7: Cross-Domain Placeholder Test")
print("-" * 80)

try:
    from src.generators.conversation_generator import replace_placeholders
    
    # Complex scenario with placeholders from multiple domains
    cross_domain_text = """Customer used [UPI_APP] to pay [LENDING_APP] loan via [MOBILE_CARRIER].
Agent from [TECH_COMPANY] called about [SOCIAL_MEDIA_APP] account.
Job at [IT_COMPANY] requires [ECOMMERCE_PLATFORM] purchase."""
    
    result = replace_placeholders(cross_domain_text, "tech_support")
    
    # Check if ALL placeholders are replaced
    placeholders_to_check = [
        '[UPI_APP]', '[LENDING_APP]', '[MOBILE_CARRIER]',
        '[TECH_COMPANY]', '[SOCIAL_MEDIA_APP]', '[IT_COMPANY]',
        '[ECOMMERCE_PLATFORM]'
    ]
    
    all_replaced = all(ph not in result for ph in placeholders_to_check)
    
    if all_replaced:
        print(f"PASS: Cross-domain placeholders: ALL REPLACED")
        print(f"   Example output:")
        for line in result.split('\n'):
            if line.strip():
                print(f"   {line.strip()}")
        cross_domain_pass = True
    else:
        remaining = [ph for ph in placeholders_to_check if ph in result]
        print(f"FAIL: Cross-domain placeholders: SOME NOT REPLACED")
        print(f"   Not replaced: {', '.join(remaining)}")
        cross_domain_pass = False
        all_tests_passed = False
        
except Exception as e:
    print(f"FAIL: Cross-domain test FAILED: {e}")
    cross_domain_pass = False
    all_tests_passed = False

print()

# =============================================================================
# FINAL SUMMARY
# =============================================================================
print("=" * 80)
print(" " * 30 + "FINAL SUMMARY")
print("=" * 80)

print("\nDomain Entity Counts:")
if domain_stats:
    total = sum(domain_stats.values())
    for domain, count in domain_stats.items():
        print(f"  {domain.capitalize():15} {count:4} entities")
    print(f"  {'-' * 30}")
    print(f"  {'TOTAL':15} {total:4} entities")

print("\nTest Results:")
test_results = [
    ("E-commerce Entities", ecommerce_pass),
    ("Utility Entities", utility_pass),
    ("Job Entities", job_pass),
    ("Loan Entities", loan_pass),
    ("Tech Entities", tech_pass),
    ("Conversation Generator Integration", integration_pass),
    ("Cross-Domain Placeholders", cross_domain_pass),
]

passed = sum(1 for _, result in test_results if result)
total_tests = len(test_results)

for test_name, result in test_results:
    status = "PASS" if result else "FAIL"
    print(f"{status}: {test_name}")

print()
print(f"Tests Passed: {passed}/{total_tests}")

if all_tests_passed:
    print()
    print("=" * 80)
    print("ALL ENTITY TESTS PASSED")
    print("=" * 80)
    print()
    print("All 5 entity domains operational")
    print(f"{sum(domain_stats.values())} total entities ready")
    print("All placeholders working across domains")
    print("Cross-domain integration verified")
    print()
    print("STATUS: Ready for generation across all domains")
    print("=" * 80)
    sys.exit(0)
else:
    print()
    print("=" * 80)
    print("SOME TESTS FAILED")
    print("=" * 80)
    print()
    print("Fix failing tests before proceeding.")
    print()
    sys.exit(1)
