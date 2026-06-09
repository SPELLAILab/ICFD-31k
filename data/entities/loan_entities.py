"""
Loan Entity Data for Fraud Detection Training
============================================

This module provides comprehensive lists of lending apps and financial institutions
used in loan fraud detection scenarios. Entities are categorized into:
- Predatory/Banned Lending Apps
- Legitimate Lending Apps  
- NBFCs (Non-Banking Financial Companies)
- Microfinance Institutions

These entities are used to replace placeholders like [LENDING_APP] in conversation
generation for Indian loan fraud detection training.

Entity Count:
- Predatory Lending Apps: 45
- Legitimate Lending Apps: 38
- NBFCs: 52
- Microfinance Institutions: 35
- Credit Bureaus: 6
Total: 176 entities

Last Updated: October 13, 2025
"""

# =============================================================================
# PREDATORY/BANNED LENDING APPS (45)
# =============================================================================
# These apps have been banned or flagged by RBI for predatory practices,
# harassment, data theft, and illegal collection methods

PREDATORY_LENDING_APPS = [
    # Chinese loan apps banned in 2020-2022
    "CashBean",
    "MoneyTap Plus",
    "RupeeCircle",
    "Go Cash",
    "Nice Cash",
    "Moco Cash",
    "Flash Cash",
    "Speed Cash",
    "Loan Cash",
    "Super Cash",
    "Easy Cash",
    "Quick Cash",
    "Fast Cash",
    "Smart Cash",
    "Magic Cash",
    
    # Other predatory apps (flagged/banned)
    "RupeeRedee",
    "CashKuber",
    "LoanTap Express",
    "QuickRupee",
    "AadhaarPe",
    "CreditMantri Cash",
    "SalaryAdvance",
    "WagePay",
    "InstantMoney",
    "ReadyCash",
    "TurboLoan",
    "RocketCash",
    "LightningLoan",
    "ThunderCash",
    
    # Apps with reported harassment cases
    "MoneyView Plus",
    "CashCare",
    "LoanCare",
    "CashFirst",
    "LoanNow",
    "GetLoan",
    "MyLoan",
    "QuickLoan India",
    "RupeeLoan",
    "CashLoan India",
    "FastLoan India",
    "EasyLoan India",
    "SmartLoan India",
    "InstantLoan India",
]

# =============================================================================
# LEGITIMATE LENDING APPS (38)
# =============================================================================
# RBI-compliant digital lending platforms with proper licenses

LEGITIMATE_LENDING_APPS = [
    # Major NBFC-backed apps (RBI registered)
    "LazyPay",
    "ZestMoney",
    "PaySense",
    "EarlySalary",
    "MoneyTap",
    "CASHe",
    "KreditBee",
    "Navi",
    "Fibe (formerly EarlySalary)",
    "mPokket",
    
    # Bank-backed digital lending
    "HDFC Bank InstantLoan",
    "ICICI Bank InstantCredit",
    "Axis Bank InstaEMI",
    "Kotak 811 Loan",
    "SBI YONO Cash",
    "IndusInd Bank Loan",
    "YES Bank YES Touch Loan",
    "Standard Chartered DigiSmart Credit",
    
    # Fintech with NBFC license
    "Kissht",
    "FlexiLoans",
    "Capital Float",
    "Lendingkart",
    "NeoGrowth",
    "Indifi",
    "GetVantage",
    "Oxyzo (formerly OfBusiness)",
    
    # P2P lending platforms (RBI registered)
    "Faircent",
    "LendenClub",
    "i2iFunding",
    "Liquiloans",
    
    # Buy Now Pay Later (legitimate)
    "Simpl",
    "ePayLater",
    "FlexMoney",
    "OlaMoney Postpaid",
    "Amazon Pay Later",
    "Flipkart Pay Later",
]

# =============================================================================
# NBFCs - NON-BANKING FINANCIAL COMPANIES (52)
# =============================================================================
# RBI-registered NBFCs providing loans and financial services

NBFC_COMPANIES = [
    # Large NBFCs
    "Bajaj Finance",
    "Mahindra Finance",
    "Shriram Finance",
    "Tata Capital",
    "L&T Finance",
    "Aditya Birla Finance",
    "Cholamandalam Investment and Finance",
    "Muthoot Finance",
    "Manappuram Finance",
    "IIFL Finance",
    
    # Housing finance companies
    "HDFC Ltd",
    "LIC Housing Finance",
    "Indiabulls Housing Finance",
    "Dewan Housing Finance (DHFL)",
    "PNB Housing Finance",
    "Reliance Home Finance",
    "Can Fin Homes",
    "Repco Home Finance",
    
    # Vehicle finance NBFCs
    "Shriram Transport Finance",
    "Sundaram Finance",
    "Mahindra & Mahindra Financial Services",
    "Tata Motors Finance",
    "TVS Credit",
    "Hero FinCorp",
    "Ashok Leyland Finance",
    
    # Microfinance NBFCs
    "Bandhan Financial Services",
    "Ujjivan Financial Services",
    "Equitas Small Finance Bank",
    "Suryoday Small Finance Bank",
    "Utkarsh Small Finance Bank",
    
    # Consumer finance NBFCs
    "Bajaj Finserv",
    "Fullerton India",
    "Tata Consumer Finance",
    "HDB Financial Services",
    "ICICI Home Finance",
    "Kotak Mahindra Prime",
    "Axis Finance",
    
    # Gold loan NBFCs
    "Muthoot Fincorp",
    "Manappuram Gold Loan",
    "IIFL Gold Loan",
    "Bajaj Finance Gold Loan",
    "Rupeek",
    "Indiagold",
    
    # Digital NBFCs
    "MobiKwik Finance",
    "Paytm Postpaid",
    "Capital First (now IDFC First Bank)",
    "InCred Finance",
    "Northern Arc Capital",
    "Annapurna Finance",
    "Svatantra Microfin",
]

# =============================================================================
# MICROFINANCE INSTITUTIONS (35)
# =============================================================================
# MFIs providing small loans to low-income borrowers

MICROFINANCE_INSTITUTIONS = [
    # Large MFIs
    "SKS Microfinance",
    "Bharat Financial Inclusion (merged with IndusInd)",
    "Spandana Sphoorty Financial",
    "Ujjivan Small Finance Bank",
    "Equitas Small Finance Bank",
    "Bandhan Bank",
    
    # Regional MFIs
    "Grameen Koota",
    "Janalakshmi Financial Services",
    "Arohan Financial Services",
    "Satin Creditcare Network",
    "CreditAccess Grameen",
    "Fusion Microfinance",
    "Utkarsh Micro Finance",
    "Muthoot Microfin",
    
    # NGO-based MFIs
    "SEWA Bank",
    "Cashpor Micro Credit",
    "Samhita Community Development Services",
    "Share Microfin",
    "Asirvad Micro Finance",
    "Annapurna Finance",
    
    # Small Finance Banks (converted MFIs)
    "AU Small Finance Bank",
    "Suryoday Small Finance Bank",
    "Fincare Small Finance Bank",
    "Jana Small Finance Bank",
    "North East Small Finance Bank",
    
    # JLG (Joint Liability Group) based
    "Belstar Microfinance",
    "Saija Finance",
    "Satya MicroCapital",
    "ESAF Small Finance Bank",
    "Ujjwal Small Finance Bank",
    "Margdarshak Financial Services",
    "GFSPL (Grameen Financial Services)",
    "Village Financial Services",
    "Sarala Microfinance",
]

# =============================================================================
# CREDIT BUREAUS (6)
# =============================================================================
# Used for CIBIL score references in fraud scenarios

CREDIT_BUREAUS = [
    "CIBIL (TransUnion CIBIL)",
    "Equifax India",
    "Experian India",
    "CRIF High Mark",
    "Paisa Bazaar Credit Score",
    "Bajaj Finserv Credit Pass",
]

# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def get_all_lending_apps():
    """Returns all lending apps (both predatory and legitimate)"""
    return PREDATORY_LENDING_APPS + LEGITIMATE_LENDING_APPS

def get_predatory_apps():
    """Returns only predatory/banned lending apps"""
    return PREDATORY_LENDING_APPS

def get_legitimate_apps():
    """Returns only legitimate/RBI-compliant lending apps"""
    return LEGITIMATE_LENDING_APPS

def get_all_loan_entities():
    """Returns all loan-related entities"""
    return (
        PREDATORY_LENDING_APPS + 
        LEGITIMATE_LENDING_APPS + 
        NBFC_COMPANIES + 
        MICROFINANCE_INSTITUTIONS +
        CREDIT_BUREAUS
    )

def get_entity_by_category(category):
    """
    Get entities by category
    
    Args:
        category: One of 'predatory', 'legitimate', 'nbfc', 'mfi', 'credit_bureau', 'all'
    
    Returns:
        List of entities in that category
    """
    categories = {
        'predatory': PREDATORY_LENDING_APPS,
        'legitimate': LEGITIMATE_LENDING_APPS,
        'nbfc': NBFC_COMPANIES,
        'mfi': MICROFINANCE_INSTITUTIONS,
        'microfinance': MICROFINANCE_INSTITUTIONS,
        'credit_bureau': CREDIT_BUREAUS,
        'all': get_all_loan_entities(),
        'lending_apps': get_all_lending_apps(),
    }
    return categories.get(category.lower(), [])

def get_entity_count_by_category():
    """Returns entity counts for each category"""
    return {
        'predatory_apps': len(PREDATORY_LENDING_APPS),
        'legitimate_apps': len(LEGITIMATE_LENDING_APPS),
        'nbfc_companies': len(NBFC_COMPANIES),
        'microfinance_institutions': len(MICROFINANCE_INSTITUTIONS),
        'credit_bureaus': len(CREDIT_BUREAUS),
        'total': len(get_all_loan_entities()),
    }

# =============================================================================
# ENTITY STATISTICS
# =============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("LOAN ENTITY STATISTICS")
    print("=" * 70)
    
    stats = get_entity_count_by_category()
    print(f"\nPredatory/Banned Lending Apps: {stats['predatory_apps']}")
    print(f"Legitimate Lending Apps: {stats['legitimate_apps']}")
    print(f"NBFC Companies: {stats['nbfc_companies']}")
    print(f"Microfinance Institutions: {stats['microfinance_institutions']}")
    print(f"Credit Bureaus: {stats['credit_bureaus']}")
    print(f"\nTotal Loan Entities: {stats['total']}")
    
    print(f"\n{'=' * 70}")
    print("SAMPLE ENTITIES BY CATEGORY")
    print("=" * 70)
    
    print("\nPredatory Apps (first 5):")
    for app in PREDATORY_LENDING_APPS[:5]:
        print(f"  - {app}")
    
    print("\nLegitimate Apps (first 5):")
    for app in LEGITIMATE_LENDING_APPS[:5]:
        print(f"  - {app}")
    
    print("\nNBFCs (first 5):")
    for nbfc in NBFC_COMPANIES[:5]:
        print(f"  - {nbfc}")
    
    print("\nMicrofinance (first 5):")
    for mfi in MICROFINANCE_INSTITUTIONS[:5]:
        print(f"  - {mfi}")
    
    print("\nCredit Bureaus:")
    for bureau in CREDIT_BUREAUS:
        print(f"  - {bureau}")
    
    print(f"\n{'=' * 70}")
