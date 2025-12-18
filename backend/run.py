"""
Flask application entry point
"""
import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add the backend directory to the Python path
sys.path.insert(0, os.path.dirname(__file__))

from app import create_app
from app.config import Config

app = create_app()

if __name__ == '__main__':
    port = Config.PORT
    debug = os.getenv('FLASK_DEBUG', 'True') == 'True'
    
    print(f"🚀 Starting AI Interviewer Backend")
    print(f"   Port: {port}")
    print(f"   Environment: {os.getenv('FLASK_ENV', 'development')}")
    print(f"   Debug mode: {debug}")
    print(f"   Model: {Config.MODEL}")
    print(f"   CORS Origins: {Config.CORS_ORIGINS}")
    print(f"🔑 OpenRouter API Key: {'✅ Configured' if Config.OPENROUTER_API_KEY else '❌ Missing'}")
    
    if not Config.OPENROUTER_API_KEY:
        print("⚠️  WARNING: OPENROUTER_API_KEY not set! The application will not work.")
    
    app.run(host='0.0.0.0', port=port, debug=debug)

