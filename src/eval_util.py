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
        return sys.stdout.write(_str + "\n")

    @staticmethod
    def getLn():
        return input()

    def mod(a, b):
        return a % b

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
