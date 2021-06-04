import re
from src.tokens import *

#----GLOBALS----#
reg = r"\w+(?:\.\w+)?|[^\s\w]?[\=\!]|\<?\-|\.{1,2}|[|&]+|[+\/*():\[\]\,\>\<\^]|\".*?\""
#----GLOBALS----#

#----UTILITIES----#
def PrintTokens(tokenArr):
    for i in tokenArr:
        print(f"Type: {i.token_type}\nStrrep: {i.strrep}")
#----UTILITIES----#

def Tokenize(fileHandle):
    buff = fileHandle.read()
    return re.findall(reg, buff)

def LexLine(ln):
    strTokens = re.findall(reg, ln)
    tokens = []

    for i in strTokens:
        tkType = DetermineToken(i)
        token = Token(tkType)

        for j in range(0, 3):
            if tkType == TokenType(j):
                token.strrep = str(i)

        tokens.append(token)

    return tokens

def LexFile(fileHandle):
    strTokens = Tokenize(fileHandle)
    tokens = []

    for i in strTokens:
        tokenType = DetermineToken(i)
        token = Token(tokenType)

        for j in range(0, 3):
            if tokenType == TokenType(j):
                token.strrep = str(i)

        tokens.append(token)

    return tokens
