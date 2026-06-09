"""
Lottery & Travel Prize Entity Lists
===================================

This module contains entity lists for lottery, travel, and prize fraud scenarios.
These entities cover travel companies, airlines, lottery shows, car brands, pilgrimage
sites, hotels, banks, and cruise lines.

Entity Categories:
- TRAVEL_COMPANIES: 46 travel agencies and tour operators
- AIRLINE_COMPANIES: 38 Indian and international airlines
- LOTTERY_NAMES: 18 TV shows and lottery brands
- CAR_BRANDS: 28 popular car manufacturers
- PILGRIMAGE_SITES: 24 famous religious sites in India
- HOTEL_NAMES: 35 major hotel chains
- BANK_NAMES: 48 Indian banks
- CRUISE_LINES: 12 cruise companies

Total Entities: 249
"""

# ============================================================================
# TRAVEL COMPANY ENTITIES (46 entities)
# ============================================================================
# Major travel agencies, tour operators, and online travel platforms in India

TRAVEL_COMPANIES = [
    # Online Travel Agencies (OTAs)
    "MakeMyTrip",
    "Yatra.com",
    "Goibibo",
    "Cleartrip",
    "EaseMyTrip",
    "ixigo",
    "Booking.com India",
    "Agoda India",
    "Expedia India",
    "Trivago India",
    
    # Traditional Travel Companies
    "Thomas Cook India",
    "Cox & Kings India",
    "SOTC Travel",
    "Kesari Tours",
    "Veena World",
    "Club Mahindra Holidays",
    "Sterling Holidays",
    "Carnival Tours & Travels",
    
    # Specialized Travel Platforms
    "Thrillophilia",
    "TravelTriangle",
    "Holiday IQ",
    "TrackMyTour",
    "Via.com",
    "Pickyourtrail",
    "WanderOn",
    "Travel Boutique Online",
    
    # Corporate & Luxury Travel
    "Akbar Travels",
    "Riya Travels",
    "Balmer Lawrie",
    "Mercury Travels",
    "JTB India",
    
    # Adventure & Niche Travel
    "Thrillophilia Adventures",
    "India Someday",
    "Enchanting Travels",
    "Greaves India",
    "Travel Corporation India (TCI)",
    
    # Regional Travel Operators
    "Paradise Holidays",
    "Flamingo Travels",
    "Ashoka Tours & Travels",
    "Raj Travels",
    "Sai Travels",
    "Sky Travels",
    "Globe Travels",
    "World Travel Studio",
    "Wanderlust Travels"
]

# ============================================================================
# AIRLINE COMPANY ENTITIES (38 entities)
# ============================================================================
# Indian and international airlines operating in/to India

AIRLINE_COMPANIES = [
    # Indian Airlines
    "Air India",
    "IndiGo Airlines",
    "SpiceJet",
    "Vistara",
    "Go First (Go Air)",
    "AirAsia India",
    "Air India Express",
    "Alliance Air",
    
    # Middle East Airlines
    "Emirates",
    "Qatar Airways",
    "Etihad Airways",
    "Oman Air",
    "Gulf Air",
    "Kuwait Airways",
    "Saudia (Saudi Arabian Airlines)",
    
    # Asian Airlines
    "Singapore Airlines",
    "Thai Airways",
    "Malaysia Airlines",
    "Cathay Pacific",
    "Japan Airlines (JAL)",
    "All Nippon Airways (ANA)",
    "Korean Air",
    "Asiana Airlines",
    
    # European Airlines
    "British Airways",
    "Lufthansa",
    "Air France",
    "KLM Royal Dutch Airlines",
    "Swiss International Air Lines",
    "Turkish Airlines",
    "Finnair",
    
    # American Airlines
    "United Airlines",
    "Delta Air Lines",
    "American Airlines",
    
    # Other International
    "Air Canada",
    "Qantas Airways",
    "Ethiopian Airlines"
]

# ============================================================================
# LOTTERY NAME ENTITIES (18 entities)
# ============================================================================
# Popular TV shows, game shows, and lottery brands in India

LOTTERY_NAMES = [
    # TV Game Shows
    "Kaun Banega Crorepati (KBC)",
    "KBC Lucky Draw",
    "Bigg Boss Lottery",
    "Indian Idol Prize Draw",
    "The Kapil Sharma Show Lottery",
    "Dance India Dance Lucky Draw",
    
    # State Lotteries
    "Kerala State Lottery",
    "Sikkim State Lottery",
    "Nagaland State Lottery",
    "Punjab State Lottery",
    "Goa State Lottery",
    
    # Fantasy Sports (often misused in scams)
    "Dream11 Mega Prize",
    "My11Circle Lucky Winner",
    "MPL (Mobile Premier League) Jackpot",
    
    # Other Prize Draws
    "Tata Sky Lucky Draw",
    "Airtel Mega Prize",
    "Reliance Jio Grand Lottery",
    "Google Lucky User Draw"
]

# ============================================================================
# CAR BRAND ENTITIES (28 entities)
# ============================================================================
# Popular car manufacturers available in India

CAR_BRANDS = [
    # Indian Brands
    "Maruti Suzuki",
    "Tata Motors",
    "Mahindra",
    
    # Japanese Brands
    "Honda",
    "Toyota",
    "Suzuki",
    "Nissan",
    "Datsun",
    "Mitsubishi",
    "Isuzu",
    
    # Korean Brands
    "Hyundai",
    "Kia",
    "MG Motor (Morris Garages)",
    
    # European Brands - Luxury
    "Mercedes-Benz",
    "BMW",
    "Audi",
    "Volkswagen",
    "Skoda",
    "Volvo",
    "Jaguar",
    "Land Rover",
    
    # European Brands - Mass Market
    "Renault",
    "Fiat",
    "Jeep",
    
    # American Brands
    "Ford",
    "Chevrolet",
    
    # French Brands
    "Peugeot",
    "Citroen"
]

# ============================================================================
# PILGRIMAGE SITE ENTITIES (24 entities)
# ============================================================================
# Famous religious and spiritual sites across India

PILGRIMAGE_SITES = [
    # Hindu Pilgrimage Sites
    "Varanasi (Kashi Vishwanath)",
    "Tirupati Balaji",
    "Shirdi Sai Baba Temple",
    "Amarnath Cave",
    "Kedarnath Temple",
    "Badrinath Temple",
    "Jagannath Puri Temple",
    "Dwarka Temple",
    "Somnath Temple",
    "Rameshwaram Temple",
    "Kanyakumari Temple",
    "Meenakshi Temple Madurai",
    "Vaishnodevi Temple",
    "Haridwar",
    "Rishikesh",
    "Ujjain Mahakaleshwar",
    
    # Sikh Pilgrimage Sites
    "Golden Temple (Amritsar)",
    "Hemkund Sahib",
    
    # Muslim Pilgrimage Sites
    "Ajmer Sharif Dargah",
    "Haji Ali Dargah Mumbai",
    
    # Christian Pilgrimage Sites
    "Velankanni Church (Tamil Nadu)",
    "Basilica of Bom Jesus (Goa)",
    
    # Buddhist Pilgrimage Sites
    "Bodh Gaya",
    "Sarnath"
]

# ============================================================================
# HOTEL NAME ENTITIES (35 entities)
# ============================================================================
# Major hotel chains and hospitality brands in India

HOTEL_NAMES = [
    # Indian Luxury Chains
    "Taj Hotels",
    "The Oberoi Hotels",
    "ITC Hotels",
    "The Leela Palaces",
    "Trident Hotels",
    "Vivanta by Taj",
    
    # Indian Mid-Range Chains
    "Lemon Tree Hotels",
    "Treebo Hotels",
    "OYO Rooms",
    "FabHotels",
    "Ginger Hotels",
    "Keys Hotels",
    "Sarovar Hotels",
    "Fortune Hotels",
    
    # International Luxury Chains
    "Marriott Hotels",
    "Hilton Hotels",
    "Hyatt Hotels",
    "InterContinental Hotels",
    "Radisson Hotels",
    "JW Marriott",
    "The Ritz-Carlton",
    "St. Regis Hotels",
    "Westin Hotels",
    
    # International Mid-Range
    "Holiday Inn",
    "Novotel",
    "Ibis Hotels",
    "Best Western",
    "Ramada Hotels",
    
    # Budget Hotels
    "Zostel",
    "Backpacker Panda",
    "goStops",
    "The Hosteller",
    "Moustache Hostel"
]

# ============================================================================
# BANK NAME ENTITIES (48 entities)
# ============================================================================
# Major Indian banks (public sector, private sector, and foreign)

BANK_NAMES = [
    # Public Sector Banks
    "State Bank of India (SBI)",
    "Punjab National Bank (PNB)",
    "Bank of Baroda",
    "Canara Bank",
    "Union Bank of India",
    "Bank of India",
    "Indian Bank",
    "Central Bank of India",
    "Indian Overseas Bank",
    "UCO Bank",
    "Bank of Maharashtra",
    "Punjab & Sind Bank",
    
    # Private Sector Banks
    "HDFC Bank",
    "ICICI Bank",
    "Axis Bank",
    "Kotak Mahindra Bank",
    "IndusInd Bank",
    "Yes Bank",
    "IDFC First Bank",
    "Bandhan Bank",
    "RBL Bank",
    "Federal Bank",
    "South Indian Bank",
    "Karur Vysya Bank",
    "City Union Bank",
    "DCB Bank",
    "Dhanlaxmi Bank",
    "Jammu & Kashmir Bank",
    "Tamilnad Mercantile Bank",
    
    # Small Finance Banks
    "AU Small Finance Bank",
    "Equitas Small Finance Bank",
    "Ujjivan Small Finance Bank",
    "Jana Small Finance Bank",
    "Suryoday Small Finance Bank",
    
    # Payment Banks
    "Paytm Payments Bank",
    "Airtel Payments Bank",
    "India Post Payments Bank",
    "Fino Payments Bank",
    
    # Foreign Banks in India
    "Citibank India",
    "HSBC India",
    "Standard Chartered India",
    "Deutsche Bank India",
    "DBS Bank India",
    "Barclays Bank India",
    "American Express Banking",
    "Royal Bank of Scotland India"
]

# ============================================================================
# CRUISE LINE ENTITIES (12 entities)
# ============================================================================
# Cruise companies operating in India and internationally

CRUISE_LINES = [
    # Indian Cruise Lines
    "Cordelia Cruises",
    "Angriya Cruises",
    "Jalesh Cruises",
    
    # International Cruise Lines (operating to/from India)
    "Royal Caribbean International",
    "Carnival Cruise Line",
    "MSC Cruises",
    "Costa Cruises",
    "Princess Cruises",
    "Norwegian Cruise Line",
    "Celebrity Cruises",
    "Holland America Line",
    "Cunard Line"
]

# ============================================================================
# ENTITY STATISTICS
# ============================================================================

LOTTERY_TRAVEL_ENTITY_STATS = {
    "travel_companies": len(TRAVEL_COMPANIES),
    "airlines": len(AIRLINE_COMPANIES),
    "lottery_names": len(LOTTERY_NAMES),
    "car_brands": len(CAR_BRANDS),
    "pilgrimage_sites": len(PILGRIMAGE_SITES),
    "hotels": len(HOTEL_NAMES),
    "banks": len(BANK_NAMES),
    "cruise_lines": len(CRUISE_LINES),
    "total_entities": (len(TRAVEL_COMPANIES) + len(AIRLINE_COMPANIES) + len(LOTTERY_NAMES) + 
                      len(CAR_BRANDS) + len(PILGRIMAGE_SITES) + len(HOTEL_NAMES) + 
                      len(BANK_NAMES) + len(CRUISE_LINES))
}

# Helper function to get all lottery/travel entities
def get_all_lottery_travel_entities():
    """Return all lottery/travel entities as a single list"""
    return (TRAVEL_COMPANIES + AIRLINE_COMPANIES + LOTTERY_NAMES + CAR_BRANDS + 
            PILGRIMAGE_SITES + HOTEL_NAMES + BANK_NAMES + CRUISE_LINES)

# Verification
if __name__ == "__main__":
    print("=" * 70)
    print("LOTTERY & TRAVEL PRIZE ENTITIES - VERIFICATION REPORT")
    print("=" * 70)
    print()
    
    print("📊 Entity Counts:")
    print(f"   Travel Companies:   {len(TRAVEL_COMPANIES)} entities")
    print(f"   Airlines:           {len(AIRLINE_COMPANIES)} entities")
    print(f"   Lottery Names:      {len(LOTTERY_NAMES)} entities")
    print(f"   Car Brands:         {len(CAR_BRANDS)} entities")
    print(f"   Pilgrimage Sites:   {len(PILGRIMAGE_SITES)} entities")
    print(f"   Hotel Names:        {len(HOTEL_NAMES)} entities")
    print(f"   Bank Names:         {len(BANK_NAMES)} entities")
    print(f"   Cruise Lines:       {len(CRUISE_LINES)} entities")
    print(f"   {'─' * 40}")
    print(f"   TOTAL:              {LOTTERY_TRAVEL_ENTITY_STATS['total_entities']} entities")
    print()
    
    print("✅ Sample Travel Companies:")
    print(f"   {', '.join(TRAVEL_COMPANIES[:5])}")
    print()
    
    print("✅ Sample Airlines:")
    print(f"   {', '.join(AIRLINE_COMPANIES[:5])}")
    print()
    
    print("✅ Sample Lottery Names:")
    print(f"   {', '.join(LOTTERY_NAMES[:3])}")
    print()
    
    print("✅ Sample Car Brands:")
    print(f"   {', '.join(CAR_BRANDS[:5])}")
    print()
    
    print("✅ Sample Pilgrimage Sites:")
    print(f"   {', '.join(PILGRIMAGE_SITES[:5])}")
    print()
    
    print("✅ Sample Hotels:")
    print(f"   {', '.join(HOTEL_NAMES[:5])}")
    print()
    
    print("✅ Sample Banks:")
    print(f"   {', '.join(BANK_NAMES[:5])}")
    print()
    
    print("✅ Sample Cruise Lines:")
    print(f"   {', '.join(CRUISE_LINES[:5])}")
    print()
    
    print("=" * 70)
    print("✅ All lottery & travel entity lists loaded successfully!")
    print("=" * 70)
