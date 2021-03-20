from src.lexer import *
import sys

#DEFINITIONS
EXIT_SUCCESS = 0
EXIT_FAILURE = -1

def entry():
    if len(sys.argv) < 2:
        print("Usage: python main.py <haskell_src>.hs")
        return EXIT_FAILURE

    with open(sys.argv[1], "r") as f:
        tokens = LexFile(f)
        PrintTokens(tokens)

    return EXIT_SUCCESS

#Program entry
if __name__ == "__main__":
    ret_code = 0
    if ret_code := entry():
        print(f"Internal error, return code: {ret_code}")
    else:
        print(f"Exited normally with return code: {ret_code}")
