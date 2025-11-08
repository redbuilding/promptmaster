import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

MODEL_PROVIDER = os.getenv("MODEL_PROVIDER", "ollama")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "gpt-oss:20b")
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434/api/generate")

# Directory for saving outputs
OUTPUT_DIR = "enhanced_prompts"
