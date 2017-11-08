import athast
from lexer import Lexer

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
    (r'BIRTH', 'BUILTIN'), # Declaration
    (r'CLONE', 'BUILTIN'), # Two-level copy
    (r'EXECUTE', 'BUILTIN'), # Subroutine Execution
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
    (r'([\'"])[^\1]*?\1', 'STR'),
    (r'(\d+\.(\d*)?|\.\d+)([eE][-+]?\d+)?', 'FLOAT'),
    (r'\d+', 'INT'),
    (r'[a-zA-Z]\w*', 'NAME'),
])


def bltinparser(token):
    return TokenGrafter(token, 'BUILTIN')
strparser = TagGrafter('STR')
fltparser = TagGrafter('FLOAT')
intparser = TagGrafter('INT')
nameparser = TagGrafter('NAME')


class TildeAthInterp(object):
    """This is supposed to be a Finite State Machine"""
    __slots__ = ()
    lexer = ath_lexer

    @classmethod
    def execute(cls, script):
        tokens = cls.lexer.lex(script)
        for token in tokens:
            print(token)
