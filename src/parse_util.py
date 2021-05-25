from enum import Enum
from src.tokens import TokenType

class ListType(Enum):
    Static = 0
    Ranged = 1
    Comprehensive = 2

class NodeType(Enum):
    Operation = 0
    Value = 1
    FunctionCall = 2

class MutableType(Enum):
    List = 0
    String = 1

class Operation(Enum):
    Add = '+'
    Sub = '-'
    Mult = '*'
    Div = '/'
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

def CheckToken(itr, *args):
    for i in args:
        if itr.get() == i:
            return True

    return False
