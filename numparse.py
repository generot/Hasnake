#Playing ground for experimenting with different components of the Haskell Parser.

from src.parse_util import *
from re import findall
from enum import Enum

class operation(Enum):
    ADD = '+'
    NEG = '-'
    MULT = '*'
    DIV = '/'
    POW = '^'
    AND = "&&"
    OR = "||"
    GT = ">"
    LT = "<"
    EQ = "=="

class expr_type(Enum):
    VALUE = 0
    OPERATION = 1

class expr:
    def __init__(self, exprtype, val = 0, oper = None, lbr = None, rbr = None):
        self.exprtype = exprtype
        self.val = val
        self.oper = oper

        self.lbr = lbr
        self.rbr = rbr

def logical():
    lbr, rbr = _cmp(), None
    oper = it.get()

    if oper == "&&" or oper == "||":
        it.next()
        rbr = logical()
        return expr(expr_type.OPERATION, 0, operation(oper), lbr, rbr)

    return lbr

def _cmp():
    lbr, rbr = term(), None
    oper = it.get()

    if oper == "<" or oper == ">" or oper == "==":
        it.next()
        rbr = _cmp()
        return expr(expr_type.OPERATION, 0, operation(oper), lbr, rbr)

    return lbr

def term():
    lbr, rbr = factor(), None
    oper = it.get()

    if oper == '+' or oper == '-':
        if oper == '+':
            it.next()

        rbr = term()
        return expr(expr_type.OPERATION, 0, operation.ADD, lbr, rbr)

    return lbr

def factor():
    lbr, rbr = negate(), None
    oper = it.get()

    if oper == '*' or oper == '/':
        it.next()
        rbr = factor()
        return expr(expr_type.OPERATION, 0, operation(oper), lbr, rbr)

    return lbr

def negate():
    oper = it.get()

    if oper == '-':
        it.next()
        lbr = negate()
        return expr(expr_type.OPERATION, 0, operation(oper), lbr, None)

    return power()


def power():
    lbr, rbr = value(), None
    oper = it.get()

    if oper == '^':
        it.next()
        rbr = negate()
        return expr(expr_type.OPERATION, 0, operation(oper), lbr, rbr)

    return lbr

def value():
    val = 0

    if it.get().isalnum():
        if it.get().isnumeric():
            val = int(it.get())
        else:
            val = it.get()

        it.next()

    if it.get() == '(':
        it.next()
        val = term()
        it.next()

    return expr(expr_type.VALUE, val)

def print_tree(exprtree):
    if not exprtree:
        return "0"

    if exprtree.exprtype == expr_type.OPERATION:
        lbr = print_tree(exprtree.lbr)
        rbr = print_tree(exprtree.rbr)

        if exprtree.oper == operation.NEG:
            return f"(NEG {lbr})"

        return f"({lbr} {exprtree.oper.value} {rbr})"

    elif exprtree.exprtype == expr_type.VALUE:
        return exprtree.val if not isinstance(exprtree.val, expr) else print_tree(exprtree.val)

def tokenize(inp):
    return findall(r"\w+|[|&=]{2}|[+*\-\(\)\/\^<>]", inp)

def main():
    tokens = tokenize(input())
    print(tokens)

    global it
    it = Iterator(tokens)

    tree = logical()
    print(print_tree(tree))
