import pytest
import numpy as np
import qibo
from qibo import Circuit, gates

# from qulacs import QuantumCircuit, QuantumState
# from qulacs.gate import X, T, H, CNOT, ParametricRZ, ParametricRX, DenseMatrix
# from qulacs.circuit import QuantumCircuitOptimizer as QCO

# import mkl
# mkl.set_num_threads(1)

qibo.set_backend("qibojit")
qibo.set_threads(1)

#nqubits_list = range(4, 26)
nqubits_list = range(4, 6)


def first_rotation(circuit, nqubits):
    for k in range(nqubits):
        circuit.add(gates.RX(k, np.random.rand()))
        circuit.add(gates.RZ(k, np.random.rand()))


def mid_rotation(circuit, nqubits):
    for k in range(nqubits):
        circuit.add(gates.RZ(k, np.random.rand()))
        circuit.add(gates.RX(k, np.random.rand()))
        circuit.add(gates.RZ(k, np.random.rand()))


def last_rotation(circuit, nqubits):
    for k in range(nqubits):
        circuit.add(gates.RZ(k, np.random.rand()))
        circuit.add(gates.RX(k, np.random.rand()))


def entangler(circuit, nqubits, pairs):
    for a, b in pairs:
        circuit.add(gates.CNOT(a, b))


def build_circuit(nqubits, depth, pairs):
    circuit = Circuit(nqubits)
    first_rotation(circuit, nqubits)
    entangler(circuit, nqubits, pairs)
    for k in range(depth):
        mid_rotation(circuit, nqubits)
        entangler(circuit, nqubits, pairs)

    last_rotation(circuit, nqubits)
    return circuit


def benchfunc_noopt(circuit, nqubits):
    circuit()


# def benchfunc(qco, circuit, nqubits):
#     st = QuantumState(nqubits)
#     qco.optimize_light(circuit)
#     circuit.update_quantum_state(st)


@pytest.mark.parametrize('nqubits', nqubits_list)
def test_QCBMopt(benchmark, nqubits):
    benchmark.group = "QCBMopt"
    pairs = [(i, (i + 1) % nqubits) for i in range(nqubits)]
    circuit = build_circuit(nqubits, 9, pairs)
    #qco = QCO()
    benchmark(benchfunc_noopt, circuit, nqubits)


@pytest.mark.parametrize('nqubits', nqubits_list)
def test_QCBM(benchmark, nqubits):
    benchmark.group = "QCBM"
    pairs = [(i, (i + 1) % nqubits) for i in range(nqubits)]
    circuit = build_circuit(nqubits, 9, pairs)
    benchmark(benchfunc_noopt, circuit, nqubits)


# nqubits = 4
# pairs = [(i, (i + 1) % nqubits) for i in range(nqubits)]
# circuit = build_circuit(nqubits, 9, pairs)
# circuit()
