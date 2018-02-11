#!/usr/bin/env python
import os
import sys
from pathlib import Path
from argparse import ArgumentParser
from symbol import (
    SymbolDeath, AthFunction, AthSymbol, 
    BuiltinSymbol, ThisSymbol, NULL,
    )
from athast import (
    CondJumpStmt, ExecuteStmt, DivulgateStmt, TildeAthLoop
    )
from athparser import ath_parser

__version__ = '1.4.4 Test Build'
__author__ = 'virtuNat'


def echo_error(msg):
    sys.stderr.write(msg)
    sys.exit(1)


def write_astfile(fname, ast):
    with open('ast_'+fname[:-4]+'py', 'w') as astfile:
        astfile.write(
            TildeAthInterp.REPRESENTATION.format(ast, fname, fname[:-5])
            )


def parse_all():
    print('Writing ~ATH scripts to local python ast script...')
    for pathname in Path('./script').glob('*.~ATH'):
        fname = os.path.basename(pathname)
        print('Processing:', fname)
        with open(pathname, 'r') as athfile:
            ast = ath_parser(athfile.read())
        write_astfile(fname, ast)
    print('Done!')


class AthStackFrame(object):
    """Keeps a record of all symbols declared in a given scope.
    ~ATH implements dynamic scope, so be wary when coding in it!

    It also keeps AST execution and evaluation state, so that the
    execution and evaluation loops know where to continue from.
    """
    __slots__ = ('scope_vars', 'ast', 'state', 'eval_stack')

    def __init__(self, scope_vars=None, ast=None, state=0, eval_stack=[]):
        if not scope_vars:
            self.scope_vars = {}
        else:
            self.scope_vars = scope_vars
        self.ast = ast
        self.state = state
        self.eval_stack = eval_stack

    def __str__(self):
        item = self.ast[self.ast.index-1]
        if isinstance(item, TildeAthLoop):
            itemstr = repr(item.__class__.__name__)
        else:
            itemstr = repr(item)
        return (
            '<~ATH StackFrame>\n'
            'Scope: {},\n'
            'Return Node: {},\n'
            'State: {},\n'
            'Evaluation: {},\n'
            ).format(
            self.scope_vars,
            itemstr,
            self.state,
            self.eval_stack,
            )

    def __repr__(self):
        return '\nAthStackFrame({}, {}, {}, {})'.format(
            self.state, self.ast, self.scope_vars, self.eval_stack
            )


class TildeAthInterp(object):
    """Runs the finite state machine governing ~ATH program behavior."""
    __slots__ = ('modules', 'bltin_vars', 'stack', 'ast', 'state')
    # Execution state final variables.
    TOPLEVEL_STATE = 0 # Toplevel imperative execution
    TILDEATH_STATE = 1 # Looping in breakable death-checking loops
    TILALIVE_STATE = 2 # Looping in continuable life-checking loops
    FUNCEXEC_STATE = 3 # Inside a function body
    FXRETURN_STATE = 4 # Returning from a function
    # Base string for AST representation that can be run in python.
    REPRESENTATION = (
        '#!/usr/bin/env python\n'
        'from athast import *\n'
        'from symbol import ThisSymbol\n'
        'from tildeath import TildeAthInterp\n\n'
        'ast = {!r}\n'
        'interp = TildeAthInterp()\n'
        'interp.bltin_vars[\'THIS\'] = ThisSymbol({!r}, ast)\n'
        'interp.execute(ast)\n'
        )

    def __init__(self):
        self.modules = {}
        self.bltin_vars = {
            'NULL': NULL,
            'DIE': BuiltinSymbol(),
            '~ATH': BuiltinSymbol(),
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

    def push_stack(self, ast, state, init_dict={}, eval_stack=[]):
        """Adds one stack frame and handles most of the internal state changes."""
        self.stack[-1].eval_stack = eval_stack
        self.stack[-1].state = self.state
        self.stack.append(AthStackFrame(init_dict, ast, state))
        ast_iterator = iter(ast)
        self.ast = ast_iterator
        self.stack[-1].ast = ast_iterator
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
        """Removes one stack frame and resets internal execution state."""
        self.stack.pop()
        self.state = self.stack[-1].state if state is None else state
        self.ast = self.stack[-1].ast

    def lookup_name(self, name):
        """Dynamic scope lookup."""
        for frame in reversed(self.stack):
            try:
                return frame.scope_vars[name]
            except KeyError:
                continue
        try:
            return self.bltin_vars[name]
        except KeyError as keyerr:
            raise NameError('Symbol {} not found'.format(name)) from keyerr

    def assign_name(self, name, value):
        """Dynamic scope assignment."""
        try:
            self.stack[-1].scope_vars[name] = value
        except IndexError:
            raise RuntimeError('All the stack frames died, what the fuck happened?')

    def is_tail_call(self, eval_len):
        """Returns True if the currently evaluated AST node is a tail call."""
        if eval_len == 2 and isinstance(self.ast[self.ast.index-1], DivulgateStmt):
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
        # If return_val is not None, a value was returned from a function.
        value = return_val
        while True:
            # Execution must continue from the expression on top of the stack.
            try:
                # Evaluate the expression at the top of the stack.
                node, value = eval_stack[-1].send(value)
            except IndexError:
                # If there are no more expressions, move on.
                return value
            except SymbolDeath as death_exc:
                if 'THIS' in death_exc.args[0]:
                    # If THIS dies, end execution.
                    sys.exit(0)
                elif self.ast.ctrl_name in death_exc.args[0]:
                    # If the AST control name dies, evaluate state.
                    if self.state == self.TILALIVE_STATE:
                        # Death as continue
                        iter(self.ast)
                    elif self.state == self.FUNCEXEC_STATE:
                        # Death as end function
                        self.pop_stack()
                        eval_stack = self.stack[-1].eval_stack
                        value = AthSymbol(False)
                        continue
                    else:
                        # Death as break  
                        self.pop_stack()
                    return AthSymbol(False)
                node, value = None, None
            if node:
                # If there's a node, see if it's a function call.
                if not isinstance(node, AthFunction):
                    # Push evaluation stack if it's not a function.
                    eval_stack.append(node.eval(self))
                    continue
                if self.is_tail_call(len(eval_stack)):
                    # If it is a tail call, don't push the stack.
                    self.stack[-1].scope_vars = value
                    self.stack[-1].eval_stack.clear()
                    ast = iter(node.body)
                    self.stack[-1].ast = ast
                    self.ast = ast
                else:
                    # If the node is a function, move to function state.
                    eval_stack.pop()
                    self.push_stack(node.body, self.FUNCEXEC_STATE, value, eval_stack)
                return None
            # If there's no node, this expression is done.
            eval_stack.pop()

    def execute(self, ast):
        """Executes an interpreter given an ast attribute."""
        # Initialize unbound loop counter.
        count = 0
        # Initialize AST iterator references.
        self.ast = iter(ast)
        self.stack[0].ast = self.ast
        try:
            while True:
                while self.state == self.FXRETURN_STATE:
                    # If returning from a function:
                    frame = self.stack[-1]
                    if not frame.eval_stack:
                        # Nothing left to evaluate, use frame state and proceed.
                        self.state = frame.state
                        del frame
                        break
                    # Continue the paused execution with the returned value.
                    return_val = self.trampoline(frame.eval_stack, return_val)
                    if isinstance(node, DivulgateStmt) and return_val is not None:
                        # Another return, move back one stack frame again.
                        self.pop_stack(self.FXRETURN_STATE)
                        node = self.ast[self.ast.index-1]
                        continue
                    # Not a return, use frame state and proceed.
                    self.state = frame.state
                    del frame
                # Get the next statement AST node.
                try:
                    node = next(self.ast)
                except StopIteration:
                    # Evaluate what to do after reaching the end based on state.
                    if self.state == self.TOPLEVEL_STATE:
                        # Reset AST iteration state if exiting toplevel.
                        iter(self.ast)
                        # Prevent infinite iteration from toplevel.
                        if count >= 1025:
                            echo_error(
                                'UnboundATHLoopError: THIS.DIE() not called'
                                )
                        count += 1
                    elif self.state == self.TILDEATH_STATE:
                        # Breakable exit-on-death loops.
                        if not self.lookup_name(self.ast.ctrl_name):
                            # If the control name died, kill the loop.
                            self.pop_stack()
                        else:
                            # Reset AST iteration state when continuing loop.
                            iter(self.ast)
                    elif self.state == self.TILALIVE_STATE:
                        # Continuable exit-on-life loops.
                        if self.lookup_name(self.ast.ctrl_name):
                            # If the control name lives, kill the loop.
                            self.pop_stack()
                        else:
                            # Reset AST iteration state when continuing loop.
                            iter(self.ast)
                    elif self.state == self.FUNCEXEC_STATE:
                        # If the function exits without a return, return NULL.
                        self.pop_stack(self.FXRETURN_STATE)
                        return_val = AthSymbol(False)
                    continue
                if isinstance(node, TildeAthLoop):
                    # Do not allow entry into the loop when the variable state matches
                    # failure condition.
                    if self.lookup_name(node.body.ctrl_name).alive == node.state:
                        continue
                    # Add stack frame and replace ast reference.
                    self.push_stack(node.body, 1 + int(node.state))
                    continue
                # Evaluate the AST node's set of expressions and logic.
                return_val = self.trampoline([node.eval(self)])
                if isinstance(node, DivulgateStmt) and return_val is not None:
                    # Return from a function.
                    self.pop_stack(self.FXRETURN_STATE)
                    node = self.ast[self.ast.index-1]
        except KeyboardInterrupt:
            print('\n'.join(repr(frame.scope_vars) for frame in self.stack))
            raise
        except Exception:
            print('\ndude its ESCAPING TO THE SIDE, stop it!!!!')
            raise

    def interpret(self, fname):
        if not fname.endswith('.~ATH'):
            echo_error('IOError: script must be a ~ATH file')
        with open(os.path.join('script', fname), 'r') as script_file:
            script = script_file.read()
            ast = ath_parser(script)
        write_astfile(fname, self.ast)
        # Initialize THIS.
        self.bltin_vars['THIS'] = ThisSymbol(fname, ast)
        self.execute(ast)


if __name__ == '__main__':
    cmdparser = ArgumentParser(
        description='a fanmande ~ATH interpreter by virtuNat',
        )
    cmdgroup = cmdparser.add_mutually_exclusive_group()
    cmdgroup.add_argument(
        '-e', '--execute',
        help='parse and run athfname.~ATH in the script directory',
        metavar='athfname',
        )
    cmdgroup.add_argument(
        '-a', '--parse_all',
        help='parse all ~ATH files in the script directory',
        action='store_true',
        )
    cmdargs = cmdparser.parse_args()
    if cmdargs.parse_all:
        parse_all()
    elif cmdargs.execute:
        ath_interp = TildeAthInterp()
        try:
            ath_interp.interpret(cmdargs.execute)
        except FileNotFoundError:
            raise IOError(
                'File {} not found in script directory'.format(cmdargs.execute)
                )
    else:
        print('usage: tildeath.py [-h] [-e athfname | -a]')
