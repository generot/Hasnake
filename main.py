from src.lexer import *
from src.parser import *

from src.evaluate import EvalExpr, Switch

import sys

#DEFINITIONS
EXIT_SUCCESS = 0
EXIT_FAILURE = -1

def DisplayHelp():
    print(f'{"#" * 20}\n'
          ":q - Exit\n"
          ":help - Open help menu\n"
          f'{"#" * 20}\n')

def Commands(inp):
    inp = inp.strip()
    res = Switch(inp, {
        ":q": lambda: exit(),
        ":help": lambda: DisplayHelp()
    })

def Interactive(symTable):
    lmb = u"\u03BB> "
    msg = "Hasnake v1.0 - A Haskell interpreter, written in Python(i.e. the slowest thing on the planet)"
    hyphens = "-" * len(msg)
    inp = None

    print(f"{msg}\n{hyphens}")

    while True:
        try:
            inp = input(lmb)
        except:
            return
        
        if inp.find(":") == 0:
            Commands(inp)
            continue

        expr = ExprParser(LexLine(inp))
        res = EvalExpr(expr, symTable)

        print(res)


def Entry():
    if len(sys.argv) < 2:
        print("Usage: python main.py <haskell_src>.hs")
        return EXIT_FAILURE

    with open(sys.argv[1], "r") as f:
        tokens = LexFile(f)
        symbolTable = Program(tokens)
        
        Interactive(symbolTable)
        #print(symbolTable["caller"].body.expr.expr.val.args[0].expr.node_type)
        

    return EXIT_SUCCESS

#Program entry
if __name__ == "__main__":
    ret_code = 0
    if ret_code := Entry():
        print(f"Internal error, return code: {ret_code}")
