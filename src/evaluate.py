from src.parser import ExprParser
from src.parse_util import ListType, NodeType, MutableType, ExpressionType
from src.tokens import TokenType

from src.eval_util import *
from src.exception import EvalError
from src.ast import *

from itertools import product

def Switch(val, cases):
    return cases[val]()

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
    if not isinstance(expr, MutableNode):
        raise EvalError(f"Mutable node should be passed to EvalMutableExpr().")

    return Switch(expr.mutype, {
    MutableType.String: lambda: expr.string.replace("\"", ""),
    MutableType.List: lambda: Switch(expr.ls.lsType, {
        ListType.Static: lambda: [EvalExpr(x, context) for x in expr.ls.seq],
        ListType.Ranged: lambda: list(range(int(EvalExpr(expr.ls.rng.begin, context)), int(EvalExpr(expr.ls.rng.end, context)) + 1)),
        ListType.Empty: lambda: [],
        ListType.Comprehensive: lambda: EvalComprehension(expr.ls.compr, context)
        })
    })

def EvalComprehension(comp, context):
    symbols = {i: EvalMutableExpr(MutableNode(MutableType.List, ls = comp.symbols[i]), context) for i in comp.symbols}

    finalLs = []
    combinations = list(product(*list(symbols.values())))

    symbols["@global@"] = context
    for i in combinations:
        for ix, j in enumerate(symbols):
            if j != "@global@":
                val = ValExprNode(NodeType.Value, i[ix])
                body = BodyNode(False, ExpressionNode(ExpressionType.Logical, val), None)
                symbols[j] = FunctionNode(j, [], body, symbols)

        finalLs.append(EvalExpr(comp.baseExpr, symbols))

    return finalLs
    

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

def EvalCall(expr, context):
    fc = None
    isBuiltin = False

    try:
        fc = getattr(BuiltinMethod, expr.ident)
        isBuiltin = True
    except:
        fc = LinkFunction(expr, context)

    if isBuiltin:
        if fc.__code__.co_argcount != len(expr.args):
            raise EvalError(f"Mismatching number of parameters between call and definition of built-in function '{expr.ident}'")

        params = [EvalExpr(x, context) for x in expr.args]
        return fc(*params)
 

    if not fc:
        raise EvalError(f"Reference to undefined function '{expr.ident}'")

    arglen1 = len(fc.args)
    arglen2 = len(expr.args)

    if arglen1 != arglen2:
        raise EvalError(f"Mismatching number of arguments in function call and function declaration of function '{expr.ident}'")

    stack = dict(fc.context)
    stack["@global@"] = context

    if arglen1 and arglen2:
        resargs = ResolveCallArgs(expr, context, EvalExpr)

        for arg, ident in zip(resargs, fc.args):
            if isinstance(ident, tuple):
                if not isinstance(arg.expr.val, list):
                    raise EvalError(f"Destructuring is not defined for {arg}")

                rst = Restructure(arg.expr.val, len(ident))
                for elem, _id in zip(rst, ident):
                    val = ValExprNode(NodeType.Value, elem)

                    body = BodyNode(False, ExpressionNode(ExpressionType.Logical, val), None)
                    stack[_id] = FunctionNode(ident, [], body, stack, None)

            elif isinstance(arg.expr.val, FunctionNode):
                stack[ident] = arg.expr.val
            else:
                body = BodyNode(False, arg, None)
                stack[ident] = FunctionNode(ident, [], body, stack, None)

    if fc.body.isGuarded:
        otherwise = None

        for guard in fc.body.guards:
            if not guard.isotherwise:
                cond = EvalExpr(guard.boolExpr, stack)
                if cond:
                    return EvalExpr(guard.asgExpr, stack)
            else:
                otherwise = guard

        return EvalExpr(otherwise.asgExpr, stack)

    return EvalExpr(fc.body.expr, stack)

def EvalArithmExpr(expr, context):
    return Switch(expr.node_type, {
    NodeType.Value: lambda: EvalArithmExpr(expr.val, context) if isinstance(expr.val, ValExprNode) else expr.val,
    NodeType.FunctionCall: lambda: EvalCall(expr.val, context),
    NodeType.Reference: lambda: LinkFunction(expr.val, context),
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


