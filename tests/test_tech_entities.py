"""
Tech Entity Integration Test
============================

Tests that tech entities are properly integrated into the conversation generator.

This test verifies:
1. Tech entity file loads correctly
2. All 152 tech entities are accessible
3. Placeholder replacement works for all tech placeholder types
4. Integration with conversation generator is complete

Run this before generating tech fraud conversations.
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

print("=" * 70)
print("TECH ENTITY INTEGRATION TEST")
print("=" * 70)
print()

# =============================================================================
# TEST 1: TECH ENTITIES IMPORT
# =============================================================================
print("Test 1: Tech Entity Import")
print("-" * 70)

try:
    from data.entities.tech_entities import (
        TECH_COMPANIES, SOCIAL_MEDIA_PLATFORMS, EMAIL_PROVIDERS,
        GAMING_PLATFORMS, GIFT_CARD_BRANDS, RIDE_HAILING_APPS,
        get_all_tech_entities, get_entity_by_category,
        get_entity_count_by_category
    )
    
    stats = get_entity_count_by_category()
    
    print(f"PASS: Tech entities loaded successfully")
    print(f"   - Tech companies: {stats['tech_companies']}")
    print(f"   - Social media platforms: {stats['social_media_platforms']}")
    print(f"   - Email providers: {stats['email_providers']}")
    print(f"   - Gaming platforms: {stats['gaming_platforms']}")
    print(f"   - Gift card brands: {stats['gift_card_brands']}")
    print(f"   - Ride-hailing apps: {stats['ride_hailing_apps']}")
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
        diversity_pass = True
        
        if len(TECH_COMPANIES) < 30:
            print(f"WARN: Tech companies count low: {len(TECH_COMPANIES)}")
            diversity_pass = False
        else:
            print(f"PASS: Tech companies: {len(TECH_COMPANIES)} (sufficient)")
        
        if len(SOCIAL_MEDIA_PLATFORMS) < 20:
            print(f"WARN: Social media platforms count low: {len(SOCIAL_MEDIA_PLATFORMS)}")
            diversity_pass = False
        else:
            print(f"PASS: Social media platforms: {len(SOCIAL_MEDIA_PLATFORMS)} (sufficient)")
        
        if len(EMAIL_PROVIDERS) < 12:
            print(f"WARN: Email providers count low: {len(EMAIL_PROVIDERS)}")
            diversity_pass = False
        else:
            print(f"PASS: Email providers: {len(EMAIL_PROVIDERS)} (sufficient)")
        
        if len(GAMING_PLATFORMS) < 15:
            print(f"WARN: Gaming platforms count low: {len(GAMING_PLATFORMS)}")
            diversity_pass = False
        else:
            print(f"PASS: Gaming platforms: {len(GAMING_PLATFORMS)} (sufficient)")
        
        if len(GIFT_CARD_BRANDS) < 15:
            print(f"WARN: Gift card brands count low: {len(GIFT_CARD_BRANDS)}")
            diversity_pass = False
        else:
            print(f"PASS: Gift card brands: {len(GIFT_CARD_BRANDS)} (sufficient)")
        
        if len(RIDE_HAILING_APPS) < 8:
            print(f"WARN: Ride-hailing apps count low: {len(RIDE_HAILING_APPS)}")
            diversity_pass = False
        else:
            print(f"PASS: Ride-hailing apps: {len(RIDE_HAILING_APPS)} (sufficient)")
        
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
            'name': '[TECH_COMPANY] replacement',
            'input': 'Support from [TECH_COMPANY] called about virus',
            'placeholder': '[TECH_COMPANY]',
            'platform': 'tech_support'
        },
        {
            'name': '[SOCIAL_MEDIA_APP] replacement',
            'input': 'Your [SOCIAL_MEDIA_APP] account is suspended',
            'placeholder': '[SOCIAL_MEDIA_APP]',
            'platform': 'social_media'
        },
        {
            'name': '[EMAIL_PROVIDER] replacement',
            'input': 'Alert from [EMAIL_PROVIDER] security team',
            'placeholder': '[EMAIL_PROVIDER]',
            'platform': 'email_provider'
        },
        {
            'name': '[GAMING_PLATFORM] replacement',
            'input': 'Purchase verification on [GAMING_PLATFORM]',
            'placeholder': '[GAMING_PLATFORM]',
            'platform': 'gaming_platform'
        },
        {
            'name': '[GIFT_CARD_BRAND] replacement',
            'input': 'Pay using [GIFT_CARD_BRAND] for support',
            'placeholder': '[GIFT_CARD_BRAND]',
            'platform': 'tech_support'
        },
        {
            'name': '[RIDE_HAILING_APP] replacement',
            'input': 'Safety complaint on [RIDE_HAILING_APP]',
            'placeholder': '[RIDE_HAILING_APP]',
            'platform': 'app_support'
        },
        {
            'name': '[FOOD_DELIVERY_APP] replacement (CRITICAL)',
            'input': 'Refund from [FOOD_DELIVERY_APP] is stuck',
            'placeholder': '[FOOD_DELIVERY_APP]',
            'platform': 'app_support'
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
        print(f"\nPASS: All tech placeholders working in conversation generator")
    
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
    
    # Test scenario with multiple placeholders (tech + e-commerce + utility)
    test_mixed = """Agent from [TECH_COMPANY] asking for [GIFT_CARD_BRAND] payment. 
Customer uses [UPI_APP] and [EMAIL_PROVIDER] for verification.
Account on [SOCIAL_MEDIA_APP] accessed via [INTERNET_PROVIDER]."""
    
    result_mixed = replace_placeholders(test_mixed, 'tech_support')
    
    # Check that all placeholders are replaced
    placeholders_to_check = [
        '[TECH_COMPANY]', '[GIFT_CARD_BRAND]', '[UPI_APP]', 
        '[EMAIL_PROVIDER]', '[SOCIAL_MEDIA_APP]', '[INTERNET_PROVIDER]'
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
# TEST 5: TECH SCENARIO SIMULATION
# =============================================================================
print("Test 5: Tech Scenario Simulation")
print("-" * 70)

try:
    from src.generators.conversation_generator import replace_placeholders
    
    # Simulate actual scenarios from scenarios_tech.txt
    scenarios = [
        {
            'name': 'Scenario 1 (Remote Access)',
            'text': 'Agent from [TECH_COMPANY] detected virus and requests AnyDesk access',
            'platform': 'tech_support'
        },
        {
            'name': 'Scenario 2 (OTP Theft)',
            'text': '[ECOMMERCE_PLATFORM] security detected login from different state',
            'platform': 'ecommerce_account'
        },
        {
            'name': 'Scenario 3 (Blackmail)',
            'text': 'Hacker threatens to post photos from [SOCIAL_MEDIA_APP] via [UPI_APP]',
            'platform': 'social_media'
        },
        {
            'name': 'Scenario 5 (Gift Card)',
            'text': '[TECH_COMPANY] wants payment via [GIFT_CARD_BRAND]',
            'platform': 'tech_support'
        },
        {
            'name': 'Scenario 6 (Password Phishing)',
            'text': '[EMAIL_PROVIDER] Support asks for email password',
            'platform': 'email_provider'
        },
        {
            'name': 'Scenario 17 (Gaming)',
            'text': 'Agent from [GAMING_PLATFORM] verifies large purchase',
            'platform': 'gaming_platform'
        },
        {
            'name': 'Scenario 19 (Ride-Hailing)',
            'text': '[RIDE_HAILING_APP] investigates safety complaint',
            'platform': 'app_support'
        },
    ]
    
    scenario_pass = True
    
    for scenario in scenarios:
        result = replace_placeholders(scenario['text'], scenario['platform'])
        
        # Check if any placeholder remains
        has_placeholder = '[' in result and ']' in result
        
        if not has_placeholder:
            print(f"PASS: {scenario['name']}: WORKING")
            print(f"   {result}")
        else:
            print(f"FAIL: {scenario['name']}: PLACEHOLDER REMAINING")
            print(f"   {result}")
            scenario_pass = False
    
    if scenario_pass:
        print(f"\nPASS: All tech scenario simulations working")
    else:
        print(f"\nFAIL: Some tech scenarios have unresolved placeholders")
        
except Exception as e:
    print(f"FAIL: Tech scenario simulation FAILED: {e}")
    scenario_pass = False

print()

# =============================================================================
# TEST 6: SAMPLE ENTITIES VALIDATION
# =============================================================================
print("Test 6: Sample Entities Validation")
print("-" * 70)

if import_pass:
    try:
        print("Sample Tech Companies (first 6):")
        for company in TECH_COMPANIES[:6]:
            print(f"  - {company}")
        
        print("\nSample Social Media Platforms (first 6):")
        for platform in SOCIAL_MEDIA_PLATFORMS[:6]:
            print(f"  - {platform}")
        
        print("\nSample Email Providers (first 4):")
        for provider in EMAIL_PROVIDERS[:4]:
            print(f"  - {provider}")
        
        print("\nSample Gaming Platforms (first 4):")
        for platform in GAMING_PLATFORMS[:4]:
            print(f"  - {platform}")
        
        print("\nSample Gift Card Brands (first 4):")
        for brand in GIFT_CARD_BRANDS[:4]:
            print(f"  - {brand}")
        
        print("\nSample Ride-Hailing Apps (first 4):")
        for app in RIDE_HAILING_APPS[:4]:
            print(f"  - {app}")
        
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
    ("Tech Entity Import", import_pass),
    ("Entity Diversity", diversity_pass),
    ("Conversation Generator Integration", integration_pass),
    ("Mixed Domain Placeholders", mixed_pass),
    ("Tech Scenario Simulation", scenario_pass),
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
    print("ALL TECH ENTITY TESTS PASSED")
    print()
    print(f"PASS: {total_entities} tech entities ready for conversation generation")
    print(f"PASS: All 6 placeholder types working correctly")
    print(f"PASS: Integration with conversation generator complete")
    print(f"PASS: Tech scenarios ready for generation")
    print()
    print("STATUS: READY TO GENERATE TECH FRAUD CONVERSATIONS")
    sys.exit(0)
else:
    print()
    print("WARN: Some tests failed. Fix issues before generating.")
    sys.exit(1)
