"""
Application configuration
"""
import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Base configuration"""
    # Flask Configuration
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    PORT = int(os.getenv('PORT', 5001))
    
    # LLM provider. Old OPENROUTER_* names still work if the generic ones are unset.
    LLM_API_KEY = os.getenv('LLM_API_KEY') or os.getenv('OPENROUTER_API_KEY')
    LLM_BASE_URL = os.getenv('LLM_BASE_URL') or os.getenv('OPENROUTER_BASE_URL') or 'https://openrouter.ai/api/v1'
    LLM_PROVIDER = os.getenv('LLM_PROVIDER') or ''
    OPENROUTER_API_KEY = LLM_API_KEY
    OPENROUTER_BASE_URL = LLM_BASE_URL
    
    # Model Configuration
    MODEL = os.getenv('MODEL') or ''
    TEMPERATURE = float(os.getenv('TEMPERATURE', '0.7'))
    
    # CORS Configuration
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', '*')
    
    # Redis Configuration (if used)
    REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
    
    # Interview Settings
    DEFAULT_QUESTIONS_COUNT = int(os.getenv('DEFAULT_QUESTIONS_COUNT', '5'))
    MAX_QUESTIONS_COUNT = int(os.getenv('MAX_QUESTIONS_COUNT', '10'))
    AGENT_TIMEOUT = int(os.getenv('AGENT_TIMEOUT', '120'))
    
    # Session Configuration
    SESSION_TIMEOUT_HOURS = int(os.getenv('SESSION_TIMEOUT_HOURS', '2'))


class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    FLASK_ENV = 'development'


class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    FLASK_ENV = 'production'

    def __init__(self):
        # Require secret key in production
        if Config.SECRET_KEY == 'dev-secret-key-change-in-production':
            raise ValueError('Must set SECRET_KEY environment variable in production')


class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    DEBUG = True


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}

