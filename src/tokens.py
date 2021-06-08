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
    AND = "&&"
    OR = "||"
    EQ = "=="
    LEQ = "<="
    GEQ = ">="
    NEQ = "/="
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
    WHERE = "where"
    IMPORT = "import"
#KEYWORDS
#RESERVED SYMBOLS
    GUARD = "|"
    ASG2 = "<-"
    SPLIT = ":"
    RANGE = ".."
    COMMA = ","
    LBPAR = "["
    RBPAR = "]"
    LAMBDA = "\\"
    ARROW = "->"
#RESERVED SYMBOLS

class Token:
    def __init__(self, ttype):
        if not isinstance(ttype, TokenType):
            raise TypeError("'Argument 'ttype' should be an instance of the TokenType class")

        self.token_type = ttype
        self.strrep = ""

def IsNumeric(strrep):
    chars = [str(x) for x in range(10)] + ["."]

    for i in strrep:
        if i not in chars:
            return False

    return True

def HandleSpecialToken(strrep):
    if IsNumeric(strrep):
        return TokenType.VALUE
    elif strrep.isalnum() and not strrep.isnumeric():
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
