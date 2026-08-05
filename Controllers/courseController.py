from flask import jsonify, request
from Models.courseModel import CourseModel
from bson.errors import InvalidId


def all_courses():

    # Bug #6 Fix: wrap DB call so a MongoDB failure returns a clean 500
    # instead of an unhandled exception with a Python traceback.
    try:

        courses = CourseModel.get_all_courses()

    except Exception as e:

        return jsonify({

            "success": False,
            "message": "Failed to fetch courses. Please try again later.",
            "error": str(e)

        }), 500

    data = []

    for course in courses:

        data.append({

            "id":            str(course["_id"]),
            "slug":          course.get("slug"),
            "title":         course.get("title"),
            "description":   course.get("description"),
            "main_image":    course.get("main_image"),
            "sub_image":     course.get("sub_image"),
            "tags":          course.get("tags"),
            "difficulty":    course.get("difficulty"),
            "estimated_time":course.get("estimated_time")

        })

    return jsonify({

        "success": True,
        "courses": data

    })


def single_course(course_id):

    # Bug #6 Fix: If course_id is not a valid MongoDB ObjectId (e.g. /api/course/abc),
    # CourseModel.get_course() raises bson.errors.InvalidId which caused an unhandled 500.
    # Now returns a clean 400 with a descriptive message.
    try:

        course = CourseModel.get_course(course_id)

    except InvalidId:

        return jsonify({

            "success": False,
            "message": f"'{course_id}' is not a valid Course ID."

        }), 400

    except Exception as e:

        return jsonify({

            "success": False,
            "message": "Failed to fetch course. Please try again later.",
            "error": str(e)

        }), 500

    if not course:

        return jsonify({

            "success": False,
            "message": "Course Not Found"

        }), 404

    return jsonify({

        "success": True,

        "course": {

            "id":           str(course["_id"]),
            "title":        course.get("title"),
            "description":  course.get("description"),
            "main_image":   course.get("main_image"),
            "sub_image":    course.get("sub_image"),
            "tags":         course.get("tags"),
            "difficulty":   course.get("difficulty"),
            "estimated_time":course.get("estimated_time"),
            "html_content": course.get("html_content")

        }

    })


def completed_courses():

    # Bug #6 Fix: data was used without a null-check.
    # If the request body is missing or not JSON, data is None and
    # data.get("id") raises: AttributeError: 'NoneType' has no attribute 'get'
    data = request.get_json()

    if not data:

        return jsonify({

            "success": False,
            "message": "No data received. Send JSON with 'id' and 'email'."

        }), 400

    user_id = data.get("id")
    email   = data.get("email")

    # Guard against Insecure Direct Object Reference (IDOR):
    # Ensure the logged-in user can only query their own data.
    from flask import session
    if session.get("user_id") != user_id:
        return jsonify({
            "success": False,
            "message": "Unauthorized: You cannot view completed courses for another user's account."
        }), 403

    # Validate required fields before hitting the database
    if not user_id or not email:

        return jsonify({

            "success": False,
            "message": "Both 'id' and 'email' are required."

        }), 400

    try:

        completed = CourseModel.get_completed_courses(user_id, email)

    except Exception as e:

        return jsonify({

            "success": False,
            "message": "Failed to fetch completed courses.",
            "error": str(e)

        }), 500

    return jsonify({

        "success": True,
        "completed_courses": completed

    })