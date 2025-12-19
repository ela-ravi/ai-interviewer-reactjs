"""
Flask application factory
"""
from flask import Flask, request, jsonify
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
    
    # Get CORS configuration
    cors_origins = os.getenv('CORS_ORIGINS', '')
    flask_env = os.getenv('FLASK_ENV', 'development')
    
    # Apply CORS globally - Production-safe configuration
    if flask_env == 'production' and cors_origins and cors_origins != '*':
        # Production: Strict CORS with specific origins
        origins_list = [origin.strip() for origin in cors_origins.split(',') if origin.strip()]
        print(f"🔒 CORS (Production): Allowing specific origins: {origins_list}")
        CORS(app,
             resources={
                 r"/*": {
                     "origins": origins_list,
                     "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
                     "allow_headers": [
                         "Content-Type",
                         "Authorization",
                         "Accept",
                         "X-Requested-With",
                         "Cache-Control"
                     ],
                     "expose_headers": ["Content-Type"],
                     "supports_credentials": False,  # No cookies needed
                     "max_age": 3600
                 }
             })
    else:
        # Development: Allow all origins
        print(f"🔓 CORS (Development): Allowing all origins")
        CORS(app,
             resources={
                 r"/*": {
                     "origins": "*",
                     "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
                     "allow_headers": [
                         "Content-Type",
                         "Authorization",
                         "Accept",
                         "X-Requested-With",
                         "Cache-Control"
                     ],
                     "expose_headers": ["Content-Type"],
                     "supports_credentials": False,
                     "max_age": 3600
                 }
             })
    
    # Register blueprints
    from app.routes.interview import interview_bp
    app.register_blueprint(interview_bp, url_prefix='/api')
    
    # Health check endpoint
    @app.route('/health')
    def health():
        return {'status': 'healthy', 'service': 'ai-interviewer-backend'}, 200
    
    # Test endpoint for production debugging
    @app.route('/api/test')
    def test_endpoint():
        """Test endpoint to verify backend configuration"""
        import sys
        from datetime import datetime
        
        # Get CORS configuration (safe to expose)
        cors_origins = os.getenv('CORS_ORIGINS', '')
        cors_mode = 'wildcard (*)' if not cors_origins or cors_origins == '*' else f'specific origins: {cors_origins}'
        
        return jsonify({
            'status': 'ok',
            'message': 'Backend is running successfully',
            'timestamp': datetime.utcnow().isoformat(),
            'environment': {
                'flask_env': os.getenv('FLASK_ENV', 'development'),
                'debug_mode': os.getenv('FLASK_DEBUG', 'False'),
                'python_version': sys.version,
            },
            'cors': {
                'mode': cors_mode,
                'enabled': True,
                'methods': ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
                'headers': ['Content-Type', 'Authorization', 'Accept']
            },
            'api': {
                'base_url': request.host_url.rstrip('/'),
                'endpoints': {
                    'health': '/health',
                    'test': '/api/test',
                    'create_interview': '/api/interview/create',
                    'start_interview': '/api/interview/<session_id>/start',
                    'submit_answer': '/api/interview/<session_id>/answer',
                    'next_question': '/api/interview/<session_id>/next-question',
                    'end_interview': '/api/interview/<session_id>/end',
                    'get_session': '/api/interview/<session_id>',
                }
            },
            'model': {
                'provider': 'OpenRouter',
                'model': os.getenv('MODEL', 'mistralai/mistral-small-creative'),
                'api_key_configured': bool(os.getenv('OPENROUTER_API_KEY'))
            }
        }), 200
    
    return app

