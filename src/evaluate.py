from src.parser import ExprParser
from src.parse_util import ListType, NodeType, MutableType, ExpressionType
from src.tokens import TokenType

from src.exception import EvalError
from src.ast import *

def Switch(val, cases):
    return cases[val]()

def InitEval(ast):
    global symbolTable
    symbolTable = ast

def EvalExpr(expr):
    if not isinstance(expr, ExpressionNode):
        raise TypeError("Expression node expected in call to EvalExpr()")

    return Switch(expr.exprType, {
    ExpressionType.Logical:     lambda: EvalArithmExpr(expr.expr),
    ExpressionType.Tuple:       lambda: EvalTupleExpr(expr.expr),
    ExpressionType.Mutable:     lambda: EvalMutableExpr(expr.expr),
    ExpressionType.Conditional: lambda: EvalConditionalExpr(expr.expr),
    ExpressionType.Chain:       lambda: EvalChainExpr(expr.expr)
    })

def EvalTupleExpr(expr):
    res = tuple()
    for i in expr:
        res += (EvalExpr(i), )

    return res

def EvalConditionalExpr(expr):
    if EvalExpr(expr.boolExpr):
        return EvalExpr(expr.thenExpr)

    return EvalExpr(expr.elseExpr)

def EvalMutableExpr(expr):
    return Switch(expr.mutype, {
    MutableType.String: lambda: expr.string.replace("\"", ""),
    MutableType.List: lambda: Switch(expr.ls.lsType, {
        ListType.Static: lambda: [EvalExpr(x) for x in expr.ls.seq],
        ListType.Ranged: lambda: list(range(int(EvalExpr(expr.ls.rng.begin)), int(EvalExpr(expr.ls.rng.end)) + 1)),
        ListType.Empty: lambda: []
        })
    })

def EvalChainExpr(expr):
    finalLs = []
    while expr:
        node = EvalExpr(expr.expr)

        if not expr.nextNode:
            if not isinstance(node, list):
                raise EvalError("No list at the end of a chain expression")
            else:
                finalLs += node

        else:
            finalLs.append(node)

        expr = expr.nextNode

    return finalLs

def EvalCall(expr):
    funcRef = symbolTable[expr.ident]
    

def EvalArithmExpr(expr):
    return Switch(expr.node_type, {
    NodeType.Value: lambda: EvalArithmExpr(expr.val) if isinstance(expr.val, ValExprNode) else expr.val,
    NodeType.Operation: 
        lambda: Switch(expr.op, {
        TokenType.ADD: lambda: EvalArithmExpr(expr.lBranch) + EvalArithmExpr(expr.rBranch),
        TokenType.MULT: lambda: EvalArithmExpr(expr.lBranch) * EvalArithmExpr(expr.rBranch),
        TokenType.DIV: lambda: EvalArithmExpr(expr.lBranch) / EvalArithmExpr(expr.rBranch),
        TokenType.POW: lambda: EvalArithmExpr(expr.lBranch) ** EvalArithmExpr(expr.rBranch),
        TokenType.AND: lambda: float(EvalArithmExpr(expr.lBranch) and EvalArithmExpr(expr.rBranch)),
        TokenType.OR: lambda: float(EvalArithmExpr(expr.lBranch) or EvalArithmExpr(expr.rBranch)),
        TokenType.EQ: lambda: EvalArithmExpr(expr.lBranch) == EvalArithmExpr(expr.rBranch),
        TokenType.NEQ: lambda: EvalArithmExpr(expr.lBranch) != EvalArithmExpr(expr.rBranch),
        TokenType.LEQ: lambda: EvalArithmExpr(expr.lBranch) <= EvalArithmExpr(expr.rBranch),
        TokenType.GEQ: lambda: EvalArithmExpr(expr.lBranch) >= EvalArithmExpr(expr.rBranch),
        TokenType.LT: lambda: EvalArithmExpr(expr.lBranch) < EvalArithmExpr(expr.rBranch),
        TokenType.GT: lambda: EvalArithmExpr(expr.lBranch) > EvalArithmExpr(expr.rBranch),
        TokenType.SUB: lambda: -EvalArithmExpr(expr.lBranch)
        })
    })
