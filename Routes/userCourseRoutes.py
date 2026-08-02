from flask import Blueprint

from Controllers.userCourseController import update_course_progress
from middleware.auth import login_required

user_course_bp = Blueprint(

    "user_course",

    __name__,

    url_prefix="/api/user-course"

)

user_course_bp.route(

    "/progress",

    methods=["POST"]

)(login_required(update_course_progress))