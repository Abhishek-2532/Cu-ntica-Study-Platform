from flask import Blueprint
from Controllers.circuitController import (
    save_circuit,
    list_circuits,
    load_circuit,
    delete_circuit,
    run_circuit_aer,
    explain_circuit
)
from middleware.auth import login_required

circuit_bp = Blueprint("circuit", __name__, url_prefix="/api/circuit")

# Secure all visualizer endpoints
circuit_bp.route("/save", methods=["POST"])(login_required(save_circuit))
circuit_bp.route("/list", methods=["GET"])(login_required(list_circuits))
circuit_bp.route("/load/<circuit_id>", methods=["GET"])(login_required(load_circuit))
circuit_bp.route("/delete/<circuit_id>", methods=["DELETE"])(login_required(delete_circuit))
circuit_bp.route("/run", methods=["POST"])(login_required(run_circuit_aer))
circuit_bp.route("/explain", methods=["POST"])(login_required(explain_circuit))
