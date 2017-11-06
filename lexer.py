import sys
import re

class Token(object):
    
    def __init__(self, token, tag):
        self.token = token
        self.tag = tag

    def __repr__(self):
        return repr(self.token)

    def __str__(self):
        return '{} token containing: {}'.format(self.tag, self.token)

class Lexer(object):

    def __init__(self, expr_list):
        self.expr_list = [
            (re.compile(pattern), tag)
            for pattern, tag in expr_list
            ]

    def lex(self, script):
        tokens = []
        seek = 0
        line = 1
        while seek < len(script):
            oldseek = seek
            for pattern, tag in self.expr_list:
                match = pattern.match(script, seek)
                if match:
                    if tag:
                        tokens.append(Token(match.group(0), tag))
                    seek = match.end(0)
                    line += script.count('\n', oldseek, seek)
                    break
            else:
                sys.stderr.write('SyntaxError: Line {}\n'.format(line))
                sys.stderr.write('Invalid character {}\n'.format(script[seek]))
                sys.exit(1)
        return tokens
