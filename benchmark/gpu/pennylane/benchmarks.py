import pennylane as qml
from pennylane import numpy as np

import pytest

nqubits_list = range(4, 26)
#nqubits_list = range(4, 6)

def first_rotation(nqubits):
    for k in range(nqubits):
        qml.RX(np.random.rand(), wires=k)
        qml.RZ(np.random.rand(), wires=k)


def mid_rotation(nqubits):
    for k in range(nqubits):
        qml.RZ(np.random.rand(), wires=k)
        qml.RX(np.random.rand(), wires=k)
        qml.RZ(np.random.rand(), wires=k)


def last_rotation(nqubits):
    for k in range(nqubits):
        qml.RZ(np.random.rand(), wires=k)
        qml.RX(np.random.rand(), wires=k)


def entangler(pairs):
    for a, b in pairs:
        qml.CNOT(wires=[a, b])

def build_circuit(nqubits, depth, pairs):
    first_rotation(nqubits)
    entangler(pairs)
    for k in range(depth):
        mid_rotation(nqubits)
        entangler(pairs)

    last_rotation(nqubits)
    return qml.expval(qml.PauliZ(wires=0))


@pytest.mark.parametrize("nqubits", nqubits_list)
def test_QCBM(benchmark, nqubits):
    benchmark.group = "QCBM"
    dev = qml.device("lightning.gpu", wires=nqubits)
    node = qml.QNode(build_circuit, dev)
    pairs = [(i, (i + 1) % nqubits) for i in range(nqubits)]
    node(nqubits, 9, pairs)

# def main():
#     nqubits = 4
#     dev = qml.device("lightning.qubit", wires=nqubits)
#     node = qml.QNode(build_circuit, dev)
#     pairs = [(i, (i + 1) % nqubits) for i in range(nqubits)]
#     node(nqubits, 9, pairs)

# main() 
