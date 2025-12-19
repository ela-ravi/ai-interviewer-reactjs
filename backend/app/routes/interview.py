"""
Interview API routes
"""
from flask import Blueprint, request, jsonify
from functools import wraps
import asyncio
from flask_cors import CORS
from app.services.interview_service import interview_service

# Create blueprint
interview_bp = Blueprint('interview', __name__)

# Enable CORS for this blueprint
CORS(
    interview_bp,
    resources={r"/interview/*": {"origins": "*"}},
    supports_credentials=False
)


def handle_errors(f):
    """Decorator to handle errors consistently for sync & async routes"""

    @wraps(f)
    async def async_wrapper(*args, **kwargs):
        try:
            return await f(*args, **kwargs)
        except ValueError as e:
            import traceback
            traceback.print_exc()
            return jsonify({'error': str(e)}), 400
        except Exception as e:
            import traceback
            traceback.print_exc()
            return jsonify({
                'error': 'Internal server error',
                'details': str(e)
            }), 500

    @wraps(f)
    def sync_wrapper(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except ValueError as e:
            import traceback
            traceback.print_exc()
            return jsonify({'error': str(e)}), 400
        except Exception as e:
            import traceback
            traceback.print_exc()
            return jsonify({
                'error': 'Internal server error',
                'details': str(e)
            }), 500

    if asyncio.iscoroutinefunction(f):
        return async_wrapper
    return sync_wrapper


# -------------------- ROUTES -------------------- #

@interview_bp.route('/interview/create', methods=['POST'])
@handle_errors
def create_interview():
    """
    Create a new interview session
    """
    data = request.get_json()

    if not data or 'technology' not in data or 'position' not in data:
        return jsonify({'error': 'Missing technology or position'}), 400

    session_id = interview_service.create_session(
        data['technology'],
        data['position']
    )

    return jsonify({
        'session_id': session_id,
        'technology': data['technology'],
        'position': data['position'],
        'message': 'Interview session created successfully'
    }), 201


@interview_bp.route('/interview/<session_id>/start', methods=['POST'])
@handle_errors
async def start_interview(session_id):
    """
    Start an interview and get the first question
    """
    result = await interview_service.start_interview(session_id)
    return jsonify(result), 200


@interview_bp.route('/interview/<session_id>/answer', methods=['POST'])
@handle_errors
async def submit_answer(session_id):
    """
    Submit an answer to the current question
    """
    data = request.get_json()

    if not data or 'answer' not in data:
        return jsonify({'error': 'Missing answer'}), 400

    result = await interview_service.submit_answer(
        session_id,
        data['answer']
    )

    return jsonify(result), 200


@interview_bp.route('/interview/<session_id>/next-question', methods=['POST'])
@handle_errors
async def get_next_question(session_id):
    """
    Get the next question
    """
    result = await interview_service.get_next_question(session_id)
    return jsonify(result), 200


@interview_bp.route('/interview/<session_id>/end', methods=['POST'])
@handle_errors
async def end_interview(session_id):
    """
    End the interview and return summary
    """
    result = await interview_service.end_interview(session_id)
    return jsonify(result), 200


@interview_bp.route('/interview/<session_id>', methods=['GET'])
@handle_errors
def get_session_info(session_id):
    """
    Get session information
    """
    info = interview_service.get_session_info(session_id)
    return jsonify(info), 200


@interview_bp.route('/interview/<session_id>', methods=['DELETE'])
@handle_errors
def delete_session(session_id):
    """
    Delete a session
    """
    success = interview_service.delete_session(session_id)

    if success:
        return jsonify({'message': 'Session deleted successfully'}), 200
    return jsonify({'error': 'Session not found'}), 404
