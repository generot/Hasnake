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

        ImportModule(token.get().replace("\"", ""))
        token.next()

    elif CheckToken(token, TokenType.IDENT):
        newSymbol = Function(parentContext)
        if newSymbol:
            parentContext[newSymbol.ident] = newSymbol

def Function(parentContext):
    funcIdent = token.get().strrep
    funcArgs = []

    token.next()

    while CheckToken(token, TokenType.IDENT, TokenType.LPAR):
        if not Destructure(funcArgs):
            funcArgs.append(token.get().strrep)
            token.next()

    if not CheckToken(token, TokenType.ASG, TokenType.GUARD):
        raise ParseError(f"Expected function declaration, got {token.get().token_type} instead.")

    localContext = {x: FunctionNode(x, [], None) for x in funcArgs}
    localContext["@global@"] = parentContext

    for i in localContext:
        if i != "@global@":
            localContext[i].context = {"@global@": localContext}

    body = Body()
    WhereContext(localContext)

    patterns = Pattern(funcIdent)
    return FunctionNode(funcIdent, funcArgs, body, localContext, patterns)

def Destructure(args):
    dTuple = ()
    if CheckToken(token, TokenType.LPAR):
        token.next()

        if CheckToken(token, TokenType.IDENT):
            dTuple += (token.get().strrep, )
            token.next()

        while CheckToken(token, TokenType.SPLIT):
            token.next()

            if CheckToken(token, TokenType.IDENT):
                dTuple += (token.get().strrep, )
                token.next()
            else:
                raise ParseError(f"Expected identifier when destructuring, got '{token.get().token_type}' instead.")

        if not CheckToken(token, TokenType.RPAR):
            raise ParseError(f"Expected closing parentheses, got '{token.get().token_type}' instead.")

        token.next()

        args.append(dTuple)
        return True

    return False

def WhereContext(parentContext):
    if not CheckToken(token, TokenType.WHERE):
        return False

    token.next()
    if not CheckToken(token, TokenType.LBPAR):
        raise ParseError("Expected '[' in 'where' block.")

    token.next()
    while not CheckToken(token, TokenType.RBPAR):
       func = Function(parentContext)
       parentContext[func.ident] = func

    token.next()
    return True

def Pattern(parentIdent):
    patterns, body = [], None

    while CheckToken(token, TokenType.IDENT) and token.get().strrep == parentIdent:
        args = tuple()
        token.next()

        while not CheckToken(token, TokenType.ASG):
            args += (Expression(),)

        body = Body()
        pattern = {args: body}

        patterns.append(PatternNode(parentIdent, pattern))

    return patterns

def Body():
    guarded, expr, guards = False, None, []

    if CheckToken(token, TokenType.GUARD):
        guarded = True
        while CheckToken(token, TokenType.GUARD):
            token.next()
            guards.append(Guard())

    elif CheckToken(token, TokenType.ASG):
        token.next()
        expr = Expression()

    return BodyNode(guarded, expr, guards)


def Guard():
    isOther = CheckToken(token, TokenType.OTHERWISE)
    boolExpr = None

    if not isOther:
        boolExpr = Expression()
    else:
        token.next()

    if not CheckToken(token, TokenType.ASG):
        raise ParseError("Expected '=' in guards")

    token.next()
    asgExpr = Expression()

    return GuardNode(boolExpr, asgExpr, isOther)

def Expression():
    (expr, exprType) = GetFirstRs(Tuple, Chain, Mutable, Conditional, Logical)

    if expr:
        return ExpressionNode(ExpressionType[exprType], expr)

    return None

def Chain():
    baseChain = None

    if CheckToken(token, TokenType.LPAR):
        currIx = token.ix

        token.next()
        expr = Expression()
    
        if CheckToken(token, TokenType.SPLIT):
            baseChain = ChainNode(expr, None)
            chain = baseChain

            while not CheckToken(token, TokenType.RPAR):
                if not CheckToken(token, TokenType.SPLIT):
                    raise ParseError(f"Expected ':' in chain, got {token.get().token_type} instead.")

                token.next()
                expr = Expression()
                
                chain.nextNode = ChainNode(expr, None)
                chain = chain.nextNode

            token.next()
        else:
            token.ix = currIx

    return baseChain

def Tuple():
    if CheckToken(token, TokenType.LPAR):
        currIx = token.ix
        token.next()

        accumulatedTuple = ()
        accumulatedTuple += (Expression(), )

        if not CheckToken(token, TokenType.COMMA):
            token.ix = currIx
            return None
        else:
            while not CheckToken(token, TokenType.RPAR):
                if not CheckToken(token, TokenType.COMMA):
                    raise ParseError(f"Expected comma in tuple, got {token.get().token_type} instead.")
                token.next()
                accumulatedTuple += (Expression(), )

            if not CheckToken(token, TokenType.RPAR):
                raise ParseError(f"Expected ')', got {token.get().token_type} instead")
        
            token.next()
            return accumulatedTuple

    return None


def Mutable():
    mutableType, string, _list = None, None, None
    if CheckToken(token, TokenType.LITERAL, TokenType.LBPAR):
        if CheckToken(token, TokenType.LITERAL):
            mutableType = MutableType.String

            string = token.get().strrep
            token.next()
        elif CheckToken(token, TokenType.LBPAR):
            mutableType = MutableType.List
            _list = List()

        return MutableNode(mutableType, string, _list)

    return None

def List():
    lsType = ListType.Empty
    seq, rng, compr = [], None, None

    if CheckToken(token, TokenType.LBPAR):
        token.next()
        if CheckToken(token, TokenType.RBPAR):
            token.next()
            return ListNode(ListType.Empty, seq, rng, compr)

        fstExpr = Expression()
        if CheckToken(token, TokenType.RBPAR):
            token.next()
            return ListNode(ListType.Static, [fstExpr], None, None)

        if CheckToken(token, TokenType.COMMA):
            lsType = ListType.Static
            seq.append(fstExpr)

            while CheckToken(token, TokenType.COMMA):
                token.next()
                seq.append(Expression())

        elif CheckToken(token, TokenType.RANGE):
            token.next()
            lsType = ListType.Ranged
            rng = RangeNode(fstExpr, Expression())

        elif CheckToken(token, TokenType.GUARD):
            token.next()
            lsType = ListType.Comprehensive
            
            symbols = {}

            (symIdent, symValues) = Assign2()
            symbols[symIdent] = symValues

            while CheckToken(token, TokenType.COMMA):
                token.next()

                (symIdent, symValues) = Assign2()
                symbols[symIdent] = symValues

            compr = ComprehensionNode(fstExpr, symbols)

        if not CheckToken(token, TokenType.RBPAR):
            raise ParseError(f"Expected list, got '${token.get().token_type}' instead.")

        token.next()
        return ListNode(lsType, seq, rng, compr)

    return None

def Assign2():
    if not CheckToken(token, TokenType.IDENT):
        raise ParseError(f"Expected identifier in comprehension, got '{token.get().token_type}' instead.")

    ident = token.get().strrep
    token.next()

    if not CheckToken(token, TokenType.ASG2):
        raise ParseError(f"Expected '<-' in comprehension")

    token.next()
    ls = List()

    return (ident, ls)

def Conditional():
    boolExpr, thenExpr, elseExpr = None, None, None

    if CheckToken(token, TokenType.IF):
        token.next()
        boolExpr = Expression()
        if not CheckToken(token, TokenType.THEN):
            raise ParseError("Expected 'then' in if-then-else statement")
    
        token.next()
        thenExpr = Expression()
        if not CheckToken(token, TokenType.ELSE):
            raise ParseError("Expected 'else' in if-then-else statement")

        token.next()
        elseExpr = Expression()
        return ConditionalNode(boolExpr, thenExpr, elseExpr)

    return None

def Logical():
    lbr, rbr = Comparison(), None
    oper = None

    if token.get():
        oper = token.get().token_type

    if CheckToken(token, TokenType.AND, TokenType.OR):
        token.next()
        if not CheckToken(token, TokenType.IDENT, TokenType.VALUE, TokenType.SUB, TokenType.LPAR):
            raise ParseError(f"Expected expression, got {token.get().token_type} instead.")

        rbr = Logical()

        return ValExprNode(NodeType.Operation, 0, oper, lbr, rbr)

    return lbr

def Comparison():
    lbr, rbr = Term(), None
    oper = None

    if token.get():
        oper = token.get().token_type

    comps = [TokenType(x) for x in ["==", "/=", "<=", ">=", "<", ">"]]

    if CheckToken(token, *comps):
        token.next()
        if not CheckToken(token, TokenType.IDENT, TokenType.VALUE, TokenType.SUB, TokenType.LPAR):
            raise ParseError(f"Expected expression, got {token.get().token_type} instead.")

        rbr = Comparison()

        return ValExprNode(NodeType.Operation, 0, oper, lbr, rbr)

    return lbr

def Term():
    lbr, rbr = Factor(), None
    oper = None

    if token.get():
        oper = token.get().token_type

    if CheckToken(token, TokenType.ADD, TokenType.SUB):
        if CheckToken(token, TokenType.ADD):
            token.next()

        if not CheckToken(token, TokenType.IDENT, TokenType.VALUE, TokenType.SUB, TokenType.LPAR):
            raise ParseError(f"Expected expression, got {token.get().token_type} instead.")

        rbr = Term()
        return ValExprNode(NodeType.Operation, 0, TokenType.ADD, lbr, rbr)

    return lbr

def Factor():
    lbr, rbr = Negate(), None
    oper = None

    if token.get():
        oper = token.get().token_type

    if CheckToken(token, TokenType.MULT, TokenType.DIV):
        token.next()

        if not CheckToken(token, TokenType.IDENT, TokenType.VALUE, TokenType.SUB, TokenType.LPAR):
            raise ParseError(f"Expected expression, got {token.get().token_type} instead.")

        rbr = Factor()
        return ValExprNode(NodeType.Operation, 0, oper, lbr, rbr)

    return lbr

def Negate():
    oper = None

    if token.get():
        oper = token.get().token_type

    if CheckToken(token, TokenType.SUB):
        token.next()

        if not CheckToken(token, TokenType.IDENT, TokenType.VALUE, TokenType.SUB, TokenType.LPAR):
            raise ParseError(f"Expected expression, got {token.get().token_type} instead.")

        lbr = Negate()
        return ValExprNode(NodeType.Operation, 0, oper, lbr, None)

    return Power()


def Power():
    lbr, rbr = Value(), None
    oper = None

    if token.get():
        oper = token.get().token_type

    if CheckToken(token, TokenType.POW):
        token.next()

        if not CheckToken(token, TokenType.IDENT, TokenType.VALUE, TokenType.SUB, TokenType.LPAR):
            raise ParseError(f"Expected expression, got {token.get().token_type} instead.")

        rbr = Power()
        return ValExprNode(NodeType.Operation, 0, oper, lbr, rbr)

    return lbr

def Value():
    val = 0
    ntype = NodeType.Value

    if CheckToken(token, TokenType.VALUE):
        val = float(token.get().strrep)
        token.next()

    elif CheckToken(token, TokenType.IDENT):
        (_val, _type) = Call()
        val = _val
        ntype = _type

    elif CheckToken(token, TokenType.LPAR):
        token.next()
        val = Logical()
        if not CheckToken(token, TokenType.RPAR):
            raise ParseError(f"Expected closing parentheses, got '{token.get().token_type}' instead.")

        token.next()

    return ValExprNode(ntype, val)

def Call():
    ident, args = token.get().strrep, []

    token.next()
    if CheckToken(token, TokenType.LPAR):
        token.next()
        if not token.get():
            raise ParseError("Expected expression, got nothing instead")

        while not CheckToken(token, TokenType.RPAR):
            args.append(Expression())

        token.next()
    else:
        return (ReferenceNode(ident), NodeType.Reference)
        
    return (CallNode(ident, args), NodeType.FunctionCall)

def Program(tokens):
    global token
    token = BetterIterator(tokens)

    globalContext = {}

    while token.get():
        Statement(globalContext)

    return globalContext

def ExprParser(tokens):
    global token
    token = BetterIterator(tokens)

    return Expression()
