#!/usr/bin/env python
from __future__ import print_function
from argparse import ArgumentParser
import re

def bifurcate(obj):
    pass

class ATHobj(object):
    pass

class ATHfunc(ATHobj):
    pass

class ATHvar(ATHobj):
    pass

class Script(object):
    __slots__ = ('script')
    tokens = {
        'import': __import__,
        'print': print,
        'input': input,
        'BIFURCATE': bifurcate,
    }

    def __init__(self, script):
        self.script = script

    def parse(self, line):
        # Two or three argument keyword, third argument optional.
        match = re.match(r'\s*([a-zA-Z]\w+) ([a-zA-Z]\w*) ?([a-zA-Z]\w*)?', line)
        if match:
            name, *args = match.groups()
            try:
                builtin = self.tokens[name]
            except KeyError:
                raise NameError('Keyword {} is not defined.'.format(name))
            if name == 'import':
                modname = args[1] if args[1] else args[0]
                if modname not in self.tokens.keys():
                    self.tokens[modname] = builtin(args[0])
            print(self.tokens)

    def execute(self):
        for line in self.script.split(';'):
            self.parse(line)

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
