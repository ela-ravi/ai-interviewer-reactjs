"""
Configuration settings for AI Interviewer
"""
import os
from dotenv import load_dotenv

load_dotenv()

# OpenRouter API Configuration (for Mistral AI)
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
DEFAULT_MODEL = os.getenv("MODEL", "mistralai/mistral-small-creative")
DEFAULT_TEMPERATURE = float(os.getenv("TEMPERATURE", "0.7"))
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"

# Interview Settings
DEFAULT_QUESTIONS_COUNT = int(os.getenv("DEFAULT_QUESTIONS_COUNT", "5"))
MAX_QUESTIONS_COUNT = int(os.getenv("MAX_QUESTIONS_COUNT", "10"))

# Agent Settings
AGENT_TIMEOUT = int(os.getenv("AGENT_TIMEOUT", "120"))

# Validate required settings
if not OPENROUTER_API_KEY:
    raise ValueError(
        "OPENROUTER_API_KEY not found in environment variables. "
        "Please create a .env file with your OpenRouter API key."
    )

