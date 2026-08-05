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
load_dotenv()

matplotlib.use("Agg")

app = Flask(__name__)

_WEAK_KEYS = {"123456", "secret", "password", "dev", "test", "flask", "change_me"}

_secret_key = os.getenv("SECRET_KEY", "")

if not _secret_key:
    raise SystemExit(
        "\n[SECURITY ERROR] SECRET_KEY is not set in your .env file.\n"
        "Run this command to generate one:\n"
        "  python -c \"import secrets; print(secrets.token_hex(32))\"\n"
        "Then add it to your .env file as: SECRET_KEY=<generated_value>\n"
    )

if len(_secret_key) < 32 or _secret_key.lower() in _WEAK_KEYS:
    raise SystemExit(
        f"\n[SECURITY ERROR] SECRET_KEY is too weak ('{_secret_key[:6]}...').\n"
        "It must be at least 32 characters long and not a common word.\n"
        "Run this command to generate a secure key:\n"
        "  python -c \"import secrets; print(secrets.token_hex(32))\"\n"
        "Then update SECRET_KEY in your .env file.\n"
    )

app.config["SECRET_KEY"] = _secret_key

# Bug #1 Fix: Session security configuration
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(days=7)  # Session lasts 7 days
app.config["SESSION_COOKIE_HTTPONLY"]    = True               # JS cannot read the cookie (XSS protection)
app.config["SESSION_COOKIE_SAMESITE"]    = "Lax"              # CSRF protection
app.config["SESSION_COOKIE_SECURE"]      = False              # Set True in production (HTTPS only)

STATIC_FOLDER = os.path.join(app.root_path, "static")
os.makedirs(STATIC_FOLDER, exist_ok=True)

app.config["STATIC_FOLDER"] = STATIC_FOLDER

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
if __name__ == "__main__":
    app.run(debug=True)