#!/usr/bin/env python
from __future__ import print_function
from argparse import ArgumentParser
import re

class ATHobj(object):
    __slots__ = ('value')

    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return '~ATH var with value: {0!r}'.format(self.value)


class ATHfunc(ATHobj):
    pass


class ATHvar(ATHobj):
    pass


class Token(object):
    __slots__ = ('value', 'type', 'builtin')

    def __init__(self, value, athtype='var', builtin=False):
        self.value = value
        self.type = athtype
        self.builtin = builtin

    def __repr__(self):
        return '{} token for: {}'.format(self.type.capitalize(), self.value)

    def __call__(self, *args):
        self.value.__call__(*args)

# Token definitions for python builtins to allow modified execution.
class ImportToken(Token):
    __slots__ = ()

    def __init__(self):
        super().__init__(__import__, 'statement', True)

    def __call__(self, pathname, tokens):
        # Import behavior varies if ~ATH or py files are attempted.
        if pathname.startswith('"'):
            return __import__(pathname[1:-1])
        else:
            if not pathname.endswith('.~ATH'):
                pathname += '.~ATH'
            with open(pathname, 'r') as modfile:
                module = Script(modfile.read())
                module.execute()
                try:
                    return module.tokens
                except FileNotFoundError:
                    raise ImportError(
                        'Script {} can\'t be found.'.format(pathname)
                        )

class InputToken(Token):
    __slots__ = ()

    def __init__(self):
        super().__init__(input, 'statement', True)

    def __call__(self, textvar):
        if textvar.startswith('"'):
            return input(textvar[1:-1])
        else:
            raise NotImplementedError(
                'Variable passing not defined yet.'
                )


class PrintToken(Token):
    __slots__ = ()

    def __init__(self):
        super().__init__(print, 'function', True)

    def __call__(self, *textargs):
        for text in textargs:
            if text.startswith('"'):
                print(text[1:-1], end='')
            else:
                raise NotImplementedError(
                    'Variable passing not defined yet.'
                    )
        print('\n', end='')


def bifurcate(obj):
    pass


class Script(object):
    __slots__ = ('script', 'alive')
    # Cerulean's token system.
    tokens = {
        'import': ImportToken(),
        'input': InputToken(),
        'print': PrintToken(),
        'BIRTH': Token(None, 'statement', True),
        'BIFURCATE': Token(bifurcate, 'statement', True),
        'CLONE': Token(None, 'statement', True),
        'THIS': Token(ATHvar(None), 'const', True),
        'NULL': Token(ATHvar(None), 'const', True),
    }
    # Compiled RegEx patterns to save on time.
    patterns = {
        'import': re.compile(r'\s*import\s+(_*[a-zA-Z]\w*|\".*?\")\s*([a-zA-Z]\w*)?'),
        'state1/2': re.compile(r'\s*([a-zA-Z]\w+)\s+([a-zA-Z]\w*)\s*(_*[a-zA-Z]\w*|\".*?\")?'),
        'function': re.compile(r'\s*([a-zA-Z]\w+)\((.*)\)'),
        'exit': re.compile(r'\s*THIS\s*\.\s*DIE()\s*'),
    }

    def __init__(self, script, tokens={}):
        self.script = script
        self.tokens.update(tokens)
        self.alive = True

    def strip_comments(self):
        # Removes single-line comments from the script.
        self.script = re.sub(re.compile(r'#.*?\n'), '\n', self.script)
        self.script = re.sub(re.compile(r'#.*?$'), '', self.script)

    def grab_key(self, key):
        """Returns key if key is valid."""
        try:
            return self.tokens[key]
        except KeyError:
            raise NameError('{} has not been defined in the script.'.format(name))

    def assign_token(self, name, token):
        """Assigns a Token value to the token dictionary."""
        if name not in self.tokens.keys() or not self.tokens[name].builtin:
            # Add the token if it's not a builtin or if it doesn't exist.
            self.tokens[name] = token
        else:
            raise NameError('Assignment to builtins are not allowed.')

    def parse(self, line):
        """Parses a line separated by semicolons. Shitty."""
        # Import statement.
        match = re.fullmatch(self.patterns['import'], line)
        if match:
            args = match.groups()
            modname = args[1] if args[1] else args[0]
            self.assign_token(modname, Token(self.tokens['import'](args[0], self.tokens), 'module'))
            return
        # A statement that takes one or two arguments, second is optional.
        match = re.fullmatch(self.patterns['state1/2'], line)
        if match:
            name, *args = match.groups()
            builtin = self.grab_key(name)
            if name == 'input':
                echoname = args[1] if args[1] else ''
                self.assign_token(args[0], Token(ATHvar(builtin(echoname)), 'var'))
            elif name == 'BIRTH':
                self.assign_token(args[0], Token(ATHvar(args[1]), 'var'))
            return
        # End statement parsing, function parsing goes here.
        match = re.match(self.patterns['function'], line)
        if match:
            name, args = match.groups()
            func = self.grab_key(name)
            func(*args.split(','))
            return
        match = re.match(self.patterns['exit'], line)
        if match:
            self.alive = False
        else:
            print(line.encode())
            raise SyntaxError(line)

    def execute(self):
        """Execute the script. Shitty."""
        self.strip_comments()
        # print('Script: """', self.script, '"""\n', sep='\n')
        print('Running ~ATH...')
        for line in self.script.split(';'):
            if not len(line):
                continue
            self.parse(line)
            if not self.alive:
                break
        # print(self.tokens)

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
    with open(cmdargs.script, 'r') as code:
        script = Script(code.read())
        script.execute()
