# # Import necessary libraries from Qiskit
from qiskit import QuantumCircuit, transpile
from qiskit.circuit import QuantumRegister, ClassicalRegister
from qiskit.quantum_info import SparsePauliOp
from qiskit.primitives import Estimator
from qiskit.primitives import Sampler
from qiskit.visualization import plot_histogram
from qiskit.quantum_info import Statevector
from qiskit.visualization import plot_state_qsphere

def BBell(circuit, a, b):
    circuit.h(a)
    circuit.cx(a, b)

def BdBell(circuit, a, b):
    circuit.cx(a, b)
    circuit.h(a)

def entanglement_swapping(B, Bd, full, evolve):
    # Create a Bell state quantum circuit
    cr = ClassicalRegister(2,'c')
    bell = QuantumCircuit(QuantumRegister(1, 'A'), QuantumRegister(1, 'B'), QuantumRegister(1, 'C'), QuantumRegister(1, 'D'), cr)

    # Z -> Bell
    # bell.h(0)
    # bell.cx(0, 1)
    B(bell, 0, 1)

    # for \Psi^+
    bell.x(3)

    # Z -> Bell
    # bell.h(2)
    # bell.cx(2, 3)
    B(bell, 2, 3)

    if (full == True):
        bell.barrier()

        # Bell -> Z
        # bell.cx(1, 2)
        # bell.h(1)
        Bd(bell, 1, 2)
        bell.barrier()

        # recover original bell state
        bell.cx(2, 0)
        bell.cz(1, 0)
        bell.barrier()

        # Z -> Bell (0,3)
        # bell.cx(0, 3)
        # bell.h(0)
        Bd(bell, 0, 3)
        bell.barrier()

    if (evolve == True):
        bell = bell.reverse_bits()
        sv_prepare = Statevector([1,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0])
        new_sv_prepare = sv_prepare.evolve(bell)
        print(new_sv_prepare)
        plot_state_qsphere(new_sv_prepare, filename = "sv_bell1_full.png" if (full == True) else "sv_bell1_init.png")
    else:
        bell.measure([0, 3],[0, 1])
        bell = bell.reverse_bits()
        print("Original Circuit:")
        print(bell)
        bell.draw("mpl", filename="c_bell1.png")

        # Use the Sampler to simulate the circuit
        sampler = Sampler()
        job = sampler.run(circuits=bell, shots=1024)
        result = job.result()

        # Get the result counts and convert quasi-probabilities to probabilities
        counts = result.quasi_dists[0].binary_probabilities()

        # print result
        print("Measuremet result:", result.quasi_dists[0])

        # Plot the result as a histogram
        plot_histogram(counts, filename="h_bell1.png")

# visualize initial state vector
entanglement_swapping(BBell, BdBell, full=False, evolve=True)

# visualize resuling state vector
entanglement_swapping(BBell, BdBell, full=True, evolve=True)

# perform simulation
entanglement_swapping(BBell, BdBell, full=True, evolve=False)