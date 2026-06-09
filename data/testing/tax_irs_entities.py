"""
Tax, IRS, and Social Security Scam Domain Entities
Used for cross-domain testing of fraud detection models
"""

# Government agencies (real)
REAL_AGENCIES = [
    "Internal Revenue Service (IRS)", "Social Security Administration (SSA)",
    "Department of Treasury", "Medicare", "Medicaid",
    "Federal Trade Commission (FTC)", "Department of Justice"
]

# Fake agency names
FAKE_AGENCIES = [
    "IRS Criminal Investigation Bureau", "National Tax Authority",
    "Federal Tax Resolution Department", "SSA Fraud Prevention Unit",
    "Treasury Enforcement Division", "Tax Compliance Agency"
]

# IRS scam threats
IRS_THREATS = [
    "arrest warrant", "deportation", "license suspension",
    "wage garnishment", "property seizure", "bank account freeze",
    "criminal charges", "immediate legal action"
]

# Payment methods (fraudulent)
FRAUDULENT_PAYMENT_METHODS = [
    "iTunes gift cards", "Google Play cards", "Amazon gift cards",
    "prepaid debit cards", "wire transfer", "Bitcoin",
    "Western Union", "MoneyGram", "cash reload cards"
]

# Legitimate IRS payment methods
LEGITIMATE_IRS_PAYMENTS = [
    "IRS Direct Pay", "Electronic Federal Tax Payment System (EFTPS)",
    "check to U.S. Treasury", "credit/debit card via approved processor",
    "installment agreement", "Offer in Compromise"
]

# Tax forms
TAX_FORMS = [
    "W-2", "1099", "W-4", "1040", "Schedule C", "8862",
    "SS-4", "941", "990", "1095-A", "5498"
]

# Social Security scam claims
SSA_SCAM_CLAIMS = [
    "SSN suspended", "SSN compromised", "fraudulent activity on SSN",
    "SSN linked to crime", "benefits will be terminated",
    "SSN about to expire", "identity theft on SSN"
]

# Tax refund scam tactics
REFUND_SCAM_TACTICS = [
    "additional refund available", "unclaimed tax credit",
    "stimulus payment", "economic impact payment",
    "verify bank account for refund", "expedited refund processing"
]

# Medicare/Medicaid scams
MEDICARE_SCAMS = [
    "card replacement fee", "new card activation",
    "verify Medicare number", "COVID-19 test billing",
    "free medical equipment", "genetic testing"
]

# Tax preparation scam red flags
TAX_PREP_RED_FLAGS = [
    "guaranteed refund", "inflated deductions", "won't sign return",
    "no PTIN", "fees based on refund amount", "direct deposit to preparer",
    "fake dependents", "false income", "fabricated expenses"
]

# Legitimate tax professionals
LEGITIMATE_TAX_PROS = [
    "CPA (Certified Public Accountant)", "EA (Enrolled Agent)",
    "tax attorney", "PTIN holder", "Annual Filing Season Program participant"
]

# Fake tax credentials
FAKE_TAX_CREDENTIALS = [
    "certified tax consultant", "master tax advisor",
    "tax resolution specialist (unlicensed)", "IRS insider",
    "tax elimination expert"
]

# Phone caller ID spoofing
SPOOFED_CALLER_IDS = [
    "IRS - Washington DC", "Social Security Administration",
    "Department of Treasury", "Federal Tax Bureau",
    "Government Tax Services", "SSA Fraud Department"
]

# Tax scam types
TAX_SCAM_TYPES = [
    "IRS impersonation", "W-2 phishing", "tax identity theft",
    "fake charity deduction", "offshore tax evasion scheme",
    "employment tax credit fraud", "offer in compromise mills"
]

# Red flag phrases
IRS_SCAM_PHRASES = [
    "final notice", "last warning", "immediate action required",
    "law enforcement will arrest you", "send payment today",
    "verify your SSN", "don't hang up", "stay on the line",
    "confirm your identity", "avoid arrest"
]

# Legitimate IRS communication methods
IRS_COMMUNICATION = [
    "mail to taxpayer's address", "certified mail for serious issues",
    "secure online account messages", "in-person visit by Revenue Officer",
    "phone call AFTER mailed notices"
]

# Tax schemes
TAX_SCHEMES = [
    "abusive tax shelter", "syndicated conservation easement",
    "micro-captive insurance", "foreign trust evasion",
    "frivolous tax arguments", "zero wage claim",
    "sovereign citizen theory"
]

# Employment tax credit scams
ETC_SCAM_TACTICS = [
    "guaranteed ERTC eligibility", "no assessment needed",
    "claim even if ineligible", "percentage-based fees",
    "backdating records", "falsifying revenue claims"
]

# Identity theft indicators
IDENTITY_THEFT_SIGNS = [
    "duplicate tax return", "unexpected tax transcript",
    "IRS notice for unknown income", "collection notice for unfamiliar year",
    "letter about online account you didn't create"
]

# Legitimate IRS processes
LEGITIMATE_IRS_PROCESSES = [
    "CP notices by mail", "audit notification by mail",
    "payment plan application", "Offer in Compromise",
    "Innocent Spouse Relief", "Penalty Abatement request",
    "Identity Protection PIN (IP PIN)"
]

# Tax resolution mills (predatory)
TAX_RESOLUTION_MILLS = [
    "Settle for Pennies!", "Stop IRS Now!", "Tax Relief Network",
    "Fresh Start Initiative (fake)", "Resolve Tax Debt Guaranteed"
]

# Offshore account reporting
OFFSHORE_REQUIREMENTS = [
    "FBAR (FinCEN Form 114)", "FATCA (Form 8938)",
    "foreign account reporting", "foreign asset disclosure"
]

# Tax preparer fraud schemes
PREPARER_FRAUD = [
    "ghost preparers (won't sign)", "identity theft mills",
    "fake deduction operations", "refund theft schemes",
    "falsified income documents"
]

# Protective measures
PROTECTIVE_MEASURES = [
    "file early", "use secure tax software", "protect SSN",
    "monitor IRS account", "check credit reports",
    "enable two-factor authentication", "get IP PIN",
    "secure W-2 storage", "shred tax documents"
]

# Verification resources
VERIFICATION_RESOURCES = [
    "IRS.gov official website", "SSA.gov official website",
    "IRS Taxpayer Advocate Service", "Treasury Inspector General",
    "FTC Identity Theft website", "PTIN lookup on IRS.gov"
]

# Seasonal scam peaks
SCAM_SEASONS = [
    "tax filing season (January-April)", "refund season",
    "economic stimulus periods", "benefit enrollment periods",
    "year-end charitable giving", "Medicare open enrollment"
]
