"""
Job & Recruitment Entity Lists for Fraud Detection Training Data

This module provides comprehensive lists of Indian IT companies, MNCs, job portals,
government departments, and airline companies to prevent overfitting in training data.

Usage:
    from data.entities.job_entities import IT_COMPANIES, MNC_COMPANIES, JOB_PORTALS

Entity Count: 197 unique entities across 5 categories
"""

# ==============================================================================
# INDIAN IT COMPANIES & IT SERVICE PROVIDERS
# ==============================================================================

IT_COMPANIES = [
    # Top Tier Indian IT Giants
    "Tata Consultancy Services (TCS)",
    "Infosys",
    "Wipro",
    "HCL Technologies",
    "Tech Mahindra",
    "LTI Mindtree",
    "Mphasis",
    "Persistent Systems",
    "Cyient",
    "Zensar Technologies",
    
    # Mid-Tier Indian IT Companies
    "L&T Infotech",
    "Hexaware Technologies",
    "Birlasoft",
    "Mastek",
    "KPIT Technologies",
    "Sonata Software",
    "3i Infotech",
    "Intellect Design Arena",
    "Polaris Consulting",
    "Nucleus Software",
    
    # Product Companies (Indian)
    "Zoho Corporation",
    "Freshworks",
    "Druva",
    "Mu Sigma",
    "Manthan",
    "BrowserStack",
    "Postman",
    "Chargebee",
    "CleverTap",
    "Exotel",
    
    # E-commerce & Consumer Tech
    "Flipkart",
    "Paytm",
    "PhonePe",
    "Swiggy",
    "Zomato",
    "Ola",
    "Uber India",
    "Amazon India",
    "Meesho",
    "Snapdeal",
    
    # Fintech
    "Razorpay",
    "CRED",
    "BharatPe",
    "PolicyBazaar",
    "Groww",
    "Zerodha",
    "Paytm Payments Bank",
    "MobiKwik",
    "FreeCharge",
    "Lendingkart",
    
    # Edtech
    "BYJU'S",
    "Unacademy",
    "upGrad",
    "Vedantu",
    "Simplilearn",
    "Great Learning",
    "Eruditus",
    "Toppr",
    "WhiteHat Jr",
    "Cuemath",
    
    # Emerging Tech Startups
    "Observe.AI",
    "Haptik",
    "Innovaccer",
    "SigTuple",
    "Niramai",
    "Darwinbox",
    "GreyOrange",
    "Delhivery",
    "BlackBuck",
    "Rivigo"
]

# ==============================================================================
# MULTINATIONAL COMPANIES (MNCs) OPERATING IN INDIA
# ==============================================================================

MNC_COMPANIES = [
    # Tech Giants (FAANG+)
    "Google India",
    "Microsoft India",
    "Amazon Development Centre",
    "Apple India",
    "Meta (Facebook) India",
    "Netflix India",
    
    # IT & Consulting MNCs
    "Accenture",
    "IBM India",
    "Cognizant",
    "Capgemini",
    "Deloitte",
    "Ernst & Young (EY)",
    "PwC India",
    "KPMG India",
    "McKinsey & Company",
    "Boston Consulting Group",
    "Bain & Company",
    
    # Tech & Software
    "Oracle India",
    "SAP Labs India",
    "Adobe Systems",
    "Salesforce India",
    "VMware India",
    "Cisco Systems India",
    "Intel India",
    "Qualcomm India",
    "NVIDIA India",
    "AMD India",
    
    # Enterprise Software
    "Workday India",
    "ServiceNow India",
    "Atlassian",
    "Slack Technologies",
    "Zoom India",
    "Twilio India",
    "MongoDB India",
    "Elastic India",
    
    # Consumer Tech
    "Samsung R&D India",
    "Sony India",
    "LG Electronics India",
    "Dell Technologies India",
    "HP India",
    "Lenovo India",
    "Xiaomi India",
    "Oppo India",
    "Vivo India",
    "OnePlus India",
    
    # E-commerce & Retail
    "Walmart India",
    "Ikea India",
    "Decathlon India",
    "H&M India",
    "Zara India",
    "Nike India",
    "Adidas India",
    
    # Automotive
    "Tesla India",
    "Ford India",
    "General Motors India",
    "BMW India",
    "Mercedes-Benz India",
    "Audi India",
    "Hyundai Motor India",
    "Toyota Kirloskar Motor",
    "Volkswagen India",
    
    # Pharmaceuticals
    "Pfizer India",
    "Johnson & Johnson India",
    "Abbott India",
    "GlaxoSmithKline India",
    "Novartis India",
    "Roche India",
    
    # FMCG
    "Unilever India",
    "Procter & Gamble India",
    "Nestle India",
    "PepsiCo India",
    "Coca-Cola India",
    "Mondelez India"
]

# ==============================================================================
# JOB PORTALS & RECRUITMENT PLATFORMS
# ==============================================================================

JOB_PORTALS = [
    # Major Indian Job Portals
    "Naukri.com",
    "Monster India",
    "TimesJobs",
    "Shine.com",
    "Foundit (formerly Monster India)",
    "Freshersworld",
    "PlacementIndia",
    "Rozgar.com",
    
    # Global Platforms
    "LinkedIn",
    "Indeed India",
    "Glassdoor India",
    
    # Freelance & Gig
    "Upwork",
    "Fiverr",
    "Freelancer India",
    "Toptal",
    "PeoplePerHour",
    
    # Tech-Specific
    "AngelList India",
    "Wellfound (formerly AngelList Talent)",
    "Instahyre",
    "Cutshort",
    "Hirist",
    "IIMJobs",
    
    # Blue Collar & Gig Workers
    "Apna",
    "WorkIndia",
    "Aasaan Jobs",
    "Babajob",
    
    # Internship Platforms
    "Internshala",
    "LetsIntern",
    "Twenty19"
]

# ==============================================================================
# GOVERNMENT DEPARTMENTS & PUBLIC SECTOR UNDERTAKINGS
# ==============================================================================

GOVERNMENT_DEPARTMENTS = [
    # Central Government Recruitment Bodies
    "UPSC (Union Public Service Commission)",
    "SSC (Staff Selection Commission)",
    "IBPS (Institute of Banking Personnel Selection)",
    "Railway Recruitment Board (RRB)",
    "Defence Ministry Recruitment",
    "DRDO (Defence Research & Development Organisation)",
    
    # Central Ministries
    "Ministry of Railways",
    "Ministry of Home Affairs",
    "Ministry of Finance",
    "Ministry of Defence",
    "Ministry of External Affairs",
    "Ministry of Electronics and Information Technology",
    "Department of Posts",
    "Income Tax Department",
    
    # Public Sector Banks
    "State Bank of India (SBI)",
    "Punjab National Bank (PNB)",
    "Bank of Baroda",
    "Canara Bank",
    "Union Bank of India",
    "Bank of India",
    "Indian Bank",
    "Central Bank of India",
    
    # Central PSUs
    "ONGC (Oil and Natural Gas Corporation)",
    "NTPC (National Thermal Power Corporation)",
    "Coal India Limited",
    "BHEL (Bharat Heavy Electricals Limited)",
    "SAIL (Steel Authority of India)",
    "Indian Oil Corporation",
    "BSNL (Bharat Sanchar Nigam Limited)",
    "HAL (Hindustan Aeronautics Limited)",
    "GAIL (Gas Authority of India Limited)",
    "Power Grid Corporation of India",
    
    # State PSUs (Examples)
    "Maharashtra State Electricity Board",
    "Delhi Metro Rail Corporation (DMRC)",
    "Mumbai Metro",
    "Bangalore Metro Rail Corporation",
    "Tamil Nadu State Transport Corporation",
    "Karnataka State Road Transport Corporation",
    
    # Research & Academic
    "ISRO (Indian Space Research Organisation)",
    "CSIR (Council of Scientific and Industrial Research)",
    "BARC (Bhabha Atomic Research Centre)",
    "AIIMS (All India Institute of Medical Sciences)",
    "IITs (Indian Institutes of Technology)",
    "NITs (National Institutes of Technology)"
]

# ==============================================================================
# INDIAN AIRLINE COMPANIES
# ==============================================================================

AIRLINE_COMPANIES = [
    # Full Service Carriers
    "Air India",
    "Vistara",
    
    # Low Cost Carriers
    "IndiGo",
    "SpiceJet",
    "GoFirst (formerly Go Air)",
    "AirAsia India",
    "Akasa Air",
    
    # Cargo & Charter
    "Blue Dart Aviation",
    "Quikjet Cargo Airlines",
    
    # Regional Carriers
    "Alliance Air",
    "FlyBig",
    "Star Air"
]

# ==============================================================================
# HELPER FUNCTIONS
# ==============================================================================

def get_all_job_entities():
    """Get all job-related entities as a single list."""
    return (IT_COMPANIES + MNC_COMPANIES + JOB_PORTALS + 
            GOVERNMENT_DEPARTMENTS + AIRLINE_COMPANIES)

def get_entity_by_category(category: str):
    """
    Get entities by category.
    
    Args:
        category: One of 'it', 'mnc', 'portal', 'government', 'airline'
    
    Returns:
        List of entities for that category
    """
    categories = {
        'it': IT_COMPANIES,
        'mnc': MNC_COMPANIES,
        'portal': JOB_PORTALS,
        'government': GOVERNMENT_DEPARTMENTS,
        'airline': AIRLINE_COMPANIES
    }
    return categories.get(category.lower(), [])

def get_entity_count_by_category():
    """Get count of entities in each category."""
    return {
        'IT Companies': len(IT_COMPANIES),
        'MNC Companies': len(MNC_COMPANIES),
        'Job Portals': len(JOB_PORTALS),
        'Government Departments': len(GOVERNMENT_DEPARTMENTS),
        'Airline Companies': len(AIRLINE_COMPANIES)
    }

# ==============================================================================
# STATISTICS
# ==============================================================================

if __name__ == "__main__":
    print("\n" + "="*80)
    print("JOB & RECRUITMENT ENTITY STATISTICS")
    print("="*80)
    print()
    
    counts = get_entity_count_by_category()
    for category, count in counts.items():
        print(f"{category}: {count}")
    
    print()
    print("="*80)
    print(f"TOTAL UNIQUE JOB ENTITIES: {len(get_all_job_entities())}")
    print("="*80)
    print()
    
    # Sample entities from each category
    print("Sample Entities:")
    print("-" * 80)
    print(f"IT Companies: {', '.join(IT_COMPANIES[:5])}")
    print(f"MNC Companies: {', '.join(MNC_COMPANIES[:5])}")
    print(f"Job Portals: {', '.join(JOB_PORTALS[:5])}")
    print(f"Government Depts: {', '.join(GOVERNMENT_DEPARTMENTS[:5])}")
    print(f"Airlines: {', '.join(AIRLINE_COMPANIES[:5])}")
    print("="*80)
