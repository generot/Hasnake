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

    elif CheckToken(token, TokenType.IDENT):
        newSymbol = Function(parentContext)
        if newSymbol:
            parentContext[newSymbol.ident] = newSymbol

def Function(parentContext):
    funcIdent = token.get()
    funcArgs = []

    token.next()

    while CheckToken(token, TokenType.IDENT, TokenType.LPAR):
        Destructure(funcArgs)
        funcArgs.append(token.get())

        token.next()

    localContext = {x: None for x in funcArgs}
    localContext["@global@"] = parentContext

    body = Body()
    WhereContext(localContext)

    patterns = Pattern(funcIdent)
    return FunctionNode(funcIdent, funcArgs, body, localContext, patterns)

def Destructure(args):
    dTuple = ()
    if CheckToken(token, TokenType.LPAR):
        token.next()

        if CheckToken(token, TokenType.IDENT):
            dTuple += (token.get(), )
            token.next()

        while CheckToken(token, TokenType.SPLIT):
            token.next()

            if CheckToken(token, TokenType.IDENT):
                dTuple += (token.get(), )
                token.next()
            else:
                raise ParseError("Expected identifier when destructuring, got '{token.get()}' instead.")

        if not CheckToken(token, TokenType.RPAR):
            raise ParseError(f"Expected closing parentheses, got '{token.get()} instead.")

        token.next()

    args.append(dTuple)

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
    exprType = None
    dc = {
        "chain": Chain()
        "_tuple": Tuple()
        "valexpr": Logical()
        "mutable": Mutable()
        "ifThenElse": Conditional()
        "IO": InputOutput()
    }

    for i in dc:
        if dc[i]:
            exprType = ExpressionType(i)
            return ExpressionNode(exprType, **dc)

    return None

def Chain():
    currIx = token.ix
    expr = Expression()

    if CheckToken(token, TokenType.SPLIT):
        nextNode = Expression()
        return ChainNode(expr, nextNode)
    
    token.ix = currIx
    return None

def Tuple():
    if CheckToken(token, TokenType.LPAR):
        lookIx = 2
        isTuple = False

        while (currToken := token.lookahead(lookIx)) != TokenType.RPAR:
            if currToken == TokenType.COMMA:
                isTuple = True
                break

        if isTuple:
            token.next()

            accumulatedTuple = ()
            accumulatedTuple += (Expression(), )

            while not CheckToken(token, TokenType.RPAR):
                if not CheckToken(token, TokenType.COMMA):
                    raise ParseError(f"Expected comma in tuple definition, got '{token.get()}' instead.")
                token.next()
                accumulatedTuple += (Expression(), )
        
            return accumulatedTuple

    return None


def Mutable():
    mutableType, string, _list = None, None, None
    if CheckToken(token, TokenType.LITERAL, TokenType.LBPAR):
        if CheckToken(token, TokenType.LITERAL):
            mutableType = String

            token.next()
            string = token.get()
            token.next()
        elif CheckToken(token, TokenType.LBPAR):
            mutableType = List
            _list = List()

        return MutableNode(mutableType, string, _list)

    return None

def List():
    lsType = ListType.Empty
    seq, rng, compr = [], None, None

    token.next()
    if CheckToken(token, TokenType.RBPAR):
        return ListNode(ListType.Empty, seq, rng, compr)

    fstExpr = Expression()
    if CheckToken(token, TokenType.COMMA):
        lsType = ListType.Static
        seq.append(fstExpr)

        while CheckToken(token, TokenType.COMMA):
            token.next()
            seq.append(Expression())

    elif CheckToken(token, TokenType.RANGE):
        token.next()
        rng = RangeNode(fstExpr, Expression())

    elif CheckToken(token, TokenType.GUARD):
        token.next()
        symbols = {}

        sym = Assign2()
        symbols[sym.ident] = sym

        while CheckToken(token, TokenType.COMMA):
            token.next()

            sym = Assign2()
            symbols[sym.ident] = sym

    if not CheckToken(token, TokenType.RBPAR):
        raise ParseError(f"Expected list, got '${token.get()}' instead."

    token.next()
    return ListNode(lsType, seq, rng, compr)

def Assign2():
    if not CheckToken(token, TokenType.IDENT):
        raise ParseError(f"Expected identifier in comprehension, got '{token.get()}' instead.")

    ident = token.get()
    token.next()

    if not CheckToken(token, TokenType.ASG2):
        raise ParseError(f"Expected '<-' in comprehension")

    token.next()
    ls = List()

    return Assign2Node(ident, ls)

def Conditional():
    boolExpr, thenExpr, elseExpr = None, None, None
    if CheckToken(token, TokenType.IF):
        token.next()
        boolExpr = Expression()
        if not CheckToken(token, TokenType.THEN):
            raise ParseError("Expected 'then' in if-then-else statement")

        thenExpr = Expression()
        if not CheckToken(token, TokenType.THEN):
            raise ParseError("Expected 'else' in if-then-else statement")

        elseExpr = Expression()
        return ConditionalNode(boolExpr, thenExpr, elseExpr)

    return None

def InputOutput():
    _type = None
    _param = None

    if CheckToken(token, TokenType.GETCHAR, TokenType.PUTCHAR):
        if CheckToken(token, TokenType.GETCHAR):
            _type = IOType.Stdin
            token.next()
        elif CheckToken(token, TokenType.PUTCHAR):
            token.next()

            _type = IOType.Stdout
            _param = Expression()

        return IONode(_type, param)

    return None


def Logical():
    lbr, rbr = Comparison(), None
    oper = token.get()

    if CheckToken(token, TokenType.AND, TokenType.OR):
        token.next()
        rbr = Logical()

        return ValExprNode(NodeType.Operation, 0, Operation(oper), lbr, rbr)

    return lbr

def Comparison():
    lbr, rbr = Term(), None
    oper = token.get()

    comps = [TokenType(x) for x in ["==", "/=", "<=", ">=", "<", ">"]]

    if CheckToken(token, *comps):
        token.next()
        rbr = Comparison()

        return ValExprNode(NodeType.Operation, 0, Operation(oper), lbr, rbr)

    return lbr

def Term():
    lbr, rbr = Factor(), None
    oper = token.get()

    if CheckToken(token, TokenType.ADD, TokenType.SUB):
        if CheckToken(token, TokenType.ADD):
            it.next()

        rbr = Term()
        return ValExprNode(NodeType.Operation, 0, Operation.Add, lbr, rbr)

    return lbr

def Factor():
    lbr, rbr = Negate(), None
    oper = token.get()

    if CheckToken(token, TokenType.MULT, TokenType.DIV):
        token.next()
        rbr = Factor()
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
        val = float(token.get())
        token.next()
    elif CheckToken(token, TokenType.IDENT):
        ntype = NodeType.FunctionCall
        val = Call()
        token.next()


    if CheckToken(token, TokenType.LPAR):
        token.next()
        val = Term()
        if not CheckToken(token, TokenType.RPAR):
            raise ParseError(f"Expected closing parentheses, got '{token.get()}' instead.")

        token.next()

    return ValExprNode(ntype, val)

def Call():
    ident, args = token.get(), []

    token.next()
    if CheckToken(token, TokenType.LPAR):
        token.next()
        while CheckToken(token, TokenType.RPAR):
            args.append(Expression())
        
    return CallNode(ident, args)

def Program(tokens):
    global token
    token = BetterIterator(tokens)

    globalContext = {}

    while token:
        Statement(globalContext)

    return globalContext
