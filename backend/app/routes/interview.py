"""
Interview API routes
"""
from flask import Blueprint, request, jsonify
from functools import wraps
from app.services.interview_service import interview_service

interview_bp = Blueprint('interview', __name__)


def handle_errors(f):
    """Decorator to handle errors consistently"""
    @wraps(f)
    async def async_wrapper(*args, **kwargs):
        try:
            return await f(*args, **kwargs)
        except ValueError as e:
            import traceback
            print(f"ValueError: {str(e)}")
            traceback.print_exc()
            return jsonify({'error': str(e)}), 400
        except Exception as e:
            import traceback
            print(f"Error in {f.__name__}: {str(e)}")
            traceback.print_exc()
            return jsonify({'error': 'Internal server error', 'details': str(e)}), 500
    
    @wraps(f)
    def sync_wrapper(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except ValueError as e:
            import traceback
            print(f"ValueError: {str(e)}")
            traceback.print_exc()
            return jsonify({'error': str(e)}), 400
        except Exception as e:
            import traceback
            print(f"Error in {f.__name__}: {str(e)}")
            traceback.print_exc()
            return jsonify({'error': 'Internal server error', 'details': str(e)}), 500
    
    # Check if function is async
    import asyncio
    if asyncio.iscoroutinefunction(f):
        return async_wrapper
    return sync_wrapper


@interview_bp.route('/interview/create', methods=['POST', 'OPTIONS'])
@handle_errors
def create_interview():
    """
    Create a new interview session
    
    Request body:
    {
        "technology": "Python",
        "position": "Senior Developer"
    }
    
    Response:
    {
        "session_id": "uuid",
        "technology": "Python",
        "position": "Senior Developer"
    }
    """
    # Handle preflight OPTIONS request
    if request.method == 'OPTIONS':
        return '', 200
    
    data = request.get_json()
    
    if not data or 'technology' not in data or 'position' not in data:
        return jsonify({'error': 'Missing technology or position'}), 400
    
    technology = data['technology']
    position = data['position']
    
    session_id = interview_service.create_session(technology, position)
    
    return jsonify({
        'session_id': session_id,
        'technology': technology,
        'position': position,
        'message': 'Interview session created successfully'
    }), 201


@interview_bp.route('/interview/<session_id>/start', methods=['POST'])
@handle_errors
async def start_interview(session_id):
    """
    Start an interview and get the first question
    
    Response:
    {
        "session_id": "uuid",
        "question_number": 1,
        "question": "What is...?"
    }
    """
    result = await interview_service.start_interview(session_id)
    return jsonify(result), 200


@interview_bp.route('/interview/<session_id>/answer', methods=['POST'])
@handle_errors
async def submit_answer(session_id):
    """
    Submit an answer to the current question
    
    Request body:
    {
        "answer": "The answer is..."
    }
    
    Response:
    {
        "session_id": "uuid",
        "question_number": 1,
        "question": "...",
        "answer": "...",
        "feedback": "...",
        "score": 8,
        "score_details": "..."
    }
    """
    data = request.get_json()
    
    if not data or 'answer' not in data:
        return jsonify({'error': 'Missing answer'}), 400
    
    answer = data['answer']
    result = await interview_service.submit_answer(session_id, answer)
    
    return jsonify(result), 200


@interview_bp.route('/interview/<session_id>/next-question', methods=['POST'])
@handle_errors
async def get_next_question(session_id):
    """
    Get the next question
    
    Response:
    {
        "session_id": "uuid",
        "question_number": 2,
        "question": "What is...?"
    }
    """
    result = await interview_service.get_next_question(session_id)
    return jsonify(result), 200


@interview_bp.route('/interview/<session_id>/end', methods=['POST'])
@handle_errors
async def end_interview(session_id):
    """
    End the interview and get summary
    
    Response:
    {
        "session_id": "uuid",
        "technology": "Python",
        "position": "Senior Developer",
        "summary": {
            "average_score": 7.5,
            "total_questions": 5,
            "scores": [8, 7, 7, 8, 8],
            "summary": "Overall assessment...",
            "history": [...]
        }
    }
    """
    result = await interview_service.end_interview(session_id)
    return jsonify(result), 200


@interview_bp.route('/interview/<session_id>', methods=['GET'])
@handle_errors
def get_session_info(session_id):
    """
    Get session information
    
    Response:
    {
        "session_id": "uuid",
        "technology": "Python",
        "position": "Senior Developer",
        "current_question_number": 3,
        "questions_answered": 2,
        "average_score": 7.5,
        "is_active": true,
        "created_at": "...",
        "last_activity": "..."
    }
    """
    info = interview_service.get_session_info(session_id)
    return jsonify(info), 200


@interview_bp.route('/interview/<session_id>', methods=['DELETE'])
@handle_errors
def delete_session(session_id):
    """
    Delete a session
    
    Response:
    {
        "message": "Session deleted successfully"
    }
    """
    success = interview_service.delete_session(session_id)
    
    if success:
        return jsonify({'message': 'Session deleted successfully'}), 200
    else:
        return jsonify({'error': 'Session not found'}), 404

