from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
import matplotlib.pyplot as plt
import os


def run_basis_encoding(binary_string, shots=1024, image_path="static/circuit.png"):

    # Validation
    if len(binary_string) == 0:
        raise ValueError("Binary string cannot be empty.")

    for bit in binary_string:
        if bit not in ["0", "1"]:
            raise ValueError("Only 0 and 1 are allowed.")

    n = len(binary_string)

    qc = QuantumCircuit(n)

    # Basis Encoding
    for i, bit in enumerate(binary_string):
        if bit == "1":
            qc.x(i)

    qc.measure_all()

    simulator = AerSimulator()

    job = simulator.run(qc, shots=shots)
    result = job.result()

    counts = result.get_counts()

    fig = qc.draw(output="mpl")

    # Bug #3 Fix: os.path.dirname("circuit.png") returns "" (empty string).
    # Calling os.makedirs("") raises FileNotFoundError on Windows.
    # Guard: only create the directory if the path actually has one.
    dir_name = os.path.dirname(image_path)
    if dir_name:
        os.makedirs(dir_name, exist_ok=True)

    fig.savefig(image_path, dpi=150, bbox_inches="tight")
    plt.close(fig)

    return counts, image_path