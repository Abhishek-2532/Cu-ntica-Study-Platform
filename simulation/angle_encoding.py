from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
import matplotlib.pyplot as plt
import os


def run_angle_encoding(data, shots=1024, image_path="static/angle_encoding.png"):
    """
    Perform Angle Encoding using RY gates.

    Parameters
    ----------
    data : list
        List of numerical values (angles in radians).
        Example: [0.5, 1.2, 2.4]

    shots : int
        Number of simulation shots.

    image_path : str
        Path where the circuit image will be saved.

    Returns
    -------
    counts : dict
        Measurement counts.

    image_path : str
        Saved circuit image path.
    """

    # Validation
    if not data:
        raise ValueError("Input data cannot be empty.")

    try:
        data = [float(x) for x in data]
    except Exception:
        raise ValueError("All input values must be numeric.")

    n = len(data)

    # Create Quantum Circuit
    qc = QuantumCircuit(n)

    # Angle Encoding using RY rotations
    for i, angle in enumerate(data):
        qc.ry(angle, i)

    # Measure all qubits
    qc.measure_all()

    # Simulator
    simulator = AerSimulator()

    job = simulator.run(qc, shots=shots)
    result = job.result()

    counts = result.get_counts()

    # Draw circuit
    fig = qc.draw(output="mpl")

    # Bug #3 Fix: os.path.dirname("angle_encoding.png") returns "" (empty string).
    # Calling os.makedirs("") raises FileNotFoundError on Windows.
    # Guard: only create the directory if the path actually has one.
    dir_name = os.path.dirname(image_path)
    if dir_name:
        os.makedirs(dir_name, exist_ok=True)

    fig.savefig(image_path, dpi=150, bbox_inches="tight")
    plt.close(fig)

    return counts, image_path