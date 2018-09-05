#!/usr/bin/env python
import os
import sys
from pathlib import Path
from argparse import ArgumentParser
from athsymbol import AthSymbol, SymbolDeath
from athstmt import(
	ath_builtins, ThisSymbol,
    LiteralToken, IdentifierToken, 
	AthStatement, AthTokenStatement, TildeAthLoop,
	)
from athgrammar import ath_parser

__version__ = '1.5.0 Test Build'
__author__ = 'virtuNat'


class AthStackFrame(object):
    """Keeps a record of all symbols declared in a given scope.
    ~ATH implements dynamic scope, so be wary when coding in it!

    It also keeps AST execution and evaluation state, so that the
    execution and evaluation loops know where to continue from.
    """
    __slots__ = ('scope_vars', 'iter_nodes', 'exec_state', 'eval_state')

    def __init__(self, scope_vars=None, iter_nodes=None, exec_state=0, eval_state=[]):
        self.scope_vars = scope_vars or {}
        self.iter_nodes = iter_nodes
        self.exec_state = exec_state
        self.eval_state = eval_state

    def __str__(self):
        return (
            '<~ATH StackFrame>\n'
            'Variables in Scope: {},\n'
            'Node Iteration: {},\n'
            'Execution State: {},\n'
            'Evaluation State: {},\n'
            ).format(
            self.scope_vars,
            self.iter_nodes,
            self.exec_state,
            self.eval_state,
            )

    def __repr__(self):
        return '\nAthStackFrame({}, {}, {}, {})'.format(
            self.scope_vars, self.ast, self.exec_state, self.eval_state
            )

    def get_current(self):
        idx = self.iter_nodes.index
        return self.iter_nodes.stmts[idx - 1 if idx > 0 else 0]


class TildeAthInterp(object):
    """Runs the finite state machine governing ~ATH program behavior."""
    __slots__ = ('modules', 'stack', 'nodes', 'exec_state')
    # Execution state final variables.
    TOPLEVEL_STATE = 0 # Toplevel imperative execution
    TILDEATH_STATE = 1 # Looping in breakable death-checking loops
    TILALIVE_STATE = 2 # Looping in continuable life-checking loops
    FUNCEXEC_STATE = 3 # Inside a function body
    # Base string for AST representation that can be run in python.
    REPRESENTATION = (
        '#!/usr/bin/env python\n'
        'from athstmt import *\n'
        'from athinterpreter import TildeAthInterp\n\n'
        'stmts = {}\n'
        'TildeAthInterp().exec_stmts({!r}, stmts)\n'
        )

    def __init__(self):
        self.modules = {}
        self.stack = []
        # Currently evaluating AST list.
        self.nodes = None
        # Current execution state.
        self.exec_state = 0

    def get_symbol(self, token):
        for frame in reversed(self.stack):
            try:
                return frame.scope_vars[token]
            except KeyError:
                pass
        try:
            return ath_builtins[token]
        except KeyError as exc:
            raise NameError('Could not find symbol {}'.format(token)) from exc

    def set_symbol(self, token, value):
        try:
            self.stack[-1].scope_vars[token] = value
        except IndexError:
            raise RuntimeError('All stack frames destroyed!!!!!')

    def eval_stmt(self, ret_value=None):
        eval_state = self.stack[-1].eval_state
        node = eval_state[-1]
        if ret_value is not None:
            node.set_argv(ret_value)
        while True:
            # print(node.stmt, node.argv)
            print(eval_state)
            try:
                arg = node.get_arg()
            except IndexError:
                try:
                    ret_value = node.execute(self)
                except SymbolDeath as exc:
                    if 'THIS' in exc.args[0]:
                        sys.exit(0)
                    elif self.stack[-1].iter_nodes.pendant in exc.args[0]:
                        state = self.stack[-1].exec_state
                        if state == self.TILALIVE_STATE:
                            self.stack[-1].iter_nodes.reset()
                        elif state == self.FUNCEXEC_STATE:
                            pass
                        else:
                            pass
                else:
                    if eval_state:
                        eval_state.pop()
                        continue
                    print('End!')
                    return ret_value
            else:
                if isinstance(arg, LiteralToken):
                    node.set_argv(arg.value)
                elif isinstance(arg, IdentifierToken):
                    node.set_argv(self.get_symbol(arg.name))
                elif isinstance(arg, AthTokenStatement):
                    pass
                elif isinstance(arg, AthStatement):
                    eval_state.append(arg.prepare())


    def eval_return(self, ret_value=None):
        while True:
            frame = self.stack[-1]
            if not frame.eval_state:
                return
            ret_value = self.eval_stmt(frame.eval_state, ret_value)
            if not (ret_value is not None
                and frame.get_current().name == 'DIVULGATE'
                ):
                return
            self.stack.pop()

    def exec_stmts(self, fname, stmts):
        athloops = 0
        while True:
            try:
                ath_builtins['THIS'] = ThisSymbol(fname, stmts)
                self.stack.append(AthStackFrame(iter_nodes=stmts.iter_nodes()))
                ast = self.stack[-1].iter_nodes
                while True:
                    try:
                        node = next(ast)
                    except StopIteration:
                        state = self.stack[-1].exec_state
                        if state == self.TOPLEVEL_STATE:
                            sys.exit(0)
                            athloops += 1
                            if athloops >= 612:
                                sys.stderr.write(
                                    'UnboundedLoopError: THIS.DIE() never called'
                                    )
                            else:
                                ast.reset()
                        elif state == self.FUNCEXEC_STATE:
                            self.stack.pop()
                            self.eval_return(AthSymbol(False))
                            ast = self.stack[-1].iter_nodes
                        else:
                            if (self.get_symbol(ast.pendant).alive
                                == bool(state - self.TILDEATH_STATE)
                                ):
                                self.stack.pop()
                                ast = self.stack[-1].iter_nodes
                            else:
                                sys.exit(0)
                                ast.reset()
                        continue
                    # print(repr(node))
                    if isinstance(node, TildeAthLoop):
                        if self.get_symbol(node.body.pendant).alive == node.state:
                            continue
                        self.stack.append(AthStackFrame(
                            iter_nodes=node.body.iter_nodes(),
                            exec_state=self.TILDEATH_STATE + int(node.state),
                            ))
                        ast = self.stack[-1].iter_nodes
                        continue
                    self.stack[-1].eval_state.append(node.prepare())
                    ret_value = self.eval_stmt()
                    if (self.stack[-1].get_current().name == 'DIVULGATE'
                        and ret_value is not None
                        ):
                        self.stack.pop()
                        self.eval_return(ret_value)
            except KeyboardInterrupt:
                break # override
                self.stack.clear()
                continue
            except Exception as exc:
                raise exc

    def write_ast(self, fname, stmts):
        with open('ast_'+fname[:-4]+'py', 'w') as astfile:
            astfile.write(
                self.REPRESENTATION.format(stmts.format(), fname)
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

    def interpret(self, fname):
        if not fname.endswith('.~ATH'):
            sys.stderr.write('IOError: script must be a ~ATH file')
            sys.exit(1)
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
    cmdargs = cmdparser.parse_args()
    ath_interp = TildeAthInterp()
    if cmdargs.athfname == 'all':
        ath_interp.write_all()
    else:
        try:
            ath_interp.interpret(cmdargs.athfname)
        except FileNotFoundError:
            raise IOError(
                'File {} not found in script directory'.format(cmdargs.execute)
                )
