from flask import Flask
from datetime import timedelta
import matplotlib
import os
from dotenv import load_dotenv

from Controllers.homeController import home_bp
from Controllers.simulationController import simulation_bp
from Routes.userRoutes import user_bp
from Routes.profileRoutes import profile_bp
from Routes.courseRoutes import course_bp
from Routes.userCourseRoutes import user_course_bp
from Routes.tutorRoutes import tutor_bp
from Routes.notebookRoutes import notebook_bp
from Routes.quizCreatorRoutes import quiz_bp
from Routes.circuitRoutes import circuit_bp
from Routes.complaintRoutes import complaint_bp

# Load environment variables (.env for local development)
load_dotenv()

# Use non-GUI backend for matplotlib (required on Render/Linux)
matplotlib.use("Agg")

# Create Flask app
app = Flask(__name__)

# ============================================================
# SECRET KEY VALIDATION
# ============================================================

_WEAK_KEYS = {
    "123456",
    "secret",
    "password",
    "dev",
    "test",
    "flask",
    "change_me",
}

_secret_key = os.getenv("SECRET_KEY", "")

if not _secret_key:
    raise SystemExit(
        "\n[SECURITY ERROR] SECRET_KEY is not set.\n"
        "Generate one using:\n"
        'python -c "import secrets; print(secrets.token_hex(32))"\n'
        "Then add it to your .env file:\n"
        "SECRET_KEY=<your_generated_key>"
    )

if len(_secret_key) < 32 or _secret_key.lower() in _WEAK_KEYS:
    raise SystemExit(
        "\n[SECURITY ERROR] SECRET_KEY is too weak.\n"
        "Generate a stronger key using:\n"
        'python -c "import secrets; print(secrets.token_hex(32))"\n'
    )

app.config["SECRET_KEY"] = _secret_key

# ============================================================
# SESSION CONFIGURATION
# ============================================================

app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(days=7)
app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"

# HTTPS-only cookies in production
app.config["SESSION_COOKIE_SECURE"] = (
    os.getenv("FLASK_ENV", "").lower() == "production"
)

# ============================================================
# STATIC FOLDER
# ============================================================

STATIC_FOLDER = os.path.join(app.root_path, "static")
os.makedirs(STATIC_FOLDER, exist_ok=True)

app.config["STATIC_FOLDER"] = STATIC_FOLDER

# ============================================================
# REGISTER BLUEPRINTS
# ============================================================

app.register_blueprint(home_bp)
app.register_blueprint(simulation_bp)
app.register_blueprint(user_bp)
app.register_blueprint(profile_bp)
app.register_blueprint(course_bp)
app.register_blueprint(user_course_bp)
app.register_blueprint(notebook_bp)
app.register_blueprint(tutor_bp)
app.register_blueprint(quiz_bp)
app.register_blueprint(circuit_bp)
app.register_blueprint(complaint_bp)


# ============================================================
# RUN APPLICATION
# ============================================================

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(
        host="0.0.0.0",
        port=port,
        debug=True
    )