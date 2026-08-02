from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
import numpy as np
import matplotlib.pyplot as plt
import os


def run_amplitude_encoding(data, shots=1024, image_path="static/amplitude_encoding.png"):

    # Validation
    if not data:
        raise ValueError("Input vector cannot be empty.")

    try:
        vector = np.array([float(x) for x in data], dtype=float)
    except Exception:
        raise ValueError("All input values must be numeric.")

    # Length must be a power of 2
    length = len(vector)

    if length & (length - 1):
        raise ValueError(
            "Vector length must be a power of 2 (2, 4, 8, 16, ...)."
        )

    # Cannot normalize zero vector
    norm = np.linalg.norm(vector)

    if norm == 0:
        raise ValueError("Vector cannot be all zeros.")

    vector = vector / norm

    num_qubits = int(np.log2(length))

    qc = QuantumCircuit(num_qubits)

    qc.initialize(vector, range(num_qubits))

    qc.measure_all()

    simulator = AerSimulator()

    job = simulator.run(qc, shots=shots)

    result = job.result()

    counts = result.get_counts()

    fig = qc.draw(output="mpl")

    # Bug #3 Fix: os.path.dirname("amplitude_encoding.png") returns "" (empty string).
    # Calling os.makedirs("") raises FileNotFoundError on Windows.
    # Guard: only create the directory if the path actually has one.
    dir_name = os.path.dirname(image_path)
    if dir_name:
        os.makedirs(dir_name, exist_ok=True)

    fig.savefig(image_path, dpi=150, bbox_inches="tight")

    plt.close(fig)

    return counts, image_path