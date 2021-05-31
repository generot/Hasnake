from src.lexer import *
from src.parser import *

import sys

#DEFINITIONS
EXIT_SUCCESS = 0
EXIT_FAILURE = -1

def entry():
    if len(sys.argv) < 2:
        print("Usage: python main.py <haskell_src>.hs")
        return EXIT_FAILURE

    #try:
    with open(sys.argv[1], "r") as f:
        tokens = LexFile(f)
        #PrintTokens(tokens)
        symbolTable = Program(tokens)

        print(symbolTable["getLine"].patterns[2].body.expr.exprType)
    #except ParseError as err:
    #    print(err)
        

    return EXIT_SUCCESS

#Program entry
if __name__ == "__main__":
    ret_code = 0
    if ret_code := entry():
        print(f"Internal error, return code: {ret_code}")
