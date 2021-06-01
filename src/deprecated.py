#Tuka slagame sichko deto she furlime v koshcheto na po-kusen etap
def GenerateRule(reservedSyms):
    finalRule = ""

    if isinstance(reservedSyms, list):
        for i in reservedSyms:
            finalRule += i + "|"

        finalRule = finalRule[:-1]
    else:
        finalRule = reservedSyms

    return finalRule

def LexSetup():
    rulesSrc = open(jsonDir, "r")
    rulesDc = json.loads(rulesSrc.read())["Rules"]

    allRules = [GenerateRule(rulesDc[x]) for x in rulesDc.keys()]

    rulesSrc.close()
    return GenerateRule(allRules)

def InputOutput():
    _type = None
    _param = None

    if CheckToken(token, TokenType.GETCHAR, TokenType.PUTCHAR):
        if CheckToken(token, TokenType.GETCHAR):
            _type = IOType.Stdin
            token.next()
        elif CheckToken(token, TokenType.PUTCHAR):
            token.next()

            _type = IOType.Stdout
            _param = Expression()

        token.next()
        return IONode(_type, _param)

    return None

#reg = r"\w+|[^\s\w]?[\=\!]|\<?\-|\.{1,2}|[+\/*()|:\[\]\,\>]|\".*?\""
#reg = r"\w+|[^\s\w]?[\=\!]|\<?\-|\.{1,2}|[|&]+|[+\/*():\[\]\,\>\<]|\".*?\""

#Should be called only once
#reg = LexSetup()

