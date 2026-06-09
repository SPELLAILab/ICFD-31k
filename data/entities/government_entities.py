"""
Government Department & Law Enforcement Entities for Fraud Detection Training Data

This module contains realistic Indian government departments, ministries, regulatory bodies,
and law enforcement agencies used for government impersonation fraud scenarios.

Usage in scenarios:
- [GOVERNMENT_DEPT] → Random government department/ministry/agency
"""

# ============================================================================
# GOVERNMENT DEPARTMENTS, MINISTRIES & AGENCIES (40 entities)
# ============================================================================

GOVERNMENT_DEPT = [
    # Central Government Ministries (Major)
    "Ministry of Home Affairs",
    "Ministry of Finance",
    "Ministry of Health and Family Welfare",
    "Ministry of Education",
    "Ministry of Agriculture and Farmers Welfare",
    "Ministry of Electronics and Information Technology (MeitY)",
    "Ministry of Railways",
    "Ministry of Road Transport and Highways",
    "Ministry of Labour and Employment",
    "Ministry of External Affairs",
    "Ministry of Defence",
    "Ministry of Communications",
    "Ministry of Consumer Affairs, Food and Public Distribution",
    "Ministry of Rural Development",
    "Ministry of Women and Child Development",
    
    # Tax & Revenue Departments (Critical for Fraud)
    "Income Tax Department",
    "Goods and Services Tax (GST) Department",
    "Central Board of Direct Taxes (CBDT)",
    "Central Board of Indirect Taxes and Customs (CBIC)",
    "Enforcement Directorate (ED)",
    
    # Law Enforcement & Security
    "Central Bureau of Investigation (CBI)",
    "Indian Cyber Crime Coordination Centre (I4C)",
    "Cybercrime Cell",
    "Economic Offences Wing (EOW)",
    "Narcotics Control Bureau (NCB)",
    
    # Identity & Authentication Bodies
    "Unique Identification Authority of India (UIDAI)",
    "Passport Seva Kendra (PSK)",
    "Regional Transport Office (RTO)",
    "Election Commission of India",
    
    # Financial Regulatory Bodies
    "Reserve Bank of India (RBI)",
    "Securities and Exchange Board of India (SEBI)",
    "Insurance Regulatory and Development Authority of India (IRDAI)",
    "Pension Fund Regulatory and Development Authority (PFRDA)",
    
    # Consumer & Telecom Regulatory Bodies
    "Telecom Regulatory Authority of India (TRAI)",
    "Food Safety and Standards Authority of India (FSSAI)",
    "Consumer Protection Authority",
    
    # State & Municipal Bodies (Common)
    "State Transport Department",
    "Municipal Corporation",
    "District Administration Office",
    "Public Works Department (PWD)",
]

# ============================================================================
# ENTITY STATISTICS
# ============================================================================

ENTITY_COUNTS = {
    "GOVERNMENT_DEPT": len(GOVERNMENT_DEPT),
}

TOTAL_ENTITIES = sum(ENTITY_COUNTS.values())

# ============================================================================
# USAGE INFORMATION
# ============================================================================

"""
PLACEHOLDER MAPPING:
-------------------
[GOVERNMENT_DEPT] → GOVERNMENT_DEPT

ENTITY COUNTS:
--------------
Government Departments/Ministries/Agencies: 40 entities

TOTAL: 40 entities

CRITICAL NOTES:
---------------
1. Mix of central ministries, tax departments, law enforcement, regulatory bodies
2. Includes high-fraud-risk departments: Income Tax, GST, Cyber Crime, UIDAI, RTO
3. State/municipal bodies included for local government impersonation scenarios
4. Focus on departments commonly impersonated in scams
5. All departments are real, verifiable entities to maintain realism

INTEGRATION STATUS:
-------------------
This is the SIMPLEST entity integration:
- Only 1 new entity type required (GOVERNMENT_DEPT)
- All other placeholders already exist from previous batches:
  * [CITY] from emergency_entities.py
  * [UPI_APP] from ecommerce_entities.py
  * [GOVERNMENT_SCHEME] from healthcare_entities.py
  * [HOSPITAL_NAME] from emergency_entities.py
  * [GIFT_CARD_BRAND] from tech_entities.py
  * [BANK_NAME] from lottery_travel_entities.py

This demonstrates exceptional cross-domain integration!

USAGE EXAMPLE:
--------------
from data.government_entities import GOVERNMENT_DEPT
import random

# Replace [GOVERNMENT_DEPT] placeholder
govt_dept = random.choice(GOVERNMENT_DEPT)
text = f"This call is from the {govt_dept}."
# Output: "This call is from the Income Tax Department."
"""

if __name__ == "__main__":
    print("=" * 80)
    print("GOVERNMENT ENTITIES - LOADED SUCCESSFULLY")
    print("=" * 80)
    print(f"\nTotal Entities: {TOTAL_ENTITIES}")
    print("\nEntity Breakdown:")
    for entity_type, count in ENTITY_COUNTS.items():
        print(f"  - {entity_type}: {count} entities")
    
    print("\n" + "=" * 80)
    print("SAMPLE ENTITIES:")
    print("=" * 80)
    
    print(f"\n[GOVERNMENT_DEPT] samples (40 total):")
    print("  Central Ministries:")
    for dept in GOVERNMENT_DEPT[:5]:
        print(f"    • {dept}")
    print("\n  Tax & Revenue:")
    for dept in GOVERNMENT_DEPT[15:20]:
        print(f"    • {dept}")
    print("\n  Law Enforcement:")
    for dept in GOVERNMENT_DEPT[20:25]:
        print(f"    • {dept}")
    print("\n  Identity & Auth:")
    for dept in GOVERNMENT_DEPT[25:29]:
        print(f"    • {dept}")
    print("\n  Financial Regulatory:")
    for dept in GOVERNMENT_DEPT[29:33]:
        print(f"    • {dept}")
    print("\n  Consumer & Telecom:")
    for dept in GOVERNMENT_DEPT[33:36]:
        print(f"    • {dept}")
    print("\n  State & Municipal:")
    for dept in GOVERNMENT_DEPT[36:40]:
        print(f"    • {dept}")
    
    print("\n" + "=" * 80)
    print("INTEGRATION NOTE:")
    print("=" * 80)
    print("✅ ONLY 1 NEW ENTITY TYPE REQUIRED!")
    print("✅ All other placeholders already exist from previous batches")
    print("✅ This is the EASIEST and MOST INTEGRATED domain integration yet!")
    print("=" * 80)
