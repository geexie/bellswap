# # Import necessary libraries from Qiskit
from qiskit import QuantumCircuit
from qiskit.circuit import QuantumRegister, ClassicalRegister
from qiskit.primitives import Sampler
from qiskit.quantum_info import Statevector
from qiskit.visualization import plot_histogram
from qiskit.visualization import plot_state_qsphere

def BBell(circuit, a, b):
    circuit.h(a)
    circuit.cx(a, b)

def BdBell(circuit, a, b):
    circuit.cx(a, b)
    circuit.h(a)

def entanglement_swapping(B, Bd, name, full, evolve):
    # Create a Bell state quantum circuit
    cr = ClassicalRegister(2,'c')
    bell = QuantumCircuit(QuantumRegister(1, 'A'), QuantumRegister(1, 'B'), QuantumRegister(1, 'C'), QuantumRegister(1, 'D'), cr)

    B(bell, 0, 1)

    # for \Psi^+
    bell.x(3)

    B(bell, 2, 3)

    if (full == True):
        bell.barrier()

        Bd(bell, 1, 2)
        bell.barrier()

        # recover original bell state
        bell.cx(2, 0)
        bell.cz(1, 0)
        bell.barrier()

        Bd(bell, 0, 3)
        bell.barrier()

    if (evolve == True):
        bell = bell.reverse_bits()
        sv_prepare = Statevector([1,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0])
        new_sv_prepare = sv_prepare.evolve(bell)
        print(new_sv_prepare)
        plot_state_qsphere(new_sv_prepare, filename = "sv_"+name+"_full.png" if (full == True) else "sv_"+name+"_init.png")
    else:
        bell.measure([0, 3],[0, 1])
        bell = bell.reverse_bits()
        print("Original Circuit:")
        print(bell)
        bell.draw("mpl", filename="c_"+name+".png")

        # Use the Sampler to simulate the circuit
        sampler = Sampler()
        job = sampler.run(circuits=bell, shots=1024)
        result = job.result()

        # Get the result counts and convert quasi-probabilities to probabilities
        counts = result.quasi_dists[0].binary_probabilities()

        # print result
        print("Measuremet result:", result.quasi_dists[0])

        # Plot the result as a histogram
        plot_histogram(counts, filename="h_"+name+".png")

# visualize initial state vector
entanglement_swapping(BBell, BdBell, name="bell", full=False, evolve=True)

# visualize resuling state vector
entanglement_swapping(BBell, BdBell, name="bell", full=True, evolve=True)

# perform simulation
entanglement_swapping(BBell, BdBell, name="bell", full=True, evolve=False)