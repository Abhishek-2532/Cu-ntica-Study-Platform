from flask import request, jsonify, make_response, session
import uuid

from config.config import Config

from kernel.kernel_manager import NotebookKernel

from notebookManager.notebook_manager import NotebookManager

from execution.execution import (
    install_package,
    list_installed_packages
)

# Dictionary to hold the active Jupyter kernels for each session
user_kernels = {}

def get_user_kernel():
    """Lazily gets or creates a Jupyter kernel instance for the current user session."""
    # Ensure the user has a notebook session ID
    if "notebook_session_id" not in session:
        session["notebook_session_id"] = str(uuid.uuid4())
    
    session_id = session["notebook_session_id"]
    if session_id not in user_kernels:
        user_kernels[session_id] = NotebookKernel()
    return user_kernels[session_id]


# Bug #2 Fix: notebook_home() removed — /notebook page is served by homeController.py.
# This controller only contains API handler functions.


def execute():

    data = request.get_json(force=True) or {}

    code = data.get("code","")

    user_kernel = get_user_kernel()

    if not code.strip():

        return jsonify({

            "status":"ok",

            "execution_count":user_kernel.execution_count,

            "outputs":[],

            "error":None

        })

    result = user_kernel.execute(

        code,

        timeout=Config.EXECUTION_TIMEOUT

    )

    return jsonify(result)


def restart_kernel():

    user_kernel = get_user_kernel()
    success = user_kernel.restart()

    return jsonify({

        "success":success,

        "message":"Kernel restarted successfully!" if success else "Failed to restart kernel."

    })


def interrupt_kernel():

    user_kernel = get_user_kernel()
    success = user_kernel.interrupt()

    return jsonify({

        "success":success,

        "message":"Kernel interrupted!" if success else "Failed to interrupt kernel."

    })


def package_install():

    data = request.get_json(force=True) or {}

    package = data.get("package","")

    if package=="":

        return jsonify({

            "success":False,

            "message":"Package name is required."

        }),400

    return jsonify(

        install_package(package)

    )


def get_packages():

    return jsonify({

        "packages":list_installed_packages()

    })


def list_notebooks():

    return jsonify({

        "notebooks":NotebookManager.list_saved_notebooks()

    })


def save_notebook():

    data = request.get_json(force=True) or {}

    filename = data.get(

        "filename",

        "untitled.ipynb"

    )

    cells = data.get(

        "cells",

        []

    )

    path = NotebookManager.save_notebook_to_file(

        filename,

        cells

    )

    return jsonify({

        "success":True,

        "filename":filename,

        "path":path

    })


def load_notebook():

    data = request.get_json(force=True) or {}

    filename = data.get("filename","")

    cells = NotebookManager.load_notebook_from_file(

        filename

    )

    if cells is None:

        return jsonify({

            "success":False,

            "message":"Notebook not found"

        }),404

    return jsonify({

        "success":True,

        "filename":filename,

        "cells":cells

    })


def export_notebook():

    data = request.get_json(force=True) or {}

    filename = data.get(

        "filename",

        "notebook.ipynb"

    )

    cells = data.get(

        "cells",

        []

    )

    if not filename.endswith(".ipynb"):

        filename += ".ipynb"

    notebook = NotebookManager.export_ipynb(cells)

    response = make_response(

        jsonify(notebook)

    )

    response.headers["Content-Disposition"] = f"attachment; filename={filename}"

    response.headers["Content-Type"]="application/json"

    return response


def import_notebook():

    if "file" not in request.files:

        return jsonify({

            "success":False,

            "message":"No file uploaded"

        }),400

    file = request.files["file"]

    try:

        import json

        content = json.load(

            file.stream

        )

        cells = NotebookManager.parse_ipynb(

            content

        )

        return jsonify({

            "success":True,

            "filename":file.filename,

            "cells":cells

        })

    except Exception as e:

        return jsonify({

            "success":False,

            "message":str(e)

        }),400