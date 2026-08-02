from flask import Blueprint, render_template

home_bp = Blueprint("home", __name__)


@home_bp.route("/")
def home():
    return render_template("home.html")


@home_bp.route("/signup")
def signup():
    return render_template("signup.html")

@home_bp.route("/login")
def login():
    return render_template("login.html")

@home_bp.route("/profile")
def profile():
    return render_template("profile.html")

@home_bp.route("/courses")
def allCourse():
    return render_template("allCourses.html")


@home_bp.route("/module<int:module_id>")
def module(module_id):
    """Dynamic route to render modules (e.g. Module_1.html, Module_2.html) automatically.
    Returns 404 if the module template does not exist.
    """
    from jinja2.exceptions import TemplateNotFound
    try:
        return render_template(f"Modules/Module_{module_id}.html")
    except TemplateNotFound:
        return f"Module {module_id} not found.", 404

@home_bp.route("/course/<course_id>")
def course(course_id):
    return render_template("getCourse.html")

@home_bp.route("/course/content")
def course_content():
    return render_template("courseContent.html")

@home_bp.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

@home_bp.route("/complaints")
def complaints():
    return render_template("complaints.html")

@home_bp.route("/test")
def test():
    return render_template("test.html")


@home_bp.route("/tutor")
def tutor():
    return render_template("aiTutor.html")

@home_bp.route("/notebook", methods=["GET"])
def notebook():
    return render_template("notebook.html")

@home_bp.route("/quiz")
def quiz():
    return render_template("quiz.html")

@home_bp.route("/visualizer", methods=["GET"])
def visualizer():
    return render_template("visualizer.html")