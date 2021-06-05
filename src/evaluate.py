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

def EvalExpr(expr, context):
    if not isinstance(expr, ExpressionNode):
        raise TypeError("Expression node expected in call to EvalExpr()")

    return Switch(expr.exprType, {
    ExpressionType.Logical:     lambda: EvalArithmExpr(expr.expr, context),
    ExpressionType.Tuple:       lambda: EvalTupleExpr(expr.expr, context),
    ExpressionType.Mutable:     lambda: EvalMutableExpr(expr.expr, context),
    ExpressionType.Conditional: lambda: EvalConditionalExpr(expr.expr, context),
    ExpressionType.Chain:       lambda: EvalChainExpr(expr.expr, context)
    })

def EvalTupleExpr(expr, context):
    res = tuple()
    for i in expr:
        res += (EvalExpr(i, context), )

    return res

def EvalConditionalExpr(expr, context):
    if EvalExpr(expr.boolExpr, context):
        return EvalExpr(expr.thenExpr, context)

    return EvalExpr(expr.elseExpr, context)

def EvalMutableExpr(expr, context):
    return Switch(expr.mutype, {
    MutableType.String: lambda: expr.string.replace("\"", ""),
    MutableType.List: lambda: Switch(expr.ls.lsType, {
        ListType.Static: lambda: [EvalExpr(x, context) for x in expr.ls.seq],
        ListType.Ranged: lambda: list(range(int(EvalExpr(expr.ls.rng.begin, context)), int(EvalExpr(expr.ls.rng.end, context)) + 1)),
        ListType.Empty: lambda: []
        })
    })

def EvalChainExpr(expr, context):
    finalLs = []
    while expr:
        node = EvalExpr(expr.expr, context)

        if not expr.nextNode:
            if not isinstance(node, list):
                raise EvalError("No list at the end of a chain expression")
            else:
                finalLs += node

        else:
            finalLs.append(node)

        expr = expr.nextNode

    return finalLs

def LinkFunction(expr, context):
    funcRef = None

    while expr.ident not in context and "@global@" in context:
        context = context["@global@"]

    if expr.ident in context:
        funcRef = context[expr.ident]

    return funcRef

def EvalCall(expr, context):
    fc = LinkFunction(expr, context)

    if not fc:
        raise EvalError(f"Reference to undefined function '{expr.ident}'")

    arglen1 = len(fc.args)
    arglen2 = len(expr.args)

    if arglen1 != arglen2:
        raise EvalError(f"Mismatching number of arguments in function call and function declaration of function {expr.ident}")

    stack = dict(fc.context)
    stack["@global@"] = context

    if arglen1 and arglen2:
        resargs = ResolveCallArgs(expr, context)

        for arg, ident in zip(resargs, fc.args):
            body = BodyNode(False, arg, None)
            stack[ident] = FunctionNode(ident, [], body, stack, None)

    return EvalExpr(fc.body.expr, stack)

def ResolveCallArgs(expr, context):
    resolvedArgs = []
    for arg in expr.args:
        argexpr = ValExprNode(NodeType.Value, EvalExpr(arg, context))
        res = ExpressionNode(ExpressionType.Logical, argexpr)

        resolvedArgs.append(res)

    return resolvedArgs

def EvalArithmExpr(expr, context):
    return Switch(expr.node_type, {
    NodeType.Value: lambda: EvalArithmExpr(expr.val) if isinstance(expr.val, ValExprNode) else expr.val,
    NodeType.FunctionCall: lambda: EvalCall(expr.val, context),
    NodeType.Operation: 
        lambda: Switch(expr.op, {
        TokenType.ADD: lambda: EvalArithmExpr(expr.lBranch, context) + EvalArithmExpr(expr.rBranch, context),
        TokenType.MULT: lambda: EvalArithmExpr(expr.lBranch, context) * EvalArithmExpr(expr.rBranch, context),
        TokenType.DIV: lambda: EvalArithmExpr(expr.lBranch, context) / EvalArithmExpr(expr.rBranch, context),
        TokenType.POW: lambda: EvalArithmExpr(expr.lBranch, context) ** EvalArithmExpr(expr.rBranch, context),
        TokenType.AND: lambda: float(EvalArithmExpr(expr.lBranch, context) and EvalArithmExpr(expr.rBranch, context)),
        TokenType.OR: lambda: float(EvalArithmExpr(expr.lBranch, context) or EvalArithmExpr(expr.rBranch, context)),
        TokenType.EQ: lambda: EvalArithmExpr(expr.lBranch, context) == EvalArithmExpr(expr.rBranch, context),
        TokenType.NEQ: lambda: EvalArithmExpr(expr.lBranch, context) != EvalArithmExpr(expr.rBranch, context),
        TokenType.LEQ: lambda: EvalArithmExpr(expr.lBranch, context) <= EvalArithmExpr(expr.rBranch, context),
        TokenType.GEQ: lambda: EvalArithmExpr(expr.lBranch, context) >= EvalArithmExpr(expr.rBranch, context),
        TokenType.LT: lambda: EvalArithmExpr(expr.lBranch, context) < EvalArithmExpr(expr.rBranch, context),
        TokenType.GT: lambda: EvalArithmExpr(expr.lBranch, context) > EvalArithmExpr(expr.rBranch, context),
        TokenType.SUB: lambda: -EvalArithmExpr(expr.lBranch, context)
        })
    })
