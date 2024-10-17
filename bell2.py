# # Import necessary libraries from Qiskit
from qiskit import QuantumCircuit, transpile
from qiskit.circuit import QuantumRegister, ClassicalRegister
from qiskit.quantum_info import SparsePauliOp
from qiskit.primitives import Estimator
from qiskit.primitives import Sampler
from qiskit.visualization import plot_histogram
from qiskit.quantum_info import Statevector
from qiskit.visualization import plot_state_qsphere

# Create a Bell state quantum circuit
cr=ClassicalRegister(2,'c')
bell = QuantumCircuit(QuantumRegister(1, 'A'), QuantumRegister(1, 'B'), QuantumRegister(1, 'C'), QuantumRegister(1, 'D'), cr)

bell.h(0)
bell.cx(0, 1)
bell.h(0)

bell.x(2)
bell.x(3)
bell.h(2)
bell.cx(2, 3)
bell.h(2)

bell.barrier()

# Bell measurement of 1 and 2
bell.h(1)
bell.cx(1,2)
bell.h(1)
bell.barrier()
# bell.measure([1,2],[0,1])

# recover original bell state
bell.cx(2, 0)
bell.cz(1, 0)
bell.barrier()

# reverce 0,3 to computational basis
bell.h(0)
bell.cx(0,3)
bell.h(0)
bell.barrier()

evolve = False# True
if (evolve == True):
    bell = bell.reverse_bits()
    sv_prepare = Statevector([1,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0])
    new_sv_prepare = sv_prepare.evolve(bell)
    print(new_sv_prepare)
    plot_state_qsphere(new_sv_prepare, filename="sv_bell2.png")
else:
    bell.measure([0, 3],[0, 1])
    bell = bell.reverse_bits()
    print("Original Circuit:")
    print(bell)
    bell.draw("mpl", filename="c_bell2.png")

    # Use the Sampler to simulate the circuit
    sampler = Sampler()
    job = sampler.run(circuits=bell, shots=1024)
    result = job.result()

    # Get the result counts and convert quasi-probabilities to probabilities
    counts = result.quasi_dists[0].binary_probabilities()

    # print result
    print("Measuremet result:", result.quasi_dists[0])

    # Plot the result as a histogram
    plot_histogram(counts, filename="h_bell2.png")