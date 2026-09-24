"""
Interview API routes
"""
from flask import Blueprint, request, jsonify, make_response
from functools import wraps
import asyncio
import threading
from app.services.interview_service import interview_service

# Create blueprint (CORS handled globally in app/__init__.py)
interview_bp = Blueprint('interview', __name__)

# One loop for the process. Flask's async views close their loop after each
# request, and the shared OpenAI client then dies with "Event loop is closed".
_loop = None
_loop_lock = threading.Lock()


def _run_loop(loop):
    asyncio.set_event_loop(loop)
    loop.run_forever()


def run_async(coro):
    global _loop
    with _loop_lock:
        if _loop is None or _loop.is_closed():
            _loop = asyncio.new_event_loop()
            threading.Thread(target=_run_loop, args=(_loop,), name="interview-loop", daemon=True).start()
    return asyncio.run_coroutine_threadsafe(coro, _loop).result()


def handle_errors(f):
    """Decorator to handle errors consistently"""

    @wraps(f)
    def sync_wrapper(*args, **kwargs):
        if request.method == 'OPTIONS':
            return make_response('', 200)

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

    return sync_wrapper


# -------------------- ROUTES -------------------- #

@interview_bp.route('/interview/create', methods=['POST', 'OPTIONS'])
@handle_errors
def create_interview():
    """
    Create a new interview session
    
    Flask-CORS handles OPTIONS automatically, but route must accept it
    """
    # OPTIONS is handled by @handle_errors decorator
    # #region agent log
    try:
        import json
        log_data = {
            "sessionId": "debug-session",
            "runId": "run1",
            "hypothesisId": "B",
            "location": "routes/interview.py:create_interview",
            "message": "Route handler called",
            "data": {
                "method": request.method,
                "path": request.path,
                "url": request.url,
                "endpoint": request.endpoint,
                "blueprint": request.blueprint if hasattr(request, 'blueprint') else None
            },
            "timestamp": __import__('time').time() * 1000
        }
        with open('/Volumes/Development/Practise/ai-interviewer/.cursor/debug.log', 'a') as f:
            f.write(json.dumps(log_data) + '\n')
    except Exception:
        pass  # Don't fail if logging fails
    # #endregion
    
    data = request.get_json()

    if not data or 'technology' not in data or 'position' not in data:
        return jsonify({'error': 'Missing technology or position'}), 400

    # Build the model client on the long-lived loop, same place later calls run.
    async def _create():
        return interview_service.create_session(data['technology'], data['position'])

    session_id = run_async(_create())

    return jsonify({
        'session_id': session_id,
        'technology': data['technology'],
        'position': data['position'],
        'message': 'Interview session created successfully'
    }), 201


@interview_bp.route('/interview/<session_id>/start', methods=['POST', 'OPTIONS'])
@handle_errors
def start_interview(session_id):
    """
    Start an interview and get the first question
    """
    result = run_async(interview_service.start_interview(session_id))
    return jsonify(result), 200


@interview_bp.route('/interview/<session_id>/answer', methods=['POST', 'OPTIONS'])
@handle_errors
def submit_answer(session_id):
    """
    Submit an answer to the current question
    """
    data = request.get_json()

    if not data or 'answer' not in data:
        return jsonify({'error': 'Missing answer'}), 400

    result = run_async(interview_service.submit_answer(
        session_id,
        data['answer']
    ))

    return jsonify(result), 200


@interview_bp.route('/interview/<session_id>/next-question', methods=['POST', 'OPTIONS'])
@handle_errors
def get_next_question(session_id):
    """
    Get the next question
    """
    result = run_async(interview_service.get_next_question(session_id))
    return jsonify(result), 200


@interview_bp.route('/interview/<session_id>/end', methods=['POST', 'OPTIONS'])
@handle_errors
def end_interview(session_id):
    """
    End the interview and return summary
    """
    result = run_async(interview_service.end_interview(session_id))
    return jsonify(result), 200


@interview_bp.route('/interview/<session_id>', methods=['GET', 'OPTIONS'])
@handle_errors
def get_session_info(session_id):
    """
    Get session information
    """
    # OPTIONS is handled by @handle_errors decorator
    info = interview_service.get_session_info(session_id)
    return jsonify(info), 200


@interview_bp.route('/interview/<session_id>', methods=['DELETE', 'OPTIONS'])
@handle_errors
def delete_session(session_id):
    """
    Delete a session
    """
    # OPTIONS is handled by @handle_errors decorator
    success = interview_service.delete_session(session_id)

    if success:
        return jsonify({'message': 'Session deleted successfully'}), 200
    return jsonify({'error': 'Session not found'}), 404


def _check_run_async():
    async def loop_id():
        await asyncio.sleep(0)
        return id(asyncio.get_running_loop())

    assert run_async(loop_id()) == run_async(loop_id())


if __name__ == "__main__":
    _check_run_async()
    print("run_async ok")
