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

import unittest
from typing import Tuple

from sympy import Symbol, symbols
from sympy.logic import ITE, And, Not, Or, false, simplify_logic, true

from qlasskit import QlassF, exceptions, qlassf

a, b, c, d = symbols("a,b,c,d")
_ret = Symbol("_ret")
a_0 = Symbol("a.0")
a_1 = Symbol("a.1")
b_0 = Symbol("b.0")
b_1 = Symbol("b.1")


class TestQlassfTuple(unittest.TestCase):
    def test_tuple_arg(self):
        f = "def test(a: Tuple[bool, bool]) -> bool:\n\treturn a[0] and a[1]"
        qf = qlassf(f, to_compile=False)
        self.assertEqual(len(qf.expressions), 1)
        self.assertEqual(qf.expressions[0][0], _ret)
        self.assertEqual(qf.expressions[0][1], And(a_0, a_1))

    def test_tuple_arg_assign(self):
        f = (
            "def test(a: Tuple[bool, bool]) -> bool:\n"
            + "\tb = a[0]\n"
            + "\tc = a[1]\n"
            + "\treturn b and c"
        )
        qf = qlassf(f, to_compile=False)
        self.assertEqual(len(qf.expressions), 3)
        self.assertEqual(qf.expressions[-1][0], _ret)
        self.assertEqual(qf.expressions[-1][1], And(b, c))

    def test_tuple_of_tuple_arg(self):
        f = "def test(a: Tuple[Tuple[bool, bool], bool]) -> bool:\n\treturn a[0][0] and a[0][1] and a[1]"
        qf = qlassf(f, to_compile=False)
        self.assertEqual(len(qf.expressions), 1)
        self.assertEqual(qf.expressions[0][0], _ret)
        self.assertEqual(
            qf.expressions[0][1], And(Symbol("a.0.0"), And(Symbol("a.0.1"), a_1))
        )

    def test_tuple_of_tuple_of_tuple_arg(self):
        f = (
            "def test(a: Tuple[Tuple[Tuple[bool, bool], bool], bool]) -> bool:\n"
            + "\treturn a[0][0][0] and a[0][0][1] and a[0][1] and a[1]"
        )
        qf = qlassf(f, to_compile=False)
        self.assertEqual(len(qf.expressions), 1)
        self.assertEqual(qf.expressions[0][0], _ret)
        self.assertEqual(
            qf.expressions[0][1],
            And(Symbol("a.0.0.0"), And(Symbol("a.0.0.1"), And(Symbol("a.0.1"), a_1))),
        )

    def test_tuple_assign(self):
        f = "def test(a: Tuple[bool, bool]) -> bool:\n\tb = (a[1],a[0])\n\treturn b[0] and b[1]"
        qf = qlassf(f, to_compile=False)
        self.assertEqual(len(qf.expressions), 3)
        self.assertEqual(qf.expressions[-1][0], _ret)
        self.assertEqual(qf.expressions[-1][1], And(b_0, b_1))

    def test_tuple_assign2(self):
        f = (
            "def test(a: Tuple[Tuple[bool, bool], bool]) -> bool:\n"
            + "\tb = (a[0][1],a[0][0],a[1])\n"
            + "\treturn b[0] and b[1] and b[2]"
        )
        qf = qlassf(f, to_compile=False)
        self.assertEqual(len(qf.expressions), 4)
        self.assertEqual(qf.expressions[-1][0], _ret)
        self.assertEqual(qf.expressions[-1][1], And(b_0, And(b_1, Symbol("b.2"))))

    def test_tuple_assign3(self):
        f = (
            "def test(a: Tuple[Tuple[bool, bool], bool]) -> bool:\n"
            + "\tb = (a[0][1],(a[0][0],a[1]))\n"
            + "\treturn b[0] and b[1][0] and b[1][1]"
        )
        qf = qlassf(f, to_compile=False)
        self.assertEqual(len(qf.expressions), 4)
        self.assertEqual(qf.expressions[-1][0], _ret)
        self.assertEqual(
            qf.expressions[-1][1], And(b_0, And(Symbol("b.1.0"), Symbol("b.1.1")))
        )

    def test_tuple_result(self):
        f = "def test(a: bool, b: bool) -> Tuple[bool,bool]:\n\treturn a,b"
        qf = qlassf(f, to_compile=False)
        self.assertEqual(len(qf.expressions), 2)
        self.assertEqual(qf.expressions[0][0], Symbol("_ret.0"))
        self.assertEqual(qf.expressions[0][1], a)
        self.assertEqual(qf.expressions[1][0], Symbol("_ret.1"))
        self.assertEqual(qf.expressions[1][1], b)
