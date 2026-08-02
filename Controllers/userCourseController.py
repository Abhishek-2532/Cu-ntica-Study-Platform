from flask import request, jsonify
from Models.userCourseModel import UserCourseModel


def update_course_progress():

    # Bug #7 Fix: The original code called data.get() on lines 10–13
    # BEFORE checking if data was None on line 15.
    # If the request body is missing or not JSON, data is None and every
    # .get() call raises: AttributeError: 'NoneType' has no attribute 'get'
    # Fix: null-check FIRST, then extract fields.
    data = request.get_json()

    if not data:

        return jsonify({

            "success": False,
            "message": "No data received. Send JSON body with required fields."

        }), 400

    user_id   = data.get("user_id")
    course_id = data.get("course_id")

    # Guard against Insecure Direct Object Reference (IDOR):
    # Ensure the logged-in user can only update their own progress data.
    from flask import session
    if session.get("user_id") != user_id:
        return jsonify({
            "success": False,
            "message": "Unauthorized: You cannot update progress data for another user's account."
        }), 403

    # Validate required string fields before touching the DB
    if not user_id or not course_id:

        return jsonify({

            "success": False,
            "message": "user_id and course_id are required."

        }), 400

    # Bug #7 Fix: int() conversion crashes with ValueError if the value is
    # not a valid number (e.g. "progress": "abc"). Use safe conversion instead.
    try:
        progress    = int(data.get("progress", 0))
        last_lesson = int(data.get("last_lesson", 0))
    except (ValueError, TypeError):

        return jsonify({

            "success": False,
            "message": "progress and last_lesson must be integers."

        }), 400

    # Clamp progress to valid range
    if progress < 0:
        progress = 0

    if progress > 100:
        progress = 100

    # Bug #7 Fix: wrap model call in try/except.
    # If user_id is not a valid MongoDB ObjectId, ObjectId(user_id) inside
    # the model raises bson.errors.InvalidId — previously unhandled.
    try:

        success, message = UserCourseModel.update_course_progress(
            user_id,
            course_id,
            progress,
            last_lesson
        )

    except Exception as e:

        return jsonify({

            "success": False,
            "message": "Failed to update progress. Check that user_id is a valid ID.",
            "error": str(e)

        }), 400

    return jsonify({

        "success": success,
        "message": message

    })