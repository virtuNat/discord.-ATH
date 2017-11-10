import inspect
from functools import reduce

from lexer import Lexer, Token

from grafter import Selector, ExprParser
from grafter import TokenGrafter, TagGrafter
from grafter import EnsureGraft, Repeater
from grafter import LazyGrafter, StrictGrafter

from athast import AthSymbol, SymbolError
from athast import IntExpr, FloatExpr, StringExpr, VarExpr
from athast import Serialize
from athast import BinaryArithExpr

from athast import InputStmt, PrintFunc
from athast import BifurcateStmt, AggregateStmt
from athast import ProcreateStmt, ReplicateStmt
from athast import TildeAthLoop, KillFunc


ath_lexer = Lexer([
    (r'(?s)/\*.*?\*/', None), # Multi-line comment
    (r'//[^\n]*', None), # Single-line comment
    (r'\s+', None), # Whitespace
    # Code enclosures
    (r'\(', 'BUILTIN'), # Conditional/Call open
    (r'\)', 'BUILTIN'), # Conditional/Call close
    (r'{', 'BUILTIN'), # Suite open
    (r'}', 'BUILTIN'), # Suite close
    (r'\[', 'BUILTIN'), # Symbol slice open
    (r'\]', 'BUILTIN'), # Symbol slice close
    # Separators
    (r';', 'BUILTIN'), # Statement separator
    (r'\.', 'BUILTIN'), # Lookup operator
    (r',', 'BUILTIN'), # Group operator
    # Arithmetic in-place operators
    (r'\+=', 'BUILTIN'), # Add
    (r'-=', 'BUILTIN'), # Sub
    (r'\*\*=', 'BUILTIN'), # Pow
    (r'\*=', 'BUILTIN'), # Mul
    (r'/_=', 'BUILTIN'), # FloorDiv
    (r'/=', 'BUILTIN'), # TrueDiv
    (r'%=', 'BUILTIN'), # Modulo
    # Arithmetic operators
    (r'\+', 'BUILTIN'), # Add, UnaryAbs
    (r'-', 'BUILTIN'), # Sub, UnaryInv
    (r'\*\*', 'BUILTIN'), # Pow
    (r'\*', 'BUILTIN'), # Mul
    (r'/_', 'BUILTIN'), # FloorDiv
    (r'/', 'BUILTIN'), # TrueDiv
    (r'%', 'BUILTIN'), # Modulo
    # Symbol operators
    (r'!=!', 'BUILTIN'), # Assert Both
    (r'!=\?', 'BUILTIN'), # Assert Left
    (r'\?=!', 'BUILTIN'), # Assert Right
    (r'~=!', 'BUILTIN'), # Negate Left
    (r'!=~', 'BUILTIN'), # Negate Right
    (r'~=~', 'BUILTIN'), # Negate Both
    # Bitwise shift in-place operators
    (r'<<=', 'BUILTIN'), # Bitwise lshift
    (r'>>=', 'BUILTIN'), # Bitwise rshift
    # Bitwise shift operators
    (r'<<', 'BUILTIN'), # Bitwise lshift
    (r'>>', 'BUILTIN'), # Bitwise rshift
    # Value operators
    (r'<=', 'BUILTIN'), # Less than or equal to
    (r'<', 'BUILTIN'), # Less than
    (r'>=', 'BUILTIN'), # Greater than or equal to
    (r'>', 'BUILTIN'), # Greater than
    (r'~=', 'BUILTIN'), # Not equal to
    (r'==', 'BUILTIN'), # Equal to
    # Boolean operators
    (r'&&', 'BUILTIN'), # Boolean AND
    (r'\|\|', 'BUILTIN'), # Boolean OR
    (r'\^\^', 'BUILTIN'), # Boolean XOR
    (r'!', 'BUILTIN'), # Boolean NOT
    # Statement keywords
    (r'DIE', 'BUILTIN'), # Kill symbol
    (r'WHEN', 'BUILTIN'), # Conditional Consequent
    (r'UNLESS', 'BUILTIN'), # Conditional Alternative
    (r'~ATH', 'BUILTIN'), # Loop
    (r'print', 'BUILTIN'), # Output
    (r'input', 'BUILTIN'), # Input
    (r'import', 'BUILTIN'), # Import another file
    (r'EXECUTE', 'BUILTIN'), # Subroutine execution
    (r'DIVULGATE', 'BUILTIN'), # Return a symbol
    (r'BIFURCATE', 'BUILTIN'), # Split a symbol
    (r'AGGREGATE', 'BUILTIN'), # Merge a symbol
    (r'PROCREATE', 'BUILTIN'), # Value declaration
    (r'FABRICATE', 'BUILTIN'), # Subroutine declaration
    (r'REPLICATE', 'BUILTIN'), # Two-level copy
    # Bitwise in-place operators
    (r'&=', 'BUILTIN'), # Bitwise and
    (r'\|=', 'BUILTIN'), # Bitwise or
    (r'\^=', 'BUILTIN'), # Bitwise xor
    # Bitwise operators
    (r'&', 'BUILTIN'), # Bitwise and
    (r'\|', 'BUILTIN'), # Bitwise or
    (r'\^', 'BUILTIN'), # Bitwise xor
    (r'~', 'BUILTIN'), # Bitwise not
    # Other identifiers
    (r'([\'"])[^\1]*?\1', 'STRING'),
    (r'(\d+\.(\d*)?|\.\d+)([eE][-+]?\d+)?', 'FLOAT'),
    (r'\d+', 'INT'),
    (r'[a-zA-Z]\w*', 'SYMBOL'),
])


strparser = TagGrafter('STRING') ^ StringExpr
fltparser = TagGrafter('FLOAT') ^ FloatExpr
intparser = TagGrafter('INT') ^ IntExpr
nameparser = TagGrafter('SYMBOL') ^ VarExpr


def bltinparser(token):
    return TokenGrafter(token, 'BUILTIN')


def break_group(tokens):
    _, expr, _ = tokens
    return expr


def operatorparser(op_list, grafter, evaluator):
    def parse_ops(op_level):
        ops = reduce(Selector, map(bltinparser, op_level))
        return ops ^ evaluator
    return reduce(ExprParser, [grafter] + [parse_ops(lvl) for lvl in op_list])


def arithexprparser():
    value = (
        fltparser
        | intparser
        | nameparser
        )
    group = (
        bltinparser('(')
        + LazyGrafter(arithexprparser)
        + bltinparser(')')
        ^ break_group
        )
    term = value | group
    op_order = [
        ('**',),
        ('*', '/', '/_', '%'),
        ('+', '-'),
        ('<<', '>>'),
        ('&',),
        ('|',),
        ('^',),
        ]
    return operatorparser(op_order, term, lambda op: lambda l, r: BinaryArithExpr(op, l, r))


def groupparser():
    def cull_seps(graft):
        return graft[0] or graft[1]
    term = (strparser | arithexprparser())
    return Repeater(term + EnsureGraft(bltinparser(',')) ^ cull_seps)


def procrstmt():
    def breakdown(tokens):
        _, name, expr = tokens
        return ProcreateStmt(name, expr)
    return bltinparser('PROCREATE') + nameparser + arithexprparser() ^ breakdown


def replistmt():
    def breakdown(tokens):
        _, name, expr = tokens
        return ReplicateStmt(name, expr)
    return bltinparser('REPLICATE') + nameparser + arithexprparser() ^ breakdown


def inputstmt():
    def breakdown(tokens):
        _, name, prompt = tokens
        return InputStmt(name, prompt)
    return bltinparser('input') + nameparser + strparser ^ breakdown


def printfunc():
    def breakdown(tokens):
        return PrintFunc(tokens[2])
    return (
        bltinparser('print')
        + bltinparser('(')
        + groupparser()
        + bltinparser(')')
        ^ breakdown
        )


def killfunc():
    def breakdown(tokens):
        return KillFunc(tokens[0], tokens[4])
    return (
        nameparser
        + bltinparser('.')
        + bltinparser('DIE')
        + bltinparser('(')
        + groupparser()
        + bltinparser(')')
        ^ breakdown
        )


def bfctstmt():
    def breakdown(tokens):
        _, name, _, lname, _, rname, _ = tokens
        return BifurcateStmt(name, lname, rname)
    return (
        bltinparser('BIFURCATE')
        + nameparser
        + bltinparser('[')
        + nameparser
        + bltinparser(',')
        + nameparser
        + bltinparser(']')
        ^ breakdown
        )


def aggrstmt():
    def breakdown(tokens):
        _, _, lname, _, rname, _, name = tokens
        return AggregateStmt(lname, rname, name)
    return (
        bltinparser('AGGREGATE')
        + bltinparser('[')
        + nameparser
        + bltinparser(',')
        + nameparser
        + bltinparser(']')
        + nameparser
        ^ breakdown
        )


def tildeath():
    def breakdown(tokens):
        _, _, graveexpr, _, _, body, _ = tokens
        return TildeAthLoop(graveexpr, body)
    return (
        bltinparser('~ATH')
        + bltinparser('(')
        + arithexprparser()
        + bltinparser(')')
        + bltinparser('{')
        + LazyGrafter(stmtparser)
        + bltinparser('}')
        ^ breakdown
        )


def stmtparser():
    stmts = (
        procrstmt()
        | replistmt()
        | inputstmt()
        | printfunc()
        | killfunc()
        | bfctstmt()
        | aggrstmt()
        | tildeath()
        )
    stmt_grp = bltinparser(';') ^ (lambda _: Serialize)
    return stmts * stmt_grp # * brace_grp


class BuiltinSymbol(AthSymbol):
    __slots__ = ()

    def assign_left(self, value):
        raise SymbolError('Builtins cannot be assigned to!')

    def assign_right(self, value):
        raise SymbolError('Builtins cannot be assigned to!')


class AthStackFrame(object):
    """Keeps a record of all symbols declared in a given scope.
    ~ATH implements dynamic scope, so be wary when coding in it!
    """
    __slots__ = ()
    global_vars = {
        'DIE': BuiltinSymbol(),
        'WHEN': BuiltinSymbol(),
        'UNLESS': BuiltinSymbol(),
        'ATH': BuiltinSymbol(),
        'print': BuiltinSymbol(),
        'input': BuiltinSymbol(),
        'import': BuiltinSymbol(),
        'EXECUTE': BuiltinSymbol(),
        'DIVULGATE': BuiltinSymbol(),
        'BIFURCATE': BuiltinSymbol(),
        'AGGREGATE': BuiltinSymbol(),
        'PROCREATE': BuiltinSymbol(),
        'FABRICATE': BuiltinSymbol(),
        'REPLICATE': BuiltinSymbol(),
        'THIS': BuiltinSymbol(),
        'NULL': BuiltinSymbol(False),
        }
    scope_vars = {}

    def __getitem__(self, name):
        try:
            return self.scope_vars[name]
        except KeyError:
            return None

    def __setitem__(self, name, value=None):
        try:
            self.global_vars[name]
        except KeyError:
            pass
        else:
            raise SymbolError('Builtins cannot be assigned to!')

        if value is None:
            value = AthSymbol(True)
        self.scope_vars[name] = value


class TildeAthInterp(object):
    """This is supposed to be a Finite State Machine"""
    __slots__ = ()
    stack = [AthStackFrame()]
    script_parser = StrictGrafter(stmtparser())

    def lookup_name(self, name):
        try:
            return self.stack[0].global_vars[name]
        except KeyError:
            pass
        for frame in reversed(self.stack):
            value = frame[name]
            if value:
                # print('{} found'.format(name))
                return value
        raise NameError('Symbol {} does not exist.'.format(name)) 

    def assign_name(self, name, value):
        # print('{} assigned'.format(name))
        self.stack[-1][name] = value

    def push_stack(self):
        self.stack.append(AthStackFrame())

    def pop_stack(self):
        if len(self.stack) > 1:
            return self.stack.pop()
        else:
            raise RuntimeError('May not pop global stack')

    def execute(self, script):
        tokens = ath_lexer.lex(script)
        for i in reversed(range(len(tokens))):
            if tokens[i].token == '}':
                if i == len(tokens) - 1:
                    tokens.append(Token(';', 'BUILTIN', tokens[i].line))
                elif tokens[i + 1].token != ';':
                    tokens.insert(i + 1, Token(';', 'BUILTIN', tokens[i].line))
        result = self.script_parser(tokens, 0)
        if result:
            result.value.eval(self)
            for frame in self.stack:
                print(frame.scope_vars)
        else:
            raise RuntimeError('Something messed up!')
