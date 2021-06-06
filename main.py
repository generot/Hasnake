from src.evaluate import Switch, EvalExpr
from src.util import Interactive, LoadFile

from utest import RunTest
from unittest import TextTestRunner
import sys

#DEFINITIONS
EXIT_SUCCESS = 0
EXIT_FAILURE = -1

def Entry():
    args = {"-m": None, "-utest": False}

    if len(sys.argv) > 1:
        for i in range(len(sys.argv)):
            args[sys.argv[i]] = Switch(sys.argv[i], {
            "-m": lambda: LoadFile(sys.argv[i + 1]),
            "-utest": lambda: True
            })

    symbolTable = args["-m"]

    if args["-utest"]:
        sys.argv.pop()

        suite = RunTest()
        testRunner = TextTestRunner()
        testRunner.run(suite)

        return EXIT_SUCCESS

    sys.setrecursionlimit(2000)
    Interactive(symbolTable)
        
    return EXIT_SUCCESS

#Program entry
if __name__ == "__main__":
    ret_code = 0
    if ret_code := Entry():
        print(f"Internal error, return code: {ret_code}")
