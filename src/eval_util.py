import sys

from src.exception import EvalError
from src.parse_util import NodeType, ExpressionType
from src.ast import *

class BuiltinMethod:
    @staticmethod
    def empty(ls):
        return not len(ls)

    @staticmethod
    def print(_str):
        return sys.stdout.write(_str)

    @staticmethod
    def printLn(_str):
        if isinstance(_str, list):
            _str = "".join(_str)

        return BuiltinMethod.print(_str + "\n")

    @staticmethod
    def getLn():
        return input()

    @staticmethod
    def mod(a, b):
        return int(a) % int(b)

    @staticmethod
    def fst(tp):
        if not isinstance(tp, tuple) or len(tp) != 2:
            raise EvalError("Expected tuple with 2 members.")

        return tp[0]

    @staticmethod
    def snd(tp):
        if not isinstance(tp, tuple) or len(tp) != 2:
            raise EvalError("Expected tuple with 2 members.")

        return tp[1]

def LinkFunction(expr, context):
    funcRef = None
    if not context:
        raise EvalError("No context found")

    while expr.ident not in context and "@global@" in context:
        context = context["@global@"]

    if expr.ident in context:
        funcRef = context[expr.ident]

    return funcRef

def ResolveCallArgs(expr, context, EvalExpr):
    resolvedArgs = []
    for arg in expr.args:
        argexpr = ValExprNode(NodeType.Value, EvalExpr(arg, context))
        res = ExpressionNode(ExpressionType.Logical, argexpr)

        resolvedArgs.append(res)

    return resolvedArgs

def Restructure(ls, ln):
    retVal = tuple(ls[:ln - 1]) + (ls[ln - 1:], )

    if ln > len(ls):
        for i in range(ln - len(ls) - 1):
            retVal += ([], )

    return retVal
