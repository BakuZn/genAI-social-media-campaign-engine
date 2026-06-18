"""
Configuration module for the campaign engine.
Handles API keys, environment settings, and system-wide constants.
"""
import os
from dotenv import load_dotenv

# Load environment variables from the local .env file
load_dotenv()

def get_gemini_api_key() -> str:
    """
    Retrieves the Gemini API key from the environment.
    """
    return os.getenv("GEMINI_API_KEY")

# Default model configuration
DEFAULT_MODEL = "gemini-2.5-flash"
