import sys
import re
import subprocess
import logging

logger = logging.getLogger("ExecutionModule")

# Regular expression to validate standard package names and version specifiers (PEP 508 / PyPI compliant)
# Allows alphanumeric characters, dot, hyphen, underscore, and optional comparison operators with versions.
# Rejects flags like --extra-index-url or any shell control characters.
PACKAGE_NAME_REGEX = re.compile(r"^[a-zA-Z0-9_\-\.]+(?:\s*(?:==|>=|<=|>|<|!=|~=)\s*[a-zA-Z0-9_\-\.\*]+)?$")

def install_package(package_name):
    """Installs a python library into the current python environment using pip."""
    package_name = package_name.strip()
    if not package_name:
        return {"success": False, "message": "Package name cannot be empty."}

    # Basic sanitization for safety
    if any(char in package_name for char in [";", "&", "|", "`", "$"]):
        return {"success": False, "message": "Invalid characters in package name."}

    # Strict whitelist regex check to prevent flag injection
    if not PACKAGE_NAME_REGEX.match(package_name):
        return {"success": False, "message": "Invalid package name format. Only letters, numbers, dot, hyphen, underscore, and optional version specifiers are allowed."}

    cmd = [sys.executable, "-m", "pip", "install", package_name]

    try:
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True
        )
        stdout, _ = process.communicate(timeout=120)

        if process.returncode == 0:
            return {
                "success": True,
                "output": stdout,
                "message": f"Successfully installed '{package_name}'!"
            }
        else:
            return {
                "success": False,
                "output": stdout,
                "message": f"Failed to install '{package_name}'."
            }
    except subprocess.TimeoutExpired:
        process.kill()
        return {"success": False, "message": "Installation timed out (120s limit)."}
    except Exception as e:
        return {"success": False, "message": f"Error running pip: {str(e)}"}


def list_installed_packages():
    """Lists installed packages in current environment."""
    try:
        cmd = [sys.executable, "-m", "pip", "list", "--format=json"]
        res = subprocess.run(cmd, capture_output=True, text=True, check=True)
        import json
        return json.loads(res.stdout)
    except Exception as e:
        logger.error(f"Error fetching packages: {e}")
        return []
