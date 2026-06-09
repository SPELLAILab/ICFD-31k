"""
Conversation generation utilities using Groq API.
"""

import json
import random
import asyncio
import re
from typing import Dict, Any
from datetime import datetime
import groq
from rich.console import Console

from config.settings import (
    GROQ_MODEL, API_TEMPERATURE, MAX_TOKENS,
    MIN_CONVERSATION_DURATION, MAX_CONVERSATION_DURATION,
    MAX_RETRIES, RETRY_DELAY_SECONDS, EXPONENTIAL_BACKOFF,
    API_TIMEOUT
)

# Import e-commerce entities for placeholder replacement
try:
    import sys
    from pathlib import Path
    
    # Add project root to path if not already there
    project_root = Path(__file__).parent.parent.parent
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))
    
    from data.entities.ecommerce_entities import (
        INDIAN_MARKETPLACES, INDIAN_ECOMMERCE_RETAIL, INDIAN_FOOD_DELIVERY,
        INDIAN_QUICK_COMMERCE, INDIAN_SERVICE_PLATFORMS, INDIAN_RESELLER_PLATFORMS,
        INDIAN_SPECIALIZED_ECOMMERCE, INDIAN_UPI_APPS, PAYMENT_METHODS,
        ELECTRONICS_ITEMS, HOME_APPLIANCES, FURNITURE_ITEMS, FASHION_ITEMS,
        VEHICLE_ITEMS, BOOKS_STATIONERY, SPORTS_FITNESS, BABY_KIDS_ITEMS,
        PET_SUPPLIES, GARDEN_OUTDOOR, MUSICAL_INSTRUMENTS,
        get_all_platforms, get_all_products, get_platform_by_type
    )
    ECOMMERCE_ENTITIES_AVAILABLE = True
except ImportError as e:
    ECOMMERCE_ENTITIES_AVAILABLE = False
    print(f"Warning: E-commerce entities not available: {e}")

# Import utility entities for placeholder replacement
try:
    from data.entities.utility_entities import (
        STATE_ELECTRICITY_BOARDS, MOBILE_CARRIERS, INTERNET_PROVIDERS,
        GAS_AGENCIES, DTH_PROVIDERS, WATER_SUPPLY_DEPARTMENTS,
        GOVERNMENT_SCHEMES, GAS_REGULATORY_AUTHORITIES,
        TELECOM_REGULATORY_AUTHORITIES, ELECTRICITY_REGULATORY_AUTHORITIES,
        get_all_utility_providers, get_provider_by_type
    )
    UTILITY_ENTITIES_AVAILABLE = True
except ImportError as e:
    UTILITY_ENTITIES_AVAILABLE = False
    print(f"Warning: Utility entities not available: {e}")

# Import job entities for placeholder replacement
try:
    from data.entities.job_entities import (
        IT_COMPANIES, MNC_COMPANIES, JOB_PORTALS,
        GOVERNMENT_DEPARTMENTS, AIRLINE_COMPANIES,
        get_all_job_entities, get_entity_by_category
    )
    JOB_ENTITIES_AVAILABLE = True
except ImportError as e:
    JOB_ENTITIES_AVAILABLE = False
    print(f"Warning: Job entities not available: {e}")

# Import loan entities for placeholder replacement
try:
    from data.entities.loan_entities import (
        PREDATORY_LENDING_APPS, LEGITIMATE_LENDING_APPS,
        NBFC_COMPANIES, MICROFINANCE_INSTITUTIONS, CREDIT_BUREAUS,
        get_all_lending_apps, get_all_loan_entities
    )
    LOAN_ENTITIES_AVAILABLE = True
except ImportError as e:
    LOAN_ENTITIES_AVAILABLE = False
    print(f"Warning: Loan entities not available: {e}")

# Import tech entities for placeholder replacement
try:
    from data.entities.tech_entities import (
        TECH_COMPANIES, SOCIAL_MEDIA_PLATFORMS, EMAIL_PROVIDERS,
        GAMING_PLATFORMS, GIFT_CARD_BRANDS, RIDE_HAILING_APPS,
        get_all_tech_entities, get_entity_by_category as get_tech_entity_by_category
    )
    TECH_ENTITIES_AVAILABLE = True
except ImportError as e:
    TECH_ENTITIES_AVAILABLE = False
    print(f"Warning: Tech entities not available: {e}")

# Emergency entities for personal crisis fraud scenarios
try:
    from data.entities.emergency_entities import (
        FAMILY_MEMBERS, HOSPITAL_NAMES, INDIAN_CITIES, NGO_NAMES
    )
    EMERGENCY_ENTITIES_AVAILABLE = True
except ImportError as e:
    EMERGENCY_ENTITIES_AVAILABLE = False
    print(f"Warning: Emergency entities not available: {e}")

# Healthcare entities for insurance fraud scenarios
try:
    from data.entities.healthcare_entities import (
        INSURANCE_COMPANIES, GOVERNMENT_SCHEMES, INSURANCE_MARKETPLACES, DISEASE_NAMES
    )
    HEALTHCARE_ENTITIES_AVAILABLE = True
except ImportError as e:
    HEALTHCARE_ENTITIES_AVAILABLE = False
    print(f"Warning: Healthcare entities not available: {e}")

# Lottery & Travel entities for prize fraud scenarios
try:
    from data.entities.lottery_travel_entities import (
        TRAVEL_COMPANIES, AIRLINE_COMPANIES, LOTTERY_NAMES, CAR_BRANDS,
        PILGRIMAGE_SITES, HOTEL_NAMES, BANK_NAMES, CRUISE_LINES
    )
    LOTTERY_TRAVEL_ENTITIES_AVAILABLE = True
except ImportError as e:
    LOTTERY_TRAVEL_ENTITIES_AVAILABLE = False
    print(f"Warning: Lottery/Travel entities not available: {e}")

# Government entities for govt impersonation fraud scenarios
try:
    from data.entities.government_entities import GOVERNMENT_DEPT
    GOVERNMENT_ENTITIES_AVAILABLE = True
except ImportError as e:
    GOVERNMENT_ENTITIES_AVAILABLE = False
    print(f"Warning: Government entities not available: {e}")

# Indian names for authentic context in conversations - 500+ diverse names from all regions
INDIAN_NAMES = [
    # North Indian names (Hindi-speaking regions)
    "Rohan Sharma", "Priya Patel", "Vikram Singh", "Anjali Rao", "Aditya Kumar", "Saanvi Gupta", 
    "Arjun Reddy", "Diya Mehta", "Rahul Verma", "Kavya Joshi", "Karan Malhotra", "Riya Kapoor",
    "Ankit Agarwal", "Neha Sharma", "Siddharth Bhatia", "Ishita Gupta", "Varun Khanna", "Ananya Singh",
    "Ayush Pandey", "Pooja Mishra", "Nikhil Saxena", "Shreya Tiwari", "Rajat Arora", "Tanvi Chopra",
    "Harsh Jain", "Meera Bansal", "Kunal Mittal", "Aarohi Sinha", "Aryan Kohli", "Nidhi Bajaj",
    
    # South Indian names (Tamil, Telugu, Kannada, Malayalam)
    "Karthik Krishnan", "Divya Iyer", "Suresh Menon", "Lakshmi Nair", "Raj Subramanian", "Priya Raman",
    "Arun Kumar", "Deepa Venkatesh", "Srikanth Reddy", "Anitha Prasad", "Venkat Narayanan", "Sangeetha Murthy",
    "Murali Krishna", "Sowmya Balaji", "Ramesh Naidu", "Madhavi Rao", "Krishna Mohan", "Vidya Srinivas",
    "Balaji Natarajan", "Kavitha Ramesh", "Harish Gowda", "Bhavana Hegde", "Naveen Shetty", "Poornima Bhat",
    "Ganesh Kumar", "Shwetha Reddy", "Mahesh Babu", "Pavithra Nair", "Ravi Shankar", "Yamuna Devi",
    "Srinivas Rao", "Uma Maheshwari", "Prakash Pillai", "Lalitha Kumari", "Jagadish Gowda", "Radha Krishna",
    "Venu Gopal", "Jayalakshmi Reddy", "Mohan Das", "Savitri Menon", "Bhaskar Rao", "Sarada Iyer",
    
    # West Indian names (Marathi, Gujarati)
    "Omkar Deshmukh", "Sanjana Kulkarni", "Rohit Patil", "Sneha Pawar", "Akash Joshi", "Manasi Deshpande",
    "Pratik Shah", "Ketaki Bhatt", "Yash Mehta", "Aditi Thakkar", "Nitin Patel", "Kajal Modi",
    "Saurabh Parikh", "Riddhi Desai", "Kiran Dave", "Nisha Trivedi", "Vinay Joshi", "Smita Sheth",
    "Abhishek Rao", "Pallavi Nene", "Gaurav Wagh", "Ashwini Kadam", "Tejas Mahajan", "Rupali Naik",
    "Mangesh Phadke", "Shilpa Ghosh", "Ameya Kulkarni", "Vrushali Patwardhan", "Sachin Gokhale", "Varsha Sawant",
    
    # East Indian names (Bengali, Odia, Assamese)
    "Arnab Chatterjee", "Ritu Banerjee", "Sourav Das", "Moumita Sen", "Avik Ghosh", "Suman Mukherjee",
    "Debashish Roy", "Shreya Chakraborty", "Rajiv Bose", "Tanusree Dutta", "Anirban Sarkar", "Payal Sinha",
    "Subham Mazumdar", "Pritha Bhattacharya", "Sanjay Dey", "Mitali Sengupta", "Kaushik Ganguly", "Aparajita Roy",
    "Biswajit Nath", "Jhilmil Sarma", "Partha Dasgupta", "Debjani Majumdar", "Santanu Pal", "Mohua Biswas",
    "Aniket Saha", "Rituparna Mitra", "Tapan Bhowmik", "Sreya Chowdhury", "Bhaskar Kar", "Tumpa Das",
    
    # Punjabi names
    "Harpreet Singh", "Jasleen Kaur", "Gurpreet Singh", "Mandeep Kaur", "Ranveer Singh", "Simran Kaur",
    "Jaspreet Singh", "Navjot Kaur", "Balvir Singh", "Rajwinder Kaur", "Kuldeep Singh", "Harleen Kaur",
    "Amrit Singh", "Kirandeep Kaur", "Tejinder Singh", "Prabhjot Kaur", "Lakhwinder Singh", "Gagandeep Kaur",
    "Surinder Singh", "Jaswinder Kaur", "Paramjit Singh", "Sukhwinder Kaur", "Avtar Singh", "Ravinder Kaur",
    
    # Additional diverse names across regions
    "Roshan Kumar", "Meenakshi Sundaram", "Dhruv Shetty", "Bhagyashree Kulkarni", "Samir Ghosh", "Uttara Hegde",
    "Chirag Patel", "Nandini Reddy", "Tarun Khanna", "Manisha Jain", "Shashank Rao", "Gayatri Iyer",
    "Vishal Agarwal", "Rekha Nair", "Sameer Sinha", "Vandana Sharma", "Praveen Kumar", "Archana Menon",
    "Akshay Verma", "Sonali Deshmukh", "Manoj Bhatia", "Devika Prasad", "Sagar Patil", "Preeti Malhotra",
    "Jatin Mittal", "Ashwini Reddy", "Rajesh Gupta", "Swati Bansal", "Amol Joshi", "Rupal Shah",
    
    # Modern urban names
    "Aarav Mehta", "Aadhya Singh", "Vihaan Sharma", "Diya Patel", "Arjun Kapoor", "Sara Khan",
    "Reyansh Gupta", "Anvi Reddy", "Advait Kumar", "Myra Iyer", "Shaurya Verma", "Kiara Joshi",
    "Vivaan Malhotra", "Aanya Desai", "Atharv Agarwal", "Navya Sinha", "Ishaan Chopra", "Pari Mehta",
    
    # Traditional names
    "Gopal Krishna", "Sita Devi", "Ram Prasad", "Durga Bai", "Vishnu Murthy", "Parvati Amma",
    "Shiv Shankar", "Laxmi Bai", "Ganesh Prasad", "Saraswati Devi", "Hanuman Das", "Kali Devi",
    "Brahma Dev", "Kamala Devi", "Indra Kumar", "Lakshmi Devi", "Surya Prakash", "Chandra Kala",
    
    # Additional North Indian
    "Abhay Thakur", "Aditi Rana", "Aman Bhardwaj", "Anushka Chauhan", "Arpit Sachdeva", "Bhavna Dhillon",
    "Chetan Saini", "Deepak Rawat", "Ekta Vohra", "Gaurav Oberoi", "Himanshu Garg", "Jyoti Nagpal",
    "Kartik Sethi", "Lalit Khurana", "Mohit Dua", "Naina Bhalla", "Pankaj Tandon", "Ritika Bawa",
    "Sahil Bindra", "Tanya Sood", "Udit Grover", "Veer Bajwa", "Yash Anand", "Zoya Ahuja",
    
    # Additional South Indian
    "Abhiram Shetty", "Akshara Rao", "Anand Pillai", "Bhavya Srinivas", "Chaitanya Gowda", "Darshan Hegde",
    "Gokul Krishna", "Harika Nair", "Ishwar Reddy", "Janaki Ramesh", "Kiran Menon", "Lavanya Kumar",
    "Manikandan Iyer", "Nithya Prasad", "Pranav Mohan", "Radhika Suresh", "Sharath Babu", "Thara Devi",
    "Usha Kumari", "Vijay Shankar", "Yamini Rajan", "Aravind Gopal", "Bhargavi Narayan", "Chandra Sekhar",
    
    # Additional West Indian
    "Amar Desai", "Bharati Kulkarni", "Chinmay Joshi", "Dhanashree Patil", "Eknath Pawar", "Gauri Deshpande",
    "Hemant Shah", "Ira Mehta", "Jayesh Patel", "Kalyani Modi", "Lata Parikh", "Milind Thakkar",
    "Namrata Dave", "Omkar Trivedi", "Parul Sheth", "Radhika Nene", "Sanjay Wagh", "Tejal Kadam",
    "Umesh Mahajan", "Vaishali Naik", "Yatin Phadke", "Anuja Ghosh", "Bhushan Kulkarni", "Chetan Patwardhan",
    
    # Additional East Indian
    "Abhijit Das", "Ananya Chatterjee", "Biplab Banerjee", "Chandrima Sen", "Dipak Ghosh", "Ena Mukherjee",
    "Gautam Roy", "Haimanti Bose", "Indrajit Dutta", "Jayanti Sarkar", "Kallol Sinha", "Laboni Mazumdar",
    "Mrinal Bhattacharya", "Nabanita Dey", "Prabir Sengupta", "Ratna Ganguly", "Samaresh Dasgupta", "Tanaya Majumdar",
    "Ujjwal Pal", "Vasundhara Biswas", "Writam Saha", "Amitabh Mitra", "Barnali Bhowmik", "Chiranjit Chowdhury",
    
    # Additional Punjabi
    "Angad Singh", "Baljit Kaur", "Charanjit Singh", "Dalvir Kaur", "Eshaan Singh", "Fateh Kaur",
    "Gobind Singh", "Harmeet Kaur", "Inderpreet Singh", "Jasmeet Kaur", "Kuldip Kaur", "Lovejit Singh",
    "Manvir Kaur", "Nirmal Singh", "Onkar Kaur", "Palwinder Singh", "Ramandeep Kaur", "Sarabjit Singh",
    
    # South surnames variety
    "Anil Pillai", "Aruna Nambiar", "Bala Subramaniam", "Chandran Nair", "Dinesh Narayanan", "Geetha Menon",
    "Hari Krishnan", "Indira Iyer", "Jayaram Kumar", "Kamala Raman", "Lakshman Reddy", "Malini Venkatesh",
    "Natarajan Mohan", "Padma Prasad", "Rajendra Naidu", "Savitha Balaji", "Thyagarajan Murthy", "Vasudevan Srinivas",
    
    # Professional sounding names
    "Abhishek Raghavan", "Anupama Krishnamurthy", "Avinash Subramanian", "Divya Ramachandran", "Harish Venkatraman",
    "Jaya Gopalakrishnan", "Karthikeyan Sundaram", "Meera Parthasarathy", "Naveen Chandrasekaran", "Prashant Narasimhan",
    "Rajiv Viswanathan", "Santosh Balasubramanian", "Uday Rajagopalan", "Venkatesh Ranganathan", "Yogesh Sivaramakrishnan",
    
    # Additional variety
    "Akshara Jain", "Alok Pandey", "Anshu Mishra", "Aparna Tiwari", "Ashok Saxena", "Bharti Arora",
    "Chandra Chopra", "Dheeraj Bajaj", "Gautam Kohli", "Harsha Sinha", "Ishita Mittal", "Jayant Bansal",
    "Kavita Khanna", "Lokesh Kapoor", "Madhur Bhatia", "Neeraj Agarwal", "Pallavi Malhotra", "Rajeev Gupta",
    "Sakshi Sharma", "Tarun Verma", "Urvashi Singh", "Vikas Patel", "Yashika Reddy", "Zubin Iyer",
    
    # Kashmiri names
    "Aamir Koul", "Asifa Wani", "Farooq Bhat", "Hina Dar", "Irfan Lone", "Mehvish Malik",
    "Nazir Ahmed", "Riyaz Khan", "Shabir Naqash", "Yasir Mir", "Zainab Andrabi", "Arif Waza",
    
    # Rajasthani names
    "Bhawani Rathore", "Chandrakanta Meena", "Daulat Shekhawat", "Gajendra Chouhan", "Kishori Bishnoi",
    "Mahendra Gehlot", "Prakash Soni", "Raghuveer Jat", "Shanti Devi", "Tejpal Sharma", "Vikram Rathore",
    
    # Bihari names
    "Avinash Yadav", "Babita Kumari", "Chandan Kumar", "Dilip Mandal", "Gudiya Devi", "Jitendra Singh",
    "Kundan Kumar", "Lalan Yadav", "Mithilesh Kumar", "Nitish Rai", "Pankaj Prasad", "Ravindra Jha",
    
    # UP names
    "Akhilesh Yadav", "Bhavesh Chauhan", "Chandra Prakash", "Dharmendra Pal", "Ghanshyam Singh", "Kamla Devi",
    "Laxman Das", "Mohan Lal", "Naresh Babu", "Prem Shankar", "Ramswaroop", "Santosh Kumar", "Tribhuvan Yadav",
    
    # Haryana names
    "Ajay Hooda", "Bimla Devi", "Deepak Malik", "Geeta Rani", "Joginder Singh", "Krishan Kumar",
    "Mahabir Singh", "Omvir Malik", "Rajbir Hooda", "Surender Kumar", "Vinod Sharma", "Yogesh Rana",
    
    # MP names
    "Babulal Patel", "Chandravati Devi", "Gopal Yadav", "Kamla Bai", "Mahendra Tomar", "Prakash Rajput",
    "Ramesh Jatav", "Santosh Kushwaha", "Tulsiram Patel", "Virendra Singh", "Asha Lodhi", "Bhupendra Ahirwar",
    
    # Chhattisgarh names
    "Balram Sahu", "Devanti Bai", "Ghanshyam Verma", "Kalawati Devi", "Manohar Patel", "Phoolmati Devi",
    "Ramkumar Yadav", "Santoshi Bai", "Vijay Thakur", "Anandi Bai", "Bhuneshwar Sahu", "Chandrika Patel",
    
    # Jharkhand names
    "Amardeep Mahto", "Basanti Devi", "Chandrabhan Singh", "Gangotri Kumari", "Hemant Oraon", "Jaimala Devi",
    "Kailash Munda", "Lalita Kumari", "Pankaj Tirkey", "Ranjit Mahto", "Savitri Kerketta", "Tulsi Hansda",
    
    # Uttarakhand names
    "Anand Rawat", "Basanti Negi", "Chandra Singh", "Deepa Bisht", "Gajendra Panwar", "Hemwati Devi",
    "Kiran Negi", "Mohan Rawat", "Pushpa Bisht", "Ramesh Negi", "Shanti Rawat", "Vijay Panwar",
    
    # Himachal names
    "Arun Thakur", "Bimla Chauhan", "Devendra Verma", "Kamla Negi", "Naresh Thakur", "Prem Chauhan",
    "Rajesh Verma", "Santosh Negi", "Vijay Thakur", "Asha Chauhan", "Bhupendra Verma", "Chandrika Negi",
    
    # Goa names
    "Anthony D'Souza", "Clara Fernandes", "Francis Lobo", "Maria Rodrigues", "Peter Pereira", "Rita Gomes",
    "Santan Dias", "Teresa Almeida", "Vincent Rebello", "Anita Pinto", "Bruno Carvalho", "Cecilia Braganza",
    
    # Kerala Christian names
    "Abraham Thomas", "Elizabeth George", "Jacob Mathew", "Mary Joseph", "Paul Varghese", "Sarah Philip",
    "Stephen John", "Susan Samuel", "Thomas Chacko", "Anna Alex", "Benjamin Kurian", "Grace Koshy",
    
    # Muslim names (Pan-India)
    "Ahmed Khan", "Ayesha Begum", "Faizal Rahman", "Hina Parveen", "Imran Ali", "Khadija Fatima",
    "Mohammed Ismail", "Nazia Siddiqui", "Riyaz Ahmed", "Sana Qureshi", "Tariq Ansari", "Yasmin Sheikh",
    "Aslam Khan", "Bushra Khatoon", "Dilshad Alam", "Farhan Malik", "Gulfam Ahmed", "Halima Begum",
    
    # Sikh names (additional)
    "Avtar Singh Gill", "Balwinder Kaur Brar", "Daljit Singh Sandhu", "Gurdeep Kaur Dhillon", "Harbans Singh Grewal",
    "Inderjit Kaur Sidhu", "Jagjit Singh Mann", "Kulwinder Kaur Virk", "Lakhbir Singh Bajwa", "Manjit Kaur Randhawa",
    
    # Parsi names
    "Boman Irani", "Cyrus Patel", "Dinshaw Mehta", "Firdaus Shroff", "Homi Bhabha", "Khorshed Davar",
    "Meher Patel", "Perviz Mehta", "Rustom Irani", "Shireen Vakil", "Zubin Mehta", "Arnavaz Patel",
    
    # Anglo-Indian names
    "Adrian D'Silva", "Bernadette Williams", "Christopher D'Mello", "Diana Fernandes", "Edward Pereira",
    "Fiona Gonsalves", "Gregory D'Costa", "Helen Rodrigues", "Ivan Pinto", "Jennifer Lobo", "Kevin Dias",
    
    # Unique regional variants
    "Amarjeet Bhatia", "Chandrashekar Rao", "Damodar Shetty", "Gopinath Iyer", "Jagmohan Reddy",
    "Krishnamurthy Nair", "Padmanabhan Menon", "Ranganathan Pillai", "Subramanian Kumar", "Varadarajan Srinivas"
]

# Indian bank names for realistic fraud scenarios - comprehensive list
INDIAN_BANKS = [
    # Major Public Sector Banks
    "State Bank of India", "Punjab National Bank", "Bank of Baroda", "Canara Bank", 
    "Union Bank of India", "Bank of India", "Indian Bank", "Central Bank of India",
    "Indian Overseas Bank", "UCO Bank", "Bank of Maharashtra", "Punjab & Sind Bank",
    
    # Major Private Sector Banks
    "HDFC Bank", "ICICI Bank", "Axis Bank", "Kotak Mahindra Bank", "IndusInd Bank",
    "Yes Bank", "IDFC First Bank", "Federal Bank", "RBL Bank", "South Indian Bank",
    "Karur Vysya Bank", "City Union Bank", "DCB Bank", "Dhanlaxmi Bank",
    
    # Foreign Banks (operating in India)
    "Citibank", "HSBC", "Standard Chartered Bank", "Deutsche Bank", "Barclays Bank",
    "American Express Banking", "DBS Bank", "Bank of America",
    
    # Small Finance Banks
    "AU Small Finance Bank", "Equitas Small Finance Bank", "Ujjivan Small Finance Bank",
    "Jana Small Finance Bank", "Suryoday Small Finance Bank", "Utkarsh Small Finance Bank",
    
    # Payment Banks
    "Paytm Payments Bank", "Airtel Payments Bank", "India Post Payments Bank",
    "Fino Payments Bank", "Jio Payments Bank",
    
    # Regional Banks
    "Karnataka Bank", "Lakshmi Vilas Bank", "Tamilnad Mercantile Bank", "Jammu & Kashmir Bank",
    "Nainital Bank", "Catholic Syrian Bank"
]


def replace_placeholders(text: str, platform_type: str = None) -> str:
    """
    Replace placeholders in scenario descriptions with random entities from the comprehensive lists.
    
    Args:
        text: The scenario description with placeholders like [MARKETPLACE_PLATFORM], [ITEM_CATEGORY], etc.
        platform_type: Optional platform type hint from scenario metadata (marketplace, ecommerce_retail, etc.)
    
    Returns:
        Text with all placeholders replaced by random entities
    """
    
    if not ECOMMERCE_ENTITIES_AVAILABLE:
        return text  # Return unchanged if entities not available
    
    result = text
    
    # Platform placeholders (context-aware based on platform_type)
    if "[MARKETPLACE_PLATFORM]" in result:
        result = result.replace("[MARKETPLACE_PLATFORM]", random.choice(INDIAN_MARKETPLACES), 1)
    
    if "[ECOMMERCE_PLATFORM]" in result:
        result = result.replace("[ECOMMERCE_PLATFORM]", random.choice(INDIAN_ECOMMERCE_RETAIL), 1)
    
    if "[FOOD_DELIVERY_PLATFORM]" in result:
        result = result.replace("[FOOD_DELIVERY_PLATFORM]", random.choice(INDIAN_FOOD_DELIVERY), 1)
    
    # Alias for tech scenarios
    if "[FOOD_DELIVERY_APP]" in result:
        result = result.replace("[FOOD_DELIVERY_APP]", random.choice(INDIAN_FOOD_DELIVERY), 1)
    
    if "[QUICK_COMMERCE_PLATFORM]" in result:
        result = result.replace("[QUICK_COMMERCE_PLATFORM]", random.choice(INDIAN_QUICK_COMMERCE), 1)
    
    if "[SERVICE_PLATFORM]" in result:
        result = result.replace("[SERVICE_PLATFORM]", random.choice(INDIAN_SERVICE_PLATFORMS), 1)
    
    if "[SOCIAL_MARKETPLACE]" in result:
        # Social marketplaces could be Facebook Marketplace, Instagram Marketplace, etc.
        social_marketplaces = ["Facebook Marketplace", "Instagram Marketplace", "WhatsApp Business Marketplace"]
        result = result.replace("[SOCIAL_MARKETPLACE]", random.choice(social_marketplaces), 1)
    
    # Payment method placeholders
    if "[UPI_APP]" in result:
        result = result.replace("[UPI_APP]", random.choice(INDIAN_UPI_APPS), 1)
    
    if "[PAYMENT_METHOD]" in result:
        result = result.replace("[PAYMENT_METHOD]", random.choice(PAYMENT_METHODS), 1)
    
    # Product category placeholders - specific categories
    if "[ELECTRONICS_ITEM]" in result:
        result = result.replace("[ELECTRONICS_ITEM]", random.choice(ELECTRONICS_ITEMS), 1)
    
    if "[HOME_APPLIANCE]" in result:
        result = result.replace("[HOME_APPLIANCE]", random.choice(HOME_APPLIANCES), 1)
    
    if "[FURNITURE_ITEM]" in result:
        result = result.replace("[FURNITURE_ITEM]", random.choice(FURNITURE_ITEMS), 1)
    
    if "[FASHION_ITEM]" in result:
        result = result.replace("[FASHION_ITEM]", random.choice(FASHION_ITEMS), 1)
    
    if "[VEHICLE_ITEM]" in result:
        result = result.replace("[VEHICLE_ITEM]", random.choice(VEHICLE_ITEMS), 1)
    
    # Generic item category placeholder - randomly select from any category
    if "[ITEM_CATEGORY]" in result:
        # Replace each occurrence with a random product
        while "[ITEM_CATEGORY]" in result:
            result = result.replace("[ITEM_CATEGORY]", random.choice(get_all_products()), 1)
    
    # Utility service provider placeholders
    if UTILITY_ENTITIES_AVAILABLE:
        if "[STATE_ELECTRICITY_BOARD]" in result:
            result = result.replace("[STATE_ELECTRICITY_BOARD]", random.choice(STATE_ELECTRICITY_BOARDS), 1)
        
        if "[MOBILE_CARRIER]" in result:
            result = result.replace("[MOBILE_CARRIER]", random.choice(MOBILE_CARRIERS), 1)
        
        if "[INTERNET_PROVIDER]" in result:
            result = result.replace("[INTERNET_PROVIDER]", random.choice(INTERNET_PROVIDERS), 1)
        
        if "[GAS_AGENCY]" in result:
            result = result.replace("[GAS_AGENCY]", random.choice(GAS_AGENCIES), 1)
        
        if "[DTH_PROVIDER]" in result:
            result = result.replace("[DTH_PROVIDER]", random.choice(DTH_PROVIDERS), 1)
        
        if "[WATER_SUPPLY_DEPARTMENT]" in result:
            result = result.replace("[WATER_SUPPLY_DEPARTMENT]", random.choice(WATER_SUPPLY_DEPARTMENTS), 1)
        
        if "[GOVERNMENT_SCHEME]" in result:
            result = result.replace("[GOVERNMENT_SCHEME]", random.choice(GOVERNMENT_SCHEMES), 1)
        
        if "[GAS_REGULATORY_AUTHORITY]" in result:
            result = result.replace("[GAS_REGULATORY_AUTHORITY]", random.choice(GAS_REGULATORY_AUTHORITIES), 1)
        
        if "[TELECOM_REGULATORY_AUTHORITY]" in result:
            result = result.replace("[TELECOM_REGULATORY_AUTHORITY]", random.choice(TELECOM_REGULATORY_AUTHORITIES), 1)
        
        if "[ELECTRICITY_REGULATORY_AUTHORITY]" in result:
            result = result.replace("[ELECTRICITY_REGULATORY_AUTHORITY]", random.choice(ELECTRICITY_REGULATORY_AUTHORITIES), 1)
    
    # Job & recruitment entity placeholders
    if JOB_ENTITIES_AVAILABLE:
        if "[IT_COMPANY]" in result:
            result = result.replace("[IT_COMPANY]", random.choice(IT_COMPANIES), 1)
        
        if "[MNC_COMPANY]" in result:
            result = result.replace("[MNC_COMPANY]", random.choice(MNC_COMPANIES), 1)
        
        if "[JOB_PORTAL]" in result:
            result = result.replace("[JOB_PORTAL]", random.choice(JOB_PORTALS), 1)
        
        if "[GOVERNMENT_DEPT]" in result:
            result = result.replace("[GOVERNMENT_DEPT]", random.choice(GOVERNMENT_DEPARTMENTS), 1)
        
        if "[AIRLINE_COMPANY]" in result:
            result = result.replace("[AIRLINE_COMPANY]", random.choice(AIRLINE_COMPANIES), 1)
    
    # Loan & lending entity placeholders
    if LOAN_ENTITIES_AVAILABLE:
        if "[LENDING_APP]" in result:
            result = result.replace("[LENDING_APP]", random.choice(get_all_lending_apps()), 1)
        
        if "[PREDATORY_APP]" in result:
            result = result.replace("[PREDATORY_APP]", random.choice(PREDATORY_LENDING_APPS), 1)
        
        if "[LEGITIMATE_APP]" in result:
            result = result.replace("[LEGITIMATE_APP]", random.choice(LEGITIMATE_LENDING_APPS), 1)
        
        if "[NBFC]" in result:
            result = result.replace("[NBFC]", random.choice(NBFC_COMPANIES), 1)
        
        if "[MICROFINANCE]" in result:
            result = result.replace("[MICROFINANCE]", random.choice(MICROFINANCE_INSTITUTIONS), 1)
        
        if "[CREDIT_BUREAU]" in result:
            result = result.replace("[CREDIT_BUREAU]", random.choice(CREDIT_BUREAUS), 1)
    
    # Tech & platform entity placeholders
    if TECH_ENTITIES_AVAILABLE:
        if "[TECH_COMPANY]" in result:
            result = result.replace("[TECH_COMPANY]", random.choice(TECH_COMPANIES), 1)
        
        if "[SOCIAL_MEDIA_APP]" in result:
            result = result.replace("[SOCIAL_MEDIA_APP]", random.choice(SOCIAL_MEDIA_PLATFORMS), 1)
        
        if "[EMAIL_PROVIDER]" in result:
            result = result.replace("[EMAIL_PROVIDER]", random.choice(EMAIL_PROVIDERS), 1)
        
        if "[GAMING_PLATFORM]" in result:
            result = result.replace("[GAMING_PLATFORM]", random.choice(GAMING_PLATFORMS), 1)
        
        if "[GIFT_CARD_BRAND]" in result:
            result = result.replace("[GIFT_CARD_BRAND]", random.choice(GIFT_CARD_BRANDS), 1)
        
        if "[RIDE_HAILING_APP]" in result:
            result = result.replace("[RIDE_HAILING_APP]", random.choice(RIDE_HAILING_APPS), 1)
    
    # Emergency entities - family, hospital, city, NGO placeholders
    if EMERGENCY_ENTITIES_AVAILABLE:
        if "[FAMILY_MEMBER]" in result:
            result = result.replace("[FAMILY_MEMBER]", random.choice(FAMILY_MEMBERS), 1)
        
        if "[HOSPITAL_NAME]" in result:
            result = result.replace("[HOSPITAL_NAME]", random.choice(HOSPITAL_NAMES), 1)
        
        if "[CITY]" in result:
            result = result.replace("[CITY]", random.choice(INDIAN_CITIES), 1)
        
        if "[NGO_NAME]" in result:
            result = result.replace("[NGO_NAME]", random.choice(NGO_NAMES), 1)
    
    # Healthcare entities - insurance, government scheme, marketplace, disease placeholders
    if HEALTHCARE_ENTITIES_AVAILABLE:
        if "[INSURANCE_COMPANY]" in result:
            result = result.replace("[INSURANCE_COMPANY]", random.choice(INSURANCE_COMPANIES), 1)
        
        if "[GOVERNMENT_SCHEME]" in result:
            result = result.replace("[GOVERNMENT_SCHEME]", random.choice(GOVERNMENT_SCHEMES), 1)
        
        if "[INSURANCE_MARKETPLACE]" in result:
            result = result.replace("[INSURANCE_MARKETPLACE]", random.choice(INSURANCE_MARKETPLACES), 1)
        
        if "[DISEASE_NAME]" in result:
            result = result.replace("[DISEASE_NAME]", random.choice(DISEASE_NAMES), 1)
    
    # Lottery & Travel entities - travel, airline, lottery, car, pilgrimage, hotel, bank, cruise placeholders
    if LOTTERY_TRAVEL_ENTITIES_AVAILABLE:
        if "[TRAVEL_COMPANY]" in result:
            result = result.replace("[TRAVEL_COMPANY]", random.choice(TRAVEL_COMPANIES), 1)
        
        if "[AIRLINE_COMPANY]" in result:
            result = result.replace("[AIRLINE_COMPANY]", random.choice(AIRLINE_COMPANIES), 1)
        
        if "[LOTTERY_NAME]" in result:
            result = result.replace("[LOTTERY_NAME]", random.choice(LOTTERY_NAMES), 1)
        
        if "[CAR_BRAND]" in result:
            result = result.replace("[CAR_BRAND]", random.choice(CAR_BRANDS), 1)
        
        if "[PILGRIMAGE_SITE]" in result:
            result = result.replace("[PILGRIMAGE_SITE]", random.choice(PILGRIMAGE_SITES), 1)
        
        if "[HOTEL_NAME]" in result:
            result = result.replace("[HOTEL_NAME]", random.choice(HOTEL_NAMES), 1)
        
        if "[BANK_NAME]" in result:
            result = result.replace("[BANK_NAME]", random.choice(BANK_NAMES), 1)
        
        if "[CRUISE_LINE]" in result:
            result = result.replace("[CRUISE_LINE]", random.choice(CRUISE_LINES), 1)
    
    # Government entities
    if GOVERNMENT_ENTITIES_AVAILABLE:
        if "[GOVERNMENT_DEPT]" in result:
            result = result.replace("[GOVERNMENT_DEPT]", random.choice(GOVERNMENT_DEPT), 1)
    
    return result


class ConversationGenerator:
    """Handles Stage 1: Source conversation generation via Groq API."""
    
    def __init__(self, console: Console, groq_client: groq.AsyncGroq):
        self.console = console
        self.groq_client = groq_client
        
        # Cache static system prompt (optimization: avoid rebuilding on each call)
        self.system_prompt = self._build_system_prompt()
    
    def _build_system_prompt(self) -> str:
        """
        Build the static system prompt once (cached for all requests).
        This enables Groq's prompt caching and reduces token overhead.
        """
        return """You are a fraud detection training data generator. Output valid JSON matching this schema:

{
  "transcript": [{"speaker": "Agent|Customer", "text": "...", "timestamp_end": float}],
  "multimodal_analysis": {"dominant_emotion": str, "secondary_emotion": str, "pace": str, "confidence_score": float},
  "key_entities": {"organization": [str], "product": [str], "pii_requested": [str]},
  "chunk_level_analysis": [{"timestamp": float, "verdict_at_chunk": "YES|NO", "rationale_at_chunk": str}],
  "final_slow_thinking_rationale": str,
  "final_verdict": "YES|NO",
  "violated_policies": [str],
  "scam_outcome": "Successful|Failed|Interrupted|N/A"
}

Requirements:
1. Transcript: Natural Indian English with occasional Hindi (Sir, ji, Achha, Thik hai, Haan). Mix 90% English + 10% Hindi words. NO full Hindi sentences.
2. Realistic progression: NO repetitive loops. Move conversation forward naturally. Vary dialogue.
3. Chunk Analysis: Every 10-15s. Verdict="YES" when violation occurs, stays "YES" after. Normal calls: all "NO".
4. Key Entities: List orgs, products, PII requested ([] if none).
5. Verdict: "YES"=policy violated, "NO"=compliant.
6. Violated Policies: Exact rule text or [].
7. Scam Outcome: Based on customer persona - "Successful"|"Failed"|"Interrupted"|"N/A".
8. Duration: Target duration is a GUIDELINE, not strict requirement (±20s flexibility acceptable).
   - END NATURALLY when scenario completes, even if before target duration
   - Better to end at 80s naturally than pad to 120s with repetition
   - NO repetitive goodbyes or filler content to reach duration
   - If conversation naturally ends, STOP - don't add artificial padding"""
    
    def construct_meta_prompt(self, agent_persona: str, customer_persona: str, 
                            scenario: Dict[str, Any], duration: int, customer_name: str, bank_name: str) -> tuple[str, str]:
        """
        Construct user prompt (system prompt is cached in self.system_prompt).
        
        Prompt order optimized for Groq caching:
        - Duration and scenario first (more cacheable)
        - Names last (most variable)
        
        Returns:
            Tuple of (system_prompt, user_prompt)
        """
        
        # Replace placeholders in scenario description with random entities
        scenario_description = scenario['description']
        platform_type = scenario.get('platform_type')  # Optional context hint
        
        # Apply placeholder replacement for ALL entity types (e-commerce, utility, job, loan, AND tech)
        # Check if any placeholder exists in the description
        if any(placeholder in scenario_description for placeholder in [
            # E-commerce placeholders
            "[MARKETPLACE_PLATFORM]", "[ECOMMERCE_PLATFORM]", "[UPI_APP]", "[ITEM_CATEGORY]", 
            "[ELECTRONICS_ITEM]", "[FURNITURE_ITEM]", "[HOME_APPLIANCE]", "[FASHION_ITEM]",
            "[VEHICLE_ITEM]", "[SOCIAL_MARKETPLACE]", "[FOOD_DELIVERY_PLATFORM]", "[FOOD_DELIVERY_APP]",
            "[QUICK_COMMERCE_PLATFORM]", "[SERVICE_PLATFORM]", "[PAYMENT_METHOD]",
            # Utility placeholders
            "[STATE_ELECTRICITY_BOARD]", "[MOBILE_CARRIER]", "[INTERNET_PROVIDER]",
            "[GAS_AGENCY]", "[DTH_PROVIDER]", "[WATER_SUPPLY_DEPARTMENT]",
            "[GOVERNMENT_SCHEME]", "[GAS_REGULATORY_AUTHORITY]",
            "[TELECOM_REGULATORY_AUTHORITY]", "[ELECTRICITY_REGULATORY_AUTHORITY]",
            # Job placeholders
            "[IT_COMPANY]", "[MNC_COMPANY]", "[JOB_PORTAL]",
            "[GOVERNMENT_DEPT]", "[AIRLINE_COMPANY]",
            # Loan placeholders
            "[LENDING_APP]", "[PREDATORY_APP]", "[LEGITIMATE_APP]",
            "[NBFC]", "[MICROFINANCE]", "[CREDIT_BUREAU]",
            # Tech placeholders
            "[TECH_COMPANY]", "[SOCIAL_MEDIA_APP]", "[EMAIL_PROVIDER]",
            "[GAMING_PLATFORM]", "[GIFT_CARD_BRAND]", "[RIDE_HAILING_APP]",
            # Emergency placeholders
            "[FAMILY_MEMBER]", "[HOSPITAL_NAME]", "[CITY]", "[NGO_NAME]",
            # Healthcare placeholders
            "[INSURANCE_COMPANY]", "[INSURANCE_MARKETPLACE]", "[DISEASE_NAME]",
            # Lottery & Travel placeholders
            "[TRAVEL_COMPANY]", "[LOTTERY_NAME]", "[CAR_BRAND]", 
            "[PILGRIMAGE_SITE]", "[HOTEL_NAME]", "[BANK_NAME]", "[CRUISE_LINE]"
        ]):
            scenario_description = replace_placeholders(scenario_description, platform_type)
        
        # USER PROMPT - Optimized order for cache locality
        user_prompt = f"""Generate ~{duration}s conversation (±20s OK):

**Scenario:** {scenario['case_type']} - {scenario_description}
**Policy:** {scenario['policy']}

**Personas:**
Agent: {agent_persona}
Customer: {customer_persona}

**Names:** Customer={customer_name}, Bank={bank_name}

Create natural dialogue. For fraud: show violation progression. For normal: stay compliant. 
END NATURALLY when scenario completes - don't pad with repetition. Output JSON only."""

        return self.system_prompt, user_prompt
    
    async def generate_source_conversation(self, combination: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate source conversation with retry logic and exponential backoff.
        
        Args:
            combination: Dictionary containing agent_persona, customer_persona, scenario, session_id
            
        Returns:
            Dictionary containing the complete conversation data
        """
        
        agent_persona = combination['agent_persona']
        customer_persona = combination['customer_persona']
        scenario = combination['scenario']
        session_id = combination['session_id']
        
        # Randomize conversation duration
        duration = random.randint(MIN_CONVERSATION_DURATION, MAX_CONVERSATION_DURATION)
        
        # Select Indian name and bank
        customer_name = random.choice(INDIAN_NAMES)
        bank_name = random.choice(INDIAN_BANKS)
        
        # Construct prompts (system prompt is cacheable)
        system_prompt, user_prompt = self.construct_meta_prompt(
            agent_persona, customer_persona, scenario, duration, customer_name, bank_name
        )
        
        # Calculate dynamic max_tokens based on duration (more efficient)
        dynamic_max_tokens = min(int(duration * 28), MAX_TOKENS)  # ~28 tokens per second
        
        # Retry logic with exponential backoff
        last_exception = None
        for attempt in range(1, MAX_RETRIES + 1):
            try:
                # Make async API call to Groq
                response = await self.groq_client.chat.completions.create(
                    model=GROQ_MODEL,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    temperature=API_TEMPERATURE,
                    max_tokens=dynamic_max_tokens,
                    response_format={"type": "json_object"}
                )
                
                # Parse the JSON response (with code fence handling)
                response_content = response.choices[0].message.content.strip()
                
                # Remove code fences if present (defensive parsing)
                if response_content.startswith("```"):
                    # Extract JSON from ```json ... ``` or ``` ... ```
                    if "```json" in response_content:
                        response_content = response_content.split("```json", 1)[-1].split("```")[0].strip()
                    else:
                        response_content = response_content.split("```", 1)[-1].rsplit("```", 1)[0].strip()
                
                conversation_data = json.loads(response_content)
                
                # Calculate actual duration from the transcript
                actual_duration = 0.0
                if 'transcript' in conversation_data and conversation_data['transcript']:
                    actual_duration = conversation_data['transcript'][-1].get('timestamp_end', 0.0)
                
                # Add metadata
                conversation_data["generation_metadata"] = {
                    "target_duration": duration,
                    "actual_duration": actual_duration,
                    "multiplier_round": combination.get('multiplier_round', 1),
                    "combination_key": combination.get('combination_key', ''),
                    "generated_at": datetime.now().isoformat(),
                    "retry_attempt": attempt
                }
                
                # Add top-level metadata
                conversation_data["session_id"] = session_id
                conversation_data["agent_persona"] = agent_persona
                conversation_data["customer_persona"] = customer_persona
                conversation_data["scenario"] = scenario
                
                # Success! Return the data
                if attempt > 1:
                    self.console.print(f"[green]Session {session_id} succeeded on attempt {attempt}[/green]")
                
                return conversation_data
                
            except json.JSONDecodeError as e:
                last_exception = e
                self.console.print(f"[yellow]Session {session_id} JSON error (attempt {attempt}/{MAX_RETRIES}): {str(e)[:100]}[/yellow]")
                
                if attempt < MAX_RETRIES:
                    # Reduce max_tokens for retry
                    dynamic_max_tokens = int(dynamic_max_tokens * 0.8)
                    
                    # Smart backoff: minimal delay for JSON errors (not rate-limit related)
                    if attempt == 1:
                        await asyncio.sleep(0.5)  # Quick first retry
                    else:
                        delay = RETRY_DELAY_SECONDS * (2 ** (attempt - 1)) if EXPONENTIAL_BACKOFF else RETRY_DELAY_SECONDS
                        await asyncio.sleep(delay)
                    
            except groq.APIError as e:
                last_exception = e
                error_str = str(e)
                
                # Check if it's a token limit error
                if "max completion tokens" in error_str.lower() or "json_validate_failed" in error_str.lower():
                    self.console.print(f"[yellow]Session {session_id} token limit (attempt {attempt}/{MAX_RETRIES})[/yellow]")
                    
                    if attempt < MAX_RETRIES:
                        # Significantly reduce max_tokens and reduce duration
                        dynamic_max_tokens = int(dynamic_max_tokens * 0.7)
                        duration = int(duration * 0.8)  # Reduce target duration
                        
                        # Regenerate prompts with shorter duration
                        system_prompt, user_prompt = self.construct_meta_prompt(
                            agent_persona, customer_persona, scenario, duration, customer_name, bank_name
                        )
                        
                        delay = RETRY_DELAY_SECONDS * (2 ** (attempt - 1)) if EXPONENTIAL_BACKOFF else RETRY_DELAY_SECONDS
                        await asyncio.sleep(delay)
                else:
                    self.console.print(f"[yellow]Session {session_id} API error (attempt {attempt}/{MAX_RETRIES}): {error_str[:100]}[/yellow]")
                    
                    if attempt < MAX_RETRIES:
                        delay = RETRY_DELAY_SECONDS * (2 ** (attempt - 1)) if EXPONENTIAL_BACKOFF else RETRY_DELAY_SECONDS
                        await asyncio.sleep(delay)
                        
            except Exception as e:
                last_exception = e
                self.console.print(f"[yellow]Session {session_id} error (attempt {attempt}/{MAX_RETRIES}): {str(e)[:100]}[/yellow]")
                
                if attempt < MAX_RETRIES:
                    delay = RETRY_DELAY_SECONDS * (2 ** (attempt - 1)) if EXPONENTIAL_BACKOFF else RETRY_DELAY_SECONDS
                    await asyncio.sleep(delay)
        
        # All retries failed
        self.console.print(f"[red]Session {session_id} failed after {MAX_RETRIES} attempts[/red]")
        raise last_exception
