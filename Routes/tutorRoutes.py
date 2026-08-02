from flask import Blueprint

from Controllers.tutorController import ask_tutor
from middleware.auth import login_required


tutor_bp = Blueprint(

    "tutor",

    __name__,

    url_prefix="/api/tutor"

)


tutor_bp.route(

    "/ask",

    methods=["POST"]

)(login_required(ask_tutor))