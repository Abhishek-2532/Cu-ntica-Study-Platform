from functools import wraps
from flask import session, jsonify

def login_required(f):
    """Decorator to protect routes and require user authentication.
    Returns 401 Unauthorized if no user session exists.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            return jsonify({
                "success": False,
                "message": "Authentication required. Please log in."
            }), 401
        return f(*args, **kwargs)
    return decorated_function
