from flask import request, jsonify, session
from Models.complaintModel import ComplaintModel


def create_complaint():
    """
    API endpoint: POST /api/complaints/create
    Submits a new complaint into MongoDB.
    """
    data = request.get_json()

    if not data:
        return jsonify({
            "success": False,
            "message": "No data received. Send JSON body with complaint fields."
        }), 400

    user_id = data.get("user_id")
    name = data.get("name")
    email = data.get("email")
    category = data.get("category")
    priority = data.get("priority")
    title = data.get("title")
    description = data.get("description")

    # IDOR Check: Ensure logged-in user matches user_id
    if session.get("user_id") and session.get("user_id") != user_id:
        return jsonify({
            "success": False,
            "message": "Unauthorized: You cannot submit complaints for another account."
        }), 403

    if not user_id or not category or not title or not description:
        return jsonify({
            "success": False,
            "message": "Please fill in all required fields: category, title, and description."
        }), 400

    success, message, complaint_id = ComplaintModel.create_complaint(
        user_id=user_id,
        name=name,
        email=email,
        category=category,
        priority=priority,
        title=title,
        description=description
    )

    if not success:
        return jsonify({
            "success": False,
            "message": message
        }), 500

    return jsonify({
        "success": True,
        "message": "Complaint submitted successfully! Our support team will review it shortly.",
        "complaint_id": complaint_id
    }), 201


def get_user_complaints():
    """
    API endpoint: POST /api/complaints/user
    Fetches all complaints submitted by the current user.
    """
    data = request.get_json() or {}
    user_id = data.get("user_id") or session.get("user_id")

    if not user_id:
        return jsonify({
            "success": False,
            "message": "User ID is required."
        }), 400

    # IDOR Check: Ensure logged-in user matches requested user_id
    if session.get("user_id") and session.get("user_id") != user_id:
        return jsonify({
            "success": False,
            "message": "Unauthorized: You cannot access complaints for another user's account."
        }), 403

    complaints = ComplaintModel.get_user_complaints(user_id)

    return jsonify({
        "success": True,
        "complaints": complaints
    }), 200
