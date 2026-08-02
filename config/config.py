import os

# Project root directory (one level up from config/)
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
NOTEBOOKS_DIR = os.path.join(BASE_DIR, "saved_notebooks")

os.makedirs(NOTEBOOKS_DIR, exist_ok=True)

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-jupyter-flask-secret-key")
    NOTEBOOKS_DIR = NOTEBOOKS_DIR
    EXECUTION_TIMEOUT = 30  # seconds timeout for kernel responses
