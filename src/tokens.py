from enum import Enum

class TokenType(Enum):
    NONE = -1
    IDENT = 0
    VALUE = 1
    LITERAL = 2
#OPERATORS
    ADD = "+"
    SUB = "-"
    MULT = "*"
    DIV = "/"
    EQ = "=="
    LEQ = "<="
    GEQ = ">="
    NEQ = "!="
    LT = "<"
    GT = ">"
    ASG = "="
    POW = "^"
    LPAR = "("
    RPAR = ")"
    DEC = "."
#OPERATORS
#KEYWORDS
    IF = "if"
    THEN = "then"
    ELSE = "else"
    OTHERWISE = "otherwise"
    GETCHAR = "getchar"
    PUTCHAR = "putchar"
    WHERE = "where"
    IMPORT = "import"
#KEYWORDS
#RESERVED SYMBOLS
    GUARD = "|"
    ASG2 = "<-"
    SPLIT = ":"
    RANGE = ".."
    LBPAR = "["
    RBPAR = "]"
#RESERVED SYMBOLS

class Token:
    def __init__(self, ttype):
        if not isinstance(ttype, TokenType):
            raise TypeError("'Argument 'ttype' should be an instance of the TokenType class")

        self.token_type = ttype
        self.strrep = ""

def HandleSpecialToken(strrep):
    if strrep.isalnum():
        if strrep.isnumeric():
            return TokenType.VALUE

        return TokenType.IDENT
    else:
        if strrep.count('"') > 1:
            return TokenType.LITERAL

    return TokenType.NONE

def DetermineToken(strrep):
    if not isinstance(strrep, str):
        raise TypeError("Parameter of non-string type passed to DetermineToken()")

    try:
        return TokenType(strrep)
    except ValueError:
        return HandleSpecialToken(strrep)
    
