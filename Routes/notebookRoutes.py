from flask import Blueprint

from Controllers.notebookController import (
    execute,
    restart_kernel,
    interrupt_kernel,
    package_install,
    get_packages,
    list_notebooks,
    save_notebook,
    load_notebook,
    export_notebook,
    import_notebook
)
from middleware.auth import login_required

notebook_bp = Blueprint(

    "notebook",

    __name__

)

# Bug #2 Fix: The /notebook PAGE is already served by homeController.py.
# This Blueprint handles ONLY the notebook API routes below.
# Registering /notebook here too caused an AssertionError at startup.

notebook_bp.route(

    "/execute",

    methods=["POST"]

)(login_required(execute))

notebook_bp.route(

    "/restart-kernel",

    methods=["POST"]

)(login_required(restart_kernel))

notebook_bp.route(

    "/interrupt-kernel",

    methods=["POST"]

)(login_required(interrupt_kernel))

notebook_bp.route(

    "/install-package",

    methods=["POST"]

)(login_required(package_install))

notebook_bp.route(

    "/packages",

    methods=["GET"]

)(login_required(get_packages))

notebook_bp.route(

    "/list-notebooks",

    methods=["GET"]

)(login_required(list_notebooks))

notebook_bp.route(

    "/save-notebook",

    methods=["POST"]

)(login_required(save_notebook))

notebook_bp.route(

    "/load-notebook",

    methods=["POST"]

)(login_required(load_notebook))

notebook_bp.route(

    "/export-notebook",

    methods=["POST"]

)(login_required(export_notebook))

notebook_bp.route(

    "/import-notebook",

    methods=["POST"]

)(login_required(import_notebook))