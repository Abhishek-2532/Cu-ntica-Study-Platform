import os
import time
from flask import request, jsonify, session
from Models.circuitModel import CircuitModel
from middleware.auth import login_required
import google.generativeai as genai

# Setup Gemini Config
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model_name = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
model = genai.GenerativeModel(model_name)

def save_circuit():
    try:
        user_id = session.get("user_id")
        data = request.get_json()
        if not data:
            return jsonify({"success": False, "error": "JSON payload required"}), 400

        name = data.get("name", "Untitled Circuit").strip()
        qubits = int(data.get("qubits", 2))
        gates = data.get("gates", [])
        circuit_id = data.get("circuit_id")

        if circuit_id:
            # Update existing
            success = CircuitModel.update_circuit(circuit_id, user_id, name, qubits, gates)
            return jsonify({"success": success, "circuit_id": circuit_id, "message": "Circuit updated successfully"})
        else:
            # Create new
            new_id = CircuitModel.create_circuit(user_id, name, qubits, gates)
            return jsonify({"success": True, "circuit_id": new_id, "message": "Circuit created successfully"})

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

def list_circuits():
    try:
        user_id = session.get("user_id")
        circuits = CircuitModel.get_circuits_by_user(user_id)
        return jsonify({"success": True, "circuits": circuits})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

def load_circuit(circuit_id):
    try:
        user_id = session.get("user_id")
        doc = CircuitModel.get_circuit(circuit_id, user_id)
        if not doc:
            return jsonify({"success": False, "error": "Circuit not found or unauthorized access"}), 404
        return jsonify({"success": True, "circuit": doc})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

def delete_circuit(circuit_id):
    try:
        user_id = session.get("user_id")
        success = CircuitModel.delete_circuit(circuit_id, user_id)
        return jsonify({"success": success, "message": "Circuit deleted successfully" if success else "Failed to delete circuit"})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

def run_circuit_aer():
    start_time = time.time()
    try:
        data = request.get_json()
        if not data:
            return jsonify({"success": False, "error": "JSON payload required"}), 400

        qubits = int(data.get("qubits", 2))
        gates = data.get("gates", [])

        if qubits < 1 or qubits > 10:
            return jsonify({"success": False, "error": "Qubits must be between 1 and 10"}), 400

        from qiskit import QuantumCircuit
        from qiskit.quantum_info import Statevector
        import numpy as np

        qc = QuantumCircuit(qubits)

        # Apply gates
        for g in gates:
            name = g.get("name", "").lower()
            targets = g.get("targets", [])
            controls = g.get("controls", [])
            params = g.get("params", [])

            if any(t < 0 or t >= qubits for t in targets) or any(c < 0 or c >= qubits for c in controls):
                return jsonify({"success": False, "error": f"Qubit index out of bounds for gate '{name}'"}), 400

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
            elif name == "ch":
                qc.ch(controls[0], targets[0])
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
            elif name == "cz":
                qc.cz(controls[0], targets[0])
            elif name == "swap":
                qc.swap(targets[0], targets[1])
            elif name == "ccx" or name == "toffoli":
                qc.ccx(controls[0], controls[1], targets[0])
            elif name == "reset":
                qc.reset(targets[0])

        # Statevector calculation
        state = Statevector.from_instruction(qc)

        # Format amplitudes
        statevector_data = []
        for i, val in enumerate(state.data):
            bin_str = bin(i)[2:].zfill(qubits)
            statevector_data.append({
                "state": f"|{bin_str}>",
                "real": float(np.round(val.real, 6)),
                "imag": float(np.round(val.imag, 6)),
                "prob": float(np.round(abs(val)**2, 6))
            })

        # Calculate ideal probabilities counts
        prob_dict = state.probabilities_dict()
        counts = {k: float(np.round(v, 6)) for k, v in prob_dict.items()}

        # Aer/Quantum Metrics
        depth = qc.depth()
        gate_count = qc.size()
        execution_time_ms = int((time.time() - start_time) * 1000)

        return jsonify({
            "success": True,
            "statevector": statevector_data,
            "counts": counts,
            "depth": depth,
            "gate_count": gate_count,
            "execution_time_ms": execution_time_ms
        })

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

def explain_circuit():
    try:
        # Check Gemini API Key Configuration
        if not os.getenv("GEMINI_API_KEY"):
            return jsonify({
                "success": False,
                "error": "AI Tutor offline: GEMINI_API_KEY environment variable is not configured."
            }), 500

        data = request.get_json()
        if not data:
            return jsonify({"success": False, "error": "JSON payload required"}), 400

        qubits = int(data.get("qubits", 2))
        gates = data.get("gates", [])

        # Construct summary description
        desc_lines = []
        for i, g in enumerate(gates):
            name = g.get("name", "").upper()
            targets = g.get("targets", [])
            controls = g.get("controls", [])
            params = g.get("params", [])
            t_str = f"q{targets[0]}" if targets else ""
            c_str = f"control q{controls[0]}" if controls else ""
            p_str = f"parameter theta={params[0]}" if params else ""
            desc_lines.append(f"Step {i+1}: Apply {name} gate to {t_str} {('with ' + c_str) if c_str else ''} {p_str}")

        gates_summary = "\n".join(desc_lines) if desc_lines else "No gates (Empty circuit)"

        prompt = f"""
You are a senior Quantum Computing professor explaining a circuit layout designed by a student.

Circuit Layout:
Qubits: {qubits}
Gates Applied:
{gates_summary}

Please provide a structured explanation with these sections:
1. WHAT IT DOES: Describe what this circuit accomplished (e.g., superposition, Bell State entanglement, phase rotation).
2. STEP-BY-STEP MATHEMATICAL EVOLUTION: Explain step-by-step how the state vector evolves from the initial state |00...0> as each gate is applied.
3. APPLICATIONS: What is this circuit useful for in quantum computing or quantum ML (e.g. quantum key distribution, algorithms, state preparation).
4. COMMON MISTAKES: What common mistakes do students make when designing this specific type of circuit?
5. DIFFICULTY: Label the difficulty level (Beginner, Intermediate, or Advanced).

Keep the tone academic, encouraging, and clear for beginners. Do not use markdown tags, formatting, or emojis that look unprofessional. Use clean spacing.
"""

        response = model.generate_content(prompt)
        return jsonify({
            "success": True,
            "explanation": response.text
        })

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
