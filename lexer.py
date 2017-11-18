"""Separates a script file into tokens defined by a list of valid regexes."""
import sys
import re


class Token(object):
    """Token wrapper. Might have more functionality than just debugging."""
    __slots__ = ('token', 'tag', 'line')

    def __init__(self, token, tag, line=0):
        self.token = token
        self.tag = tag
        self.line = line

    def __repr__(self):
        return '{}({}, {}, {})'.format(
            self.__class__.__name__,
            self.token,
            self.tag,
            self.line
            )

    def __str__(self):
        return '{} token containing: {}'.format(self.tag, self.token)


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
        line = 0
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
                sys.stderr.write('SyntaxError: Line {}\n'.format(line + 1))
                sys.stderr.write('{}\n'.format(script.split('\n')[line]))
                sys.stderr.write('Invalid character {}\n'.format(script[seek]))
                sys.exit(1)
        return tokens
