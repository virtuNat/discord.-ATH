#!/usr/bin/env python
import os
import sys
from pathlib import Path
from argparse import ArgumentParser
from athsymbol import AthSymbol, SymbolDeath, AthBuiltinFunction, AthCustomFunction
from athstmt import(
	ath_builtins, ThisSymbol,
    LiteralToken, IdentifierToken, 
	AthStatement, AthTokenStatement, TildeAthLoop,
	)
from athgrammar import ath_parser

__version__ = '1.6.1'
__author__ = 'virtuNat'


class AthStackFrame(object):
    """Keeps a record of all symbols declared in a given scope.
    ~ATH implements dynamic scope, so be wary when coding in it!

    It also keeps AST execution and evaluation state, so that the
    execution and evaluation loops know where to continue from.
    """
    __slots__ = ('scope_vars', 'iter_nodes', 'exec_state', 'eval_state')

    def __init__(self, scope_vars=None, iter_nodes=None, exec_state=0, eval_state=None):
        self.scope_vars = scope_vars or {}
        self.iter_nodes = iter_nodes
        self.exec_state = exec_state
        self.eval_state = eval_state or []

    def __str__(self):
        return (
            f'<~ATH StackFrame>\n'
            f'Variables in Scope: {self.scope_vars},\n'
            f'Node Iteration: {self.iter_nodes},\n'
            f'Execution State: {self.exec_state},\n'
            f'Evaluation State: {self.eval_state},\n'
            )

    def __repr__(self):
        return f'\nAthStackFrame{tuple(getattr(self, slot) for slot in self.__slots__)}'

    def get_current(self):
        idx = self.iter_nodes.index
        return self.iter_nodes.stmts[idx - 1 if idx > 0 else 0]


class TildeAthInterp(object):
    """Runs the finite state machine governing ~ATH program behavior."""
    __slots__ = ('modules', 'stack', 'nodes', 'ast', 'exec_state')
    # Execution state final variables.
    TOPLEVEL_STATE = 0 # Toplevel imperative execution
    TILDEATH_STATE = 1 # Looping in breakable death-checking loops
    TILALIVE_STATE = 2 # Looping in continuable life-checking loops
    FUNCEXEC_STATE = 3 # Inside a function body

    def __init__(self):
        self.modules = {}
        self.stack = []
        # Currently evaluating AST list.
        self.nodes = None
        # Current item in the AST list.
        self.ast = None
        # Current execution state.
        self.exec_state = 0
        
    def get_symbol(self, token):
        """Search the stack frames top first, then the builtins."""
        for frame in reversed(self.stack):
            try:
                return frame.scope_vars[token]
            except KeyError:
                pass
        try:
            return ath_builtins[token]
        except KeyError as exc:
            raise NameError(f'Could not find symbol {token}') from exc

    def set_symbol(self, token, value):
        """Attempt to add symbol to the top of the stack."""
        try:
            self.stack[-1].scope_vars[token] = value
        except IndexError:
            raise RuntimeError('All stack frames destroyed!!!!!')

    def is_tail_call(self, eval_len):
        """Returns True if the currently evaluated AST node is a tail call."""
        if eval_len == 2 and self.ast.get_current().name == 'DIVULGATE':
            # Top expression in a return statement is a function call
            return True
        if eval_len == 1 and self.stack[-1].exec_state == self.FUNCEXEC_STATE:
            # The statement being evaluated in a function is another call
            if self.ast.index >= len(self.ast.stmts):
                # Execution points outside function body
                return True
            node = self.ast.get_current()
            if node.name == 'CondiJump' and node.args[0] is None:
                # Execution points to an unconditional jump
                if self.ast.index + node.args[1] + 1 >= len(self.ast):
                    # Jump points outside function body
                    return True
        return False

    def eval_stmt(self, ret_value=None):
        # Statement evaluation trampoline.
        eval_state = self.stack[-1].eval_state
        node = eval_state[-1]
        if ret_value is not None:
            node.set_argv(ret_value)
        while True:
            try:
                # Try to get the next argument AST node from the expression.
                arg = node.get_arg()
            except IndexError:
                # If there are no more left, execute the associated function.
                try:
                    ret_value = node.execute(self)
                except SymbolDeath as exc:
                    # In a DIE statement, SymbolDeath will be raised.
                    if 'THIS' in exc.args[0]:
                        # End the program only when THIS is killed.
                        sys.exit(0)
                    elif self.stack[-1].iter_nodes.pendant in exc.args[0]:
                        # If the current frame's control variable is killed, evaluate:
                        state = self.stack[-1].exec_state
                        if state == self.TILALIVE_STATE:
                            # If in keep-dead loop, force the loop to repeat.
                            self.stack[-1].iter_nodes.reset()
                        else:
                            # Otherwise, pop the execution stack and move on.
                            self.stack.pop()
                            self.ast = self.stack[-1].iter_nodes
                            if state == self.FUNCEXEC_STATE:
                                # If popping from a function, evaluate from here instead.
                                eval_state = self.stack[-1].eval_state
                                ret_val = AthSymbol(False)
                                continue
                    eval_state.clear()
                    return AthSymbol(False)
                except Exception as exc:
                    # When other errors occur, pass the exception upward.
                    raise exc
                else:
                    # When the function has finished, move down the evaluation stack.    
                    if node.stmt.name == 'EXECUTE': # Function call
                        eval_state.pop()
                        func, scope_vars = ret_value
                        if isinstance(func, AthBuiltinFunction):
                            node = eval_state[-1]
                            node.set_argv(func(self, *scope_vars))
                            continue
                        if self.is_tail_call(len(eval_state) + 1):
                            frame = self.stack[-1]
                            frame.scope_vars = scope_vars
                            frame.iter_nodes = func.body.iter_nodes()
                            frame.exec_state = self.FUNCEXEC_STATE
                            eval_state.clear()
                        else:
                            self.stack.append(AthStackFrame(
                                scope_vars=scope_vars,
                                iter_nodes=func.body.iter_nodes(),
                                exec_state=self.FUNCEXEC_STATE,
                                ))
                        self.ast = self.stack[-1].iter_nodes
                        return None
                    if len(eval_state) > 1:
                        eval_state.pop()
                        node = eval_state[-1]
                        node.set_argv(ret_value)
                        continue
                    # If this is the last expression in the stack, return to the AST.
                    eval_state.clear()
                    return ret_value
            else:
                # If there is an argument left to evaluate, deal with it first.
                if arg is None or isinstance(arg, (int, str, AthCustomFunction)):
                    # Name, Number, Function, and Empty items are passed as is.
                    node.set_argv(arg)
                elif isinstance(arg, LiteralToken):
                    # Tokens pass their values.
                    node.set_argv(arg.value)
                elif isinstance(arg, IdentifierToken):
                    # Name tokens pass either their names or evaluate their values.
                    if node.is_name_arg():
                        node.set_argv(arg.name)
                    else:
                        node.set_argv(self.get_symbol(arg.name))
                elif isinstance(arg, AthStatement):
                    # Evaluate expressions for their values before passing the result.
                    node = arg.prepare()
                    eval_state.append(node)

    def eval_return(self, ret_value):
        while True:
            frame = self.stack[-1]
            self.ast = frame.iter_nodes
            if not frame.eval_state:
                return
            ret_value = self.eval_stmt(ret_value)
            if not (ret_value is not None
                and frame.get_current().name == 'DIVULGATE'
                ):
                return
            self.stack.pop()

    def exec_stmts(self, fname, stmts):
        # AST Execution trampoline.
        athloops = 0
        while True:
            try:
                ath_builtins['THIS'] = ThisSymbol(fname, stmts)
                self.stack.append(AthStackFrame(iter_nodes=stmts.iter_nodes()))
                self.ast = self.stack[-1].iter_nodes
                while True:
                    try:
                        node = next(self.ast)
                    except StopIteration:
                        state = self.stack[-1].exec_state
                        if state == self.TOPLEVEL_STATE:
                            sys.exit(0) # override
                            athloops += 1
                            if athloops >= 612:
                                sys.stderr.write(
                                    'UnboundedLoopError: THIS.DIE() never called'
                                    )
                            else:
                                self.ast.reset()
                        elif state == self.FUNCEXEC_STATE:
                            self.stack.pop()
                            self.eval_return(AthSymbol(False))
                            self.ast = self.stack[-1].iter_nodes
                        else:
                            if (self.get_symbol(self.ast.pendant).alive
                                == bool(state - self.TILDEATH_STATE)
                                ):
                                self.stack.pop()
                                self.ast = self.stack[-1].iter_nodes
                            else:
                                self.ast.reset()
                        continue
                    # print(repr(node))
                    if isinstance(node, TildeAthLoop):
                        if self.get_symbol(node.body.pendant).alive == node.state:
                            continue
                        self.stack.append(AthStackFrame(
                            iter_nodes=node.body.iter_nodes(),
                            exec_state=self.TILDEATH_STATE + int(node.state),
                            ))
                        self.ast = self.stack[-1].iter_nodes
                        continue
                    self.stack[-1].eval_state.append(node.prepare())
                    ret_value = self.eval_stmt()
                    if (self.stack[-1].get_current().name == 'DIVULGATE'
                        and ret_value is not None
                        ):
                        self.stack.pop()
                        self.eval_return(ret_value)
            except KeyboardInterrupt:
                raise # override
                self.stack.clear()
                continue
            except Exception as exc:
                raise exc

    def write_ast(self, fname, stmts):
        with open(f'ast_{fname[:-4]}py', 'w') as astfile:
            astfile.write(
                f'#!/usr/bin/env python\n'
                f'from athstmt import *\n'
                f'from athinterpreter import TildeAthInterp\n\n'
                f'stmts = {stmts.format()}\n\n'
                f"if __name__ == '__main__':\n"
                f'    TildeAthInterp().exec_stmts({fname!r}, stmts)\n'
                )

    def write_all(self):
        print('Writing ~ATH scripts to local python ast script...')
        for pathname in Path('./script').glob('*.~ATH'):
            fname = os.path.basename(pathname)
            print('Processing:', fname)
            with open(pathname, 'r') as athfile:
                stmts = ath_parser(athfile.read())
            self.write_ast(fname, stmts)
        print('Done!')

    def interpret(self, fname, force):
        if not fname.endswith('.~ATH'):
            sys.stderr.write('IOError: script must be a ~ATH file')
            sys.exit(IOError)
        if not force and os.path.isfile(f'ast_{fname[:-4]}py'):
            ast = __import__(f'ast_{fname[:-5]}').stmts
        else:
            with open(os.path.join('script', fname), 'r') as script_file:
                ast = ath_parser(script_file.read())
        self.write_ast(fname, ast)
        self.exec_stmts(fname, ast)


if __name__ == '__main__':
    cmdparser = ArgumentParser(
        description='a fanmande ~ATH interpreter by virtuNat',
        )
    cmdparser.add_argument(
        'athfname',
        help='parse and run athfname.~ATH in the script directory',
        metavar='athfname',
        )
    cmdparser.add_argument(
        '-f', '--force',
        action='store_true',
        help='parse directly from the script',
        )
    cmdargs = cmdparser.parse_args()
    ath_interp = TildeAthInterp()
    if cmdargs.athfname == 'all':
        ath_interp.write_all()
    else:
        try:
            ath_interp.interpret(cmdargs.athfname, cmdargs.force)
        except FileNotFoundError:
            raise IOError(
                f'File {cmdargs.athfname} not found in script directory'
                )
