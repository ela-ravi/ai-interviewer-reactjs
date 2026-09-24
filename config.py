"""
Configuration settings for AI Interviewer
"""
import os
from dotenv import load_dotenv

load_dotenv()

# LLM provider. Old OPENROUTER_* names still work if the generic ones are unset.
LLM_API_KEY = os.getenv("LLM_API_KEY") or os.getenv("OPENROUTER_API_KEY")
LLM_BASE_URL = os.getenv("LLM_BASE_URL") or os.getenv("OPENROUTER_BASE_URL") or "https://openrouter.ai/api/v1"
LLM_PROVIDER = os.getenv("LLM_PROVIDER") or ""
OPENROUTER_API_KEY = LLM_API_KEY
OPENROUTER_BASE_URL = LLM_BASE_URL
DEFAULT_MODEL = os.getenv("MODEL", "mistralai/mistral-small-2603")
DEFAULT_TEMPERATURE = float(os.getenv("TEMPERATURE", "0.7"))

# Interview Settings
DEFAULT_QUESTIONS_COUNT = int(os.getenv("DEFAULT_QUESTIONS_COUNT", "5"))
MAX_QUESTIONS_COUNT = int(os.getenv("MAX_QUESTIONS_COUNT", "10"))

# Agent Settings
AGENT_TIMEOUT = int(os.getenv("AGENT_TIMEOUT", "120"))

# Validate required settings
if not LLM_API_KEY:
    raise ValueError(
        "LLM_API_KEY not found in environment variables. "
        "Set LLM_API_KEY, or OPENROUTER_API_KEY, in your .env file."
    )

