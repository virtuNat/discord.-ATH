#!/usr/bin/env python
import os
import sys
from argparse import ArgumentParser
from symbol import AthSymbol, NullSymbol, AthFunction, BuiltinSymbol, SymbolDeath
from athast import AthAstList, CondJumpStmt, ExecuteStmt, DivulgateStmt, TildeAthLoop
from athparser import ath_lexer, ath_parser

__version__ = '1.4.3 Dev Build'
__author__ = 'virtuNat'


def echo_error(msg):
    sys.stderr.write(msg)
    sys.exit(1)


class AthStackFrame(object):
    """Keeps a record of all symbols declared in a given scope.
    ~ATH implements dynamic scope, so be wary when coding in it!

    It also keeps AST execution and evaluation state, so that the
    execution and evaluation trampolines know where to continue.
    """
    __slots__ = ('scope_vars', 'return_pt', 'state', 'eval_stack')

    def __init__(self, scope_vars=None, return_pt=None, state=0, eval_stack=[]):
        if not scope_vars:
            self.scope_vars = {}
        else:
            self.scope_vars = scope_vars
        self.return_pt = return_pt
        self.state = state
        self.eval_stack = eval_stack

    def __str__(self):
        return '\nAthStackFrame({}, {}, {}, {})'.format(
            self.state, self.return_pt, self.scope_vars, self.eval_stack
            )

    def __repr__(self):
        return '{}({}, {}, {}, {})'.format(
            self.__class__.__name__,
            self.scope_vars,
            self.return_pt.__class__.__name__,
            self.state,
            [item.__class__.__name__ for item in self.eval_stack],
            )

    def __getitem__(self, name):
        return self.scope_vars[name]

    def __setitem__(self, name, value=None):
        if value is None:
            value = AthSymbol(False)
        try:
            symbol = self.scope_vars[name]
        except KeyError:
            pass
        finally:
            self.scope_vars[name] = value


class TildeAthInterp(object):
    """This is supposed to be a Finite State Machine"""
    __slots__ = ('modules', 'bltin_vars', 'stack', 'ast', 'state')
    # Execution state final variables.
    TOPLEVEL_STATE = 0 # Toplevel imperative execution
    TILDEATH_STATE = 1 # Looping in breakable death-checking loops
    TILALIVE_STATE = 2 # Looping in continuable life-checking loops
    FUNCEXEC_STATE = 3 # Inside a function body
    FXRETURN_STATE = 4 # Returning from a function

    def __init__(self):
        self.modules = {}
        self.bltin_vars = {
            'THIS': BuiltinSymbol(),
            'NULL': NullSymbol(),
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
        self.stack = [AthStackFrame()]
        # Currently evaluating AST list.
        self.ast = None
        # Current execution state.
        self.state = 0

    def push_stack(self, state, init_dict={}):
        """Adds one stack frame and handles most of the internal state changes."""
        self.stack[-1].return_pt = self.ast
        self.stack[-1].state = self.state
        self.stack.append(AthStackFrame(init_dict, None, state))
        self.state = state
        stacklen = len(self.stack)
        if stacklen == 1000:
            print('i told you DOG i TOLD you about STACKS!!')
        elif stacklen == 2000:
            print('quick dude come get the ruler its ESCAPING from ABOVE!!')
        elif stacklen == 3000:
            print('dude how HIGH do you have to even BE to do such a thing??')
        elif stacklen == 4000:
            print('my GUY.')
            print('stop making the stack not STOP from getting any taller!!!')

    def pop_stack(self, state=None):
        """Removes one stack frame."""
        self.stack.pop()
        self.state = self.stack[-1].state if state is None else state
        self.ast = self.stack[-1].return_pt

    def lookup_name(self, name):
        """Dynamic scope lookup."""
        for frame in reversed(self.stack):
            try:
                return frame[name]
            except KeyError:
                continue
        try:
            return self.bltin_vars[name]
        except KeyError:
            raise NameError('Symbol {} not found'.format(name))

    def assign_name(self, name, value):
        """Dynamic scope assignment."""
        try:
            self.stack[-1][name] = value
        except IndexError:
            raise RuntimeError('All the stack frames died, what the fuck happened?')

    def is_tail_call(self, eval_stack):
        """Returns True if the currently evaluated AST node is a tail call."""
        eval_len = len(eval_stack)
        if eval_len == 2 and isinstance(eval_stack[0], DivulgateStmt):
            # Top expression in a return statement is a function call
            return True
        if eval_len == 1 and self.state == self.FUNCEXEC_STATE:
            # The statement being evaluated in a function is another call
            ast_len = len(self.ast)
            if self.ast.index >= ast_len:
                # Execution points outside function body
                return True
            node = self.ast[self.ast.index]
            if isinstance(node, CondJumpStmt) and node.clause is None:
                # Execution points to an unconditional jump
                if self.ast.index + node.height + 1 >= ast_len:
                    # Jump points outside function body
                    return True
        return False

    def trampoline(self, eval_stack, return_val=None):
        """Evaluation trampoline that models recursive AST node calls."""
        ctrl_name = self.ast.ctrl_name
        # If return_val is not None, a value was returned from a function.
        if return_val is not None:
            # Pass the return value to the caller.
            eval_stack[-1].return_val = return_val
        while True:
            # Execution must continue from the expression on top of the stack.
            try:
                # Evaluate the expression at the top of the stack.
                callback, value = next(eval_stack[-1].eval_gen)
            except SymbolDeath:
                if not self.lookup_name('THIS'):
                    # If THIS dies, end execution.
                    sys.exit(0)
                elif not self.lookup_name(ctrl_name):
                    # print(self.stack)
                    # If the AST control name dies, reraise.
                    raise
                callback, value = None, None
            # print(value if value is not None else '')
            if callback:
                # If there's a callback, see if it's a function call.
                if not isinstance(callback, AthFunction):
                    # Push evaluation stack if it's not a function.
                    eval_stack.append(callback.iterate(self))
                    continue
                # If it is a tail call, don't push the stack.
                if self.is_tail_call(eval_stack):
                    self.stack[-1].scope_vars = value
                    self.stack[-1].eval_stack = []
                    return iter(callback.body)
                # If the callback is a function, move to function state.
                eval_stack.pop()
                self.stack[-1].eval_stack = eval_stack
                self.push_stack(self.FUNCEXEC_STATE, value)
                return iter(callback.body)
            # If there's no callback, this expression is done.
            eval_stack.pop()
            try:
                # Use the return value in the next expression.
                eval_stack[-1].return_val = value
            except IndexError:
                # If there are no more statements, move on.
                self.stack[-1].eval_stack = []
                return value

    def execute(self):
        """Executes an interpreter given an ast attribute."""
        count = 0
        try:
            while True:
                if self.state == self.TOPLEVEL_STATE:
                    try:
                        node = next(self.ast)
                    except StopIteration:
                        # Reset AST iteration state.
                        iter(self.ast)
                        # Prevent infinite iteration from toplevel.
                        if count == 1025:
                            echo_error(
                                'UnboundATHLoopError: THIS.DIE() not called'
                                )
                        count += 1
                        continue
                elif self.state == self.TILDEATH_STATE:
                    try:
                        node = next(self.ast)
                    except StopIteration:
                        if not self.lookup_name(self.ast.ctrl_name):
                            # If the control name died, kill the loop.
                            self.pop_stack()
                        else:
                            # Reset AST iteration state when continuing loop.
                            iter(self.ast)
                        continue
                elif self.state == self.TILALIVE_STATE:
                    try:
                        node = next(self.ast)
                    except StopIteration:
                        if self.lookup_name(self.ast.ctrl_name):
                            # If the control name lives, kill the loop.
                            self.pop_stack()
                        else:
                            # Reset AST iteration state when continuing loop.
                            iter(self.ast)
                        continue
                elif self.state == self.FUNCEXEC_STATE:
                    try:
                        node = next(self.ast)
                    except StopIteration:
                        self.pop_stack(self.FXRETURN_STATE)
                        return_val = AthSymbol(False)
                        continue
                elif self.state == self.FXRETURN_STATE:
                    if not self.stack[-1].eval_stack:
                        self.state = self.stack[-1].state
                        continue
                    try:
                        value = self.trampoline(self.stack[-1].eval_stack, return_val)
                    except SymbolDeath:
                        self.state = self.stack[-1].state
                    else:
                        if isinstance(value, AthAstList):
                            self.ast = value
                        elif isinstance(self.ast[self.ast.index-1], DivulgateStmt):
                            self.pop_stack(self.FXRETURN_STATE)
                            return_val = value
                        else:
                            self.state = self.stack[-1].state
                    continue
                # print(node.__class__)
                # Evalutate execution state.
                if isinstance(node, TildeAthLoop):
                    # Do not allow entry into the loop when the variable state matches
                    # failure condition.
                    if self.lookup_name(node.grave.name).alive == node.state:
                        continue
                    # Add stack frame and replace ast reference.
                    self.push_stack(1 + int(node.state))
                    self.ast = iter(node.body)
                    continue
                # print(self.stack[-1])
                try:
                    value = self.trampoline([node.iterate(self)])
                except SymbolDeath:
                    if self.state != self.TILALIVE_STATE:
                        # Death as break
                        self.pop_stack()
                        if self.state == self.FUNCEXEC_STATE:
                            return_val = AthSymbol(False)
                            self.state = self.FXRETURN_STATE
                    else:
                        # print(self.stack[-1])
                        # Death as continue
                        iter(self.ast)
                    continue
                if isinstance(value, AthAstList):
                    self.ast = value
                elif isinstance(node, DivulgateStmt):
                    self.pop_stack(self.FXRETURN_STATE)
                    return_val = value
        except KeyboardInterrupt:
            print('\n'.join(repr(frame.scope_vars) for frame in self.stack))
            raise
        except Exception:
            print('dude its ESCAPING TO THE SIDE, stop it!!!!')
            raise

    def interpret(self, fname):
        if not fname.endswith('.~ATH'):
            echo_error('IOError: script must be a ~ATH file')
        with open(os.path.join('script', fname), 'r') as script_file:
            script = script_file.read()
        tokens = ath_lexer(script)
        try:
            self.ast = ath_parser(tokens, 0).value
        except SyntaxError:
            echo_error('RuntimeError: the parser could not understand the script')
        self.ast.flatten()

        for stmt in self.ast:
            if isinstance(stmt, TildeAthLoop):
                self.ast.index = 0
                break
        else:
            echo_error('RuntimeError: no ~ATH loop found in top-level script')

        with open('ast_'+fname[:-4]+'py', 'w') as py_file:
            py_file.write('#!/usr/bin/env python\nfrom athast import *\n')
            py_file.write('from tildeath import TildeAthInterp\n\n')
            py_file.write('interp = TildeAthInterp()\n')
            py_file.write('interp.ast = ' + repr(self.ast))
            py_file.write('\ninterp.execute()\n')
        self.execute()


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
    try:
        ath_interp.interpret(cmdargs.script)
    except FileNotFoundError:
        raise IOError(
            'File {} not found in script directory'.format(cmdargs.script)
            )
