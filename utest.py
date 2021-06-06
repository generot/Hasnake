from src.parser import ExprParser
from src.evaluate import EvalExpr
from src.lexer import LexLine

from src.util import LoadFile

import unittest

class HasnakeTest(unittest.TestCase):
    def test_where(self):
        self.assertEqual(LineExpr("someFunc(10 20)", callHs), 240)

    def test_if(self):
        self.assertEqual(LineExpr("ifTest(13)", callHs), "Greater than 10")
        self.assertEqual(LineExpr("ifTest(9)", callHs), "Less than 10")

    def test_guards(self):
        self.assertEqual(LineExpr("guarded(10)", callHs), "Bigger than 0")
        self.assertEqual(LineExpr("guarded(-10)", callHs), "Less than 0")
        self.assertEqual(LineExpr("guarded(0)", callHs), "Is 0")
    
    def test_list(self):
        self.assertEqual(LineExpr("[0, 1, 2, 3]", None), [0, 1, 2, 3])

    def test_range(self):
        self.assertEqual(LineExpr("[-5..5]", None), list(range(-5, 6)))

    def test_chain(self):
        self.assertEqual(LineExpr("(1 : 2 + 3 : [1, 2])", None), [1, 5, 1, 2])

    def test_compr(self):
        self.assertEqual(LineExpr("[x() * 2 | x <- [0..10]]", None), [x * 2 for x in range(11)])

    def test_ref(self):
        self.assertEqual(LineExpr("passByRef(3 sq)", callHs), 9)

    def test_builtins(self):
        self.assertEqual(LineExpr("empty([])", None), True)
        self.assertEqual(LineExpr('print("Hello, world")', None), 13)
        self.assertEqual(LineExpr("mod(3 2)", None), 1)

    def test_destr(self):
        #We test recursion here too :)
        self.assertEqual(LineExpr("length([0..10])", callHs), 11)

    def test_math_expr(self):
        self.assertEqual(LineExpr("-(4 + 10 / 2) ^ 0.5", None), -3)
        self.assertEqual(LineExpr("2 + 5 < 5 * 2 && -1 + 3 == 2", None), 1)

    def test_call_expr(self):
        self.assertEqual(LineExpr("(sq(3) + sq(4)) ^ 0.5", callHs), 5)

def LineExpr(strexpr, context):
    tokens = LexLine(strexpr)
    expr = ExprParser(tokens)

    return EvalExpr(expr, context)

def RunTest():
    global callHs
    callHs = LoadFile("tests/call.hs")

    suite = unittest.TestSuite()
    members = [x for x in dir(HasnakeTest) if x.find("test_") != -1]

    for i in members:
        suite.addTest(HasnakeTest(i))

    print("Testing...\n")
    return suite
