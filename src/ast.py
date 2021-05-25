class FunctionNode:
    def __init__(self, ident, args, body, context, parCont, patterns):
        self.ident = ident              #String
        self.args = args                #[String]
        self.body = body                #BodyNode
        self.context = context          #Dict<String, FunctionNode>
        self.parentCont = parCont       #Dict<String, FunctionNode>
        self.patterns = patterns        #FunctionNode

class PatternNode:
    def __init__(self, ident, args, body):
        self.ident = ident              #String
        self.args = args                #ExpressionNode
        self.body = body                #BodyNode

class IONode:
    def __init__(self, IOTp, param = None):
        self.IOTp = IOTp                #IOType
        self.param = param              #ExpressionNode

class BodyNode:
    def __init__(self, isGuarded,  expr, guards):
        self.isGuarded                  #Boolean
        self.expr = expr                #ExpressionNode
        self.guards = guards            #GuardNode

class GuardNode:
    def __init__(self, bool_expr, asg_expr):
        self.boolExpr = boolExpr        #ExpressionNode
        self.asgExpr = asgExpr          #ExpressionNode

class ExpressionNode:
    def __init__(self, valexpr, _tuple, mutable, ifThenElse, IO):
        self.valexpr = valexpr          #ValExprNode
        self._tuple = _tuple            #TupleNode
        self.mutable = mutable          #MutableNode
        self.ifThenElse = ifThenElse    #ConditionalNode
        self.IO = IO                    #IONode

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
        self.args = args                #ExpressionNode

class ConditionalNode:
    def __init__(self, boolExpr, thenExpr, elseExpr):
        self.boolExpr = boolExpr        #ExpressionNode
        self.thenExpr = thenExpr        #ExpressionNode
        self.elseExpr = elseExpr        #ExpressionNode

class TupleNode:
    def __init__(self, members):
        self.members = members          #List<ExpressionNode>

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
