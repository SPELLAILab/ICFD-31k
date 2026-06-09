# Global configuration for the synthetic dataset generator

# Dataset Generation Configuration
COMBINATION_MULTIPLIER = 1  # Generate N variations of each unique combination
CHUNK_INTERVAL_SECONDS = 3
MIN_CONVERSATION_DURATION = 60
MAX_CONVERSATION_DURATION = 360  # Reduced to avoid repetitive padding and hallucination

# API Configuration
GROQ_MODEL = "llama-3.3-70b-versatile"  # More stable model
API_TEMPERATURE = 0.7  # Lower for more consistent output
MAX_TOKENS = 10000
API_TIMEOUT = 120  # Timeout in seconds (increased for long conversations)

# Performance Configuration
MAX_WORKERS = 10
RATE_LIMIT_PER_MINUTE = 500
ENABLE_ADAPTIVE_SCALING = True
MIN_WORKERS = 5

# Recovery Configuration
ENABLE_RECOVERY = True
CHECKPOINT_INTERVAL = 50
AUTO_RESUME = True
MAX_RETRIES = 5
RETRY_DELAY_SECONDS = 3
EXPONENTIAL_BACKOFF = True

# Output Configuration
OUTPUT_DIR = "output"
SOURCE_CONVERSATIONS_DIR = "source_conversations"
TRAINING_DATA_DIR = "training_data"
RECOVERY_DIR = "recovery"

# Batch Configuration
ENABLE_BATCH_FOLDERS = True
SAVE_BATCH_METADATA = True

# File Configuration
PERSONAS_FILE = "data/personas.txt"
SCENARIOS_FILE = "data/scenarios/scenarios.txt"
BATCH_CONFIG_FILE = "config/batch_config.yaml"

# Logging Configuration
LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
