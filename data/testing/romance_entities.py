"""
Romance and Dating Scam Domain Entities
Used for cross-domain testing of fraud detection models
"""

# Dating platforms
DATING_PLATFORMS = [
    "Tinder", "Bumble", "Match.com", "eHarmony", "OkCupid", "Hinge",
    "Plenty of Fish", "Christian Mingle", "Elite Singles", "Zoosk"
]

# Social media platforms (where scams occur)
SOCIAL_PLATFORMS = [
    "Facebook", "Instagram", "LinkedIn", "TikTok", "Snapchat", "WhatsApp"
]

# Scammer personas/occupations
SCAMMER_OCCUPATIONS = [
    "deployed soldier", "oil rig worker", "international doctor",
    "business owner abroad", "military contractor", "UN peacekeeper",
    "engineer overseas", "diplomat", "merchant marine", "aid worker"
]

# Deployment locations (military scams)
DEPLOYMENT_LOCATIONS = [
    "Afghanistan", "Syria", "Yemen", "South Sudan", "peacekeeping mission",
    "classified location", "overseas base", "special operations"
]

# Emergency types
EMERGENCY_TYPES = [
    "medical emergency", "visa problems", "stranded abroad", "legal troubles",
    "family crisis", "business deal collapsing", "hospital bills",
    "passport stolen", "stuck at customs", "accident expenses"
]

# Payment requests
PAYMENT_METHODS = [
    "Western Union", "MoneyGram", "gift cards", "wire transfer",
    "Bitcoin", "cash app", "Zelle", "Venmo", "bank transfer", "PayPal"
]

# Relationship timelines
RELATIONSHIP_STAGES = [
    "love at first chat", "soulmates", "meant to be together",
    "planning marriage", "want to meet in person", "life partners",
    "true love", "destiny brought us together"
]

# Excuses for not meeting
NO_MEETING_EXCUSES = [
    "deployed overseas", "busy with work project", "visa complications",
    "family emergency", "flight cancelled", "medical issues",
    "financial problems", "passport renewal pending", "quarantine requirements"
]

# Red flag phrases
RED_FLAG_PHRASES = [
    "my love", "darling", "sweetheart" (too soon),
    "need your help", "urgent situation", "prove your love",
    "if you really care", "trust me", "I promise to repay",
    "investment opportunity", "business partner", "send money"
]

# Countries scammers claim to be from
SCAMMER_LOCATIONS = [
    "UK", "USA (overseas)", "Canada", "Australia", "Germany",
    "military base", "oil platform", "construction site abroad"
]

# Investment scam combinations
INVESTMENT_COMBOS = [
    "forex trading opportunity", "cryptocurrency investment",
    "real estate deal", "gold trading", "business partnership",
    "oil and gas investment", "stock trading mentorship"
]

# Visa/travel related
VISA_TRAVEL_FEES = [
    "visa application fee", "embassy processing", "lawyer fees",
    "flight ticket", "hotel deposit", "travel insurance",
    "customs clearance", "airport fees", "medical clearance"
]

# Inheritance/business scams
INHERITANCE_SCHEMES = [
    "family inheritance", "business deal abroad", "frozen bank account",
    "gold inheritance", "estate settlement", "trust fund release",
    "property sale proceeds", "insurance payout"
]

# Medical emergencies
MEDICAL_SCENARIOS = [
    "heart attack", "car accident", "surgery needed", "cancer treatment",
    "COVID-19 complications", "emergency operation", "hospital bills",
    "medical evacuation", "prescription medications"
]

# Gift/package scams
GIFT_SCAMS = [
    "expensive jewelry", "luxury watch", "designer bags", "electronics",
    "money/gold bars", "documents", "inheritance papers"
]

# Customs/shipping fees
CUSTOMS_FEES = [
    "customs clearance fee", "import duty", "storage charges",
    "handling fees", "insurance", "security deposit", "release fee"
]

# Celebrity impersonation
FAKE_CELEBRITIES = [
    "famous actor", "musician", "athlete", "entrepreneur",
    "social media influencer", "business mogul", "TV personality"
]

# Legitimate relationship indicators (for contrast)
LEGITIMATE_RELATIONSHIP_SIGNS = [
    "video calls", "in-person meetings", "mutual friends", "social media presence",
    "no money requests", "gradual progression", "meet family", "shared experiences"
]
