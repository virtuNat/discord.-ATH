import re

class Token(object):

    def __init__(self, name, type, args=[]):
        self.name = name
        self.type = type # can be var, math 
        self.args = args

    def __call__(self, *args):
        return self.type(*self.args)
    
class Script:
    
    tokens = {
        'print': print,
        'import': __import__
    }

    def __init__(self, script):
        self.script = script
        __slots__ = ('script', 'tokens')

    def tokenize(self, line):
        args = ()
        return (self.tokens['testname'], args)

    def dispatch(self, token, *args):
        return token(*args)
    
    def parse(self):
        for line in self.script.split('\n'):
            # Find import statements
            match = re.search('import ([^;]+)',line)
            if match:
                m = match.group(0)
                type, *args = m.split() # Split the string into sections
                name = None
                if 'as' in args:
                    # Presume args is "import math as m"
                    try:
                        name = args[2]
                    except IndexError:
                        raise TypeError('Import has keyword "as" but nothing after it.')

                t = Token(type, self.tokens[type], args=args)()
                self.tokens[args[0] if not name else name] = t
                print(self.tokens)
code = open('sample.txt','r').read()
print(code)
s = Script(code)
s.parse()