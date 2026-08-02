from flask import Blueprint

from Controllers.quizCreatorController import generate_quiz
from middleware.auth import login_required

quiz_bp = Blueprint(

    "quiz",

    __name__,

    url_prefix="/api/quiz"

)

quiz_bp.route(

    "/generate",

    methods=["POST"]

)(login_required(generate_quiz))