from enum import Enum
from src.tokens import TokenType

class IOType(Enum):
    Stdout = 0
    Stdin = 1

class ListType(Enum):
    Static = 0
    Ranged = 1
    Comprehensive = 2
    Empty = 3

class NodeType(Enum):
    Operation = 0
    Value = 1
    FunctionCall = 2
    Reference = 3
    Lambda = 4

class MutableType(Enum):
    List = 0
    String = 1

class ExpressionType(Enum):
    Logical = 0
    Tuple = 1
    Mutable = 2
    Conditional = 3
    Chain = 4

class Operation(Enum):
    Add = '+'
    Sub = '-'
    Mult = '*'
    Div = '/'
    And = '&&'
    Or = '||'
    Eq = '=='
    Neq = '/='
    Leq = '<='
    Geq = '>='
    Lt = '<'
    Gt = '>'
    Pow = '^'

class Iterator:
    def __init__(self, ls):
        self.ls = ls
        self.iter = self.iterator(self.ls)
        self.curr = self.gnext(self.iter)

    def concat(self, otherLs):
        for i in otherLs:
            self.ls.append(i)

    def next(self):
        self.curr = self.gnext(self.iter)

    def get(self):
        return self.curr

    @staticmethod
    def iterator(arr):
        for i in arr:
            yield(i)

    @staticmethod
    def gnext(_iterator):
        try:
            return next(_iterator)
        except StopIteration:
            return None

class BetterIterator:
    def __init__(self, ls):
        self.ls = list(ls)
        self.len = len(ls)
        self.ix = 0

    def __neq__(self, ttype):
        return self.ls[self.ix].token_type != ttype

    def concat(self, otherLs):
        for i in otherLs:
            self.ls.append(i)

        self.len = len(self.ls)

    def next(self):
        if self.ix < self.len:
            self.ix += 1

    def lookahead(self, pos):
        if self.ix + pos < self.len:
            return self.ls[self.ix + pos]
        
        return None

    def get(self):
        if self.ix < self.len:
            return self.ls[self.ix]

        return None

def GetFirstRs(*funcs):
    for i in funcs:
        res = i()
        if res:
            return (res, i.__name__)

    return (None, None)

def CheckToken(itr, *args):
    if not itr.get():
        return False

    for i in args:
        if itr.get().token_type == i:
            return True

    return False
