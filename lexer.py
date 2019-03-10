"""Separates a script file into tokens defined by a list of valid regexes."""
import sys
import re


class Token(object):
    """Token wrapper. Might have more functionality than just debugging."""
    __slots__ = ('token', 'tag', 'line')

    def __init__(self, token, tag, line=1):
        self.token = token
        self.tag = tag
        self.line = line

    def __repr__(self):
        attr_list = tuple(repr(slot) for slot in self.__slots__)
        return f'{self.__class__.__name__}{attr_list}'

    def __str__(self):
        return f'"{self.token}" {self.tag} token on line {self.line}'


class Lexer(object):
    """Lexer used to tokenize a script."""
    __slots__ = ('expr_list',)

    def __init__(self, expr_list):
        self.expr_list = [
            (re.compile(pattern), tag)
            for pattern, tag in expr_list
            ]

    def __call__(self, script):
        tokens = []
        seek = 0
        line = 1
        while seek < len(script):
            oldseek = seek
            for pattern, tag in self.expr_list:
                match = pattern.match(script, seek)
                if match:
                    if tag:
                        tokens.append(Token(match.group(0), tag, line))
                    seek = match.end(0)
                    line += script.count('\n', oldseek, seek)
                    break
            else:
                sys.stderr.write(
                    f'SyntaxError on Line {line}:\n'
                    f'{script.splitlines()[line - 1]}\n'
                    f'Invalid token detected: {script[seek]}\n'
                    )
                sys.exit(SyntaxError)
        return tokens
