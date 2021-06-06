from src.lexer import LexLine, LexFile
from src.parser import ExprParser, Program
from src.evaluate import EvalExpr, Switch

def Perror(err):
    err = str(err)
    msg, hyphens = "EXCEPTION", ""

    lnerr = len(err)
    lnmsg = len(msg)

    diff = lnerr - lnmsg
    hyphens = "-" * (abs(diff) // 2)

    print(f"{hyphens}{msg}{hyphens}\n{err}")

def DisplayHelp():
    print(f'{"_" * 20}\n'
          ":q - Exit\n"
          ":help - Open help menu\n"
          f'{"-" * 20}\n')

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

        try:
            expr = ExprParser(LexLine(inp))
            res = EvalExpr(expr, symTable)

            print(res)

        except Exception as err:
            Perror(err)

def LoadFile(_dir):
    fileHandle = open(_dir, "r")

    tokens = LexFile(fileHandle)
    fileHandle.close()

    return Program(tokens)
