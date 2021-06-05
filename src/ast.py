class FunctionNode:
    def __init__(self, ident, args, body, context = None, patterns = None):
        self.ident = ident              #String
        self.args = args                #[String]
        self.body = body                #BodyNode
        self.context = context          #Dict<String, FunctionNode>
        self.patterns = patterns        #FunctionNode

    def __repr__(self):
        return f"<Function reference - Identifier: {self.ident}>"

    @staticmethod
    def From(fNode):
        if not isinstance(fNode, FunctionNode):
            raise TypeError("fNode should be of type 'FunctionNode'")

        return FunctionNode(fNode.ident, fNode.args, fNode.body, fNode.context, fNode.patterns)

class PatternNode:
    def __init__(self, ident, pattern):
        self.ident = ident              #String
        self.pattern = pattern          #Dict<Tuple, BodyNode>

class ReferenceNode:
    def __init__(self, ident):
        self.ident = ident

class BodyNode:
    def __init__(self, isGuarded,  expr, guards):
        self.isGuarded = isGuarded      #Boolean
        self.expr = expr                #ExpressionNode
        self.guards = guards            #GuardNode

class GuardNode:
    def __init__(self, boolExpr, asgExpr, isOther = False):
        self.isotherwise = isOther      #Boolean
        self.boolExpr = boolExpr        #ExpressionNode
        self.asgExpr = asgExpr          #ExpressionNode

class ExpressionNode:
    def __init__(self, _type, expr):
        self.exprType = _type           #ExpressionType
        self.expr = expr

    def __repr__(self):
        return f"<Expression - Type: {self.exprType}>"

class ChainNode:
    def __init__(self, expr, nextNode):
        self.expr = expr                #ExpressionNode
        self.nextNode = nextNode        #ChainNode

#Only to be used in list comprehension, nowhere else.
class Assign2Node:
    def __init__(self, ident, ls):
        self.ident = ident              #String
        self.ls = ls                    #ListNode

class ValExprNode:
    def __init__(self, node_type, val, op = None, lBranch = None, rBranch = None):
        self.node_type = node_type      #NodeType
        self.op = op                    #/Operation/
        self.val = val                  #/Numeric type/, MutableNode or CallNode

        self.lBranch = lBranch          #ValExprNode
        self.rBranch = rBranch          #<--^

class CallNode:
    def __init__(self, ident, args):
        self.ident = ident              #String
        self.args = args                #List<ExpressionNode>

class ConditionalNode:
    def __init__(self, boolExpr, thenExpr, elseExpr):
        self.boolExpr = boolExpr        #ExpressionNode
        self.thenExpr = thenExpr        #ExpressionNode
        self.elseExpr = elseExpr        #ExpressionNode

class MutableNode:
    def __init__(self, mutype, string = "", ls = []):
        self.mutype = mutype            #MutableType
        self.string = string            #String
        self.ls = ls                    #ListNode

class ListNode:
    def __init__(self, lsType, seq, rng, compr):
        self.lsType = lsType            #ListType
        self.seq = seq                  #List<ExpressionNode>
        self.rng = rng                  #RangeNode
        self.compr = compr              #ComprehensionNode

class RangeNode:
    def __init__(self, begin, end):
        self.begin = begin              #ExpressionNode
        self.end = end                  #ExpressionNode

class ComprehensionNode:
    def __init__(self, baseExpr, symbols):
        self.baseExpr = baseExpr        #ExpressionNode
        self.symbols = symbols          #Dict<String, ListNode>
