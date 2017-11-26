"""The ~ATH interpreter.

This contains the token regex list used by the lexer and all
the parser builders used to build the parser that creates the
abstract syntax tree.
"""
from functools import partial, reduce

from lexer import Lexer
from grafter import (
    Selector, ExprParser, StrictExpr,
    TokenGrafter, TagGrafter,
    EnsureGraft, Repeater,
    LazyGrafter, StrictGrafter,
    )
from athast import (
    IntExpr, FloatExpr, StringExpr, VarExpr,
    UnaryArithExpr, BinaryExpr,
    Serialize, InspectStack,

    ImportStmt, InputStmt, PrintFunc, KillFunc,
    BifurcateStmt, AggregateStmt, EnumerateStmt,
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
    (r'INSPECT', 'BUILTIN'), # Debug
    (r'DEBATE', 'BUILTIN'), # Conditional Consequent
    (r'UNLESS', 'BUILTIN'), # Conditional Alternative
    (r'EXECUTE', 'BUILTIN'), # Subroutine execution
    (r'DIVULGATE', 'BUILTIN'), # Return a symbol
    (r'FABRICATE', 'BUILTIN'), # Subroutine declaration
    (r'PROCREATE', 'BUILTIN'), # Value declaration
    (r'REPLICATE', 'BUILTIN'), # Deep copy
    (r'BIFURCATE', 'BUILTIN'), # Split a symbol
    (r'AGGREGATE', 'BUILTIN'), # Merge a symbol
    (r'ENUMERATE', 'BUILTIN'), # Merge a string
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

# Value/variable token primitives
fltparser = TagGrafter('FLOAT') ^ FloatExpr
intparser = TagGrafter('INT') ^ IntExpr
nameparser = TagGrafter('SYMBOL') ^ VarExpr
strparser = TagGrafter('STRING') ^ (lambda s: StringExpr(s[1:-1]))

# Builtin primitive
def bltinparser(token):
    """Parses builtin tokens."""
    return TokenGrafter(token, 'BUILTIN')

# Expresssions
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


def exprvalparser():
    """Parses expression primitives."""
    return (
        LazyGrafter(execexpr)
        | LazyGrafter(unaryexprparser)
        | nameparser
        | fltparser
        | intparser
        | strparser
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


def unaryexprparser():
    """Parses unary expressions."""
    term = exprvalparser() | exprgrpparser()
    ops = bltinparser('+') | bltinparser('-') | bltinparser('~') | bltinparser('!')
    return ops + term ^ (lambda e: UnaryArithExpr(*e))


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


def callparser():
    """Parses a group of expressions."""
    def cull_seps(graft):
        return graft[0] or graft[1]
    return Repeater(exprparser() + EnsureGraft(bltinparser(',')) ^ cull_seps)

# Statements
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


def procrstmt():
    """Parses value declarations."""
    def breakdown(tokens):
        _, name, expr, _ = tokens
        return ProcreateStmt(name, expr)
    return (
        bltinparser('PROCREATE')
        + nameparser
        + EnsureGraft(exprparser())
        + bltinparser(';')
        ^ breakdown
        )


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


def enumstmt():
    """Parses the enumerate statement."""
    def breakdown(tokens):
        _, string, stack, _ = tokens
        return EnumerateStmt(string, stack)
    return (
        bltinparser('ENUMERATE')
        + EnsureGraft(exprvalparser() | exprgrpparser())
        + nameparser
        + bltinparser(';')
        ^ breakdown
        )


def importstmt():
    """Parses the import statement."""
    def breakdown(tokens):
        _, module, alias, _ = tokens
        return ImportStmt(module, alias)
    return (
        bltinparser('import')
        + nameparser
        + nameparser
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
        + EnsureGraft(exprvalparser() | exprgrpparser())
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


def inspstmt():
    def breakdown(tokens):
        return InspectStack(tokens[2])
    return(
        bltinparser('INSPECT')
        + bltinparser('(')
        + LazyGrafter(callparser)
        + bltinparser(')')
        + bltinparser(';')
        ^ breakdown
        )


def funcstmts():
    """Parses the set of statements used in functions."""
    return Repeater(
        replistmt() # assignment
        | procrstmt() # val dec
        | bfctstmt() # obtain ptrs
        | aggrstmt() # stack ptrs
        | enumstmt() # split str
        | importstmt() # imports
        | inputstmt() # input
        | printfunc() # output
        | killfunc() # kill ctrl
        | execfunc() # run func
        | divlgstmt() # return
        | LazyGrafter(fabristmt) # func dec
        | tildeath() # cond loop
        | condistmt(True) # conditionals
        | inspstmt() # Debug, remove
        ) ^ Serialize


def stmtparser():
    """Parses the set of statements used top-level."""
    return Repeater(
        replistmt() # assignment
        | procrstmt() # val dec
        | bfctstmt() # obtain ptrs
        | aggrstmt() # stack ptrs
        | enumstmt() # split str
        | importstmt() # imports
        | inputstmt() # input
        | printfunc() # output
        | killfunc() # kill ctrl
        | execfunc() # run func
        | fabristmt() # func dec
        | tildeath() # cond loop
        | condistmt() # conditionals
        | inspstmt() # Debug, remove
        ) ^ Serialize
ath_parser = StrictGrafter(stmtparser())
