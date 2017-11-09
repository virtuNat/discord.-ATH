import inspect
from functools import reduce

from lexer import Lexer

from athast import AthSymbol, SymbolError
from athast import IntExpr, FloatExpr, StringExpr
from athast import Serialize
from athast import BinaryArithExpr
from athast import ProcreateStmt, InputStmt
from athast import PrintFunc

from grafter import Selector, ExprParser
from grafter import TokenGrafter, TagGrafter
from grafter import EnsureGraft, Repeater
from grafter import LazyGrafter, StrictGrafter


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
    (r'~~', 'BUILTIN'), # Boolean NOT
    # Statement keywords
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
fltparser = TagGrafter('FLOAT') ^ (lambda x: FloatExpr(float(x)))
intparser = TagGrafter('INT') ^ (lambda x: IntExpr(int(x)))
nameparser = TagGrafter('SYMBOL')


def bltinparser(token):
    return TokenGrafter(token, 'BUILTIN')


def break_group(ast):
    ((_, expr), _) = ast
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
    return operatorparser(op_order, term, BinaryArithExpr)


def groupparser():
    def cull_seps(graft):
        return graft[0] or graft[1]
    term = (
        strparser
        | fltparser
        | intparser
        | nameparser
        | arithexprparser()
        )
    return Repeater(term + EnsureGraft(bltinparser(';')) ^ cull_seps)


def procrstmt():
    def breakdown(ast):
        ((_, name), expr) = ast
        return ProcreateStmt(name, expr)
    return bltinparser('PROCREATE') + nameparser + arithexprparser() ^ breakdown


def inputstmt():
    def breakdown(ast):
        ((_, name), prompt) = ast
        return InputStmt(name, prompt)
    return bltinparser('input') + nameparser + strparser ^ breakdown


def printfunc():
    def breakdown(ast):
        ((_, args), _) = ast
        return PrintFunc(args)
    return (
        bltinparser('print')
        + bltinparser('(')
        + groupparser()
        + bltinparser(')')
        ^ breakdown
        )


def stmtparser():
    statements = (
        procrstmt()
        | inputstmt()
        | printfunc()
        )
    series_grouper = bltinparser(',') ^ (lambda _: Serialize)
    return statements * series_grouper


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
    scope_vars = {}

    def __init__(self, builtins=None):
        if builtins:
            self.scope_vars = builtins

    def __getitem__(self, name):
        try:
            return self.scope_vars[name]
        except KeyError:
            return None

    def __setitem__(self, name, value=None):
        try:
            oldval = self.scope_vars[name]
        except KeyError:
            pass
        else:
            if isinstance(oldval, BuiltinSymbol):
                raise SymbolError('Builtins cannot be assigned to!')

        if value is None:
            value = AthSymbol(True)
        self.scope_vars[name] = value


class TildeAthInterp(object):
    """This is supposed to be a Finite State Machine"""
    __slots__ = ()

    stack = [
        AthStackFrame({
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
            })
        ]

    def lookup_name(self, name):
        for frame in reversed(self.stack):
            value = frame[name]
            if value:
                return value
        raise NameError('Symbol {} does not exist.'.format(name))

    def assign_name(self, name, value):
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
        script_parser = StrictGrafter(stmtparser())
        result = script_parser(tokens, 0)
        result.value.eval(self)
