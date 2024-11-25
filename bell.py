from qiskit import QuantumCircuit
from qiskit.circuit import QuantumRegister, ClassicalRegister
from qiskit.primitives import StatevectorSampler
from qiskit.quantum_info import Statevector
from qiskit.visualization import plot_histogram
from qiskit.visualization import plot_state_qsphere
from numpy import pi

# B and B^{\dagger} for Z<->Bell conversion
def Bell():
    def B(circuit, a, b):
        circuit.h(a)
        circuit.cx(a, b)
    def Bd(circuit, a, b):
        circuit.cx(a, b)
        circuit.h(a)
    return (B, Bd)

# B and B^{\dagger} for Z<->X-Bell conversion
def XBell():
    def B(circuit, a, b):
        circuit.h(a)
        circuit.cx(a, b)
        circuit.h(a)
    return (B, B)

# B and B^{\dagger} for Z<->R_x-Bell conversion
def RBell():
    def B(circuit, a, b):
        circuit.rx(pi/3, a)
        circuit.s(a)
        circuit.x(a)
        circuit.cx(a, b)

    def Bd(circuit, a, b):
        circuit.cx(a, b)
        circuit.x(a)
        circuit.z(a)
        circuit.s(a)
        circuit.rx(-pi/3, a)
    return (B, Bd)

def makePsi(a):
    def f(circuit):
        circuit.x(a)
    return f

def entanglement_swapping(basis, makePsi, full, evolve):
    cr = ClassicalRegister(2,'c')
    bell = QuantumCircuit(QuantumRegister(1, 'A'), QuantumRegister(1, 'B'), QuantumRegister(1, 'C'), QuantumRegister(1, 'D'), cr)

    name = basis.__name__.lower()
    (B, Bd) = basis()
    makePsi(bell)

    B(bell, 0, 1)
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
        print(bell)
        bell.draw("mpl", filename="c_"+name+".png")

        nshots = 1024
        sampler = StatevectorSampler()
        result = sampler.run([bell], shots=nshots).result()
        counts = result[0].data.c.get_counts()
        counts = {k: (v / nshots )  for (k, v) in counts.items() }
        print (counts)
        plot_histogram(counts, filename="h_"+name+".png")

# visualize initial state vector
entanglement_swapping(Bell, makePsi(3), full=False, evolve=True)

# visualize resuling state vector
entanglement_swapping(Bell, makePsi(3), full=True, evolve=True)

# perform simulation
entanglement_swapping(Bell, makePsi(3), full=True, evolve=False)


# visualize initial state vector
entanglement_swapping(XBell, makePsi(2), full=False, evolve=True)

# visualize resuling state vector
entanglement_swapping(XBell, makePsi(2), full=True, evolve=True)

# perform simulation
entanglement_swapping(XBell, makePsi(2), full=True, evolve=False)


# visualize initial state vector
entanglement_swapping(RBell, makePsi(3), full=False, evolve=True)

# visualize resuling state vector
entanglement_swapping(RBell, makePsi(3), full=True, evolve=True)

# perform simulation
entanglement_swapping(RBell, makePsi(3), full=True, evolve=False)