"""
Flask application factory
"""
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
import os
from dotenv import load_dotenv

load_dotenv()


def create_app():
    """Create and configure the Flask application"""
    app = Flask(__name__)
    
    # Configuration
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    app.config['OPENROUTER_API_KEY'] = os.getenv('OPENROUTER_API_KEY')
    
    # Get CORS configuration
    cors_origins = os.getenv('CORS_ORIGINS', '')
    
    # Configure CORS settings based on environment
    if not cors_origins or cors_origins == '*':
        # Development: Allow all origins
        print("🔓 CORS: Allowing all origins (development mode)")
        cors_config = {
            'origins': '*',
            'methods': ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
            'allow_headers': ['Content-Type', 'Authorization', 'Accept'],
            'expose_headers': ['Content-Type'],
            'supports_credentials': False,
            'max_age': 3600
        }
    else:
        # Production: Allow specific origins
        origins_list = [origin.strip() for origin in cors_origins.split(',') if origin.strip()]
        print(f"🔒 CORS: Allowing origins: {origins_list}")
        cors_config = {
            'origins': origins_list,
            'methods': ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
            'allow_headers': ['Content-Type', 'Authorization', 'Accept'],
            'expose_headers': ['Content-Type'],
            'supports_credentials': True,
            'max_age': 3600
        }
    
    # Initialize CORS
    CORS(app, resources={r"/*": cors_config})
    
    # Add after_request handler for additional CORS headers
    @app.after_request
    def after_request(response):
        origin = request.headers.get('Origin')
        if origin:
            if cors_config['origins'] == '*':
                response.headers['Access-Control-Allow-Origin'] = '*'
            elif origin in cors_config.get('origins', []):
                response.headers['Access-Control-Allow-Origin'] = origin
        
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization, Accept'
        response.headers['Access-Control-Max-Age'] = '3600'
        
        if cors_config.get('supports_credentials'):
            response.headers['Access-Control-Allow-Credentials'] = 'true'
        
        return response
    
    # Register blueprints
    from app.routes.interview import interview_bp
    app.register_blueprint(interview_bp, url_prefix='/api')
    
    # Health check endpoint
    @app.route('/health')
    def health():
        return {'status': 'healthy', 'service': 'ai-interviewer-backend'}, 200
    
    return app

