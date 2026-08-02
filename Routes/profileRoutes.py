from flask import Blueprint
# Bug #4 Fix: get_profile was imported twice — once on its own (line 2)
# and again inside the tuple import (line 3-6). Merged into one clean import.
from Controllers.profileController import get_profile, get_completed_courses
from middleware.auth import login_required

profile_bp = Blueprint(

    "profile",

    __name__,

    url_prefix="/api/profile"

)

profile_bp.route(

    "/get",

    methods=["POST"]

)(login_required(get_profile))

profile_bp.route(

    "/get-completed-course",

    methods=["POST"]

)(login_required(get_completed_courses))