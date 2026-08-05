from flask import Blueprint
from Controllers.complaintController import (
    create_complaint,
    get_user_complaints
)

complaint_bp = Blueprint("complaint_bp", __name__)

complaint_bp.route("/api/complaints/create", methods=["POST"])(create_complaint)
complaint_bp.route("/api/complaints/user", methods=["POST"])(get_user_complaints)
