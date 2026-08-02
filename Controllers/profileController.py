# Bug #4 Fix: duplicate imports removed.
# UserModel was imported on line 2 AND line 4.
# flask request/jsonify was imported on line 1 AND line 6.
from flask import request, jsonify
from Models.userModel import UserModel
from Models.courseModel import CourseModel


def get_completed_courses():

    data = request.get_json()

    if not data:

        return jsonify({

            "success": False,

            "message": "No data received."

        }), 400

    user_id = data.get("id")
    email = data.get("email")

    # Guard against Insecure Direct Object Reference (IDOR):
    # Ensure the logged-in user can only query their own data.
    from flask import session
    if session.get("user_id") != user_id:
        return jsonify({
            "success": False,
            "message": "Unauthorized: You cannot access completed courses for another user's account."
        }), 403

    if not user_id or not email:

        return jsonify({

            "success": False,

            "message": "User ID and Email are required."

        }), 400

    try:

        user = UserModel.get_profile(user_id, email)

    except Exception:

        return jsonify({

            "success": False,

            "message": "Invalid User ID."

        }), 400

    if not user:

        return jsonify({

            "success": False,

            "message": "User not found."

        }), 404

    completed_courses = []

    for course_id in user.get("completed_courses", []):

        course = CourseModel.get_course(course_id)

        if not course:
            continue

        completed_courses.append({

            "course_id": str(course["_id"]),

            "title": course.get("title"),

            "description": course.get("description"),

            "difficulty": course.get("difficulty"),

            "estimated_time": course.get("estimated_time"),

            "main_image": course.get("main_image")

        })

    completed_lessons = []

    for lesson in user.get("completed_lessons", []):

        course = CourseModel.get_course(

            lesson.get("course_id")

        )

        if not course:
            continue

        completed_lessons.append({

            "course_id": str(course["_id"]),

            "title": course.get("title"),

            "description": course.get("description"),

            "progress": lesson.get("progress", 0),

            "last_lesson": lesson.get("last_lesson", 0),

            "updated_at": lesson.get("updated_at")

        })

    return jsonify({

        "success": True,

        "completed_courses": completed_courses,

        "completed_lessons": completed_lessons

    })

    
def get_profile():

    data = request.get_json()

    if not data:

        return jsonify({

            "success": False,
            "message": "No data received."

        }), 400

    user_id = data.get("id")
    email = data.get("email")

    # Guard against Insecure Direct Object Reference (IDOR):
    # Ensure the logged-in user can only query their own data.
    from flask import session
    if session.get("user_id") != user_id:
        return jsonify({
            "success": False,
            "message": "Unauthorized: You cannot access profile details of another user's account."
        }), 403

    if not user_id or not email:

        return jsonify({

            "success": False,
            "message": "User ID and Email are required."

        }), 400

    try:

        user = UserModel.get_profile(user_id, email)

    except Exception:

        return jsonify({

            "success": False,
            "message": "Invalid User ID."

        }), 400

    if not user:

        return jsonify({

            "success": False,
            "message": "User not found."

        }), 404

    profile = {

        "id": str(user["_id"]),

        # Personal
        "first_name": user.get("first_name"),
        "last_name": user.get("last_name"),
        "full_name": user.get("full_name"),

        "email": user.get("email"),
        "phone": user.get("phone"),

        "profile_image": user.get("profile_image"),

        "gender": user.get("gender"),
        "dob": user.get("dob"),
        "bio": user.get("bio"),

        # Academic

        "college": user.get("college"),
        "university": user.get("university"),
        "course": user.get("course"),
        "branch": user.get("branch"),
        "semester": user.get("semester"),

        # Address

        "country": user.get("country"),
        "state": user.get("state"),
        "city": user.get("city"),

        # Learning

        "learning_level": user.get("learning_level"),
        "current_course": user.get("current_course"),

        "completed_courses": user.get("completed_courses"),
        "completed_lessons": user.get("completed_lessons"),

        "favorite_courses": user.get("favorite_courses"),
        "bookmarked_lessons": user.get("bookmarked_lessons"),

        "learning_streak": user.get("learning_streak"),

        "total_learning_hours": user.get("total_learning_hours"),

        "xp": user.get("xp"),

        "coins": user.get("coins"),

        "badges": user.get("badges"),

        "certificates": user.get("certificates"),

        "simulation_history": user.get("simulation_history"),

        # Account

        "role": user.get("role"),

        "is_verified": user.get("is_verified"),

        "email_verified": user.get("email_verified"),

        "phone_verified": user.get("phone_verified"),

        "is_active": user.get("is_active"),

        "last_login": user.get("last_login"),

        "created_at": user.get("created_at")

    }

    return jsonify({

        "success": True,

        "profile": profile

    }), 200