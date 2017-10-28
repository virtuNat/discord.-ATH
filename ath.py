
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
        'BIFURCATE': bifurcate
    }

    def __init__(self, script):
        self.script = script

    def parse(self, line):
        # Two or three argument keyword, third argument optional.
        match = re.match(r'\s*([a-zA-Z]\w+) ([a-zA-Z]\w*) ?([a-zA-Z]\w*)?', line)
        if match:
            name, *args = match.groups()
            # Last arg is var, right?
            try:
                builtin = self.tokens[name]
            except KeyError:
                raise NameError('Keyword {} is not defined.'.format(name))
            if name == 'import':
                modname = args[1] if args[1] else args[0]
                if modname not in self.tokens.keys():
                    self.tokens[modname] = builtin(args[0])
            elif name in self.tokens:
                builtin  = self.tokens[name]
                builtin(*args[:-1]) # Run the function
            # End of statement parsing, lets move onto function parse
        match = re.match('(.*)\((.*?)\)',line)
        if match:
            name, args = match.groups()
            name = name.lstrip()
            builtin = self.tokens.get(name)
            
            if builtin:
                builtin(*args.split(','))

    def execute(self):
        for line in self.script.split('\n'):
            self.parse(line)

if __name__ == '__main__':
    with open('sample.txt', 'r') as code:
        script = Script(code.read())
        script.execute()
