from flask import Blueprint
from Controllers.userController import register_user, login_user, logout_user, get_session

user_bp = Blueprint(
    "user",
    __name__,
    url_prefix="/api/users"
)

user_bp.route(
    "/register",
    methods=["POST"]
)(register_user)

user_bp.route(
    "/login",
    methods=["POST"]
)(login_user)

# Bug #1 Fix — new routes added
user_bp.route(
    "/logout",
    methods=["POST"]
)(logout_user)

user_bp.route(
    "/session",
    methods=["GET"]
)(get_session)

