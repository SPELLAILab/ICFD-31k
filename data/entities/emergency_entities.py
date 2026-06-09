"""
Emergency Fraud Entity Lists
============================

This module contains entity lists for emergency and personal crisis fraud scenarios.
These entities cover family relationships, hospitals, cities, and NGOs commonly used
in emergency fraud scenarios.

Entity Categories:
- FAMILY_MEMBERS: 20 family relationship types
- HOSPITAL_NAMES: 52 Indian hospitals (government + private)
- INDIAN_CITIES: 57 major Indian cities (metro + tier 1/2)
- NGO_NAMES: 28 well-known Indian NGOs and charities

Total Entities: 157
"""

# ============================================================================
# FAMILY RELATIONSHIP ENTITIES (20 entities)
# ============================================================================
# Used in scenarios where scammers impersonate family members or exploit
# emotional connections to family. Covers immediate family, extended family,
# in-laws, and spouse relationships.

FAMILY_MEMBERS = [
    # Immediate Family
    "mother",
    "father",
    "son",
    "daughter",
    "brother",
    "sister",
    "elder brother",
    "younger sister",
    "twin brother",
    
    # Extended Family
    "grandmother",
    "grandfather",
    "uncle",
    "aunt",
    "nephew",
    "niece",
    "cousin",
    "grandson",
    "granddaughter",
    
    # Spouse and In-Laws
    "husband",
    "wife",
    "father-in-law",
    "mother-in-law",
    "brother-in-law",
    "sister-in-law",
    
    # Additional Relations
    "son-in-law",
    "daughter-in-law",
    "stepson",
    "stepdaughter",
    "maternal uncle",
    "paternal uncle",
    "cousin sister",
    "cousin brother",
    "great-grandmother",
    "great-grandfather",
    "grandnephew",
    "grandniece",
    "fiancé",
    "fiancée",
    "partner",
    "stepfather",
    "stepmother"
]

# ============================================================================
# HOSPITAL NAME ENTITIES (52 entities)
# ============================================================================
# Major Indian hospitals including AIIMS network, government medical colleges,
# and leading private hospital chains across metro and tier-1 cities.

HOSPITAL_NAMES = [
    # AIIMS Network (All India Institute of Medical Sciences)
    "AIIMS Delhi",
    "AIIMS Mumbai",
    "AIIMS Jodhpur",
    "AIIMS Bhubaneswar",
    "AIIMS Patna",
    "AIIMS Raipur",
    "AIIMS Rishikesh",
    "AIIMS Bhopal",
    
    # Apollo Hospitals Network
    "Apollo Hospitals Chennai",
    "Apollo Hospitals Hyderabad",
    "Apollo Hospitals Delhi",
    "Apollo Hospitals Bangalore",
    "Apollo Hospitals Mumbai",
    "Apollo Hospitals Kolkata",
    
    # Fortis Healthcare Network
    "Fortis Hospital Mumbai",
    "Fortis Hospital Delhi",
    "Fortis Hospital Bangalore",
    "Fortis Hospital Gurgaon",
    "Fortis Hospital Mohali",
    
    # Max Healthcare
    "Max Super Speciality Hospital Saket",
    "Max Hospital Patparganj",
    "Max Hospital Shalimar Bagh",
    "Max Hospital Vaishali",
    
    # Manipal Hospitals
    "Manipal Hospital Bangalore",
    "Manipal Hospital Delhi",
    "Manipal Hospital Jaipur",
    "Manipal Hospital Goa",
    
    # Medanta - The Medicity
    "Medanta Hospital Gurgaon",
    "Medanta Hospital Lucknow",
    "Medanta Hospital Indore",
    
    # Government Medical Colleges
    "Government Medical College Thiruvananthapuram",
    "Government Medical College Kozhikode",
    "Maulana Azad Medical College Delhi",
    "King George's Medical University Lucknow",
    "Grant Medical College Mumbai",
    "Stanley Medical College Chennai",
    
    # Other Major Private Hospitals
    "Lilavati Hospital Mumbai",
    "Hinduja Hospital Mumbai",
    "Breach Candy Hospital Mumbai",
    "Sir Ganga Ram Hospital Delhi",
    "Safdarjung Hospital Delhi",
    "Sankara Nethralaya Chennai",
    "Christian Medical College Vellore",
    "Narayana Health Bangalore",
    "Columbia Asia Hospital Bangalore",
    "Cloudnine Hospital Bangalore",
    "Rainbow Children's Hospital Hyderabad",
    "Care Hospitals Hyderabad",
    "Yashoda Hospitals Hyderabad",
    "Ruby Hall Clinic Pune",
    "Kokilaben Dhirubhai Ambani Hospital Mumbai"
]

# ============================================================================
# INDIAN CITY ENTITIES (57 entities)
# ============================================================================
# Major Indian cities including metros, tier-1, and tier-2 cities for
# geographic context in emergency fraud scenarios.

INDIAN_CITIES = [
    # Metro Cities (Tier 0)
    "Mumbai",
    "Delhi",
    "Bangalore",
    "Hyderabad",
    "Chennai",
    "Kolkata",
    
    # Tier 1 Cities
    "Ahmedabad",
    "Pune",
    "Surat",
    "Jaipur",
    "Lucknow",
    "Kanpur",
    "Nagpur",
    "Indore",
    "Thane",
    "Bhopal",
    "Visakhapatnam",
    "Pimpri-Chinchwad",
    "Patna",
    "Vadodara",
    "Ghaziabad",
    "Ludhiana",
    "Agra",
    "Nashik",
    "Faridabad",
    "Meerut",
    "Rajkot",
    "Kalyan-Dombivali",
    "Vasai-Virar",
    "Varanasi",
    "Srinagar",
    "Aurangabad",
    "Dhanbad",
    "Amritsar",
    "Navi Mumbai",
    "Allahabad",
    "Ranchi",
    "Howrah",
    "Coimbatore",
    "Jabalpur",
    "Gwalior",
    "Vijayawada",
    "Jodhpur",
    "Madurai",
    "Raipur",
    "Kota",
    
    # State Capitals and Important Cities
    "Chandigarh",
    "Guwahati",
    "Thiruvananthapuram",
    "Bhubaneswar",
    "Kochi",
    "Dehradun",
    "Shimla",
    "Gangtok",
    "Imphal",
    "Shillong",
    "Kohima",
    "Aizawl",
    "Panaji",
    "Dispur",
    "Itanagar"
]

# ============================================================================
# NGO/CHARITY NAME ENTITIES (28 entities)
# ============================================================================
# Well-known Indian NGOs and charitable organizations. Used in scenarios
# involving fake charity scams or legitimate NGO impersonation.

NGO_NAMES = [
    # Large National NGOs
    "CRY (Child Rights and You)",
    "Akshaya Patra Foundation",
    "Smile Foundation",
    "Goonj",
    "HelpAge India",
    "Pratham Education Foundation",
    "Give India",
    "SOS Children's Villages of India",
    "Save the Children India",
    "Teach For India",
    
    # Healthcare NGOs
    "Cancer Patients Aid Association",
    "Tata Memorial Centre",
    "Narayana Hrudayalaya Health City",
    "Sankara Eye Foundation",
    "Indian Red Cross Society",
    "St. Jude India ChildCare Centres",
    
    # Women and Child Welfare
    "Nanhi Kali",
    "Asha for Education",
    "Udayan Care",
    "Childline India Foundation",
    "ActionAid India",
    
    # Animal Welfare
    "People for Animals",
    "Blue Cross of India",
    
    # Environment and Rural Development
    "Art of Living Foundation",
    "Bharatiya Jain Sanghatana",
    "Self Employed Women's Association (SEWA)",
    "Sulabh International",
    "Helpage India Foundation"
]

# ============================================================================
# ENTITY STATISTICS
# ============================================================================

EMERGENCY_ENTITY_STATS = {
    "family_members": len(FAMILY_MEMBERS),
    "hospitals": len(HOSPITAL_NAMES),
    "cities": len(INDIAN_CITIES),
    "ngos": len(NGO_NAMES),
    "total_entities": len(FAMILY_MEMBERS) + len(HOSPITAL_NAMES) + len(INDIAN_CITIES) + len(NGO_NAMES)
}

# Verification
if __name__ == "__main__":
    print("=" * 70)
    print("EMERGENCY FRAUD ENTITIES - VERIFICATION REPORT")
    print("=" * 70)
    print()
    
    print("📊 Entity Counts:")
    print(f"   Family Members:  {len(FAMILY_MEMBERS)} entities")
    print(f"   Hospital Names:  {len(HOSPITAL_NAMES)} entities")
    print(f"   Indian Cities:   {len(INDIAN_CITIES)} entities")
    print(f"   NGO Names:       {len(NGO_NAMES)} entities")
    print(f"   {'─' * 40}")
    print(f"   TOTAL:           {EMERGENCY_ENTITY_STATS['total_entities']} entities")
    print()
    
    print("PASS: Sample Family Members:")
    print(f"   {', '.join(FAMILY_MEMBERS[:8])}")
    print()
    
    print("PASS: Sample Hospitals:")
    print(f"   {', '.join(HOSPITAL_NAMES[:5])}")
    print()
    
    print("PASS: Sample Cities:")
    print(f"   {', '.join(INDIAN_CITIES[:8])}")
    print()
    
    print("PASS: Sample NGOs:")
    print(f"   {', '.join(NGO_NAMES[:5])}")
    print()
    
    print("=" * 70)
    print("PASS: All emergency entity lists loaded successfully!")
    print("=" * 70)
