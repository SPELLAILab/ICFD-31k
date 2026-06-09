"""
Healthcare Insurance Entity Lists
==================================

This module contains entity lists for healthcare and insurance fraud scenarios.
These entities cover insurance companies, government health schemes, insurance
marketplaces, and common disease names used in insurance claims.

Entity Categories:
- INSURANCE_COMPANIES: 59 major insurance providers (life, health, general)
- GOVERNMENT_SCHEMES: 12 government health/insurance schemes
- INSURANCE_MARKETPLACES: 10 third-party insurance aggregator platforms
- DISEASE_NAMES: 40 common medical conditions and procedures

Total Entities: 121
"""

# ============================================================================
# INSURANCE COMPANY ENTITIES (59 entities)
# ============================================================================
# Major insurance providers in India across life insurance, health insurance,
# and general insurance sectors. Includes both public and private companies.

INSURANCE_COMPANIES = [
    # Life Insurance Companies (Public)
    "Life Insurance Corporation of India (LIC)",
    "LIC of India",
    
    # Life Insurance Companies (Private)
    "HDFC Life Insurance",
    "ICICI Prudential Life Insurance",
    "SBI Life Insurance",
    "Max Life Insurance",
    "Bajaj Allianz Life Insurance",
    "Tata AIA Life Insurance",
    "Aditya Birla Sun Life Insurance",
    "Kotak Mahindra Life Insurance",
    "PNB MetLife Insurance",
    "Canara HSBC Oriental Bank of Commerce Life Insurance",
    "Bharti AXA Life Insurance",
    "Edelweiss Tokio Life Insurance",
    "Aegon Life Insurance",
    "IndiaFirst Life Insurance",
    "Aviva Life Insurance",
    "Exide Life Insurance",
    "Future Generali Life Insurance",
    "IDBI Federal Life Insurance",
    "Pramerica Life Insurance",
    "Reliance Nippon Life Insurance",
    "Sahara India Life Insurance",
    "Shriram Life Insurance",
    "Star Union Dai-ichi Life Insurance",
    
    # Health Insurance Companies
    "Star Health and Allied Insurance",
    "Care Health Insurance",
    "Niva Bupa Health Insurance",
    "Manipal Cigna Health Insurance",
    "Aditya Birla Health Insurance",
    "HDFC ERGO Health Insurance",
    "Max Bupa Health Insurance",
    "Religare Health Insurance",
    "Apollo Munich Health Insurance",
    "Cigna TTK Health Insurance",
    
    # General Insurance Companies (Public)
    "National Insurance Company",
    "The New India Assurance Company",
    "The Oriental Insurance Company",
    "United India Insurance Company",
    "Agriculture Insurance Company of India",
    
    # General Insurance Companies (Private)
    "ICICI Lombard General Insurance",
    "HDFC ERGO General Insurance",
    "Bajaj Allianz General Insurance",
    "Tata AIG General Insurance",
    "Cholamandalam MS General Insurance",
    "Reliance General Insurance",
    "Royal Sundaram General Insurance",
    "SBI General Insurance",
    "Future Generali India Insurance",
    "IFFCO Tokio General Insurance",
    "Kotak Mahindra General Insurance",
    "Liberty General Insurance",
    "Magma HDI General Insurance",
    "Raheja QBE General Insurance",
    "Shriram General Insurance",
    "Universal Sompo General Insurance",
    "Bharti AXA General Insurance",
    "Digit Insurance",
    "Go Digit General Insurance",
    "Acko General Insurance"
]

# ============================================================================
# GOVERNMENT HEALTH SCHEME ENTITIES (12 entities)
# ============================================================================
# Major government health insurance and social security schemes in India
# at central and state levels.

GOVERNMENT_SCHEMES = [
    # Central Government Schemes
    "Ayushman Bharat - Pradhan Mantri Jan Arogya Yojana (PM-JAY)",
    "Ayushman Bharat",
    "Pradhan Mantri Jeevan Jyoti Bima Yojana (PMJJBY)",
    "Pradhan Mantri Suraksha Bima Yojana (PMSBY)",
    "Atal Pension Yojana (APY)",
    "Employees' State Insurance Scheme (ESI)",
    "Central Government Health Scheme (CGHS)",
    "Rashtriya Swasthya Bima Yojana (RSBY)",
    
    # State Government Schemes
    "Rajiv Gandhi Jeevandayee Arogya Yojana (Maharashtra)",
    "Chief Minister's Comprehensive Health Insurance Scheme (Tamil Nadu)",
    "Bhamashah Swasthya Bima Yojana (Rajasthan)",
    "Mukhyamantri Amrutum Yojana (Gujarat)"
]

# ============================================================================
# INSURANCE MARKETPLACE ENTITIES (10 entities)
# ============================================================================
# Third-party insurance aggregator and comparison platforms where users
# can compare and purchase insurance policies online.

INSURANCE_MARKETPLACES = [
    "PolicyBazaar",
    "Coverfox",
    "BankBazaar Insurance",
    "Turtlemint",
    "RenewBuy",
    "InsuranceDekho",
    "EasyPolicy",
    "MyInsuranceClub",
    "Compare Policy",
    "Policyx.com"
]

# ============================================================================
# DISEASE NAME ENTITIES (40 entities)
# ============================================================================
# Common medical conditions, diseases, and medical procedures used in
# insurance claims and health insurance contexts.

DISEASE_NAMES = [
    # Chronic Conditions
    "diabetes",
    "hypertension",
    "high blood pressure",
    "heart disease",
    "coronary artery disease",
    "kidney disease",
    "chronic kidney disease",
    "liver cirrhosis",
    "asthma",
    "chronic obstructive pulmonary disease (COPD)",
    "thyroid disorder",
    "arthritis",
    "rheumatoid arthritis",
    
    # Major Diseases
    "cancer",
    "lung cancer",
    "breast cancer",
    "prostate cancer",
    "stroke",
    "heart attack",
    "myocardial infarction",
    "tuberculosis",
    "hepatitis",
    
    # Acute Conditions
    "dengue fever",
    "malaria",
    "typhoid",
    "pneumonia",
    "COVID-19",
    "appendicitis",
    "gallstones",
    "kidney stones",
    
    # Medical Procedures/Surgeries
    "bypass surgery",
    "angioplasty",
    "knee replacement surgery",
    "hip replacement surgery",
    "cataract surgery",
    "hernia repair",
    "cesarean section",
    "chemotherapy treatment",
    "dialysis treatment",
    "organ transplant",
    "bone fracture"
]

# ============================================================================
# ENTITY STATISTICS
# ============================================================================

HEALTHCARE_ENTITY_STATS = {
    "insurance_companies": len(INSURANCE_COMPANIES),
    "government_schemes": len(GOVERNMENT_SCHEMES),
    "insurance_marketplaces": len(INSURANCE_MARKETPLACES),
    "disease_names": len(DISEASE_NAMES),
    "total_entities": len(INSURANCE_COMPANIES) + len(GOVERNMENT_SCHEMES) + len(INSURANCE_MARKETPLACES) + len(DISEASE_NAMES)
}

# Helper function to get all healthcare entities
def get_all_healthcare_entities():
    """Return all healthcare entities as a single list"""
    return (INSURANCE_COMPANIES + GOVERNMENT_SCHEMES + 
            INSURANCE_MARKETPLACES + DISEASE_NAMES)

# Verification
if __name__ == "__main__":
    print("=" * 70)
    print("HEALTHCARE INSURANCE ENTITIES - VERIFICATION REPORT")
    print("=" * 70)
    print()
    
    print("📊 Entity Counts:")
    print(f"   Insurance Companies:     {len(INSURANCE_COMPANIES)} entities")
    print(f"   Government Schemes:      {len(GOVERNMENT_SCHEMES)} entities")
    print(f"   Insurance Marketplaces:  {len(INSURANCE_MARKETPLACES)} entities")
    print(f"   Disease Names:           {len(DISEASE_NAMES)} entities")
    print(f"   {'─' * 40}")
    print(f"   TOTAL:                   {HEALTHCARE_ENTITY_STATS['total_entities']} entities")
    print()
    
    print("✅ Sample Insurance Companies:")
    print(f"   {', '.join(INSURANCE_COMPANIES[:5])}")
    print()
    
    print("✅ Sample Government Schemes:")
    print(f"   {', '.join(GOVERNMENT_SCHEMES[:3])}")
    print()
    
    print("✅ Sample Insurance Marketplaces:")
    print(f"   {', '.join(INSURANCE_MARKETPLACES[:5])}")
    print()
    
    print("✅ Sample Disease Names:")
    print(f"   {', '.join(DISEASE_NAMES[:8])}")
    print()
    
    print("=" * 70)
    print("✅ All healthcare entity lists loaded successfully!")
    print("=" * 70)
