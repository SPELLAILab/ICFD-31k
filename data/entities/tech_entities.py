"""
Tech Entity Data for Fraud Detection Training
============================================

This module provides comprehensive lists of tech companies, platforms, and services
used in tech support and online account fraud detection scenarios. Entities are categorized into:
- Tech Companies (Microsoft, Apple, Google, etc.)
- Social Media Platforms
- Email Providers
- Gaming Platforms
- Gift Card Brands
- Ride-Hailing Apps

These entities are used to replace placeholders like [TECH_COMPANY], [SOCIAL_MEDIA_APP], 
[EMAIL_PROVIDER], etc. in conversation generation for tech fraud detection training.

Entity Count:
- Tech Companies: 48
- Social Media Platforms: 28
- Email Providers: 18
- Gaming Platforms: 22
- Gift Card Brands: 26
- Ride-Hailing Apps: 12
Total: 154 entities

Last Updated: October 13, 2025
"""

# =============================================================================
# TECH COMPANIES (48)
# =============================================================================
# Major technology companies that are frequently impersonated in tech support scams

TECH_COMPANIES = [
    # Operating System / Desktop Software
    "Microsoft",
    "Apple",
    "Google",
    "Adobe",
    "Oracle",
    "IBM",
    "SAP",
    "Salesforce",
    
    # Security / Antivirus Companies
    "Norton (NortonLifeLock)",
    "McAfee",
    "Kaspersky",
    "Avast",
    "AVG",
    "Bitdefender",
    "ESET",
    "Trend Micro",
    "Malwarebytes",
    "Sophos",
    
    # Cloud / Productivity Software
    "Zoom",
    "Microsoft Teams",
    "Slack",
    "Dropbox",
    "Box",
    "Notion",
    "Asana",
    "Trello",
    "Monday.com",
    
    # Hardware Manufacturers
    "Dell",
    "HP (Hewlett-Packard)",
    "Lenovo",
    "Asus",
    "Acer",
    "Samsung",
    "LG",
    "Sony",
    
    # Software / SaaS Companies
    "Intuit (QuickBooks)",
    "Atlassian (Jira)",
    "Autodesk",
    "Cisco",
    "VMware",
    "Red Hat",
    "Mozilla (Firefox)",
    "Opera",
    
    # Indian Tech Companies
    "Tata Consultancy Services (TCS)",
    "Infosys",
    "Wipro",
    "Tech Mahindra",
]

# =============================================================================
# SOCIAL MEDIA PLATFORMS (28)
# =============================================================================
# Social media and messaging apps commonly targeted in account takeover scams

SOCIAL_MEDIA_PLATFORMS = [
    # Global Major Platforms
    "Facebook",
    "Instagram",
    "Twitter (X)",
    "LinkedIn",
    "WhatsApp",
    "Telegram",
    "Snapchat",
    "TikTok",
    "Pinterest",
    "Reddit",
    "Discord",
    
    # Messaging Apps
    "Signal",
    "Viber",
    "WeChat",
    "Line",
    "KakaoTalk",
    
    # Indian Social Media
    "ShareChat",
    "Koo",
    "Moj",
    "Josh",
    "Roposo",
    "Chingari",
    
    # Professional / Niche Platforms
    "YouTube",
    "Vimeo",
    "Twitch",
    "Clubhouse",
    "Threads (by Meta)",
    "Mastodon",
]

# =============================================================================
# EMAIL PROVIDERS (18)
# =============================================================================
# Email service providers targeted in account compromise scams

EMAIL_PROVIDERS = [
    # Major Consumer Email
    "Gmail",
    "Outlook (Microsoft)",
    "Yahoo Mail",
    "iCloud Mail (Apple)",
    "ProtonMail",
    "Tutanota",
    
    # Business Email
    "Microsoft 365 (Office 365)",
    "Google Workspace (G Suite)",
    "Zoho Mail",
    "FastMail",
    "Mailgun",
    
    # Regional / Other
    "Yandex Mail",
    "Mail.ru",
    "AOL Mail",
    "GMX Mail",
    "Mail.com",
    "Rediffmail",
    "Outlook.com",
]

# =============================================================================
# GAMING PLATFORMS (22)
# =============================================================================
# Gaming platforms and services where accounts are valuable targets

GAMING_PLATFORMS = [
    # PC Gaming
    "Steam",
    "Epic Games Store",
    "GOG (Good Old Games)",
    "Origin (EA)",
    "Ubisoft Connect",
    "Battle.net (Blizzard)",
    "Riot Games (League of Legends)",
    
    # Console Gaming
    "PlayStation Network (PSN)",
    "Xbox Live",
    "Nintendo eShop",
    "Nintendo Switch Online",
    
    # Mobile Gaming
    "Google Play Games",
    "Apple Arcade",
    "Garena Free Fire",
    "PUBG Mobile",
    
    # Indian Gaming Platforms
    "MPL (Mobile Premier League)",
    "Dream11",
    "WinZO",
    "Paytm First Games",
    "RummyCircle",
    "A23 (Ace2Three)",
]

# =============================================================================
# GIFT CARD BRANDS (26)
# =============================================================================
# Gift cards commonly requested as payment in tech support scams

GIFT_CARD_BRANDS = [
    # E-commerce
    "Amazon Gift Card",
    "Flipkart Gift Card",
    "Myntra Gift Voucher",
    "Shoppers Stop Gift Card",
    "Lifestyle Gift Voucher",
    
    # Gaming
    "Steam Wallet Card",
    "PlayStation Store Card",
    "Xbox Gift Card",
    "Nintendo eShop Card",
    "Google Play Gift Card",
    "Apple iTunes Gift Card",
    
    # Entertainment
    "Netflix Gift Card",
    "Spotify Gift Card",
    "BookMyShow Gift Card",
    "PVR Cinemas Gift Card",
    
    # Restaurants / Food
    "Domino's Gift Voucher",
    "McDonald's Gift Card",
    "Starbucks Gift Card",
    "Zomato Gift Card",
    "Swiggy Money",
    
    # Retail
    "Walmart Gift Card",
    "Target Gift Card",
    "Visa Prepaid Card",
    "Mastercard Gift Card",
    "American Express Gift Card",
    "Big Bazaar Gift Voucher",
]

# =============================================================================
# RIDE-HAILING APPS (12)
# =============================================================================
# Ride-hailing and transportation apps

RIDE_HAILING_APPS = [
    # Major Indian Apps
    "Uber",
    "Ola",
    "Rapido",
    "BluSmart",
    "Namma Yatri",
    
    # Bike Taxi
    "Rapido Bike",
    "Ola Bike",
    "Uber Moto",
    
    # Regional / Auto
    "Jugnoo",
    "Meru Cabs",
    "Mega Cabs",
    "Quick Ride",
]

# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def get_all_tech_entities():
    """Returns all tech-related entities"""
    return (
        TECH_COMPANIES +
        SOCIAL_MEDIA_PLATFORMS +
        EMAIL_PROVIDERS +
        GAMING_PLATFORMS +
        GIFT_CARD_BRANDS +
        RIDE_HAILING_APPS
    )

def get_entity_by_category(category):
    """
    Get entities by category
    
    Args:
        category: One of 'tech_company', 'social_media', 'email', 'gaming', 
                 'gift_card', 'ride_hailing', 'all'
    
    Returns:
        List of entities in that category
    """
    categories = {
        'tech_company': TECH_COMPANIES,
        'tech': TECH_COMPANIES,
        'social_media': SOCIAL_MEDIA_PLATFORMS,
        'social': SOCIAL_MEDIA_PLATFORMS,
        'email': EMAIL_PROVIDERS,
        'email_provider': EMAIL_PROVIDERS,
        'gaming': GAMING_PLATFORMS,
        'gaming_platform': GAMING_PLATFORMS,
        'gift_card': GIFT_CARD_BRANDS,
        'gift': GIFT_CARD_BRANDS,
        'ride_hailing': RIDE_HAILING_APPS,
        'ride': RIDE_HAILING_APPS,
        'all': get_all_tech_entities(),
    }
    return categories.get(category.lower(), [])

def get_entity_count_by_category():
    """Returns entity counts for each category"""
    return {
        'tech_companies': len(TECH_COMPANIES),
        'social_media_platforms': len(SOCIAL_MEDIA_PLATFORMS),
        'email_providers': len(EMAIL_PROVIDERS),
        'gaming_platforms': len(GAMING_PLATFORMS),
        'gift_card_brands': len(GIFT_CARD_BRANDS),
        'ride_hailing_apps': len(RIDE_HAILING_APPS),
        'total': len(get_all_tech_entities()),
    }

# =============================================================================
# ENTITY STATISTICS
# =============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("TECH ENTITY STATISTICS")
    print("=" * 70)
    
    stats = get_entity_count_by_category()
    print(f"\nTech Companies: {stats['tech_companies']}")
    print(f"Social Media Platforms: {stats['social_media_platforms']}")
    print(f"Email Providers: {stats['email_providers']}")
    print(f"Gaming Platforms: {stats['gaming_platforms']}")
    print(f"Gift Card Brands: {stats['gift_card_brands']}")
    print(f"Ride-Hailing Apps: {stats['ride_hailing_apps']}")
    print(f"\nTotal Tech Entities: {stats['total']}")
    
    print(f"\n{'=' * 70}")
    print("SAMPLE ENTITIES BY CATEGORY")
    print("=" * 70)
    
    print("\nTech Companies (first 8):")
    for company in TECH_COMPANIES[:8]:
        print(f"  - {company}")
    
    print("\nSocial Media Platforms (first 8):")
    for platform in SOCIAL_MEDIA_PLATFORMS[:8]:
        print(f"  - {platform}")
    
    print("\nEmail Providers (first 6):")
    for provider in EMAIL_PROVIDERS[:6]:
        print(f"  - {provider}")
    
    print("\nGaming Platforms (first 6):")
    for platform in GAMING_PLATFORMS[:6]:
        print(f"  - {platform}")
    
    print("\nGift Card Brands (first 6):")
    for brand in GIFT_CARD_BRANDS[:6]:
        print(f"  - {brand}")
    
    print("\nRide-Hailing Apps (first 6):")
    for app in RIDE_HAILING_APPS[:6]:
        print(f"  - {app}")
    
    print(f"\n{'=' * 70}")
