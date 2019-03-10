"""The ~ATH interpreter grammar.

This contains the token regex list used by the lexer and all
the parser builders used to build the parser that creates the
abstract syntax tree.
"""
import sys
from functools import partial, reduce

from lexer import Lexer
from grafter import (
    ItemParser, TagsParser, Graft,
    SelectParser, StrictParser,
    OptionParser, RepeatParser,
    LazierParser, ScriptParser,
    )
from athstmt import (
    LiteralToken, IdentifierToken,
    AthStatement, AthTokenStatement, AthStatementList,
    AthCustomFunction, TildeAthLoop,
    UnaryExpr, BnaryExpr, CondiJump,
    )
from athbuiltins_default import ath_builtins


class StmtParser(RepeatParser):
    """RepeatParser that accomodates for flattened statements."""
    __slots__ = ()

    def __repr__(self):
        return f'{self.__class__.__name__}({self.graft!r})'

    def __call__(self, tokens, index=0):
        stmtlist = []
        graft = self.graft(tokens, index)
        while graft:
            if isinstance(graft.value, list):
                stmtlist.extend(graft.value)
            else:
                stmtlist.append(graft.value)
            index = graft.index
            graft = self.graft(tokens, index)
        # Thread all unconditional jumps.
        for idx, stmt in zip(range(len(stmtlist), -1, -1), reversed(stmtlist)):
            if isinstance(stmt, CondiJump) and not stmt.args[0]:
                try:
                    target = stmtlist[idx + stmt.args[1]]
                except IndexError:
                    continue
                if isinstance(target, CondiJump) and not target.args[0]:
                    stmt.args[1] += target.args[1] + 1
        return Graft(AthStatementList(stmtlist), index)


ath_lexer = Lexer([
    (r'(?s)/\*.*?\*/', None), # Multi-line comment
    (r'//[^\n]*', None), # Single-line comment
    (r'\s+', None), # Whitespace
    # Code enclosures
    (r'\(', 'DELIMITER'), # Group open
    (r'\)', 'DELIMITER'), # Group close
    (r'{', 'DELIMITER'), # Suite open
    (r'}', 'DELIMITER'), # Suite close
    (r'\[', 'DELIMITER'), # Symbol open
    (r'\]', 'DELIMITER'), # Symbol close
    # Separators
    (r';', 'DELIMITER'), # Statement separator
    (r',', 'DELIMITER'), # Group operator
    # Boolean operators
    (r'\bl&', 'OPERATOR'), # Boolean AND
    (r'\bl\|', 'OPERATOR'), # Boolean OR
    (r'\bl\^', 'OPERATOR'), # Boolean XOR
    # Bitwise operators
    (r'\bb&', 'OPERATOR'), # Bitwise and
    (r'\bb\|', 'OPERATOR'), # Bitwise or
    (r'\bb\^', 'OPERATOR'), # Bitwise xor
    # Arithmetic operators
    (r'\+', 'OPERATOR'), # Add, UnaryPos
    (r'-', 'OPERATOR'), # Sub, UnaryInv
    (r'\^', 'OPERATOR'), # Pow
    (r'\*', 'OPERATOR'), # Mul
    (r'/_', 'OPERATOR'), # FloorDiv
    (r'/', 'OPERATOR'), # TrueDiv
    (r'%', 'OPERATOR'), # Modulo
    # Symbol operators
    (r'!=!', 'OPERATOR'), # Assert Both
    (r'!=\?', 'OPERATOR'), # Assert Left
    (r'\?=!', 'OPERATOR'), # Assert Right
    (r'~=!', 'OPERATOR'), # Negate Left
    (r'!=~', 'OPERATOR'), # Negate Right
    (r'~=~', 'OPERATOR'), # Negate Both
    # Bitwise shift operators
    (r'<<', 'OPERATOR'), # Bitwise lshift
    (r'>>', 'OPERATOR'), # Bitwise rshift
    # Value operators
    (r'<=', 'OPERATOR'), # Less than or equal to
    (r'<', 'OPERATOR'), # Less than
    (r'>=', 'OPERATOR'), # Greater than or equal to
    (r'>', 'OPERATOR'), # Greater than
    (r'~=', 'OPERATOR'), # Not equal to
    (r'==', 'OPERATOR'), # Equal to
    # Statement keywords
    (r'DIE', 'KEYWORD'), # Kill symbol
    (r'~ATH', 'KEYWORD'), # Loop
    (r'print', 'KEYWORD'), # Output
    (r'input', 'KEYWORD'), # Input
    (r'import', 'KEYWORD'), # Import another file
    (r'EXECUTE', 'KEYWORD'), # Subroutine execution
    (r'INSPECT', 'KEYWORD'), # Debug
    (r'REPLICATE', 'KEYWORD'), # Deep copy to current frame
    (r'PROCREATE', 'KEYWORD'), # Value declaration or modification
    (r'ENUMERATE', 'KEYWORD'), # Split a string
    (r'BIFURCATE', 'KEYWORD'), # Split a symbol
    (r'AGGREGATE', 'KEYWORD'), # Merge a symbol
    (r'FABRICATE', 'KEYWORD'), # Subroutine declaration
    (r'DIVULGATE', 'KEYWORD'), # Return a symbol
    (r'DEBATE', 'KEYWORD'), # Conditional Consequent
    (r'UNLESS', 'KEYWORD'), # Conditional Alternative
    # Inverters
    (r'!', 'OPERATOR'), # Boolean NOT
    (r'~', 'OPERATOR'), # Bitwise not
    # Literals and Identifiers
    (r'([\'"])(?:[^\1]|\\\1)*?\1', 'LITERAL_STR'),
    (r'(\d+\.(\d*)?|\.\d+)([eE][-+]?\d+)?[jJ]', 'LITERAL_IMG'),
    (r'(\d+\.(\d*)?|\.\d+)([eE][-+]?\d+)?', 'LITERAL_FLT'),
    (r'\d+[jJ]', 'LITERAL_IMG'),
    (r'\d{1,3}(?:_\d{1,3})*', 'LITERAL_INT'),
    (r'[a-zA-Z]\w*', 'IDENTIFIER'),
    # Literally only used in DIE calls
    (r'\.', 'DELIMITER'),
])

# Value/variable token primitives
imgparser = TagsParser('LITERAL_IMG') ^ partial(LiteralToken, vtype=complex)
fltparser = TagsParser('LITERAL_FLT') ^ partial(LiteralToken, vtype=float)
intparser = TagsParser('LITERAL_INT') ^ partial(LiteralToken, vtype=int)
strparser = TagsParser('LITERAL_STR') ^ (lambda s: LiteralToken(s[1:-1]))
idnparser = TagsParser('KEYWORD') | TagsParser('IDENTIFIER') ^ IdentifierToken
varparser = TagsParser('IDENTIFIER') ^ IdentifierToken
kwdparser = lambda t: ItemParser(t, 'KEYWORD')
dlmparser = lambda t: ItemParser(t, 'DELIMITER')
oprparser = lambda t: ItemParser(t, 'OPERATOR')

# Expresssions
def execexpr():
    """Parses the execution statement as an expression."""
    def breakdown(tokens):
        kwd, _, args, _ = tokens
        return AthTokenStatement(kwd, args)
    return (
        kwdparser('EXECUTE')
        + dlmparser('(')
        + callparser()
        + dlmparser(')')
        ^ breakdown
        )

def exprvalparser():
    """Parses expression primitives."""
    return (
        LazierParser(execexpr)
        | LazierParser(unaryexprparser)
        | idnparser
        | imgparser
        | fltparser
        | intparser
        | strparser
        )

def exprgrpparser():
    """Parses expression groups."""
    return (
        dlmparser('(')
        + LazierParser(exprparser)
        + dlmparser(')')
        ^ (lambda t: t[1])
        )

def unaryexprparser():
    """Parses unary expressions."""
    term = exprvalparser() | exprgrpparser()
    ops = oprparser('+') | oprparser('-') | oprparser('~') | oprparser('!')
    return ops + term ^ UnaryExpr

# Operators listed in precendence order. Each tuple is a level of precedence.
op_order = (
    ('^',),
    ('*', '/', '/_', '%'),
    ('+', '-'),
    ('<<', '>>'),
    ('b&',), ('b|',), ('b^',),
    ('<', '<=', '>', '>=', '==', '~='),
    ('l&',), ('l|',), ('l^',),
    ('!=!', '!=?', '?=!', '~=!', '!=~', '~=~')
    )

def exprparser():
    """Parses an infix expression."""
    def parse_ops(op_level):
        # Parser that picks among a set of operators with the same precedence level.
        ops = reduce(SelectParser, map(oprparser, op_level))
        # Double lambda juju that magically ensures the operator is preserved.
        return ops ^ (lambda op: lambda l, r: BnaryExpr((op, l, r)))
    # Expression terms are either primitives, other expressions, or either in groups.
    term = exprvalparser() | exprgrpparser()
    # What the fuck does this do and why does it work??????????
    return reduce(StrictParser, [term] + [parse_ops(lvl) for lvl in op_order])

def callparser():
    """Parses a group of expressions."""
    def cull_seps(tokens):
        return tokens[0] or tokens[1]
    return RepeatParser(exprparser() + OptionParser(dlmparser(',')) ^ cull_seps)

# Statements
def replistmt():
    """Parses the assignment statement."""
    def breakdown(tokens):
        kwd, dst, src, _ = tokens
        return AthTokenStatement(kwd, (dst, src))
    return (
        kwdparser('REPLICATE')
        + varparser
        + OptionParser(exprparser())
        + dlmparser(';')
        ^ breakdown
        )

def procrstmt():
    """Parses value declarations."""
    def breakdown(tokens):
        kwd, dst, src, _ = tokens
        return AthTokenStatement(kwd, (dst, src))
    return (
        kwdparser('PROCREATE')
        + varparser
        + OptionParser(exprparser())
        + dlmparser(';')
        ^ breakdown
        )

def bfctstmt():
    """Parses the bifurcate statement."""
    def breakdown(tokens):
        kwd, src, _, lft, _, rht, _, _ = tokens
        return AthTokenStatement(kwd, (src, lft, rht))
    return (
        kwdparser('BIFURCATE')
        + idnparser
        + dlmparser('[')
        + varparser
        + dlmparser(',')
        + varparser
        + dlmparser(']')
        + dlmparser(';')
        ^ breakdown
        )

def aggrstmt():
    """Parses the aggregate statement."""
    def breakdown(tokens):
        kwd, _, lft, _, rht, _, dst, _ = tokens
        return AthTokenStatement(kwd, (dst, lft, rht))
    return (
        kwdparser('AGGREGATE')
        + dlmparser('[')
        + exprparser()
        + dlmparser(',')
        + exprparser()
        + dlmparser(']')
        + varparser
        + dlmparser(';')
        ^ breakdown
        )

def enumstmt():
    """Parses the enumerate statement."""
    def breakdown(tokens):
        kwd, src, dst, _ = tokens
        return AthTokenStatement(kwd, (src, dst))
    return (
        kwdparser('ENUMERATE')
        + OptionParser(exprvalparser() | exprgrpparser())
        + varparser
        + dlmparser(';')
        ^ breakdown
        )

def importstmt():
    """Parses the import statement."""
    def breakdown(tokens):
        kwd, module, symbol, _ = tokens
        return AthTokenStatement(kwd, (module.name, symbol.name))
    return (
        kwdparser('import')
        + varparser
        + varparser
        + dlmparser(';')
        ^ breakdown
        )

def inputstmt():
    """Parses the input statement."""
    def breakdown(tokens):
        kwd, dst, ech, _ = tokens
        return AthTokenStatement(kwd, (
            dst or None,
            ech if ech is not None else LiteralToken('')
            ))
    return (
        kwdparser('input')
        + varparser
        + OptionParser(exprvalparser() | exprgrpparser())
        + dlmparser(';')
        ^ breakdown
        )

def printfunc():
    """Parses the print function."""
    def breakdown(tokens):
        kwd, _, args, _, _ = tokens
        return AthTokenStatement(kwd, args)
    return (
        kwdparser('print')
        + dlmparser('(')
        + callparser()
        + dlmparser(')')
        + dlmparser(';')
        ^ breakdown
        )

def killfunc():
    """Parses the kill function."""
    def cull_seps(graft):
        return graft[0] or graft[1]
    def breakdown(tokens):
        if len(tokens) > 6:
            return AthTokenStatement(tokens[-4], tokens[1])
        else:
            return AthTokenStatement(tokens[-4], [tokens[0]])
    return (
        (idnparser | (
            dlmparser('[')
            + RepeatParser(
                idnparser + OptionParser(dlmparser(',')) ^ cull_seps
                )
            + dlmparser(']')
            )
        )
        + dlmparser('.')
        + kwdparser('DIE')
        + dlmparser('(')
        + dlmparser(')')
        + dlmparser(';')
        ^ breakdown
        )

def execfunc():
    """Parses the execution statement as a statement."""
    def breakdown(tokens):
        kwd, _, args, _, _ = tokens
        return AthTokenStatement(kwd, args)
    return (
        kwdparser('EXECUTE')
        + dlmparser('(')
        + callparser()
        + dlmparser(')')
        + dlmparser(';')
        ^ breakdown
        )

def divlgstmt():
    """Parses the return statement."""
    def breakdown(tokens):
        kwd, expr, _ = tokens
        return AthTokenStatement(kwd, (expr,))
    return (
        kwdparser('DIVULGATE')
        + exprparser()
        + dlmparser(';')
        ^ breakdown
        )

def fabristmt():
    """Parses function declarations."""
    def cull_seps(graft):
        return graft[0] or graft[1]
    def breakdown(tokens):
        kwd, name, _, args, _, _, body, _ = tokens
        body.pendant = name.name
        return AthTokenStatement(kwd,
            (AthCustomFunction(name.name, [arg.name for arg in args], body),)
            )
    return (
        kwdparser('FABRICATE')
        + varparser
        + dlmparser('(')
        + OptionParser(RepeatParser(
            varparser + OptionParser(dlmparser(',')) ^ cull_seps
            ))
        + dlmparser(')')
        + dlmparser('{')
        + LazierParser(funcstmts)
        + dlmparser('}')
        ^ breakdown
        )

def tildeath():
    """Parses ~ATH loops."""
    def breakdown(tokens):
        _, _, state, grave, _, _, body, _, coro = tokens
        body.pendant = grave.name
        return TildeAthLoop(bool(state), body, coro)
    return (
        kwdparser('~ATH')
        + dlmparser('(')
        + OptionParser(oprparser('!'))
        + idnparser
        + dlmparser(')')
        + dlmparser('{')
        + LazierParser(stmtparser)
        + dlmparser('}')
        + execfunc()
        ^ breakdown
        )

def condistmt(fabri=False):
    """Parses conditional statements."""
    def brkunless(tokens):
        _, condexpr, _, body, _ = tokens
        return (condexpr and condexpr[1], body)
    def breakdown(tokens):
        _, _, condexpr, _, _, body, _, unlesses = tokens
        # Create list of flattened statements.
        stmtlist = [CondiJump([condexpr, len(body) + int(bool(unlesses))])]
        stmtlist.extend(body)
        if unlesses:
            # The offset created when due to the last UNLESS's lack of jumps.
            # The last UNLESS or a lone DEBATE will not jump off the end,
            # and if the last UNLESS has no clause, there will be no
            # conditional jump at the head of its body.
            jumpoffset = -2 + int(unlesses[-1][0] is not None)
            for idx, unless in enumerate(unlesses):
                # Check if this is a clauseless unless that isn't the last unless.
                if unless[0] is None and idx < len(unlesses) - 1:
                    sys.stderr.write('SyntaxError: invalid unless format')
                    sys.exit(SyntaxError)
                # Calculate jump length.
                bodylen = sum(
                    map(lambda u: len(u[1]) + 2, unlesses[idx:]),
                    jumpoffset
                    )
                # Add the jump that allows execution to jump to the end.
                stmtlist.append(CondiJump([None, bodylen]))
                # Add the jump at the head of this unless.
                if unless[0]:
                    bodylen = len(unless[1]) + 3 + jumpoffset
                    stmtlist.append(CondiJump([unless[0], bodylen]))
                # Add the body.
                stmtlist.extend(unless[1])
        return stmtlist
    stmts = (stmtparser, funcstmts)[fabri]
    return (
        kwdparser('DEBATE')
        + dlmparser('(')
        + exprparser()
        + dlmparser(')')
        + dlmparser('{')
        + LazierParser(stmts)
        + dlmparser('}')
        + OptionParser(
            RepeatParser(
                kwdparser('UNLESS')
                + OptionParser(
                    dlmparser('(')
                    + exprparser()
                    + dlmparser(')')
                    )
                + dlmparser('{')
                + LazierParser(stmts)
                + dlmparser('}')
                ^ brkunless
                )
            )
        ^ breakdown
        )

def inspstmt():
    def breakdown(tokens):
        kwd, _, args, _, _ = tokens
        return AthTokenStatement(kwd, args)
    return(
        kwdparser('INSPECT')
        + dlmparser('(')
        + LazierParser(callparser)
        + dlmparser(')')
        + dlmparser(';')
        ^ breakdown
        )

def funcstmts():
    """Parses the set of statements used in functions."""
    return StmtParser(
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
        )

def stmtparser():
    """Parses the set of statements used top-level."""
    return StmtParser(
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
        )

def ath_parser(script):
    """Parses a given script and returns an AthAstList object."""
    try:
        ast = ScriptParser(stmtparser())(ath_lexer(script), 0).value
    except SyntaxError:
        print('your doing it WRONG u dumb HOMO TOOL!')
        raise
    for stmt in ast:
        if isinstance(stmt, TildeAthLoop):
            break
    else:
        raise SyntaxError('no ~ATH loop found in top-level script')
    return ast
