"""
Comprehensive lists of e-commerce entities for fraud detection dataset generation.
These lists prevent overfitting by providing extensive variety across all categories.
"""

# ============================================================================
# E-COMMERCE & MARKETPLACE PLATFORMS (100+ entries)
# ============================================================================

# C2C Marketplaces (Second-hand items, peer-to-peer)
INDIAN_MARKETPLACES = [
    "OLX", "Quikr", "Facebook Marketplace", "IndiaMART", "Sulekha",
    "ClickIndia", "Locanto", "Junglee", "eBay India", "2GUD by Flipkart",
    "Bikroy", "Classifieds India", "IndianListed", "Vivastreet",
    "Khojle", "Adpost", "Cifiyah", "YBrant", "Khaleej Times Classifieds",
    "Shopo", "Zefo", "Elanic", "Cashify Marketplace", "Overcart",
    "Oodle India", "Recycler India", "Gumtree India", "Trovit India",
    "Mitula India", "Nestoria India", "Olx Autos", "Quikr Jobs",
    "IndiaProperty", "99acres Classifieds", "MagicBricks Classifieds"
]

# E-commerce Retail Platforms (B2C - Business to Consumer)
INDIAN_ECOMMERCE_RETAIL = [
    "Amazon India", "Flipkart", "Myntra", "Ajio", "Snapdeal",
    "Tata CLiQ", "Shoppers Stop", "Nykaa", "FirstCry", "Bewakoof",
    "Limeroad", "Pepperfry", "Urban Ladder", "FabIndia", "Max Fashion",
    "Pantaloons", "Westside", "Lifestyle Stores", "Central", "Reliance Digital",
    "Croma", "Vijay Sales", "Poorvika", "Sangeetha Mobiles", "Pai International",
    "Decathlon India", "Titan", "Tanishq", "CaratLane", "BlueStone",
    "Lenskart", "Coolwinks", "John Jacobs", "Clovia", "Jockey",
    "Van Heusen", "Allen Solly", "Peter England", "Louis Philippe", "Park Avenue",
    "W for Woman", "Biba", "Global Desi", "Aurelia", "Libas",
    "Chumbak", "The Souled Store", "Redwolf", "Flying Machine", "Wrogn",
    "HRX by Hrithik Roshan", "Puma India", "Nike India", "Adidas India", "Reebok India",
    "Shopclues", "Paytm Mall", "Club Factory", "ShopUp", "Voonik",
    "StalkBuyLove", "Koovs", "Jabong", "Fynd", "Tata Neu"
]

# Food Delivery Platforms
INDIAN_FOOD_DELIVERY = [
    "Zomato", "Swiggy", "Swiggy Genie", "Domino's India", "Pizza Hut India",
    "McDonald's India", "KFC India", "Subway India", "Burger King India",
    "EatSure", "Box8", "Faasos", "Behrouz Biryani", "Oven Story Pizza",
    "The Bowl Company", "Lunch Box", "Mandarin Oak", "Firangi Bake",
    "Zomato Pro", "Swiggy Super", "Freshmenu", "InnerChef", "HolaChef",
    "Foodpanda India", "UberEats India", "Dunzo Daily", "Thrive"
]

# Quick Commerce / Hyperlocal Delivery (Groceries, essentials)
INDIAN_QUICK_COMMERCE = [
    "Blinkit", "Zepto", "Dunzo", "Swiggy Instamart", "BigBasket",
    "BigBasket Now", "JioMart", "Amazon Fresh", "Amazon Pantry", "Flipkart Quick",
    "Flipkart Supermart", "Grofers (now Blinkit)", "Nature's Basket", "Spencer's",
    "Reliance Fresh", "More Supermarket", "D-Mart Ready", "24Seven",
    "FreshMenu", "Milkbasket", "Country Delight", "Licious", "FreshToHome",
    "BB Daily", "Supr Daily", "DailyNinja", "Doodhwala", "Mr. D Food",
    "Snapdeal Instant", "Shadowfax", "Porter", "LoadShare", "WeFast"
]

# Service Marketplaces (Home services, repairs, professional services)
INDIAN_SERVICE_PLATFORMS = [
    "Urban Company", "UrbanClap", "Sulekha", "Justdial", "Housejoy",
    "Quikr Services", "Zimmber", "MyGate", "NoBroker", "Housing.com Services",
    "99acres Services", "MagicBricks Services", "TaskBob", "Timesaverz",
    "ClickIndia Services", "LocalOye", "ZopNow Services", "Airtasker India",
    "HelpIndia", "Mr. Right", "Urbanpro", "BookMyPainter", "ShiftKarado",
    "Porter Services", "LoadShare Network", "QuikrEasy", "Homezhub"
]

# Budget E-commerce / Reseller Platforms
INDIAN_RESELLER_PLATFORMS = [
    "Meesho", "GlowRoad", "Shop101", "DealShare", "Udaan",
    "Bulbul", "SimSim", "Moj Shop", "ShareChat Moj Shop", "Mall91",
    "CityMall", "Apna", "Khatabook Shop", "OkCredit Marketplace"
]

# Specialized E-commerce
INDIAN_SPECIALIZED_ECOMMERCE = [
    "BookMyShow", "Paytm Insider", "Insider.in", "TicketGenie", "Explara",
    "BookMyForex", "Thomas Cook India", "MakeMyTrip", "Goibibo", "Cleartrip",
    "Yatra", "ixigo", "EaseMyTrip", "Ola", "Uber India",
    "Rapido", "Bounce", "Vogo", "Yulu", "Mobycy",
    "1mg", "PharmEasy", "Netmeds", "Apollo 247", "MedLife",
    "Practo", "DocsApp", "mfine", "Lybrate", "HealthifyMe"
]

# ============================================================================
# PAYMENT METHODS & UPI APPS (50+ entries)
# ============================================================================

INDIAN_UPI_APPS = [
    # Major UPI Apps
    "Google Pay", "PhonePe", "Paytm", "Amazon Pay", "BHIM UPI",
    "WhatsApp Pay", "Mobikwik", "Freecharge", "PayZapp", "BHIM",
    
    # Bank UPI Apps
    "SBI YONO", "HDFC PayZapp", "ICICI iMobile Pay", "Axis Mobile",
    "Kotak 811", "PNB One", "Bank of Baroda M-Connect Plus", "Canara ai1",
    "Union Bank UPI", "IndusInd Bank UPI", "Yes Pay", "IDFC First Bank UPI",
    "Federal Bank FedMobile", "RBL MyCard", "South Indian Bank SIB Mirror+",
    
    # Telecom & Other UPI
    "Airtel Payments Bank", "Jio Pay", "Vodafone M-Pesa", "Idea Money",
    "BSNL Wallet", "Postpe", "Slice", "Jupiter", "Fi Money",
    
    # E-wallet & Others
    "Ola Money", "Uber Cash", "Flipkart SuperCoin", "Amazon Pay Balance",
    "Snapdeal Wallet", "ShopClues Wallet", "Zomato Pay", "Swiggy Money",
    "BookMyShow Wallet", "MakeMyTrip Wallet", "Goibibo GoCash", "Cleartrip Wallet",
    
    # Neobanks & Fintech
    "Niyo", "Razorpay", "Instamojo", "PayU", "CCAvenue",
    "BillDesk", "Citrus Pay", "Simpl", "LazyPay", "ZestMoney"
]

# Traditional Payment Methods
PAYMENT_METHODS = [
    "UPI", "net banking", "debit card", "credit card", "cash on delivery",
    "EMI", "digital wallet", "bank transfer", "NEFT", "RTGS", "IMPS",
    "cheque", "demand draft", "cash", "PayPal", "international card"
]

# ============================================================================
# PRODUCT CATEGORIES (200+ items across categories)
# ============================================================================

# Electronics
ELECTRONICS_ITEMS = [
    # Mobile & Accessories
    "mobile phone", "smartphone", "iPhone", "Android phone", "feature phone",
    "mobile cover", "phone case", "tempered glass", "screen protector", "power bank",
    "charging cable", "USB cable", "Type-C cable", "Lightning cable", "charger",
    "wireless charger", "earphones", "headphones", "Bluetooth earbuds", "AirPods",
    "smartwatch", "fitness band", "smart band", "Apple Watch", "Galaxy Watch",
    
    # Computers & Laptops
    "laptop", "gaming laptop", "MacBook", "desktop computer", "PC",
    "computer monitor", "LED monitor", "gaming monitor", "keyboard", "wireless keyboard",
    "mouse", "gaming mouse", "wireless mouse", "webcam", "laptop stand",
    "laptop bag", "laptop charger", "RAM", "SSD", "hard disk", "external hard drive",
    "pen drive", "USB flash drive", "graphics card", "motherboard", "processor",
    
    # TV & Entertainment
    "LED TV", "smart TV", "4K TV", "television", "TV remote", "Fire TV Stick",
    "Chromecast", "Android TV box", "set-top box", "DTH connection", "home theatre",
    "soundbar", "speaker", "Bluetooth speaker", "JBL speaker", "Alexa Echo",
    "Google Home", "smart speaker", "gaming console", "PlayStation", "Xbox",
    "Nintendo Switch", "VR headset", "projector", "home projector",
    
    # Camera & Photography
    "DSLR camera", "mirrorless camera", "digital camera", "action camera", "GoPro",
    "webcam", "camera lens", "tripod", "camera bag", "memory card", "SD card",
    "camera battery", "camera charger", "drone", "photography equipment",
    
    # Other Electronics
    "tablet", "iPad", "Kindle", "e-reader", "calculator", "scientific calculator",
    "smart home device", "router", "WiFi router", "modem", "range extender",
    "printer", "scanner", "3D printer", "laminator", "shredder"
]

# Home Appliances
HOME_APPLIANCES = [
    # Kitchen Appliances
    "refrigerator", "fridge", "double door fridge", "single door fridge", "mini fridge",
    "washing machine", "front load washing machine", "top load washing machine",
    "microwave", "microwave oven", "OTG", "oven", "toaster", "sandwich maker",
    "mixer grinder", "juicer", "blender", "hand blender", "food processor",
    "induction cooktop", "gas stove", "electric stove", "chimney", "kitchen chimney",
    "water purifier", "RO purifier", "water filter", "electric kettle", "kettle",
    "rice cooker", "pressure cooker", "electric cooker", "air fryer", "coffee maker",
    "dishwasher", "dish dryer", "vegetable chopper",
    
    # Climate Control
    "air conditioner", "AC", "split AC", "window AC", "portable AC", "air cooler",
    "desert cooler", "tower fan", "ceiling fan", "table fan", "pedestal fan",
    "exhaust fan", "room heater", "water heater", "geyser", "instant geyser",
    "electric heater", "halogen heater", "oil-filled radiator", "humidifier", "dehumidifier",
    
    # Cleaning Appliances
    "vacuum cleaner", "robot vacuum", "wet and dry vacuum", "steam cleaner",
    "iron", "steam iron", "dry iron", "ironing board", "garment steamer",
    
    # Other Home Appliances
    "voltage stabilizer", "inverter", "UPS", "generator", "solar panel",
    "water pump", "submersible pump", "bore pump", "motor pump"
]

# Furniture
FURNITURE_ITEMS = [
    # Living Room
    "sofa", "sofa set", "3-seater sofa", "2-seater sofa", "L-shaped sofa",
    "recliner", "recliner chair", "bean bag", "pouf", "ottoman",
    "coffee table", "center table", "side table", "TV unit", "TV stand",
    "showcase", "display cabinet", "bookshelf", "wall shelf", "corner shelf",
    "shoe rack", "shoe cabinet", "magazine rack", "coat stand",
    
    # Bedroom
    "bed", "king size bed", "queen size bed", "single bed", "double bed",
    "bunk bed", "divan bed", "bed frame", "mattress", "memory foam mattress",
    "wardrobe", "3-door wardrobe", "2-door wardrobe", "sliding wardrobe",
    "chest of drawers", "bedside table", "nightstand", "dressing table",
    "study table", "computer table", "laptop table", "writing desk",
    
    # Dining
    "dining table", "dining set", "4-seater dining table", "6-seater dining table",
    "dining chair", "bar stool", "high chair", "folding chair",
    
    # Office
    "office chair", "ergonomic chair", "executive chair", "office desk",
    "filing cabinet", "storage cabinet", "locker", "conference table",
    
    # Other Furniture
    "swing", "garden swing", "outdoor furniture", "camping chair", "folding table"
]

# Fashion & Clothing
FASHION_ITEMS = [
    # Men's Clothing
    "shirt", "t-shirt", "polo shirt", "formal shirt", "casual shirt",
    "jeans", "trousers", "chinos", "shorts", "track pants", "joggers",
    "suit", "blazer", "jacket", "leather jacket", "denim jacket", "hoodie",
    "sweater", "cardigan", "sweatshirt", "kurta", "sherwani", "ethnic wear",
    
    # Women's Clothing
    "saree", "lehenga", "salwar kameez", "kurti", "palazzo", "dupatta",
    "dress", "maxi dress", "midi dress", "gown", "anarkali", "churidar",
    "top", "tunic", "blouse", "crop top", "tank top", "western wear",
    "skirt", "jeans", "jeggings", "leggings", "tights", "shorts",
    "jacket", "blazer", "shrug", "cardigan", "ethnic jacket",
    
    # Footwear
    "shoes", "sneakers", "sports shoes", "running shoes", "casual shoes",
    "formal shoes", "loafers", "boat shoes", "sandals", "slippers",
    "flip-flops", "floaters", "heels", "high heels", "wedges", "pumps",
    "boots", "ankle boots", "Chelsea boots", "kolhapuri chappal",
    
    # Accessories
    "watch", "smartwatch", "analog watch", "digital watch", "wrist watch",
    "sunglasses", "eyeglasses", "reading glasses", "belt", "leather belt",
    "wallet", "purse", "handbag", "shoulder bag", "tote bag", "backpack",
    "sling bag", "clutch", "laptop bag", "travel bag", "duffel bag",
    "cap", "hat", "scarf", "stole", "tie", "bow tie", "cufflinks",
    "bracelet", "necklace", "earrings", "ring", "pendant", "chain",
    
    # Kids
    "kids clothing", "baby clothes", "kids shoes", "school uniform", "frock"
]

# Vehicles & Accessories
VEHICLE_ITEMS = [
    "bicycle", "cycle", "mountain bike", "road bike", "hybrid cycle",
    "electric cycle", "kids cycle", "BMX", "folding cycle",
    "motorcycle", "bike", "scooter", "scooty", "moped", "electric scooter",
    "car", "sedan", "hatchback", "SUV", "MUV", "electric car",
    "helmet", "bike helmet", "full-face helmet", "half-face helmet",
    "bike accessories", "car accessories", "bike cover", "car cover",
    "car seat cover", "steering wheel cover", "floor mat", "car charger",
    "dashcam", "GPS device", "tyre", "alloy wheel", "battery",
    "bike lock", "cycle lock", "bike stand", "cycle carrier"
]

# Books & Stationery
BOOKS_STATIONERY = [
    "book", "novel", "textbook", "notebook", "register", "diary",
    "planner", "calendar", "pen", "ballpoint pen", "gel pen", "fountain pen",
    "pencil", "mechanical pencil", "eraser", "sharpener", "ruler",
    "compass", "protractor", "calculator", "stapler", "punch machine",
    "file folder", "binder", "paper clips", "sticky notes", "highlighter",
    "marker", "whiteboard marker", "permanent marker", "crayon", "color pencil",
    "sketchbook", "drawing book", "art supplies", "painting kit"
]

# Sports & Fitness
SPORTS_FITNESS = [
    "treadmill", "exercise bike", "elliptical trainer", "cross trainer",
    "gym equipment", "dumbbell set", "weight plates", "barbell", "kettlebell",
    "resistance band", "yoga mat", "yoga block", "foam roller",
    "cricket bat", "cricket ball", "cricket kit", "stumps", "helmet",
    "football", "basketball", "volleyball", "tennis ball", "tennis racket",
    "badminton racket", "shuttlecock", "table tennis bat", "carrom board",
    "chess board", "gym bag", "sports bag", "water bottle", "sipper",
    "fitness tracker", "heart rate monitor", "skipping rope", "hula hoop"
]

# Baby & Kids Products
BABY_KIDS_ITEMS = [
    "baby stroller", "pram", "baby walker", "baby carrier", "car seat",
    "baby crib", "cradle", "baby cot", "high chair", "feeding chair",
    "baby rocker", "baby swing", "play mat", "activity gym", "playpen",
    "baby monitor", "diaper bag", "baby clothes", "baby toys", "soft toys",
    "educational toys", "building blocks", "puzzle", "board game", "video game",
    "doll", "action figure", "toy car", "remote control car", "tricycle"
]

# Pet Supplies
PET_SUPPLIES = [
    "dog food", "cat food", "pet food", "pet bowl", "pet bed",
    "pet cage", "dog leash", "collar", "pet toys", "cat litter",
    "aquarium", "fish tank", "fish food", "bird cage", "pet carrier"
]

# Garden & Outdoor
GARDEN_OUTDOOR = [
    "plant", "indoor plant", "outdoor plant", "flower pot", "planter",
    "gardening tools", "garden hose", "watering can", "lawn mower",
    "camping tent", "sleeping bag", "camping gear", "outdoor chair"
]

# Musical Instruments
MUSICAL_INSTRUMENTS = [
    "guitar", "acoustic guitar", "electric guitar", "bass guitar",
    "keyboard", "piano", "digital piano", "harmonium", "tabla",
    "drum set", "drums", "flute", "violin", "ukulele", "saxophone"
]

# ============================================================================
# FRAUD TECHNIQUES & SCAM TYPES
# ============================================================================

FRAUD_TECHNIQUES = [
    "QR code scam", "fake payment screenshot", "overpayment scam",
    "remote access scam", "AnyDesk scam", "TeamViewer scam",
    "OTP theft", "UPI PIN theft", "password phishing",
    "fake refund process", "fake delivery agent", "fake customer support",
    "advance fee scam", "token money scam", "verification fee scam",
    "prize/lottery scam", "cashback scam", "reward points scam",
    "KYC update scam", "account verification scam", "SIM swap scam",
    "identity theft", "Aadhaar theft", "PAN card theft",
    "fake website redirect", "phishing link", "malicious app install",
    "social engineering", "trust building scam", "impersonation",
    "urgency creation", "threat of legal action", "fake order cancellation",
    "fake job offer", "task-based scam", "data breach exploitation"
]

# ============================================================================
# SCAMMER IDENTITIES & ROLES
# ============================================================================

SCAMMER_ROLES = [
    "customer support agent", "delivery agent", "technical support",
    "refund department", "verification team", "KYC team",
    "fraud prevention team", "risk management", "accounts department",
    "logistics team", "dispatch team", "warehouse team",
    "quality check team", "seller support", "buyer support",
    "payment gateway team", "bank representative", "courier company",
    "customs officer", "legal department", "collections team",
    "marketing team", "promotional team", "loyalty program team",
    "Army officer", "police officer", "government official",
    "verified buyer", "verified seller", "premium member"
]

# ============================================================================
# LEGITIMATE ACTIONS (For Normal Scenarios)
# ============================================================================

LEGITIMATE_ACTIONS = [
    "address confirmation", "delivery schedule", "order status update",
    "feedback collection", "review request", "rating request",
    "return/exchange process", "refund status", "order tracking",
    "payment confirmation", "transaction verification", "delivery OTP",
    "product information", "specification inquiry", "availability check",
    "price negotiation", "bulk order inquiry", "custom order request",
    "warranty information", "installation service", "after-sales support",
    "complaint resolution", "issue escalation", "service request"
]

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def get_all_platforms():
    """Get all e-commerce platforms combined."""
    return (INDIAN_MARKETPLACES + INDIAN_ECOMMERCE_RETAIL + 
            INDIAN_FOOD_DELIVERY + INDIAN_QUICK_COMMERCE + 
            INDIAN_SERVICE_PLATFORMS + INDIAN_RESELLER_PLATFORMS + 
            INDIAN_SPECIALIZED_ECOMMERCE)

def get_all_products():
    """Get all product categories combined."""
    return (ELECTRONICS_ITEMS + HOME_APPLIANCES + FURNITURE_ITEMS + 
            FASHION_ITEMS + VEHICLE_ITEMS + BOOKS_STATIONERY + 
            SPORTS_FITNESS + BABY_KIDS_ITEMS + PET_SUPPLIES + 
            GARDEN_OUTDOOR + MUSICAL_INSTRUMENTS)

def get_platform_by_type(platform_type: str) -> list:
    """Get platforms filtered by type."""
    mapping = {
        "MARKETPLACE": INDIAN_MARKETPLACES,
        "ECOMMERCE": INDIAN_ECOMMERCE_RETAIL,
        "FOOD_DELIVERY": INDIAN_FOOD_DELIVERY,
        "QUICK_COMMERCE": INDIAN_QUICK_COMMERCE,
        "SERVICE": INDIAN_SERVICE_PLATFORMS,
        "RESELLER": INDIAN_RESELLER_PLATFORMS,
        "SPECIALIZED": INDIAN_SPECIALIZED_ECOMMERCE
    }
    return mapping.get(platform_type, get_all_platforms())

# ============================================================================
# STATISTICS
# ============================================================================

if __name__ == "__main__":
    print("=" * 80)
    print("E-COMMERCE ENTITIES STATISTICS")
    print("=" * 80)
    print(f"Marketplaces (C2C): {len(INDIAN_MARKETPLACES)}")
    print(f"E-commerce Retail (B2C): {len(INDIAN_ECOMMERCE_RETAIL)}")
    print(f"Food Delivery: {len(INDIAN_FOOD_DELIVERY)}")
    print(f"Quick Commerce: {len(INDIAN_QUICK_COMMERCE)}")
    print(f"Service Platforms: {len(INDIAN_SERVICE_PLATFORMS)}")
    print(f"Reseller Platforms: {len(INDIAN_RESELLER_PLATFORMS)}")
    print(f"Specialized E-commerce: {len(INDIAN_SPECIALIZED_ECOMMERCE)}")
    print(f"\nTotal Platforms: {len(get_all_platforms())}")
    print(f"\nUPI Apps: {len(INDIAN_UPI_APPS)}")
    print(f"Payment Methods: {len(PAYMENT_METHODS)}")
    print(f"\nElectronics: {len(ELECTRONICS_ITEMS)}")
    print(f"Home Appliances: {len(HOME_APPLIANCES)}")
    print(f"Furniture: {len(FURNITURE_ITEMS)}")
    print(f"Fashion: {len(FASHION_ITEMS)}")
    print(f"Vehicles: {len(VEHICLE_ITEMS)}")
    print(f"Books & Stationery: {len(BOOKS_STATIONERY)}")
    print(f"Sports & Fitness: {len(SPORTS_FITNESS)}")
    print(f"Baby & Kids: {len(BABY_KIDS_ITEMS)}")
    print(f"Pet Supplies: {len(PET_SUPPLIES)}")
    print(f"Garden & Outdoor: {len(GARDEN_OUTDOOR)}")
    print(f"Musical Instruments: {len(MUSICAL_INSTRUMENTS)}")
    print(f"\nTotal Products: {len(get_all_products())}")
    print(f"\nFraud Techniques: {len(FRAUD_TECHNIQUES)}")
    print(f"Scammer Roles: {len(SCAMMER_ROLES)}")
    print(f"Legitimate Actions: {len(LEGITIMATE_ACTIONS)}")
    print("=" * 80)
    print(f"\nTOTAL UNIQUE ENTITIES: {len(get_all_platforms()) + len(INDIAN_UPI_APPS) + len(get_all_products())}")
    print("=" * 80)
