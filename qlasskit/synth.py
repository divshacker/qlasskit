# Copyright 2023 Davide Gessa

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

# http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


""" Algorithm and functions able to synthetize a boolean function to a quantum circuit """
# TODO: synthetizer should translate the boolexp to an intermediate form
# with invertible boolean gates; then we can apply simplifications and ancilla optimizations
# After that, we do another compilation pass that decompose invertible logic to quantum gates

from sympy import Symbol
from sympy.logic import And, Not, Or


class SynthResult:
    def __init__(self, res_qubit, gate_list, qubit_map):
        self.res_qubit = res_qubit
        self.gate_list = gate_list
        self.qubit_map = qubit_map

    @property
    def num_qubits(self):
        return len(self.qubit_map)

    def to_qiskit(self):
        from qiskit import QuantumCircuit

        qc = QuantumCircuit(len(self.qubit_map), 0)

        for g in self.gate_list:
            # match g[0]:
            if g[0] == "x":
                qc.x(g[1])
            elif g[0] == "cx":
                qc.cx(g[1], g[2])
            elif g[0] == "ccx":
                qc.ccx(g[1], g[2], g[3])

        return qc.to_gate()


class Synthetizer:
    def __init__(self):
        self.qmap = {}

    def synth(self, expr):
        raise Exception("abstract")


class Synthetizer_0(Synthetizer):
    def synth(self, expr):
        # match expr:
        if expr == Symbol():
            # print('sym', expr.name)
            if expr.name not in self.qmap:
                self.qmap[expr.name] = len(self.qmap)
            return self.qmap[expr.name], []

        elif expr == Not():
            # print('NOT', expr.args)
            i, g = self.synth(expr.args[0])
            return i, g + [("x", i)]

        elif expr == And():
            il = []
            gl = []

            for x in expr.args:
                ii, gg = self.synth(x)
                il.append(ii)
                gl.extend(gg)

            iold = il[0]
            for x in range(1, len(il)):
                inew = len(self.qmap)
                self.qmap[f"anc_{len(self.qmap)}"] = inew
                gl.append(("ccx", iold, il[x], inew))
                iold = inew

            return inew, gl

        elif expr == Or():
            if len(expr.args) > 2:
                raise Exception("too many clause")

            i1, g1 = self.synth(expr.args[0])
            i2, g2 = self.synth(expr.args[1])
            i3 = len(self.qmap)
            self.qmap[f"anc_{len(self.qmap)}"] = i3

            return i3, g1 + g2 + [
                ("x", i2),
                ("ccx", i1, i2, i3),
                ("x", i2),
                ("cx", i2, i3),
            ]

        else:
            print("notrec", expr)


def to_quantum(bexp):
    s = Synthetizer_0()
    res_qubit, gate_list = s.synth(bexp)
    # print('res',c, s.qmap)
    return SynthResult(res_qubit, gate_list, s.qmap)