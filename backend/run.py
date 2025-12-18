"""
Flask application entry point
"""
import os
import sys

# Add the backend directory to the Python path
sys.path.insert(0, os.path.dirname(__file__))

from app import create_app

app = create_app()

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', 'True') == 'True'
    
    print(f"🚀 Starting AI Interviewer Backend on port {port}")
    print(f"📝 Debug mode: {debug}")
    print(f"🔑 OpenRouter API Key configured: {'Yes' if os.getenv('OPENROUTER_API_KEY') else 'No'}")
    
    app.run(host='0.0.0.0', port=port, debug=debug)

