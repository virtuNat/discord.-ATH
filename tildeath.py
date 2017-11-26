#!/usr/bin/env python
import sys
from traceback import print_exception
from argparse import ArgumentParser
from symbol import AthSymbol, BuiltinSymbol, EndTilDeath
from athparser import ath_lexer, ath_parser, TildeAthLoop

__version__ = '1.2.0 Beta'
__author__ = 'virtuNat'


def echo_error(msg):
    sys.stderr.write(msg)
    sys.exit(1)


class AthStackFrame(object):
    """Keeps a record of all symbols declared in a given scope.
    ~ATH implements dynamic scope, so be wary when coding in it!
    """
    __slots__ = ('scope_vars',)

    def __init__(self, scope_vars=None):
        if not scope_vars:
            self.scope_vars = {}
        else:
            self.scope_vars = scope_vars

    def __getitem__(self, name):
        try:
            return self.scope_vars[name]
        except KeyError:
            return None

    def __setitem__(self, name, value=None):
        if value is None:
            value = AthSymbol(False)
        try:
            symbol = self.scope_vars[name]
        except KeyError:
            pass
        # else:
        #     if isinstance(symbol.left, AthSymbol):
        #         symbol.left.leftof.remove(symbol)
        #     if isinstance(symbol.right, AthSymbol):
        #         symbol.right.rightof.remove(symbol)
        finally:
            self.scope_vars[name] = value


class TildeAthInterp(object):
    """This is supposed to be a Finite State Machine"""
    __slots__ = ('modules', 'global_vars', 'stack')

    def __init__(self):
        self.modules = {}
        self.global_vars = {
            'THIS': BuiltinSymbol(),
            'NULL': BuiltinSymbol(False),
            'DIE': BuiltinSymbol(),
            'ATH': BuiltinSymbol(),
            'print': BuiltinSymbol(),
            'input': BuiltinSymbol(),
            'import': BuiltinSymbol(),
            'DEBATE': BuiltinSymbol(),
            'UNLESS': BuiltinSymbol(),
            'EXECUTE': BuiltinSymbol(),
            'DIVULGATE': BuiltinSymbol(),
            'FABRICATE': BuiltinSymbol(),
            'REPLICATE': BuiltinSymbol(),
            'PROCREATE': BuiltinSymbol(),
            'BIFURCATE': BuiltinSymbol(),
            'AGGREGATE': BuiltinSymbol(),
            'ENUMERATE': BuiltinSymbol(),
            }
        self.stack = []

    def __enter__(self):
        stacklen = len(self.stack)
        if stacklen >= 1000:
            print('i told you DOG i TOLD you about STACKS!!')
        elif stacklen >= 4000:
            print('quick dude come get the ruler its ESCAPING from ABOVE!!')
        elif stacklen >= 16000:
            print('dude how HIGH do you have to even BE to do such a thing??')
        return self

    def __exit__(self, *exc_info):
        if len(self.stack):
            self.stack.pop()
        else:
            raise RuntimeError('Stack is already empty, dingus!')

    def push_stack(self, init_dict={}):
        self.stack.append(AthStackFrame(init_dict))
        return self

    def lookup_name(self, name):
        for frame in reversed(self.stack):
            value = frame[name]
            if value is not None:
                # print('{} found'.format(name))
                return value
        try:
            return self.global_vars[name]
        except KeyError:
            raise NameError('Symbol {} not found'.format(name))

    def assign_name(self, name, value):
        try:
            self.stack[-1][name] = value
        except IndexError:
            try:
                symbol = self.lookup_name(name)
            except NameError:
                self.global_vars[name] = value
            else:
                if not isinstance(symbol, BuiltinSymbol):
                    self.global_vars[name] = value
                else:
                    raise SymbolError('builtins can\'t be assigned to')

    def execute(self, script):
        count = 0
        try:
            while True:
                script.eval(self)
                count += 1
                if count >= 1025:
                    echo_error('UnboundATHLoopError: THIS.DIE() not called')
        except EndTilDeath:
            sys.exit(0)
        except Exception:
            print('Something really messed up!')
            print_exception(*sys.exc_info(), file=sys.stdout)
            raise
        finally:
            for frame in reversed(self.stack):
                print('Frame:')
                print(frame.scope_vars)
            print('Globals:')
            print(self.global_vars)

    def interpret(self, fname):
        if not fname.endswith('~ATH'):
            echo_error('IOError: script must be a ~ATH file')
        with open(fname, 'r') as script_file:
            script = script_file.read()
        tokens = ath_lexer(script)
        result = ath_parser(tokens, 0)
        if not result:
            echo_error('RuntimeError: the parser could not understand the script')

        for stmt in result.value.stmt_list:
            if isinstance(stmt, TildeAthLoop):
                break
        else:
            echo_error('RuntimeError: no ~ATH loop found in top-level script')

        with open(fname[:-4]+'py', 'w') as py_file:
            py_file.write('#!/usr/bin/env python\nfrom athast import *\n')
            py_file.write('from athparser import TildeAthInterp\n\n')
            py_file.write('ath_script = ' + repr(result.value))
            py_file.write('\nTildeAthInterp().execute(ath_script)\n')
        self.execute(result.value)


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
    ath_interp = TildeAthInterp()
    ath_interp.interpret(cmdargs.script)
