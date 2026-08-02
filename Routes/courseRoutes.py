from flask import Blueprint

from Controllers.courseController import all_courses, single_course, completed_courses

course_bp=Blueprint(

    "course",

    __name__,

    url_prefix="/api/course"

)

course_bp.route(

    "/all",

    methods=["GET"]

)(all_courses)

course_bp.route(

    "/<course_id>",

    methods=["GET"]

)(single_course)

from middleware.auth import login_required

course_bp.route(

    "/completed",

    methods=["POST"]

)(login_required(completed_courses))


