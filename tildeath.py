#!/usr/bin/env python
from __future__ import print_function
from argparse import ArgumentParser
import re

class ATHobj(object):
    __slots__ = ('value')

    def __init__(self, value):
        self.value = value


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

    def __call__(self, *args):
        newargs = []
        for arg in args:
            arg = arg.strip();
            if arg.startswith('"') and arg.endswith('"') and len(arg) > 1:
                arg = arg[1:-1]
            newargs.append(arg)
        self.value(*tuple(newargs))

# Token definitions for python builtins to allow modified execution.
class ImportToken(Token):
    __slots__ = ()

    def __init__(self):
        super().__init__(__import__, 'statement', True)

    def __call__(self, modfile):
        # So import can have different behavior later.
        self.value(modfile)


class InputToken(Token):
    pass


def bifurcate(obj):
    pass


class Script(object):
    __slots__ = ('script')
    tokens = {
        'import': ImportToken(),
        'print': Token(print, 'function', True),
        'input': Token(input, 'statement', True),
        'BIRTH': Token(None, 'statement', True),
        'BIFURCATE': Token(bifurcate, 'statement', True),
        'CLONE': Token(None, 'statement', True),
        'THIS': Token(ATHvar(self), 'const', True),
        'NULL': Token(ATHvar(None), 'const', True),
    }

    def __init__(self, script):
        self.script = script

    def grab_key(self, key):
        try:
            return self.tokens[key]
        except KeyError:
            raise NameError('{} has not been defined in the script.'.format(name))

    def assign_token(self, name, token):
        if name not in self.tokens.keys() or not self.tokens[name].builtin:
            # Add the token if it's not a builtin or if it doesn't exist.
            self.tokens[name] = token
        else:
            raise NameError('Assignment to builtins are not allowed.')

    def parse(self, line):
        # A statement that takes one or two arguments, second is optional.
        match = re.match(r'\s*([a-zA-Z]\w+) ([a-zA-Z]\w*) ?([a-zA-Z]\w*)?', line)
        if match:
            name, *args = match.groups()
            builtin = grab_key(name)
            if name == 'import':
                modname = args[1] if args[1] else args[0]
                self.assign_token(modname, Token(builtin(args[0]), 'module'))
            elif name == 'input':
                echoname = args[1] if args[1] else ''
                self.assign_token(args[0], Token(builtin(echoname), 'var'))
            elif name == 'BIRTH':
                self.assign_token(args[0], Token(ATHvar(args[1]), 'var'))
        # End statement parsing, function parsing goes here.
        match = re.match(r'\s*([a-zA-Z]\w+)\((.*)\)', line)
        if match:
            name, args = match.groups()
            func = grab_key(name)
            func(*args.split(','))

    def execute(self):
        for line in self.script.split(';'):
            match = re.match(r'\s*#.*\n', line)
            if match:
                continue
            self.parse(line)
        print(self.tokens)

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
