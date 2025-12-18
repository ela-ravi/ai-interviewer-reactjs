"""
Flask application factory
"""
from flask import Flask
from flask_cors import CORS
import os
from dotenv import load_dotenv

load_dotenv()


def create_app():
    """Create and configure the Flask application"""
    app = Flask(__name__)
    
    # Configuration
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    app.config['OPENROUTER_API_KEY'] = os.getenv('OPENROUTER_API_KEY')
    
    # Enable CORS - Simpler configuration that works reliably
    cors_origins = os.getenv('CORS_ORIGINS', '*')
    
    if cors_origins == '*' or cors_origins == '':
        # Development or not set: Allow all origins
        CORS(app, 
             origins="*",
             methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
             allow_headers=["Content-Type", "Authorization", "Accept"],
             expose_headers=["Content-Type"],
             supports_credentials=False,
             send_wildcard=True,
             always_send=True)
    else:
        # Production: Allow specific origins
        origins_list = [origin.strip() for origin in cors_origins.split(',') if origin.strip()]
        CORS(app,
             origins=origins_list,
             methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
             allow_headers=["Content-Type", "Authorization", "Accept"],
             expose_headers=["Content-Type"],
             supports_credentials=True,
             always_send=True)
    
    # Register blueprints
    from app.routes.interview import interview_bp
    app.register_blueprint(interview_bp, url_prefix='/api')
    
    # Health check endpoint
    @app.route('/health')
    def health():
        return {'status': 'healthy', 'service': 'ai-interviewer-backend'}, 200
    
    return app

