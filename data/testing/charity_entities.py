"""
Charity and Donation Fraud Domain Entities
Used for cross-domain testing of fraud detection models
"""

# Types of disasters (real and fabricated)
DISASTERS = [
    "hurricane", "earthquake", "wildfire", "flood", "tornado",
    "tsunami", "volcanic eruption", "drought", "famine", "landslide"
]

# Disaster locations
DISASTER_LOCATIONS = [
    "Gulf Coast", "California", "Florida", "Texas", "Puerto Rico",
    "Haiti", "Philippines", "Indonesia", "Nepal", "Turkey"
]

# Fake charity names
FAKE_CHARITIES = [
    "American Disaster Relief Fund", "Global Children's Foundation",
    "Veterans Support Network", "Cancer Research Alliance", "Save the Ocean Foundation",
    "International Food Bank", "Hope for Tomorrow", "Care for America",
    "United Relief Fund", "National Emergency Response"
]

# Real charity names (for comparison)
REAL_CHARITIES = [
    "American Red Cross", "Salvation Army", "UNICEF", "Doctors Without Borders",
    "Habitat for Humanity", "St. Jude Children's Hospital", "Feeding America"
]

# Charity types
CHARITY_CATEGORIES = [
    "disaster relief", "medical research", "veterans support", "children's welfare",
    "animal rescue", "environmental conservation", "homeless assistance",
    "education support", "religious mission", "international aid"
]

# Medical conditions (for medical charity scams)
MEDICAL_CONDITIONS = [
    "cancer", "heart disease", "rare genetic disorder", "organ transplant",
    "pediatric illness", "PTSD treatment", "addiction recovery",
    "mental health services", "diabetes care", "disability support"
]

# Veterans-related causes
VETERANS_CAUSES = [
    "homeless veterans", "PTSD counseling", "service dog programs",
    "job placement", "housing assistance", "medical care",
    "disability benefits support", "family support", "suicide prevention"
]

# Animal-related causes
ANIMAL_CAUSES = [
    "abused animals", "shelter operations", "veterinary care",
    "rescue operations", "wildlife conservation", "endangered species",
    "spay/neuter programs", "adoption services"
]

# Children-related causes
CHILDREN_CAUSES = [
    "orphan care", "education scholarships", "school supplies",
    "medical treatment", "food programs", "clean water",
    "abuse prevention", "literacy programs", "after-school programs"
]

# Environmental causes
ENVIRONMENTAL_CAUSES = [
    "tree planting", "ocean cleanup", "rainforest protection",
    "endangered species", "climate change", "pollution reduction",
    "renewable energy", "habitat restoration"
]

# Religious organizations (fake)
FAKE_RELIGIOUS_ORGS = [
    "First Baptist Church Relief Fund", "St. Michael's Mission",
    "Global Christian Outreach", "Faith-Based Disaster Response",
    "Church of Compassion", "United Methodist Relief"
]

# Payment pressure tactics
PRESSURE_TACTICS = [
    "matching donations expire tonight", "limited time double impact",
    "urgent need", "immediate crisis", "tax deduction deadline",
    "goal almost reached", "every dollar counts", "make a difference now"
]

# Suspicious payment methods
SUSPICIOUS_PAYMENTS = [
    "wire transfer", "gift cards", "cryptocurrency", "cash only",
    "money order", "Western Union", "MoneyGram", "Zelle to personal account"
]

# Legitimate payment methods
LEGITIMATE_PAYMENTS = [
    "credit card", "check to organization", "PayPal to verified charity",
    "donor-advised fund", "stock donation", "IRA charitable rollover"
]

# Red flags in charity appeals
RED_FLAGS = [
    "no tax ID number", "gift card payment", "pressure tactics",
    "can't verify online", "no physical address", "spelling errors",
    "similar name to real charity", "no financial disclosure"
]

# Legitimate charity verification
VERIFICATION_SOURCES = [
    "Charity Navigator", "GuideStar", "BBB Wise Giving Alliance",
    "IRS Tax Exempt Organization Search", "state charity registry"
]

# Fundraising platforms
FUNDRAISING_PLATFORMS = [
    "GoFundMe", "Kickstarter", "Indiegogo", "Facebook Fundraisers",
    "JustGiving", "Crowdrise", "DonorsChoose", "Patreon"
]

# Scammer tactics
SCAM_TACTICS = [
    "emotional manipulation", "fake photos", "urgency pressure",
    "mimics real charity", "unverifiable claims", "no registration",
    "vague fund usage", "no receipts", "high administration costs"
]

# Legitimate charity practices
LEGITIMATE_PRACTICES = [
    "501(c)(3) status", "EIN number provided", "tax receipts",
    "annual reports", "financial transparency", "board of directors",
    "program details", "impact reports", "third-party verification"
]

# Telemarketing red flags
TELEMARKETING_RED_FLAGS = [
    "aggressive tactics", "immediate payment demand", "officer safety claims",
    "implies obligation", "won't send information", "pressure callbacks"
]

# Police/Fire fund scams
FIRST_RESPONDER_SCAMS = [
    "Police Benevolent Association", "Firefighters Support Fund",
    "Officer Safety Equipment", "Fallen Heroes Memorial",
    "First Responders Alliance", "Law Enforcement Charity"
]
