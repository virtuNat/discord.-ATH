import sys
import re
from argparse import ArgumentParser
from lexer import Lexer

ATH_EXPRS = [
    (r'(?s)###.*?###', None), # Multi-line comment
    (r'#[^\n]*', None), # Single-line comment
    (r'\s+', None), # Whitespace
    # Code enclosures
    (r'\(', 'BUILTIN'),
    (r'\)', 'BUILTIN'),
    (r'{', 'BUILTIN'),
    (r'}', 'BUILTIN'),
    (r'\[', 'BUILTIN'),
    (r'\]', 'BUILTIN'),
    # Separators
    (r';', 'BUILTIN'),
    (r'\.', 'BUILTIN'),
    (r',', 'BUILTIN'),
    # Arithmetic in-place operators
    (r'\+=', 'BUILTIN'),
    (r'-=', 'BUILTIN'),
    (r'\*=', 'BUILTIN'),
    (r'/=', 'BUILTIN'),
    # Arithmetic operators
    (r'\+', 'BUILTIN'),
    (r'-', 'BUILTIN'),
    (r'\*', 'BUILTIN'),
    (r'/', 'BUILTIN'),
    # Symbol operators
    (r'!=!', 'BUILTIN'),
    (r'!=\?', 'BUILTIN'),
    (r'\?=!', 'BUILTIN'),
    (r'~=!', 'BUILTIN'),
    (r'!=~', 'BUILTIN'),
    (r'~=~', 'BUILTIN'),
    # Value operators
    (r'<=', 'BUILTIN'),
    (r'<', 'BUILTIN'),
    (r'>=', 'BUILTIN'),
    (r'>', 'BUILTIN'),
    (r'~=', 'BUILTIN'),
    (r'==', 'BUILTIN'),
    # Boolean operators
    (r'&&', 'BUILTIN'),
    (r'\|\|', 'BUILTIN'),
    (r'\^\^', 'BUILTIN'),
    (r'~~', 'BUILTIN'),
    # Statement keywords
    (r'WHEN', 'BUILTIN'),
    (r'UNLESS', 'BUILTIN'),
    (r'~ATH', 'BUILTIN'),
    (r'print', 'BUILTIN'),
    (r'input', 'BUILTIN'),
    (r'BIRTH', 'BUILTIN'),
    (r'EXECUTE', 'BUILTIN'),
    (r'BIFURCATE', 'BUILTIN'),
    (r'MERGE', 'BUILTIN'),
    # Bitwise operators
    (r'&', 'BUILTIN'),
    (r'\|', 'BUILTIN'),
    (r'\^', 'BUILTIN'),
    (r'~', 'BUILTIN'),
    # Other identifiers
    (r'([\'"])[^\1]*?\1', 'STR'),
    (r'(\d+\.(\d*)?|\.\d+)([eE][-+]?\d+)?', 'FLOAT'),
    (r'\d+', 'INT'),
    (r'[a-zA-Z]\w*', 'NAME'),
]

ath_lexer = Lexer(ATH_EXPRS)

if __name__ == '__main__':
    cmdparser = ArgumentParser(
        description='A fanmade ~ATH interpreter.',
        )
    cmdparser.add_argument(
        'script',
        help='The ~ATH file to run.',
        metavar='scr_name',
        )
    cmdargs = cmdparser.parse_args()
    with open(cmdargs.script, 'r') as codefile:
        script = codefile.read()
        tokens = ath_lexer.lex(script)
        print(tokens)
        for token in tokens:
            print(token)
