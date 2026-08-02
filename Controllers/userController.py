from flask import request, jsonify, session
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from Models.userModel import UserModel


DEFAULT_PROFILE_IMAGE = "https://i.pinimg.com/736x/1c/c5/35/1cc535901e32f18db87fa5e340a18aff.jpg"


def register_user():

    data = request.get_json()

    if not data:
        return jsonify({
            "success": False,
            "message": "No data received."
        }), 400

    # Required Fields
    required_fields = [
        "first_name",
        "last_name",
        "email",
        "password"
    ]

    for field in required_fields:
        if not data.get(field):
            return jsonify({
                "success": False,
                "message": f"{field} is required."
            }), 400

    # Duplicate Email Check
    existing_user = UserModel.get_user_by_email(data["email"])

    if existing_user:
        return jsonify({
            "success": False,
            "message": "Email already registered."
        }), 409

    user = {

        # Personal Information
        "first_name": data.get("first_name", "").strip(),
        "last_name": data.get("last_name", "").strip(),
        "full_name": data.get(
            "full_name",
            f'{data.get("first_name","")} {data.get("last_name","")}'
        ).strip(),

        "email": data.get("email", "").lower().strip(),
        "phone": data.get("phone", "").strip(),

        # Store Hashed Password
        "password": generate_password_hash(data.get("password")),

        # Profile
        "profile_image": data.get(
            "profile_image",
            DEFAULT_PROFILE_IMAGE
        ),

        "gender": data.get("gender", ""),
        "dob": data.get("dob", ""),
        "bio": data.get("bio", ""),

        # Academic
        "college": data.get("college", ""),
        "university": data.get("university", ""),
        "course": data.get("course", ""),
        "branch": data.get("branch", ""),
        "semester": data.get("semester", ""),

        # Address
        "country": data.get("country", ""),
        "state": data.get("state", ""),
        "city": data.get("city", ""),

        # Learning
        "learning_level": data.get("learning_level", "Beginner"),

        "current_course": data.get("current_course", ""),

        "completed_courses": [],
        "completed_lessons": [],
        "favorite_courses": [],
        "bookmarked_lessons": [],

        "learning_streak": 0,
        "total_learning_hours": 0,

        "xp": 0,
        "coins": 0,

        "badges": [],
        "certificates": [],
        "quiz_attempts": [],
        "simulation_history": [],

        # Preferences
        "theme": data.get("theme", "light"),
        "language": data.get("language", "English"),
        "notifications": data.get("notifications", True),

        # Account
        "role": "student",

        "is_verified": False,
        "email_verified": False,
        "phone_verified": False,

        "is_active": True,
        "is_banned": False,

        "login_provider": "email",

        "last_login": None,

        # Security
        "password_reset_token": None,

        "otp": None,
        "otp_expiry": None,

        # Timestamp
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()

    }

    result = UserModel.create_user(user)

    return jsonify({

        "success": True,

        "message": "Registration Successful.",

        "user_id": str(result.inserted_id)

    }), 201

def login_user():

    data = request.get_json()

    if not data:
        return jsonify({
            "success": False,
            "message": "No data received."
        }), 400

    email = data.get("email", "").strip().lower()
    password = data.get("password", "").strip()

    if not email or not password:
        return jsonify({
            "success": False,
            "message": "Email and Password are required."
        }), 400

    user = UserModel.get_user_by_email(email)

    if not user:
        return jsonify({
            "success": False,
            "message": "Invalid Email or Password."
        }), 401

    if not check_password_hash(user["password"], password):
        return jsonify({
            "success": False,
            "message": "Invalid Email or Password."
        }), 401

    # Update Last Login
    UserModel.update_last_login(user["_id"])

    # ── Bug #1 Fix: Set Flask session so the server knows who is logged in ──
    session.clear()                                  # Clear any old session first
    session["user_id"]      = str(user["_id"])      # Store user ID server-side
    session["email"]        = user.get("email")     # Store email server-side
    session["full_name"]    = user.get("full_name") # Store name for quick access
    session["role"]         = user.get("role")      # Store role for auth checks
    session.permanent       = True                   # Keep session alive (uses PERMANENT_SESSION_LIFETIME)

    return jsonify({

        "success": True,
        "message": "Login Successful",

        "user": {
            "id": str(user["_id"]),
            "first_name": user.get("first_name"),
            "last_name": user.get("last_name"),
            "full_name": user.get("full_name"),
            "email": user.get("email"),
            "profile_image": user.get("profile_image"),
            "role": user.get("role"),
            "learning_level": user.get("learning_level"),
            "xp": user.get("xp"),
            "coins": user.get("coins")
        }

    }), 200


def logout_user():
    """Clears the server-side session, logging the user out completely."""

    session.clear()

    return jsonify({
        "success": True,
        "message": "Logged out successfully."
    }), 200


def get_session():
    """Returns the currently logged-in user's session data.
    The frontend can call this on page load to restore the user state.
    """

    if "user_id" not in session:
        return jsonify({
            "success": False,
            "logged_in": False,
            "message": "No active session. Please log in."
        }), 401

    return jsonify({
        "success": True,
        "logged_in": True,
        "user": {
            "id":        session.get("user_id"),
            "email":     session.get("email"),
            "full_name": session.get("full_name"),
            "role":      session.get("role")
        }
    }), 200