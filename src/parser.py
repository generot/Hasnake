from src.ast import *
from src.parse_util import *
from src.exception import *

from src.lexer import LexFile

def ImportModule(_dir):
    with open(_dir) as modSrc:
        modTokens = LexFile(modSrc)
        token.concat(modTokens)

def Statement(parentContext):
    if CheckToken(token, TokenType.IMPORT):
        token.next()

        if not CheckToken(token, TokenType.LITERAL):
            raise ParseError("Expected string literal after 'import'.")

        moduleContext = ImportModule(token.get().replace("\"", ""))

        for symbol in moduleContext.values():
            parentContext[symbol.ident] = symbol

        token.next()
    
    if CheckToken(token, TokenType.IDENT):
        Function(parentContext)

def Function(parentContext):
    funcIdent = token.get()
    funcArgs = []

    token.next()

    while CheckToken(token, TokenType.IDENT, TokenType.LPAR):
        if CheckToken(token, TokenType.LPAR):
            token.next()
            head = token.get()

            token.next()
            if not CheckToken(token, TokenType.SPLIT):
                raise ParseError("Expected ':' in head-tail pair.")

            token.next()
            tail = token.get()

            funcArgs.append((head, tail))

            if not CheckToken(token, TokenType.RPAR):
                raise ParseError(f"Expected ')' in the signature of symbol '{funcIdent}'.")
            token.next()

        funcArgs.append(token.get())
        token.next()

    localContext = {x: None for x in funcArgs}

    body = Body()
    WhereContext(localContext)

    patterns = Pattern(funcIdent)
    parentContext[funcIdent] = FunctionNode(funcIdent, funcArgs, body, localContext, parentContext, patterns)

def WhereContext(parentContext):
    if not CheckToken(token, TokenType.WHERE):
        return False

    token.next()
    if not CheckToken(token, TokenType.LBPAR):
        raise ParseError("Expected '[' in 'where' block.")

    token.next()
    while not CheckToken(token, TokenType.RBPAR):
        Function(parentContext)

    token.next()
    return True

def Pattern(parentIdent):
    args, patterns, body = [], [], None

    while CheckToken(token, TokenType.IDENT) and token.strrep == parentIdent:
        token.next()
        while not CheckToken(token, TokenType.ASG):
            args.append(Expression(None))

        body = Body(None)
        patterns.append(PatternNode(parentIdent, args, body))

    return patterns

def Body():
    guarded, expr, guards = False, None, []

    if CheckToken(token, TokenType.GUARD):
        guarded = True
        while CheckToken(token, TokenType.GUARD):
            token.next()
            guards.append(Guard())

    elif CheckToken(token, TokenType.ASG):
        expr = Expression()

    return BodyNode(guarded, expr, guards)

def Guard():
    boolExpr = Expression()

    if not CheckToken(token, TokenType.ASG):
        raise ParseError("Expected '=' in guards")

    token.next()
    asgExpr = Expression()

    return GuardNode(boolExpr, asgExpr)

def Expression():
    pass

def Term():
    lbr, rbr = Factor(), None
    oper = it.get()

    if oper == '+' or oper == '-':
        if oper == '+':
            it.next()

        rbr = term()
        return ValExprNode(NodeType.Operation, 0, Operation.Add, lbr, rbr)

    return lbr

def Factor():
    lbr, rbr = Negate(), None
    oper = token.get()

    if CheckToken(token, TokenType.MULT, TokenType.DIV):
        token.next()
        rbr = factor()
        return ValExprNode(NodeType.Operation, 0, Operation(oper), lbr, rbr)

    return lbr

def Negate():
    oper = token.get()

    if CheckToken(token, TokenType.SUB):
        token.next()
        lbr = Negate()
        return ValExprNode(NodeType.Operation, 0, Operation(oper), lbr, None)

    return Power()


def Power():
    lbr, rbr = Value(), None
    oper = token.get()

    if CheckToken(token, TokenType.POW):
        token.next()
        rbr = Power()
        return ValExprNode(NodeType.Operation, 0, Operation(oper), lbr, rbr)

    return lbr

def Value():
    val = 0
    ntype = NodeType.Value

    if CheckToken(token, TokenType.VALUE):
        val = int(it.get())
    elif CheckToken(token, TokenType.IDENT):
        val = Call()
        ntype = NodeType.FunctionCall


    if CheckToken(token, TokenType.LPAR):
        token.next()
        val = Term()
        token.next()

    return ValExprNode(ntype, val)

def Call():
    pass

def Program(tokens):
    global token
    token = Iterator(tokens)

    globalContext = {}

    while token:
        Statement(globalContext)
        Expression()

    return globalContext
