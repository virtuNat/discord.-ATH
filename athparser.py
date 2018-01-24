"""The ~ATH interpreter.

This contains the token regex list used by the lexer and all
the parser builders used to build the parser that creates the
abstract syntax tree.
"""
from functools import partial, reduce

from lexer import Lexer
from grafter import (
    ItemParser, TagsParser,
    SelectParser, StrictParser,
    OptionParser, RepeatParser,
    LazierParser, ScriptParser,
    )
from athast import (
    IntExpr, FloatExpr, StringExpr, VarExpr,
    UnaryExpr, BinaryExpr,
    AthAstList, InspectStack,

    ImportStmt, InputStmt, PrintStmt, KillStmt,
    BifurcateStmt, AggregateStmt, EnumerateStmt,
    ProcreateStmt, PropagateStmt, ReplicateStmt,
    FabricateStmt, ExecuteStmt, DivulgateStmt,
    DebateStmt, UnlessStmt, TildeAthLoop,
    )


ath_lexer = Lexer([
    (r'(?s)/\*.*?\*/', None), # Multi-line comment
    (r'//[^\n]*', None), # Single-line comment
    (r'\s+', None), # Whitespace
    # Code enclosures
    (r'\(', 'BUILTIN'), # Group open
    (r'\)', 'BUILTIN'), # Group close
    (r'{', 'BUILTIN'), # Suite open
    (r'}', 'BUILTIN'), # Suite close
    (r'\[', 'BUILTIN'), # Value reference open
    (r'\]', 'BUILTIN'), # Value reference close
    # Separators
    (r';', 'BUILTIN'), # Statement separator
    (r',', 'BUILTIN'), # Group operator
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
    # (r'PROPAGATE', 'BUILTIN'), # Reference copy
    (r'REPLICATE', 'BUILTIN'), # Deep copy
    (r'BIFURCATE', 'BUILTIN'), # Split a symbol
    (r'AGGREGATE', 'BUILTIN'), # Merge a symbol
    (r'ENUMERATE', 'BUILTIN'), # Merge a string
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
    # Lookup operator
    (r'\.', 'BUILTIN'),
])

# Value/variable token primitives
fltparser = TagsParser('FLOAT') ^ FloatExpr
intparser = TagsParser('INT') ^ IntExpr
nameparser = TagsParser('SYMBOL') ^ VarExpr
strparser = TagsParser('STRING') ^ (lambda s: StringExpr(s[1:-1]))
bltinparser = lambda t: ItemParser(t, 'BUILTIN')

# Expresssions
def execexpr():
    """Parses the execution statement as an expression."""
    return (
        bltinparser('EXECUTE')
        + bltinparser('(')
        + callparser()
        + bltinparser(')')
        ^ (lambda t: ExecuteStmt(t[2]))
        )


def exprvalparser():
    """Parses expression primitives."""
    return (
        LazierParser(execexpr)
        | LazierParser(unaryexprparser)
        | nameparser
        | fltparser
        | intparser
        | strparser
        )


def exprgrpparser():
    """Parses expression groups."""
    return (
        bltinparser('(')
        + LazierParser(exprparser)
        + bltinparser(')')
        ^ (lambda t: t[1])
        )


def unaryexprparser():
    """Parses unary expressions."""
    term = exprvalparser() | exprgrpparser()
    ops = bltinparser('+') | bltinparser('-') | bltinparser('~') | bltinparser('!')
    return ops + term ^ UnaryExpr


def exprparser():
    """Parses an infix expression."""
    def parse_ops(op_level):
        # Parser that picks among a set of operators with the same precedence level.
        ops = reduce(SelectParser, map(bltinparser, op_level))
        # Double lambda juju that magically ensures the operator is preserved.
        return ops ^ (lambda op: lambda l, r: BinaryExpr(op, l, r))
    # Operators listed in precendence order. Each tuple is a level of precedence.
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
    # Expression terms are either primitives, other expressions, or either in groups.
    term = exprvalparser() | exprgrpparser()
    # What the fuck does this do and why does it work??????????
    return reduce(StrictParser, [term] + [parse_ops(lvl) for lvl in op_order])


def callparser():
    """Parses a group of expressions."""
    def cull_seps(tokens):
        return tokens[0] or tokens[1]
    return RepeatParser(exprparser() + OptionParser(bltinparser(',')) ^ cull_seps)

# Statements
# def propastmt():
#     """Parses the reference statement."""
#     def breakdown(tokens):
#         _, src, tgt, _ = tokens
#         return PropagateStmt(src, tgt)
#     return (
#         bltinparser('PROPAGATE')
#         + nameparser
#         + OptionParser(nameparser)
#         + bltinparser(';')
#         ^ breakdown
#         )


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
        ^ breakdown
        )


def procrstmt():
    """Parses value declarations."""
    def breakdown(tokens):
        _, name, expr, _ = tokens
        return ProcreateStmt(name, expr)
    return (
        bltinparser('PROCREATE')
        + nameparser
        + OptionParser(exprparser())
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
        + OptionParser(exprvalparser() | exprgrpparser())
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
        + OptionParser(exprvalparser() | exprgrpparser())
        + bltinparser(';')
        ^ breakdown
        )


def printfunc():
    """Parses the print function."""
    def breakdown(tokens):
        return PrintStmt(tokens[2])
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
    def cull_seps(graft):
        return graft[0] or graft[1]
    argparser = RepeatParser(nameparser + OptionParser(bltinparser(',')) ^ cull_seps)
    def breakdown(tokens):
        name, _, _, _, args, _, _ = tokens
        return KillStmt(name, args)
    return (
        (nameparser | (
            bltinparser('[')
            + argparser
            + bltinparser(']')
            )
        )
        + bltinparser('.')
        + bltinparser('DIE')
        + bltinparser('(')
        + LazierParser(callparser)
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
    argparser = RepeatParser(nameparser + OptionParser(bltinparser(',')) ^ cull_seps)

    def breakdown(tokens):
        _, name, _, args, _, _, body, _ = tokens
        return FabricateStmt(name, args, body)

    return (
        bltinparser('FABRICATE')
        + nameparser
        + bltinparser('(')
        + OptionParser(argparser)
        + bltinparser(')')
        + bltinparser('{')
        + LazierParser(funcstmts)
        + bltinparser('}')
        ^ breakdown
        )



def tildeath():
    """Parses ~ATH loops."""
    def breakdown(tokens):
        _, _, state, grave, _, _, body, _, coro = tokens
        return TildeAthLoop(bool(state), grave, body, coro)
    return (
        bltinparser('~ATH')
        + bltinparser('(')
        + OptionParser(bltinparser('!'))
        + nameparser
        + bltinparser(')')
        + bltinparser('{')
        + LazierParser(stmtparser)
        + bltinparser('}')
        + execfunc()
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
        for idx, unless in enumerate(unlesses):
            if not unless.clause and idx < len(unlesses) - 1:
                print('Invalid DEBATE/UNLESS format')
                raise SyntaxError
        return DebateStmt(condexpr, body, unlesses)
    stmts = funcstmts if fabri else stmtparser

    return (
        bltinparser('DEBATE')
        + bltinparser('(')
        + exprparser()
        + bltinparser(')')
        + bltinparser('{')
        + LazierParser(stmts)
        + bltinparser('}')
        + OptionParser(
            RepeatParser(
                bltinparser('UNLESS')
                + OptionParser(
                    bltinparser('(')
                    + exprparser()
                    + bltinparser(')')
                    )
                + bltinparser('{')
                + LazierParser(stmts)
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
        + LazierParser(callparser)
        + bltinparser(')')
        + bltinparser(';')
        ^ breakdown
        )


def funcstmts():
    """Parses the set of statements used in functions."""
    return RepeatParser(
        replistmt() # assignment
        # | propastmt() # reference
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
        | LazierParser(fabristmt) # func dec
        | tildeath() # cond loop
        | condistmt(True) # conditionals
        | inspstmt() # Debug, remove
        ) ^ AthAstList


def stmtparser():
    """Parses the set of statements used top-level."""
    return RepeatParser(
        replistmt() # assignment
        # | propastmt() # reference
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
        ) ^ AthAstList
ath_parser = ScriptParser(stmtparser())
