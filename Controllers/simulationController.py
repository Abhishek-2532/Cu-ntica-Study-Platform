from flask import Blueprint, render_template, request, jsonify, current_app
import os

from simulation.basic_coding import run_basis_encoding
from simulation.angle_encoding import run_angle_encoding
from simulation.amplitude_encoding import run_amplitude_encoding 
from middleware.auth import login_required


simulation_bp = Blueprint(
    "simulation",
    __name__,
    url_prefix="/simulation"
)


# ----------------------------
# Basis Encoding
# ----------------------------

@simulation_bp.route("/basis-encoding")
def basis_encoding_page():
    return render_template("basic_encoding.html")


@simulation_bp.route("/basis_encoding", methods=["POST"])
@login_required
def basis_encoding():

    try:

        data = request.get_json()

        # Bug #3 Fix: guard against missing or non-JSON request body
        if not data:
            return jsonify({
                "success": False,
                "error": "Request body is required and must be JSON."
            }), 400

        binary = data.get("binary", "")
        shots  = int(data.get("shots", 1024))

        image_path = os.path.join(
            current_app.config["STATIC_FOLDER"],
            "circuit.png"
        )

        counts, image = run_basis_encoding(
            binary,
            shots,
            image_path
        )

        return jsonify({
            "success": True,
            "counts": counts,
            "image": "/static/circuit.png"
        })

    except Exception as e:

        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


# ----------------------------
# Angle Encoding
# ----------------------------

@simulation_bp.route("/angle-encoding")
def angle_encoding_page():
    return render_template("angle_encoding.html")


@simulation_bp.route("/angle_encoding", methods=["POST"])
@login_required
def angle_encoding():

    try:

        data = request.get_json()

        # Bug #3 Fix: guard against missing or non-JSON request body
        if not data:
            return jsonify({
                "success": False,
                "error": "Request body is required and must be JSON."
            }), 400

        angles = data.get("data", [])
        shots  = int(data.get("shots", 1024))

        image_path = os.path.join(
            current_app.config["STATIC_FOLDER"],
            "angle_encoding.png"
        )

        counts, image = run_angle_encoding(
            angles,
            shots,
            image_path
        )

        return jsonify({
            "success": True,
            "counts": counts,
            "image": "/static/angle_encoding.png"
        })

    except Exception as e:

        return jsonify({
            "success": False,
            "error": str(e)
        }), 500
        
# ----------------------------
# Amplitude Encoding
# ----------------------------

@simulation_bp.route("/amplitude-encoding")
def amplitude_encoding_page():
    return render_template("amplitude_encoding.html")

@simulation_bp.route("/amplitude_encoding", methods=["POST"])
@login_required
def amplitude_encoding():

    try:

        data = request.get_json()

        # Bug #3 Fix: guard against missing or non-JSON request body
        if not data:
            return jsonify({
                "success": False,
                "error": "Request body is required and must be JSON."
            }), 400

        vector = data.get("data", [])
        shots  = int(data.get("shots", 1024))

        image_path = os.path.join(
            current_app.config["STATIC_FOLDER"],
            "amplitude_encoding.png"
        )

        counts, image = run_amplitude_encoding(
            vector,
            shots,
            image_path
        )

        return jsonify({
            "success": True,
            "counts": counts,
            "image": "/static/amplitude_encoding.png"
        })

    except Exception as e:

        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@simulation_bp.route("/run-circuit", methods=["POST"])
@login_required
def run_circuit():
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                "success": False,
                "error": "Request body is required and must be JSON."
            }), 400

        qubits = int(data.get("qubits", 2))
        gates = data.get("gates", [])

        if qubits < 1 or qubits > 10:
            return jsonify({
                "success": False,
                "error": "Qubit count must be between 1 and 10."
            }), 400

        from qiskit import QuantumCircuit
        from qiskit.quantum_info import Statevector
        import numpy as np

        qc = QuantumCircuit(qubits)
        
        for gate in gates:
            name = gate.get("name", "").lower()
            targets = gate.get("targets", [])
            controls = gate.get("controls", [])
            params = gate.get("params", [])

            if any(t < 0 or t >= qubits for t in targets) or any(c < 0 or c >= qubits for c in controls):
                return jsonify({
                    "success": False,
                    "error": f"Invalid qubit index for gate '{name}'."
                }), 400

            if name == "h":
                qc.h(targets[0])
            elif name == "x":
                qc.x(targets[0])
            elif name == "y":
                qc.y(targets[0])
            elif name == "z":
                qc.z(targets[0])
            elif name == "s":
                qc.s(targets[0])
            elif name == "t":
                qc.t(targets[0])
            elif name == "rx":
                val = float(params[0]) if params else 0.0
                qc.rx(val, targets[0])
            elif name == "ry":
                val = float(params[0]) if params else 0.0
                qc.ry(val, targets[0])
            elif name == "rz":
                val = float(params[0]) if params else 0.0
                qc.rz(val, targets[0])
            elif name == "cx" or name == "cnot":
                qc.cx(controls[0], targets[0])
            elif name == "swap":
                qc.swap(targets[0], targets[1])
            elif name == "cz":
                qc.cz(controls[0], targets[0])
            elif name == "ccx" or name == "toffoli":
                qc.ccx(controls[0], controls[1], targets[0])

        state = Statevector.from_instruction(qc)

        statevector_data = []
        for i, val in enumerate(state.data):
            bin_str = bin(i)[2:].zfill(qubits)
            statevector_data.append({
                "state": f"|{bin_str}>",
                "real": float(np.round(val.real, 6)),
                "imag": float(np.round(val.imag, 6)),
                "prob": float(np.round(abs(val)**2, 6))
            })

        prob_dict = state.probabilities_dict()
        counts = {k: float(np.round(v, 6)) for k, v in prob_dict.items()}

        return jsonify({
            "success": True,
            "statevector": statevector_data,
            "counts": counts
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500