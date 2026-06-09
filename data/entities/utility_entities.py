"""
Utility & Service Provider Entities for Indian Context
Comprehensive lists to prevent overfitting in utility fraud dataset generation.
"""

# =============================================================================
# ELECTRICITY PROVIDERS
# =============================================================================

# State Electricity Boards (SEBs) and Distribution Companies (DISCOMs)
STATE_ELECTRICITY_BOARDS = [
    # Major State Boards
    "Maharashtra State Electricity Distribution Company (MSEDCL)",
    "Tata Power Delhi Distribution Limited (TPDDL)",
    "BSES Rajdhani Power Limited (BRPL)",
    "BSES Yamuna Power Limited (BYPL)",
    "Adani Electricity Mumbai",
    "Torrent Power Ahmedabad",
    "Torrent Power Surat",
    
    # North India
    "Punjab State Power Corporation Limited (PSPCL)",
    "Uttar Pradesh Power Corporation Limited (UPPCL)",
    "Haryana Vidyut Prasaran Nigam (HVPN)",
    "Rajasthan Rajya Vidyut Prasaran Nigam (RRVPNL)",
    "Himachal Pradesh State Electricity Board (HPSEB)",
    "Jammu & Kashmir Power Development Department",
    "Uttarakhand Power Corporation Limited (UPCL)",
    "Chandigarh Electricity Department",
    
    # South India
    "Tamil Nadu Generation and Distribution Corporation (TANGEDCO)",
    "Karnataka Power Transmission Corporation Limited (KPTCL)",
    "Bangalore Electricity Supply Company (BESCOM)",
    "Kerala State Electricity Board (KSEB)",
    "Andhra Pradesh Southern Power Distribution Company (APSPDCL)",
    "Telangana State Southern Power Distribution Company Limited (TSSPDCL)",
    "Greater Hyderabad Municipal Corporation Electricity Department",
    
    # East India
    "West Bengal State Electricity Distribution Company Limited (WBSEDCL)",
    "Calcutta Electric Supply Corporation (CESC)",
    "Odisha Power Transmission Corporation Limited (OPTCL)",
    "Jharkhand Bijli Vitran Nigam Limited (JBVNL)",
    "Bihar State Power Holding Company Limited",
    "Assam Power Distribution Company Limited (APDCL)",
    
    # West India
    "Gujarat Urja Vikas Nigam Limited (GUVNL)",
    "Madhya Pradesh Power Distribution Company",
    "Chhattisgarh State Power Distribution Company Limited",
    "Goa Electricity Department",
    
    # Central India
    "New Delhi Municipal Council (NDMC) Electricity Department",
    "Daman and Diu Electricity Department",
]

# =============================================================================
# MOBILE CARRIERS (Telecom Operators)
# =============================================================================

MOBILE_CARRIERS = [
    # Major Operators
    "Jio", "Reliance Jio", "Jio 5G",
    "Airtel", "Bharti Airtel", "Airtel 5G",
    "Vi", "Vodafone Idea", "Vi 5G",
    
    # BSNL
    "BSNL", "Bharat Sanchar Nigam Limited",
    "MTNL", "Mahanagar Telephone Nigam Limited",
    
    # Regional/Historical (still recognized)
    "Aircel",
    "Reliance Communications",
    "Tata Docomo",
    "MTS India",
    "Videocon Telecom",
]

# =============================================================================
# INTERNET/BROADBAND PROVIDERS
# =============================================================================

INTERNET_PROVIDERS = [
    # Major Fiber/Broadband ISPs
    "Jio Fiber", "JioFiber",
    "Airtel Xstream Fiber", "Airtel Broadband",
    "ACT Fibernet",
    "BSNL Bharat Fiber",
    "Hathway Broadband",
    "Tikona Broadband",
    "Excitel Broadband",
    "YOU Broadband",
    "Spectra Broadband",
    "Asianet Broadband",
    "GTPL Broadband",
    "Nextra Broadband",
    "Connect Broadband",
    "Alliance Broadband",
    
    # Cable + Broadband
    "DEN Broadband",
    "Siti Broadband",
    "In Cable Broadband",
    "Manthan Broadband",
    
    # Metro ISPs
    "Wishnet (Calcutta)", "Wishnet Kolkata",
    "7 Star Digital (Hyderabad)",
    "Pioneer Elabs (Delhi)",
    "MyRepublic India",
    "Fusionnet (Chennai)",
]

# =============================================================================
# GAS AGENCIES (LPG Distributors)
# =============================================================================

GAS_AGENCIES = [
    # Major Oil Marketing Companies
    "HP Gas", "Hindustan Petroleum Gas",
    "Bharat Gas", "Bharat Petroleum Gas",
    "Indane Gas", "Indian Oil Corporation Gas",
    
    # PNG/Piped Gas Providers
    "Gujarat Gas Limited",
    "Mahanagar Gas Limited (MGL)",
    "Indraprastha Gas Limited (IGL)",
    "Adani Gas",
    "Green Gas Limited",
    "Sabarmati Gas Limited",
    "Tripura Natural Gas Company Limited",
    "Assam Gas Company Limited",
    "Central UP Gas Limited",
    "Maharashtra Natural Gas Limited (MNGL)",
]

# =============================================================================
# DTH (Direct-to-Home) PROVIDERS
# =============================================================================

DTH_PROVIDERS = [
    "Tata Play", "Tata Sky",
    "Airtel Digital TV", "Airtel Xstream",
    "Dish TV",
    "d2h", "Videocon d2h",
    "Sun Direct",
    "DD Free Dish", "Doordarshan Free Dish",
]

# =============================================================================
# WATER SUPPLY DEPARTMENTS
# =============================================================================

WATER_SUPPLY_DEPARTMENTS = [
    # Major City Water Boards
    "Mumbai Municipal Corporation Water Department",
    "Delhi Jal Board (DJB)",
    "Bangalore Water Supply and Sewerage Board (BWSSB)",
    "Chennai Metro Water Supply and Sewerage Board",
    "Hyderabad Metropolitan Water Supply and Sewerage Board (HMWSSB)",
    "Kolkata Municipal Corporation Water Supply",
    "Ahmedabad Municipal Corporation Water Department",
    "Pune Municipal Corporation Water Supply",
    "Jaipur Water Works Department",
    "Lucknow Jal Sansthan",
    "Indore Municipal Corporation Water Department",
    "Surat Municipal Corporation Water Supply",
    "Kochi Municipal Corporation Water Authority",
    "Visakhapatnam Water Board",
    "Chandigarh Water Supply Department",
]

# =============================================================================
# GOVERNMENT SCHEMES & REGULATORY AUTHORITIES
# =============================================================================

GOVERNMENT_SCHEMES = [
    # Real Government Schemes
    "PM Ujjwala Yojana",
    "Pradhan Mantri Sahaj Bijli Har Ghar Yojana (Saubhagya)",
    "PM Kusum Solar Scheme",
    "Atal Bhujal Yojana",
    "Digital India Program",
    "BharatNet Project",
    "Smart Cities Mission",
]

GAS_REGULATORY_AUTHORITIES = [
    "Petroleum and Natural Gas Regulatory Board (PNGRB)",
    "Oil and Natural Gas Corporation (ONGC)",
    "Gas Authority of India Limited (GAIL)",
    "Ministry of Petroleum and Natural Gas",
]

TELECOM_REGULATORY_AUTHORITIES = [
    "Telecom Regulatory Authority of India (TRAI)",
    "Department of Telecommunications (DoT)",
    "Unique Identification Authority of India (UIDAI)",
]

ELECTRICITY_REGULATORY_AUTHORITIES = [
    "Central Electricity Regulatory Commission (CERC)",
    "State Electricity Regulatory Commission",
    "Power Grid Corporation of India",
    "Ministry of Power",
]

# =============================================================================
# UPI APPS (from ecommerce_entities.py - reuse)
# =============================================================================

# Note: We'll import from ecommerce_entities.py, but listing here for completeness
INDIAN_UPI_APPS_UTILITY = [
    "Google Pay", "GPay", "PhonePe", "Paytm",
    "BHIM", "Amazon Pay", "Mobikwik", "FreeCharge",
    "CRED", "Slice", "Jupiter", "Fi Money",
    "Airtel Payments Bank", "Jio Payments Bank",
    "HDFC Bank PayZapp", "ICICI iMobile Pay",
    "SBI YONO", "Axis Pay", "Kotak 811",
    "Punjab National Bank UPI", "Bank of Baroda UPI",
    "Canara Bank UPI", "Union Bank UPI",
    "IndusInd Bank UPI", "Yes Bank UPI",
    "IDFC First Bank UPI", "Federal Bank UPI",
]

# =============================================================================
# COMMON SERVICES & ITEMS
# =============================================================================

UTILITY_SERVICES = [
    "electricity connection", "power supply",
    "mobile connection", "SIM card", "prepaid plan", "postpaid plan",
    "broadband connection", "fiber internet", "WiFi connection",
    "LPG cylinder", "gas connection", "refill booking",
    "DTH connection", "set-top box", "channel package",
    "water connection", "water meter", "water bill",
]

UTILITY_EQUIPMENT = [
    "electricity meter", "smart meter", "prepaid meter",
    "SIM card", "4G SIM", "5G SIM",
    "WiFi router", "broadband modem", "ONT device",
    "gas cylinder", "regulator", "gas stove",
    "DTH set-top box", "dish antenna", "remote control",
    "water meter", "water purifier connection",
]

# =============================================================================
# FRAUD TECHNIQUES (Utility-specific)
# =============================================================================

UTILITY_FRAUD_TECHNIQUES = [
    "Disconnection threat with urgent payment",
    "Remote access app installation for KYC",
    "OTP theft for subsidy/linking",
    "Advance fee for equipment upgrade",
    "SIM card number phishing for SIM swap",
    "Faulty meter extortion",
    "Fake government scheme registration fee",
    "UPI request scam disguised as technical fix",
    "SMS forwarding for unauthorized port-out",
    "Panic creation for emergency fee",
    "Security question answer phishing",
    "Data breach exploitation for refund scam",
    "QR code scam for fake refund",
    "Multi-account linking phishing",
    "Fake bill payment link",
]

# =============================================================================
# SCAMMER ROLES (Utility Context)
# =============================================================================

UTILITY_SCAMMER_ROLES = [
    "Electricity board officer",
    "Mobile carrier customer support",
    "KYC verification team",
    "Gas agency delivery person",
    "Broadband technician",
    "DTH customer care executive",
    "Water department inspector",
    "Government scheme coordinator",
    "SIM card delivery agent",
    "Meter reading inspector",
    "Billing department officer",
    "Technical support engineer",
    "Collections department agent",
    "Network tower maintenance team",
    "Subsidy processing officer",
]

# =============================================================================
# LEGITIMATE ACTIONS (Normal Utility Interactions)
# =============================================================================

LEGITIMATE_UTILITY_ACTIONS = [
    "Scheduled maintenance notification",
    "Bill generation reminder",
    "Complaint follow-up",
    "Service upgrade offer",
    "Appointment confirmation",
    "Customer satisfaction survey",
    "Delivery status update",
    "Plan expiry notification",
    "Overdue payment reminder",
    "Service activation confirmation",
    "Technical support guidance",
    "Procedural information",
    "Marketing call for new services",
    "Address verification for delivery",
]

# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def get_all_utility_providers():
    """Return all utility provider names."""
    return (STATE_ELECTRICITY_BOARDS + MOBILE_CARRIERS + 
            INTERNET_PROVIDERS + GAS_AGENCIES + DTH_PROVIDERS + 
            WATER_SUPPLY_DEPARTMENTS)

def get_all_regulatory_authorities():
    """Return all regulatory authority names."""
    return (GAS_REGULATORY_AUTHORITIES + TELECOM_REGULATORY_AUTHORITIES + 
            ELECTRICITY_REGULATORY_AUTHORITIES)

def get_all_government_schemes():
    """Return all government scheme names."""
    return GOVERNMENT_SCHEMES

def get_provider_by_type(provider_type):
    """Get providers by specific type."""
    mapping = {
        'electricity': STATE_ELECTRICITY_BOARDS,
        'mobile': MOBILE_CARRIERS,
        'internet': INTERNET_PROVIDERS,
        'gas': GAS_AGENCIES,
        'dth': DTH_PROVIDERS,
        'water': WATER_SUPPLY_DEPARTMENTS,
    }
    return mapping.get(provider_type, [])

# =============================================================================
# STATISTICS (for verification)
# =============================================================================

if __name__ == "__main__":
    print("=" * 80)
    print("UTILITY & SERVICE PROVIDER ENTITIES STATISTICS")
    print("=" * 80)
    
    print(f"\nElectricity Providers: {len(STATE_ELECTRICITY_BOARDS)}")
    print(f"Mobile Carriers: {len(MOBILE_CARRIERS)}")
    print(f"Internet Providers: {len(INTERNET_PROVIDERS)}")
    print(f"Gas Agencies: {len(GAS_AGENCIES)}")
    print(f"DTH Providers: {len(DTH_PROVIDERS)}")
    print(f"Water Supply Departments: {len(WATER_SUPPLY_DEPARTMENTS)}")
    
    print(f"\nGovernment Schemes: {len(GOVERNMENT_SCHEMES)}")
    print(f"Gas Regulatory Authorities: {len(GAS_REGULATORY_AUTHORITIES)}")
    print(f"Telecom Regulatory Authorities: {len(TELECOM_REGULATORY_AUTHORITIES)}")
    print(f"Electricity Regulatory Authorities: {len(ELECTRICITY_REGULATORY_AUTHORITIES)}")
    
    print(f"\nUPI Apps: {len(INDIAN_UPI_APPS_UTILITY)}")
    print(f"Utility Services: {len(UTILITY_SERVICES)}")
    print(f"Utility Equipment: {len(UTILITY_EQUIPMENT)}")
    
    print(f"\nFraud Techniques: {len(UTILITY_FRAUD_TECHNIQUES)}")
    print(f"Scammer Roles: {len(UTILITY_SCAMMER_ROLES)}")
    print(f"Legitimate Actions: {len(LEGITIMATE_UTILITY_ACTIONS)}")
    
    print(f"\n{'=' * 80}")
    total = (len(STATE_ELECTRICITY_BOARDS) + len(MOBILE_CARRIERS) + 
             len(INTERNET_PROVIDERS) + len(GAS_AGENCIES) + 
             len(DTH_PROVIDERS) + len(WATER_SUPPLY_DEPARTMENTS) +
             len(GOVERNMENT_SCHEMES) + len(GAS_REGULATORY_AUTHORITIES) +
             len(TELECOM_REGULATORY_AUTHORITIES) + len(ELECTRICITY_REGULATORY_AUTHORITIES) +
             len(INDIAN_UPI_APPS_UTILITY))
    
    print(f"TOTAL UNIQUE UTILITY ENTITIES: {total}")
    print("=" * 80)
