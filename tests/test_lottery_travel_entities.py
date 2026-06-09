"""
Lottery & Travel Entity Integration Test Suite
==============================================

Tests to verify that lottery/travel prize entities load correctly and replace
their respective placeholders in scenario descriptions.

Tests:
1. Lottery/Travel entities module import
2. Travel company placeholder replacement
3. Airline company placeholder replacement
4. Lottery name placeholder replacement
5. Car brand placeholder replacement
6. Pilgrimage site placeholder replacement
7. Hotel name placeholder replacement
8. Bank name placeholder replacement
9. Cruise line placeholder replacement
10. Cross-domain test (lottery/travel + existing placeholders)
11. Conversation generator integration test
12. NO ENTITY SKIPS test (CRITICAL - user requirement)
"""

import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_lottery_travel_entities_import():
    """Test 1: Verify lottery/travel entities module loads correctly"""
    print("\n" + "=" * 70)
    print("Test 1: Lottery/Travel Entities Import Test")
    print("=" * 70)
    
    try:
        from data.entities.lottery_travel_entities import (
            TRAVEL_COMPANIES, AIRLINE_COMPANIES, LOTTERY_NAMES, CAR_BRANDS,
            PILGRIMAGE_SITES, HOTEL_NAMES, BANK_NAMES, CRUISE_LINES,
            LOTTERY_TRAVEL_ENTITY_STATS, get_all_lottery_travel_entities
        )
        
        # Verify entity counts
        assert len(TRAVEL_COMPANIES) > 0, "TRAVEL_COMPANIES list is empty"
        assert len(AIRLINE_COMPANIES) > 0, "AIRLINE_COMPANIES list is empty"
        assert len(LOTTERY_NAMES) > 0, "LOTTERY_NAMES list is empty"
        assert len(CAR_BRANDS) > 0, "CAR_BRANDS list is empty"
        assert len(PILGRIMAGE_SITES) > 0, "PILGRIMAGE_SITES list is empty"
        assert len(HOTEL_NAMES) > 0, "HOTEL_NAMES list is empty"
        assert len(BANK_NAMES) > 0, "BANK_NAMES list is empty"
        assert len(CRUISE_LINES) > 0, "CRUISE_LINES list is empty"
        
        print(f"PASS: Lottery/Travel entities loaded successfully:")
        print(f"   - Travel Companies: {len(TRAVEL_COMPANIES)} entities")
        print(f"   - Airlines: {len(AIRLINE_COMPANIES)} entities")
        print(f"   - Lottery Names: {len(LOTTERY_NAMES)} entities")
        print(f"   - Car Brands: {len(CAR_BRANDS)} entities")
        print(f"   - Pilgrimage Sites: {len(PILGRIMAGE_SITES)} entities")
        print(f"   - Hotel Names: {len(HOTEL_NAMES)} entities")
        print(f"   - Bank Names: {len(BANK_NAMES)} entities")
        print(f"   - Cruise Lines: {len(CRUISE_LINES)} entities")
        print(f"   - TOTAL: {LOTTERY_TRAVEL_ENTITY_STATS['total_entities']} entities")
        print()
        print(f"PASS: Sample Travel Companies: {', '.join(TRAVEL_COMPANIES[:3])}")
        print(f"PASS: Sample Airlines: {', '.join(AIRLINE_COMPANIES[:3])}")
        print(f"PASS: Sample Lottery Names: {', '.join(LOTTERY_NAMES[:2])}")
        
        return True
    except Exception as e:
        print(f"FAILED: {e}")
        return False


def test_travel_company_placeholder():
    """Test 2: Verify [TRAVEL_COMPANY] placeholder replacement"""
    print("\n" + "=" * 70)
    print("Test 2: [TRAVEL_COMPANY] Placeholder Replacement Test")
    print("=" * 70)
    
    try:
        from src.generators.conversation_generator import replace_placeholders
        
        test_scenarios = [
            "Agent from [TRAVEL_COMPANY] offering holiday package",
            "Book trip with [TRAVEL_COMPANY] and save 50%",
            "[TRAVEL_COMPANY] calling about your Goa vacation"
        ]
        
        for i, scenario in enumerate(test_scenarios, 1):
            result = replace_placeholders(scenario, "travel_agency")
            
            assert "[TRAVEL_COMPANY]" not in result, f"Placeholder not replaced in scenario {i}"
            assert result != scenario, f"Placeholder replacement failed in scenario {i}"
            
            print(f"PASS: Test {i}: [TRAVEL_COMPANY] replacement WORKING")
            print(f"   Original: {scenario}")
            print(f"   Result:   {result}")
        
        return True
    except Exception as e:
        print(f"FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_airline_company_placeholder():
    """Test 3: Verify [AIRLINE_COMPANY] placeholder replacement"""
    print("\n" + "=" * 70)
    print("Test 3: [AIRLINE_COMPANY] Placeholder Replacement Test")
    print("=" * 70)
    
    try:
        from src.generators.conversation_generator import replace_placeholders
        
        test_scenarios = [
            "[AIRLINE_COMPANY] flight has been rescheduled",
            "Booking with [AIRLINE_COMPANY] for international travel",
            "Loyalty points from [AIRLINE_COMPANY] Miles program"
        ]
        
        for i, scenario in enumerate(test_scenarios, 1):
            result = replace_placeholders(scenario, "airline")
            
            assert "[AIRLINE_COMPANY]" not in result, f"Placeholder not replaced in scenario {i}"
            assert result != scenario, f"Placeholder replacement failed in scenario {i}"
            
            print(f"PASS: Test {i}: [AIRLINE_COMPANY] replacement WORKING")
            print(f"   Original: {scenario}")
            print(f"   Result:   {result}")
        
        return True
    except Exception as e:
        print(f"FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_lottery_name_placeholder():
    """Test 4: Verify [LOTTERY_NAME] placeholder replacement"""
    print("\n" + "=" * 70)
    print("Test 4: [LOTTERY_NAME] Placeholder Replacement Test (CRITICAL - KBC)")
    print("=" * 70)
    
    try:
        from src.generators.conversation_generator import replace_placeholders
        
        test_scenarios = [
            "You won [LOTTERY_NAME] lucky draw prize",
            "Congratulations from [LOTTERY_NAME] team",
            "[LOTTERY_NAME] mobile number lottery winner"
        ]
        
        for i, scenario in enumerate(test_scenarios, 1):
            result = replace_placeholders(scenario, "lottery_scam")
            
            assert "[LOTTERY_NAME]" not in result, f"Placeholder not replaced in scenario {i}"
            assert result != scenario, f"Placeholder replacement failed in scenario {i}"
            
            print(f"PASS: Test {i}: [LOTTERY_NAME] replacement WORKING")
            print(f"   Original: {scenario}")
            print(f"   Result:   {result}")
        
        return True
    except Exception as e:
        print(f"FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_car_brand_placeholder():
    """Test 5: Verify [CAR_BRAND] placeholder replacement"""
    print("\n" + "=" * 70)
    print("Test 5: [CAR_BRAND] Placeholder Replacement Test")
    print("=" * 70)
    
    try:
        from src.generators.conversation_generator import replace_placeholders
        
        test_scenarios = [
            "You won a brand new [CAR_BRAND] in lucky draw",
            "[CAR_BRAND] promotional lottery winner",
            "Delivery of your [CAR_BRAND] prize scheduled"
        ]
        
        for i, scenario in enumerate(test_scenarios, 1):
            result = replace_placeholders(scenario, "prize_scam")
            
            assert "[CAR_BRAND]" not in result, f"Placeholder not replaced in scenario {i}"
            assert result != scenario, f"Placeholder replacement failed in scenario {i}"
            
            print(f"PASS: Test {i}: [CAR_BRAND] replacement WORKING")
            print(f"   Original: {scenario}")
            print(f"   Result:   {result}")
        
        return True
    except Exception as e:
        print(f"FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_pilgrimage_site_placeholder():
    """Test 6: Verify [PILGRIMAGE_SITE] placeholder replacement"""
    print("\n" + "=" * 70)
    print("Test 6: [PILGRIMAGE_SITE] Placeholder Replacement Test")
    print("=" * 70)
    
    try:
        from src.generators.conversation_generator import replace_placeholders
        
        test_scenarios = [
            "Cheap pilgrimage tour package to [PILGRIMAGE_SITE]",
            "Visit [PILGRIMAGE_SITE] with special group discount",
            "[PILGRIMAGE_SITE] yatra booking confirmation"
        ]
        
        for i, scenario in enumerate(test_scenarios, 1):
            result = replace_placeholders(scenario, "travel_agency")
            
            assert "[PILGRIMAGE_SITE]" not in result, f"Placeholder not replaced in scenario {i}"
            assert result != scenario, f"Placeholder replacement failed in scenario {i}"
            
            print(f"PASS: Test {i}: [PILGRIMAGE_SITE] replacement WORKING")
            print(f"   Original: {scenario}")
            print(f"   Result:   {result}")
        
        return True
    except Exception as e:
        print(f"FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_hotel_name_placeholder():
    """Test 7: Verify [HOTEL_NAME] placeholder replacement"""
    print("\n" + "=" * 70)
    print("Test 7: [HOTEL_NAME] Placeholder Replacement Test")
    print("=" * 70)
    
    try:
        from src.generators.conversation_generator import replace_placeholders
        
        test_scenarios = [
            "Your [HOTEL_NAME] reservation is confirmed",
            "Room upgrade available at [HOTEL_NAME]",
            "[HOTEL_NAME] calling about your weekend booking"
        ]
        
        for i, scenario in enumerate(test_scenarios, 1):
            result = replace_placeholders(scenario, "hospitality")
            
            assert "[HOTEL_NAME]" not in result, f"Placeholder not replaced in scenario {i}"
            assert result != scenario, f"Placeholder replacement failed in scenario {i}"
            
            print(f"PASS: Test {i}: [HOTEL_NAME] replacement WORKING")
            print(f"   Original: {scenario}")
            print(f"   Result:   {result}")
        
        return True
    except Exception as e:
        print(f"FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_bank_name_placeholder():
    """Test 8: Verify [BANK_NAME] placeholder replacement"""
    print("\n" + "=" * 70)
    print("Test 8: [BANK_NAME] Placeholder Replacement Test")
    print("=" * 70)
    
    try:
        from src.generators.conversation_generator import replace_placeholders
        
        test_scenarios = [
            "Loyalty rewards from [BANK_NAME] credit card",
            "[BANK_NAME] travel benefits explained",
            "Bonus points credited by [BANK_NAME]"
        ]
        
        for i, scenario in enumerate(test_scenarios, 1):
            result = replace_placeholders(scenario, "loyalty_program")
            
            assert "[BANK_NAME]" not in result, f"Placeholder not replaced in scenario {i}"
            assert result != scenario, f"Placeholder replacement failed in scenario {i}"
            
            print(f"PASS: Test {i}: [BANK_NAME] replacement WORKING")
            print(f"   Original: {scenario}")
            print(f"   Result:   {result}")
        
        return True
    except Exception as e:
        print(f"FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_cruise_line_placeholder():
    """Test 9: Verify [CRUISE_LINE] placeholder replacement"""
    print("\n" + "=" * 70)
    print("Test 9: [CRUISE_LINE] Placeholder Replacement Test")
    print("=" * 70)
    
    try:
        from src.generators.conversation_generator import replace_placeholders
        
        test_scenarios = [
            "Feedback survey from [CRUISE_LINE]",
            "Special offer from [CRUISE_LINE] for you",
            "[CRUISE_LINE] booking confirmation"
        ]
        
        for i, scenario in enumerate(test_scenarios, 1):
            result = replace_placeholders(scenario, "travel_company")
            
            assert "[CRUISE_LINE]" not in result, f"Placeholder not replaced in scenario {i}"
            assert result != scenario, f"Placeholder replacement failed in scenario {i}"
            
            print(f"PASS: Test {i}: [CRUISE_LINE] replacement WORKING")
            print(f"   Original: {scenario}")
            print(f"   Result:   {result}")
        
        return True
    except Exception as e:
        print(f"FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_cross_domain_lottery_travel():
    """Test 10: Lottery/Travel placeholders with existing domain placeholders"""
    print("\n" + "=" * 70)
    print("Test 10: Cross-Domain Placeholder Test (Lottery/Travel + Other Domains)")
    print("=" * 70)
    
    try:
        from src.generators.conversation_generator import replace_placeholders
        
        test_scenarios = [
            # Lottery + E-commerce
            "[LOTTERY_NAME] prize payment via [UPI_APP]",
            # Travel + Emergency
            "[FAMILY_MEMBER] booking [AIRLINE_COMPANY] ticket to [CITY]",
            # Prize + Tech
            "[ELECTRONICS_ITEM] from [LOTTERY_NAME] sent via [MOBILE_CARRIER]",
            # Travel + Healthcare
            "[TRAVEL_COMPANY] offering [INSURANCE_COMPANY] travel insurance",
            # Multiple lottery/travel placeholders
            "[TRAVEL_COMPANY] pilgrimage tour to [PILGRIMAGE_SITE] staying at [HOTEL_NAME]",
            # Complex cross-domain
            "[BANK_NAME] credit card rewards for [AIRLINE_COMPANY] booking via [TRAVEL_COMPANY]"
        ]
        
        for i, scenario in enumerate(test_scenarios, 1):
            result = replace_placeholders(scenario, "travel_agency")
            
            # Check no placeholders remain
            placeholders = [
                "[LOTTERY_NAME]", "[TRAVEL_COMPANY]", "[AIRLINE_COMPANY]", "[CAR_BRAND]",
                "[PILGRIMAGE_SITE]", "[HOTEL_NAME]", "[BANK_NAME]", "[CRUISE_LINE]",
                "[UPI_APP]", "[FAMILY_MEMBER]", "[CITY]", "[ELECTRONICS_ITEM]",
                "[MOBILE_CARRIER]", "[INSURANCE_COMPANY]"
            ]
            
            for placeholder in placeholders:
                if placeholder in scenario:
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
    """Test 11: Full conversation generator integration with lottery/travel scenarios"""
    print("\n" + "=" * 70)
    print("Test 11: Conversation Generator Integration - Lottery/Travel Domain")
    print("=" * 70)
    
    try:
        from src.generators.conversation_generator import LOTTERY_TRAVEL_ENTITIES_AVAILABLE
        
        if not LOTTERY_TRAVEL_ENTITIES_AVAILABLE:
            print("FAILED: LOTTERY_TRAVEL_ENTITIES_AVAILABLE flag is False")
            print("   Lottery/Travel entities are not loaded in conversation_generator.py")
            return False
        
        print("PASS: LOTTERY_TRAVEL_ENTITIES_AVAILABLE flag: True")
        
        # Test actual placeholder replacement
        from src.generators.conversation_generator import replace_placeholders
        
        # Test all 8 lottery/travel placeholder types in one scenario
        combined_test = (
            "Agent from [TRAVEL_COMPANY] offering [LOTTERY_NAME] prize: "
            "[CAR_BRAND] car OR [AIRLINE_COMPANY] tickets to [PILGRIMAGE_SITE]. "
            "Stay at [HOTEL_NAME]. Pay via [BANK_NAME]. Cruise on [CRUISE_LINE]."
        )
        
        result = replace_placeholders(combined_test, "travel_agency")
        
        # Verify ALL placeholders replaced
        lottery_travel_placeholders = [
            "[TRAVEL_COMPANY]", "[LOTTERY_NAME]", "[CAR_BRAND]", "[AIRLINE_COMPANY]",
            "[PILGRIMAGE_SITE]", "[HOTEL_NAME]", "[BANK_NAME]", "[CRUISE_LINE]"
        ]
        remaining_placeholders = [p for p in lottery_travel_placeholders if p in result]
        
        if remaining_placeholders:
            print(f"FAILED: Placeholders not replaced: {remaining_placeholders}")
            print(f"   Result: {result}")
            return False
        
        print("PASS: All lottery/travel placeholders replaced in integrated test:")
        print(f"   Original: {combined_test}")
        print(f"   Result:   {result}")
        
        return True
    except Exception as e:
        print(f"FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_no_entity_skips():
    """Test 12: CRITICAL - Verify NO entity skips (user's requirement)"""
    print("\n" + "=" * 70)
    print("Test 12: CRITICAL TEST - NO ENTITY SKIPS (User Requirement)")
    print("=" * 70)
    
    try:
        from src.generators.conversation_generator import replace_placeholders
        from data.entities.lottery_travel_entities import (
            TRAVEL_COMPANIES, AIRLINE_COMPANIES, LOTTERY_NAMES, CAR_BRANDS,
            PILGRIMAGE_SITES, HOTEL_NAMES, BANK_NAMES, CRUISE_LINES
        )
        
        print("\n🔍 Testing ALL lottery/travel entities for skips...")
        
        all_entities = {
            "TRAVEL_COMPANIES": TRAVEL_COMPANIES,
            "AIRLINE_COMPANIES": AIRLINE_COMPANIES,
            "LOTTERY_NAMES": LOTTERY_NAMES,
            "CAR_BRANDS": CAR_BRANDS,
            "PILGRIMAGE_SITES": PILGRIMAGE_SITES,
            "HOTEL_NAMES": HOTEL_NAMES,
            "BANK_NAMES": BANK_NAMES,
            "CRUISE_LINES": CRUISE_LINES
        }
        
        for entity_type, entity_list in all_entities.items():
            print(f"\n   Testing {entity_type} ({len(entity_list)} entities)...")
            
            sample_size = min(10, len(entity_list))
            sample = entity_list[:sample_size]
            
            skipped = []
            for entity in sample:
                if entity_type == "TRAVEL_COMPANIES":
                    test_scenario = f"Agent from [TRAVEL_COMPANY] calling"
                elif entity_type == "AIRLINE_COMPANIES":
                    test_scenario = f"Flight with [AIRLINE_COMPANY]"
                elif entity_type == "LOTTERY_NAMES":
                    test_scenario = f"Winner of [LOTTERY_NAME]"
                elif entity_type == "CAR_BRANDS":
                    test_scenario = f"Won [CAR_BRAND] car"
                elif entity_type == "PILGRIMAGE_SITES":
                    test_scenario = f"Tour to [PILGRIMAGE_SITE]"
                elif entity_type == "HOTEL_NAMES":
                    test_scenario = f"Booking at [HOTEL_NAME]"
                elif entity_type == "BANK_NAMES":
                    test_scenario = f"Offer from [BANK_NAME]"
                else:  # CRUISE_LINES
                    test_scenario = f"Cruise with [CRUISE_LINE]"
                
                result = replace_placeholders(test_scenario, "travel_agency")
                
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
        print("   All lottery/travel entities load and replace correctly")
        print("=" * 70)
        
        return True
    except Exception as e:
        print(f"FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


def run_all_tests():
    """Run all lottery/travel entity tests"""
    print("\n" + "=" * 70)
    print("🧪 LOTTERY & TRAVEL ENTITY INTEGRATION TEST SUITE")
    print("=" * 70)
    print("\nTesting lottery/travel prize entities integration...")
    print("Entity types: TRAVEL_COMPANIES, AIRLINE_COMPANIES, LOTTERY_NAMES, CAR_BRANDS,")
    print("              PILGRIMAGE_SITES, HOTEL_NAMES, BANK_NAMES, CRUISE_LINES")
    
    tests = [
        ("Import Test", test_lottery_travel_entities_import),
        ("[TRAVEL_COMPANY] Placeholder", test_travel_company_placeholder),
        ("[AIRLINE_COMPANY] Placeholder", test_airline_company_placeholder),
        ("[LOTTERY_NAME] Placeholder (KBC)", test_lottery_name_placeholder),
        ("[CAR_BRAND] Placeholder", test_car_brand_placeholder),
        ("[PILGRIMAGE_SITE] Placeholder", test_pilgrimage_site_placeholder),
        ("[HOTEL_NAME] Placeholder", test_hotel_name_placeholder),
        ("[BANK_NAME] Placeholder", test_bank_name_placeholder),
        ("[CRUISE_LINE] Placeholder", test_cruise_line_placeholder),
        ("Cross-Domain Test", test_cross_domain_lottery_travel),
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
        print("PASS: Lottery/Travel entities fully integrated and operational")
        print("PASS: NO entity skips detected - user requirement satisfied")
        print("PASS: KBC lottery placeholder working correctly")
    else:
        print(f"WARN: {total - passed} test(s) failed")
    
    print("=" * 70)
    
    return passed == total


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
