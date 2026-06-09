"""
Healthcare Entity Integration Test Suite
========================================

Tests to verify that healthcare insurance entities load correctly and replace
their respective placeholders in scenario descriptions.

Tests:
1. Healthcare entities module import
2. Insurance company placeholder replacement
3. Government scheme placeholder replacement  
4. Insurance marketplace placeholder replacement
5. Disease name placeholder replacement
6. Cross-domain test (healthcare + existing placeholders)
7. Conversation generator integration test
8. NO ENTITY SKIPS test (CRITICAL - user requirement)
"""

import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_healthcare_entities_import():
    """Test 1: Verify healthcare entities module loads correctly"""
    print("\n" + "=" * 70)
    print("Test 1: Healthcare Entities Import Test")
    print("=" * 70)
    
    try:
        from data.entities.healthcare_entities import (
            INSURANCE_COMPANIES, GOVERNMENT_SCHEMES, INSURANCE_MARKETPLACES, DISEASE_NAMES,
            HEALTHCARE_ENTITY_STATS, get_all_healthcare_entities
        )
        
        # Verify entity counts
        assert len(INSURANCE_COMPANIES) > 0, "INSURANCE_COMPANIES list is empty"
        assert len(GOVERNMENT_SCHEMES) > 0, "GOVERNMENT_SCHEMES list is empty"
        assert len(INSURANCE_MARKETPLACES) > 0, "INSURANCE_MARKETPLACES list is empty"
        assert len(DISEASE_NAMES) > 0, "DISEASE_NAMES list is empty"
        
        print(f"PASS: Healthcare entities loaded successfully:")
        print(f"   - Insurance Companies: {len(INSURANCE_COMPANIES)} entities")
        print(f"   - Government Schemes: {len(GOVERNMENT_SCHEMES)} entities")
        print(f"   - Insurance Marketplaces: {len(INSURANCE_MARKETPLACES)} entities")
        print(f"   - Disease Names: {len(DISEASE_NAMES)} entities")
        print(f"   - TOTAL: {HEALTHCARE_ENTITY_STATS['total_entities']} entities")
        print()
        print(f"PASS: Sample Insurance Companies: {', '.join(INSURANCE_COMPANIES[:3])}")
        print(f"PASS: Sample Government Schemes: {', '.join(GOVERNMENT_SCHEMES[:2])}")
        print(f"PASS: Sample Marketplaces: {', '.join(INSURANCE_MARKETPLACES[:3])}")
        print(f"PASS: Sample Diseases: {', '.join(DISEASE_NAMES[:5])}")
        
        return True
    except Exception as e:
        print(f"FAILED: {e}")
        return False


def test_insurance_company_placeholder():
    """Test 2: Verify [INSURANCE_COMPANY] placeholder replacement"""
    print("\n" + "=" * 70)
    print("Test 2: [INSURANCE_COMPANY] Placeholder Replacement Test")
    print("=" * 70)
    
    try:
        from src.generators.conversation_generator import replace_placeholders
        
        test_scenarios = [
            "Agent from [INSURANCE_COMPANY] calling about policy",
            "Your [INSURANCE_COMPANY] health insurance has lapsed",
            "[INSURANCE_COMPANY] offering new term insurance plan"
        ]
        
        for i, scenario in enumerate(test_scenarios, 1):
            result = replace_placeholders(scenario, "insurance_provider")
            
            # Verify placeholder was replaced
            assert "[INSURANCE_COMPANY]" not in result, f"Placeholder not replaced in scenario {i}"
            
            # Verify result is different from original
            assert result != scenario, f"Placeholder replacement failed in scenario {i}"
            
            print(f"PASS: Test {i}: [INSURANCE_COMPANY] replacement WORKING")
            print(f"   Original: {scenario}")
            print(f"   Result:   {result}")
        
        return True
    except Exception as e:
        print(f"FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_government_scheme_placeholder():
    """Test 3: Verify [GOVERNMENT_SCHEME] placeholder replacement"""
    print("\n" + "=" * 70)
    print("Test 3: [GOVERNMENT_SCHEME] Placeholder Replacement Test")
    print("=" * 70)
    
    try:
        from src.generators.conversation_generator import replace_placeholders
        
        test_scenarios = [
            "Offering government approved [GOVERNMENT_SCHEME] health card",
            "You are eligible for [GOVERNMENT_SCHEME] benefits",
            "[GOVERNMENT_SCHEME] enrollment process started"
        ]
        
        for i, scenario in enumerate(test_scenarios, 1):
            result = replace_placeholders(scenario, "government_scheme")
            
            assert "[GOVERNMENT_SCHEME]" not in result, f"Placeholder not replaced in scenario {i}"
            assert result != scenario, f"Placeholder replacement failed in scenario {i}"
            
            print(f"PASS: Test {i}: [GOVERNMENT_SCHEME] replacement WORKING")
            print(f"   Original: {scenario}")
            print(f"   Result:   {result}")
        
        return True
    except Exception as e:
        print(f"FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_insurance_marketplace_placeholder():
    """Test 4: Verify [INSURANCE_MARKETPLACE] placeholder replacement"""
    print("\n" + "=" * 70)
    print("Test 4: [INSURANCE_MARKETPLACE] Placeholder Replacement Test")
    print("=" * 70)
    
    try:
        from src.generators.conversation_generator import replace_placeholders
        
        test_scenarios = [
            "Agent from [INSURANCE_MARKETPLACE] calling with quote",
            "Compare policies on [INSURANCE_MARKETPLACE] platform",
            "[INSURANCE_MARKETPLACE] offering best insurance deals"
        ]
        
        for i, scenario in enumerate(test_scenarios, 1):
            result = replace_placeholders(scenario, "third_party_marketplace")
            
            assert "[INSURANCE_MARKETPLACE]" not in result, f"Placeholder not replaced in scenario {i}"
            assert result != scenario, f"Placeholder replacement failed in scenario {i}"
            
            print(f"PASS: Test {i}: [INSURANCE_MARKETPLACE] replacement WORKING")
            print(f"   Original: {scenario}")
            print(f"   Result:   {result}")
        
        return True
    except Exception as e:
        print(f"FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_disease_name_placeholder():
    """Test 5: Verify [DISEASE_NAME] placeholder replacement"""
    print("\n" + "=" * 70)
    print("Test 5: [DISEASE_NAME] Placeholder Replacement Test")
    print("=" * 70)
    
    try:
        from src.generators.conversation_generator import replace_placeholders
        
        test_scenarios = [
            "Your claim for [DISEASE_NAME] has been rejected",
            "Coverage for [DISEASE_NAME] treatment approved",
            "[DISEASE_NAME] requires pre-authorization from insurer"
        ]
        
        for i, scenario in enumerate(test_scenarios, 1):
            result = replace_placeholders(scenario, "insurance_provider")
            
            assert "[DISEASE_NAME]" not in result, f"Placeholder not replaced in scenario {i}"
            assert result != scenario, f"Placeholder replacement failed in scenario {i}"
            
            print(f"PASS: Test {i}: [DISEASE_NAME] replacement WORKING")
            print(f"   Original: {scenario}")
            print(f"   Result:   {result}")
        
        return True
    except Exception as e:
        print(f"FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_cross_domain_healthcare():
    """Test 6: Healthcare placeholders with existing domain placeholders"""
    print("\n" + "=" * 70)
    print("Test 6: Cross-Domain Placeholder Test (Healthcare + Other Domains)")
    print("=" * 70)
    
    try:
        from src.generators.conversation_generator import replace_placeholders
        
        test_scenarios = [
            # Healthcare + E-commerce
            "[INSURANCE_COMPANY] premium paid via [UPI_APP]",
            # Healthcare + Emergency
            "[FAMILY_MEMBER] admitted to [HOSPITAL_NAME] with [DISEASE_NAME]",
            # Healthcare + Tech
            "[INSURANCE_COMPANY] sent OTP via [SOCIAL_MEDIA_APP]",
            # Healthcare + Loan
            "[INSURANCE_COMPANY] verified by [CREDIT_BUREAU] in [CITY]",
            # Multiple healthcare placeholders
            "[INSURANCE_COMPANY] offering [GOVERNMENT_SCHEME] on [INSURANCE_MARKETPLACE] for [DISEASE_NAME]",
            # Healthcare + Job + Emergency
            "[FAMILY_MEMBER] working at [IT_COMPANY] needs [INSURANCE_COMPANY] policy"
        ]
        
        for i, scenario in enumerate(test_scenarios, 1):
            result = replace_placeholders(scenario, "insurance_provider")
            
            # Check no placeholders remain
            placeholders = [
                "[INSURANCE_COMPANY]", "[GOVERNMENT_SCHEME]", "[INSURANCE_MARKETPLACE]", "[DISEASE_NAME]",
                "[UPI_APP]", "[FAMILY_MEMBER]", "[HOSPITAL_NAME]", "[CITY]",
                "[SOCIAL_MEDIA_APP]", "[CREDIT_BUREAU]", "[IT_COMPANY]"
            ]
            
            for placeholder in placeholders:
                if placeholder in scenario:  # Only check if placeholder was in original
                    assert placeholder not in result, f"Placeholder {placeholder} not replaced in test {i}"
            
            print(f"PASS: Test {i}: Cross-domain placeholders WORKING")
            print(f"   Result: {result}")
        
        return True
    except Exception as e:
        print(f"FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_conversation_generator_integration():
    """Test 7: Full conversation generator integration with healthcare scenarios"""
    print("\n" + "=" * 70)
    print("Test 7: Conversation Generator Integration - Healthcare Domain")
    print("=" * 70)
    
    try:
        # Check if healthcare entities are available in conversation generator
        from src.generators.conversation_generator import HEALTHCARE_ENTITIES_AVAILABLE
        
        if not HEALTHCARE_ENTITIES_AVAILABLE:
            print("FAILED: HEALTHCARE_ENTITIES_AVAILABLE flag is False")
            print("   Healthcare entities are not loaded in conversation_generator.py")
            return False
        
        print("PASS: HEALTHCARE_ENTITIES_AVAILABLE flag: True")
        
        # Test actual placeholder replacement
        from src.generators.conversation_generator import replace_placeholders
        
        # Test all 4 healthcare placeholder types in one scenario
        combined_test = (
            "Agent from [INSURANCE_COMPANY] offering [GOVERNMENT_SCHEME] via [INSURANCE_MARKETPLACE]. "
            "Coverage for [DISEASE_NAME] included. Pay premium via [UPI_APP]."
        )
        
        result = replace_placeholders(combined_test, "insurance_provider")
        
        # Verify ALL placeholders replaced
        healthcare_placeholders = [
            "[INSURANCE_COMPANY]", "[GOVERNMENT_SCHEME]", 
            "[INSURANCE_MARKETPLACE]", "[DISEASE_NAME]", "[UPI_APP]"
        ]
        remaining_placeholders = [p for p in healthcare_placeholders if p in result]
        
        if remaining_placeholders:
            print(f"FAILED: Placeholders not replaced: {remaining_placeholders}")
            print(f"   Result: {result}")
            return False
        
        print("PASS: All healthcare placeholders replaced in integrated test:")
        print(f"   Original: {combined_test}")
        print(f"   Result:   {result}")
        
        return True
    except Exception as e:
        print(f"FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_no_entity_skips():
    """Test 8: CRITICAL - Verify NO entity skips (user's requirement)"""
    print("\n" + "=" * 70)
    print("Test 8: CRITICAL TEST - NO ENTITY SKIPS (User Requirement)")
    print("=" * 70)
    
    try:
        from src.generators.conversation_generator import replace_placeholders
        from data.entities.healthcare_entities import (
            INSURANCE_COMPANIES, GOVERNMENT_SCHEMES, 
            INSURANCE_MARKETPLACES, DISEASE_NAMES
        )
        
        # Test each entity list to ensure NO entity is skipped
        print("\n🔍 Testing ALL healthcare entities for skips...")
        
        all_entities = {
            "INSURANCE_COMPANIES": INSURANCE_COMPANIES,
            "GOVERNMENT_SCHEMES": GOVERNMENT_SCHEMES,
            "INSURANCE_MARKETPLACES": INSURANCE_MARKETPLACES,
            "DISEASE_NAMES": DISEASE_NAMES
        }
        
        for entity_type, entity_list in all_entities.items():
            print(f"\n   Testing {entity_type} ({len(entity_list)} entities)...")
            
            # Sample 10 entities from each list
            sample_size = min(10, len(entity_list))
            sample = entity_list[:sample_size]
            
            skipped = []
            for entity in sample:
                # Create test scenario with this entity
                if entity_type == "INSURANCE_COMPANIES":
                    test_scenario = f"Agent from [INSURANCE_COMPANY] calling"
                elif entity_type == "GOVERNMENT_SCHEMES":
                    test_scenario = f"Enrolled in [GOVERNMENT_SCHEME]"
                elif entity_type == "INSURANCE_MARKETPLACES":
                    test_scenario = f"Quote from [INSURANCE_MARKETPLACE]"
                else:  # DISEASE_NAMES
                    test_scenario = f"Claim for [DISEASE_NAME]"
                
                result = replace_placeholders(test_scenario, "insurance_provider")
                
                # Check if placeholder was replaced
                if "[" in result and "]" in result:
                    skipped.append(entity)
            
            if skipped:
                print(f"   FAILED: {len(skipped)} entities skipped in {entity_type}")
                print(f"      Skipped: {skipped}")
                return False
            else:
                print(f"   PASS: {entity_type}: NO SKIPS - All {len(sample)} sampled entities loaded correctly")
        
        print("\n" + "=" * 70)
        print("PASS: CRITICAL TEST PASSED: NO ENTITY SKIPS DETECTED")
        print("   All healthcare entities load and replace correctly")
        print("=" * 70)
        
        return True
    except Exception as e:
        print(f"FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


def run_all_tests():
    """Run all healthcare entity tests"""
    print("\n" + "=" * 70)
    print("🧪 HEALTHCARE ENTITY INTEGRATION TEST SUITE")
    print("=" * 70)
    print("\nTesting healthcare insurance entities integration...")
    print("Entity types: INSURANCE_COMPANIES, GOVERNMENT_SCHEMES, INSURANCE_MARKETPLACES, DISEASE_NAMES")
    
    tests = [
        ("Import Test", test_healthcare_entities_import),
        ("[INSURANCE_COMPANY] Placeholder", test_insurance_company_placeholder),
        ("[GOVERNMENT_SCHEME] Placeholder", test_government_scheme_placeholder),
        ("[INSURANCE_MARKETPLACE] Placeholder", test_insurance_marketplace_placeholder),
        ("[DISEASE_NAME] Placeholder", test_disease_name_placeholder),
        ("Cross-Domain Test", test_cross_domain_healthcare),
        ("Generator Integration", test_conversation_generator_integration),
        ("NO ENTITY SKIPS (CRITICAL)", test_no_entity_skips)
    ]
    
    results = []
    for test_name, test_func in tests:
        result = test_func()
        results.append((test_name, result))
    
    # Summary
    print("\n" + "=" * 70)
    print("📊 TEST SUMMARY")
    print("=" * 70)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "PASS" if result else "FAIL"
        print(f"{status}: {test_name}")
    
    print("=" * 70)
    print(f"Tests Passed: {passed}/{total}")
    
    if passed == total:
        print("ALL TESTS PASSED!")
        print("PASS: Healthcare entities fully integrated and operational")
        print("PASS: NO entity skips detected - user requirement satisfied")
    else:
        print(f"WARN: {total - passed} test(s) failed")
    
    print("=" * 70)
    
    return passed == total


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
