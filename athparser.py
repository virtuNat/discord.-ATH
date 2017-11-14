import sys
from functools import partial, reduce

from lexer import Lexer, Token
from grafter import (
    Selector, ExprParser, StrictExpr,
    TokenGrafter, TagGrafter,
    EnsureGraft, Repeater,
    LazyGrafter, StrictGrafter,
    )
from athast import (
    AthSymbol, SymbolError, EndTilDeath,
    IntExpr, FloatExpr, StringExpr, VarExpr,
    NotExpr, UnaryArithExpr, BinaryExpr,
    TernaryExpr, Serialize,

    InputStmt, PrintFunc, KillFunc,
    BifurcateStmt, AggregateStmt,
    ProcreateStmt, ReplicateStmt,
    FabricateStmt, ExecuteStmt, DivulgateStmt,
    DebateStmt, UnlessStmt, TildeAthLoop,
    )


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
    (r'\+', 'BUILTIN'), # Add, UnaryPos
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
    (r'~ATH', 'BUILTIN'), # Loop
    (r'print', 'BUILTIN'), # Output
    (r'input', 'BUILTIN'), # Input
    (r'import', 'BUILTIN'), # Import another file
    (r'DEBATE', 'BUILTIN'), # Conditional Consequent
    (r'UNLESS', 'BUILTIN'), # Conditional Alternative
    (r'EXECUTE', 'BUILTIN'), # Subroutine execution
    (r'DIVULGATE', 'BUILTIN'), # Return a symbol
    (r'FABRICATE', 'BUILTIN'), # Subroutine declaration
    (r'PROCREATE', 'BUILTIN'), # Value declaration
    (r'REPLICATE', 'BUILTIN'), # Deep copy
    (r'BIFURCATE', 'BUILTIN'), # Split a symbol
    (r'AGGREGATE', 'BUILTIN'), # Merge a symbol
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


strparser = TagGrafter('STRING') ^ (lambda s: StringExpr(s[1:-1]))
fltparser = TagGrafter('FLOAT') ^ FloatExpr
intparser = TagGrafter('INT') ^ IntExpr
nameparser = TagGrafter('SYMBOL') ^ VarExpr


def bltinparser(token):
    """Parses builtin tokens."""
    return TokenGrafter(token, 'BUILTIN')


def ternaryexprparser(term):
    def breakdown(tokens):
        trueexpr, _, cond, _, falseexpr = tokens
        return TernaryExpr(truexpr, cond, falseexpr)
    return (
        term
        + bltinparser('DEBATE')
        + term
        + bltinparser('UNLESS')
        + term
        ^ breakdown
        )


def execexpr():
    """Parses the execution statement as an expression."""
    def breakdown(tokens):
        return ExecuteStmt(tokens[2])
    return (
        bltinparser('EXECUTE')
        + bltinparser('(')
        + callparser()
        + bltinparser(')')
        ^ breakdown
        )


def exprgrpparser():
    """Parses expression groups."""
    def breakdown(tokens):
        return tokens[1]
    return (
        bltinparser('(')
        + LazyGrafter(exprparser)
        + bltinparser(')')
        ^ breakdown
        )


def exprvalparser():
    """Parses expression primitives."""
    return (
        fltparser
        | intparser
        | nameparser
        | LazyGrafter(execexpr)
        # | LazyGrafter(unaryexprparser)
        )


def unaryexprparser():
    term = exprgrpparser() | exprvalparser()
    ops = bltinparser('+') | bltinparser('-') | bltinparser('~')
    return ops + term ^ (lambda _: UnaryArithExpr)


def exprparser():
    """Parses an expression."""
    def parse_ops(op_level):
        ops = reduce(Selector, map(bltinparser, op_level))
        return ops ^ (lambda op: lambda l, r: BinaryExpr(op, l, r))
    op_order = [
        ('**',),
        ('*', '/', '/_', '%'),
        ('+', '-'),
        ('<<', '>>'),
        ('&',), ('|',), ('^',),
        ('<', '<=', '>', '>=', '==', '~='),
        ('&&',), ('||',), ('^^',),
        ('!=!', '!=?', '?=!', '~=!', '!=~', '~=~')
        ]
    term = exprvalparser() | exprgrpparser()
    return reduce(StrictExpr, [term] + [parse_ops(lvl) for lvl in op_order])
# print(exprparser())

def callparser():
    """Parses a group of expressions."""
    def cull_seps(graft):
        return graft[0] or graft[1]
    term = (strparser | exprparser())
    return Repeater(term + EnsureGraft(bltinparser(',')) ^ cull_seps)


def tildeath():
    """Parses ~ATH loops."""
    def breakdown(tokens):
        _, _, graveexpr, _, _, body, _ = tokens
        return TildeAthLoop(graveexpr, body)
    return (
        bltinparser('~ATH')
        + bltinparser('(')
        + exprparser()
        + bltinparser(')')
        + bltinparser('{')
        + LazyGrafter(stmtparser)
        + bltinparser('}')
        ^ breakdown
        )


def condistmt(fabri=False):
    """Parses conditional statements."""
    def brkunless(tokens):
        _, condexpr, _, body, _ = tokens
        if condexpr:
            condexpr = condexpr[1]
        return UnlessStmt(condexpr, body)
    def breakdown(tokens):
        _, _, condexpr, _, _, body, _, unlesses = tokens
        return DebateStmt(condexpr, body, unlesses)
    stmts = funcstmts if fabri else stmtparser

    return (
        bltinparser('DEBATE')
        + bltinparser('(')
        + exprparser()
        + bltinparser(')')
        + bltinparser('{')
        + LazyGrafter(stmts)
        + bltinparser('}')
        + EnsureGraft(
            Repeater(
                bltinparser('UNLESS')
                + EnsureGraft(
                    bltinparser('(')
                    + exprparser()
                    + bltinparser(')')
                    )
                + bltinparser('{')
                + LazyGrafter(stmts)
                + bltinparser('}')
                ^ brkunless
                )
            )
        ^ breakdown
        )


def execfunc():
    """Parses the execution statement as a statement."""
    def breakdown(tokens):
        return ExecuteStmt(tokens[2])
    return (
        bltinparser('EXECUTE')
        + bltinparser('(')
        + callparser()
        + bltinparser(')')
        + bltinparser(';')
        ^ breakdown
        )


def divlgstmt():
    """Parses the return statement."""
    def breakdown(tokens):
        return DivulgateStmt(tokens[1])
    return (
        bltinparser('DIVULGATE')
        + exprparser()
        + bltinparser(';')
        ^ breakdown
        )


def inputstmt():
    """Parses the input statement."""
    def breakdown(tokens):
        _, name, prompt, _ = tokens
        return InputStmt(name, prompt)
    return (
        bltinparser('input')
        + nameparser
        + EnsureGraft(
            strparser
            | fltparser
            | intparser
            | nameparser
            | exprgrpparser()
            )
        + bltinparser(';')
        ^ breakdown
        )


def printfunc():
    """Parses the print function."""
    def breakdown(tokens):
        return PrintFunc(tokens[2])
    return (
        bltinparser('print')
        + bltinparser('(')
        + callparser()
        + bltinparser(')')
        + bltinparser(';')
        ^ breakdown
        )


def killfunc():
    """Parses the kill function."""
    def breakdown(tokens):
        name, _, _, _, args, _, _ = tokens
        return KillFunc(name, args)
    return (
        nameparser
        + bltinparser('.')
        + bltinparser('DIE')
        + bltinparser('(')
        + LazyGrafter(callparser)
        + bltinparser(')')
        + bltinparser(';')
        ^ breakdown
        )


def fabristmt():
    """Parses function declarations."""
    def cull_seps(graft):
        return graft[0] or graft[1]
    argparser = Repeater(nameparser + EnsureGraft(bltinparser(',')) ^ cull_seps)

    def breakdown(tokens):
        _, name, _, args, _, _, body, _ = tokens
        return FabricateStmt(name, args, body)

    return (
        bltinparser('FABRICATE')
        + nameparser
        + bltinparser('(')
        + EnsureGraft(argparser)
        + bltinparser(')')
        + bltinparser('{')
        + LazyGrafter(funcstmts)
        + bltinparser('}')
        ^ breakdown
        )


def procrstmt():
    """Parses value declarations."""
    def breakdown(tokens):
        _, name, expr, _ = tokens
        if not expr:
            expr = VarExpr('NULL')
        return ProcreateStmt(name, expr)
    return (
        bltinparser('PROCREATE')
        + nameparser
        + EnsureGraft(exprparser())
        + bltinparser(';')
        ^ breakdown
        )


def replistmt():
    """Parses the assignment statement."""
    def breakdown(tokens):
        _, name, expr, _ = tokens
        return ReplicateStmt(name, expr)
    return (
        bltinparser('REPLICATE')
        + nameparser
        + (exprgrpparser() | exprvalparser())
        + bltinparser(';')
        ^ breakdown)


def bfctstmt():
    """Parses the bifurcate statement."""
    def breakdown(tokens):
        _, name, _, lname, _, rname, _, _ = tokens
        return BifurcateStmt(name, lname, rname)
    return (
        bltinparser('BIFURCATE')
        + nameparser
        + bltinparser('[')
        + nameparser
        + bltinparser(',')
        + nameparser
        + bltinparser(']')
        + bltinparser(';')
        ^ breakdown
        )


def aggrstmt():
    """Parses the aggregate statement."""
    def breakdown(tokens):
        _, _, lname, _, rname, _, name, _ = tokens
        return AggregateStmt(lname, rname, name)
    return (
        bltinparser('AGGREGATE')
        + bltinparser('[')
        + exprparser()
        + bltinparser(',')
        + exprparser()
        + bltinparser(']')
        + nameparser
        + bltinparser(';')
        ^ breakdown
        )


def funcstmts():
    """Parses the set of statements used in functions."""
    return Repeater(
        replistmt()
        | procrstmt()
        | bfctstmt()
        | aggrstmt()
        | killfunc()
        | execfunc()
        | printfunc()
        | inputstmt()
        | tildeath()
        | LazyGrafter(fabristmt)
        | condistmt(True)
        | divlgstmt()
        ) ^ Serialize


def stmtparser():
    """Parses the set of statements used top-level."""
    stmts = (
        replistmt()
        | procrstmt()
        | bfctstmt()
        | aggrstmt()
        | killfunc()
        | execfunc()
        | printfunc()
        | inputstmt()
        | tildeath()
        | fabristmt()
        | condistmt()
        )
    return Repeater(stmts) ^ Serialize
# print(stmtparser())

def echo_error(msg):
    sys.stderr.write(msg)
    sys.exit(1)


class BuiltinSymbol(AthSymbol):
    __slots__ = ()

    def assign_left(self, value):
        echo_error('SymbolError: Builtins cannot be assigned to!')

    def assign_right(self, value):
        echo_error('SymbolError: Builtins cannot be assigned to!')

    def inop(self, other, op):
        echo_error('SymbolError: Builtins cannot be assigned to!')


class AthStackFrame(object):
    """Keeps a record of all symbols declared in a given scope.
    ~ATH implements dynamic scope, so be wary when coding in it!
    """
    __slots__ = ('scope_vars',)

    def __init__(self):
        self.scope_vars = {}

    def __getitem__(self, name):
        try:
            return self.scope_vars[name]
        except KeyError:
            return None

    def __setitem__(self, name, value=None):
        if value is None:
            value = AthSymbol(True)
        self.scope_vars[name] = value


class TildeAthInterp(object):
    """This is supposed to be a Finite State Machine"""
    __slots__ = ()
    global_vars = {
        'THIS': BuiltinSymbol(),
        'NULL': BuiltinSymbol(False),
        'DIE': BuiltinSymbol(),
        'ATH': BuiltinSymbol(),
        'print': BuiltinSymbol(),
        'input': BuiltinSymbol(),
        'import': BuiltinSymbol(),
        'DEBATE': BuiltinSymbol(),
        'UNLESS': BuiltinSymbol(),
        'EXECUTE': BuiltinSymbol(),
        'DIVULGATE': BuiltinSymbol(),
        'FABRICATE': BuiltinSymbol(),
        'REPLICATE': BuiltinSymbol(),
        'PROCREATE': BuiltinSymbol(),
        'BIFURCATE': BuiltinSymbol(),
        'AGGREGATE': BuiltinSymbol(),
        }
    stack = []
    script_parser = StrictGrafter(stmtparser())

    def lookup_name(self, name):
        for frame in reversed(self.stack):
            value = frame[name]
            if value is not None:
                # print('{} found'.format(name))
                return value
        try:
            return self.global_vars[name]
        except KeyError:
            raise NameError('Symbol {} not found'.format(name))

    def assign_name(self, name, value):
        # print('{} assigned'.format(name))
        try:
            symbol = self.lookup_name(name)
        except NameError:
            self.create_name(name, value)
        else:
            if not isinstance(symbol, BuiltinSymbol):
                self.global_vars[name] = value
            else:
                raise SymbolError('builtins can\'t be assigned to!')

    def create_name(self, name, value):
        if not len(self.stack):
            self.global_vars[name] = value
        else:
            self.stack[-1][name] = value

    def push_stack(self, init_dict={}):
        newframe = AthStackFrame()
        newframe.scope_vars.update(init_dict)
        self.stack.append(newframe)

    def pop_stack(self):
        if len(self.stack):
            return self.stack.pop()
        else:
            raise RuntimeError('Stack is already empty, dingus!')

    def execute(self, script):
        while True:
            try:
                script.eval(self)
            except EndTilDeath:
                sys.exit(0)
            finally:
                print(self.global_vars)
                for frame in self.stack:
                    print(frame.scope_vars)

    def interpret(self, fname):
        if not fname.endswith('~ATH'):
            echo_error('IOError: script must be a ~ATH file')
        with open(fname, 'r') as script_file:
            script = script_file.read()
        tokens = ath_lexer.lex(script)
        result = self.script_parser(tokens, 0)
        if result:
            with open(fname[:-4]+'py', 'w') as py_file:
                py_file.write('#!/usr/bin/env python\nfrom athast import *\n')
                py_file.write('from athparser import TildeAthInterp\n\n')
                py_file.write('ath_script = ' + repr(result.value))
                py_file.write('\nTildeAthInterp().execute(ath_script)\n')
            self.execute(result.value)
        else:
            echo_error('RuntimeError: the parser could not understand the script')
