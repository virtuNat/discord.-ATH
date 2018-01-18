"""~ATH's Abstract Syntax Tree definition.

This contains the data structure of ~ATH syntax and its variables,
as well as their implementations. This does not, however, contain
the literals used for lexing.
"""
import re
import operator
from functools import partial
from symbol import (
    isAthValue, SymbolError,
    AstExpr, AthSymbol, BuiltinSymbol, AthFunction,
    SymbolDeath, DivulgateBack
    )


class EvalExpr(AstExpr):
    """Superclass to all expressions that are not statements."""
    __slots__ = ()


class NumExpr(EvalExpr):
    """Superclass of both integers and floats."""
    __slots__ = ('num',)

    def __repr__(self):
        return '{}({!r})'.format(self.__class__.__name__, self.num)

    def eval(self, fsm):
        yield None, self.num


class FloatExpr(NumExpr):
    """Holds float number values."""
    __slots__ = ()

    def __init__(self, num):
        self.num = float(num)


class IntExpr(NumExpr):
    """Holds integer number values."""
    __slots__ = ()

    def __init__(self, num):
        self.num = int(num)


class VarExpr(EvalExpr):
    """Contains a symbol name."""
    __slots__ = ('name',)

    def __init__(self, name):
        self.name = name

    def eval(self, fsm):
        yield None, fsm.lookup_name(self.name)


class StringExpr(EvalExpr):
    """Holds string values."""
    __slots__ = ('string',)

    def __init__(self, string):
        self.string = string

    def eval(self, fsm):
        yield None, self.string


def cmp_opr(lval, rval, op):
    if isAthValue(lval):
        lval = AthSymbol(bool(lval), left=lval)
    return op(lval, rval)


def bool_not(val):
    if isAthValue(val):
        val = AthSymbol(bool(val), left=val)
    return AthSymbol(not val, val.left, val.right)


def bool_opr(lval, rval, op):
    if isAthValue(lval):
        lval = AthSymbol(bool(lval), left=lval)
    if isAthValue(rval):
        rval = AthSymbol(bool(rval), left=rval)
    if op == '&&':
        return lval and rval
    elif op == '||':
        return lval or rval
    elif op == '^^':
        return (
            lval if lval and not rval else
            rval if rval and not lval else
            AthSymbol(False)
            )
    raise SyntaxError('Invalid comparison operator: {}', op)


def symbol_opr(lval, rval, op):
    if not (isinstance(lval, AthSymbol) and isinstance(rval, AthSymbol)):
        raise TypeError('May only perform living assertions on symbols')
    try:
        if op == '!=!':
            value = lval is rval
        elif op == '?=!':
            value = lval.left.alive and rval.left.alive
        elif op == '!=?':
            value = lval.right.alive and rval.right.alive
        elif op == '~=!':
            value = not (lval.left.alive or rval.left.alive)
        elif op == '!=~':
            value = not (lval.right.alive or rval.right.alive)
        elif op == '~=~':
            value = lval is not rval
        else:
            raise SyntaxError('Invalid comparison operator: {}', op)
    except AttributeError:
        raise SymbolError('The relevant side(s) must be symbols')
    return AthSymbol(value)


class UnaryArithExpr(EvalExpr):
    """Handles unary arithmetic expressions."""
    __slots__ = ('op', 'expr')
    ops = {
        '+': operator.pos,
        '-': operator.neg,
        '~': operator.inv,
        '!': bool_not,
    }

    def __init__(self, args):
        self.op, self.expr = args

    def eval(self, fsm):
        yield self.expr, None
        try:
            result = self.ops[self.op](self.return_val)
        except KeyError:
            raise SyntaxError('Unknown operator: {}', self.op)
        if isinstance(result, AthSymbol):
            yield None, result
        elif isAthValue(result):
            yield None, AthSymbol(left=result)
        raise ValueError('Invalid result: {}'.format(result))


class BinaryExpr(EvalExpr):
    """Handles binary expressions."""
    __slots__ = ('op', 'lexpr', 'rexpr')
    ops = {
        '**': operator.pow,
        '*': operator.mul,
        '/': operator.truediv,
        '/_': operator.floordiv,
        '%': operator.mod,
        '+': operator.add,
        '-': operator.sub,
        '<<': operator.lshift,
        '>>': operator.rshift,
        '&': operator.and_,
        '|': operator.or_,
        '^': operator.xor,
        '<': partial(cmp_opr, op=operator.lt),
        '<=': partial(cmp_opr, op=operator.le),
        '>': partial(cmp_opr, op=operator.gt),
        '>=': partial(cmp_opr, op=operator.ge),
        '==': partial(cmp_opr, op=operator.eq),
        '~=': partial(cmp_opr, op=operator.ne),
        '&&': partial(bool_opr, op='&&'),
        '||': partial(bool_opr, op='||'),
        '^^': partial(bool_opr, op='^^'),
        '!=!': partial(symbol_opr, op='!=!'),
        '?=!': partial(symbol_opr, op='?=!'),
        '!=?': partial(symbol_opr, op='!=?'),
        '~=!': partial(symbol_opr, op='~=!'),
        '!=~': partial(symbol_opr, op='!=~'),
        '~=~': partial(symbol_opr, op='~=~'),
    }

    def __init__(self, op, lexpr, rexpr):
        self.op = op
        self.lexpr = lexpr
        self.rexpr = rexpr

    def eval(self, fsm):
        yield self.lexpr, None
        lval = self.return_val
        yield self.rexpr, None
        try:
            result = self.ops[self.op](lval, self.return_val)
        except KeyError:
            raise SyntaxError('Invalid operator: {}'.format(self.op))
        if isinstance(result, AthSymbol):
            yield None, result
        elif isAthValue(result):
            yield None, AthSymbol(left=result)
        raise ValueError('Invalid result: {}'.format(result))


class Statement(AstExpr):
    """Superclass to all statements."""
    __slots__ = ()


class ControlStmt(Statement):
    """Superclass to all control flow statements."""
    __slots__ = ()

    def eval(self, fsm):
        raise NotImplementedError(
            'The FSM evaluates these statements.'
            )
    

class CondJumpStmt(ControlStmt):
    """Statement that signals the execution to skip a number
    of statements equivalent to its height if the clause is
    evaluated to a living symbol.
    """
    __slots__ = ('clause', 'height')

    def __init__(self, clause, height):
        self.clause = clause
        self.height = height


class ATHASTList(ControlStmt):
    __slots__ = ('stmt_list', 'ctrl_name', 'index')

    def __init__(self, stmt_list, ctrl_name=None):
        self.stmt_list = stmt_list
        self.index = 0
        if not ctrl_name:
            super().__setattr__('ctrl_name', 'THIS')
        else:
            self.ctrl_name = ctrl_name

    def __setattr__(self, name, value):
        if name == 'ctrl_name':
            super().__setattr__(name, value)
            for stmt in self.stmt_list:
                if isinstance(stmt, DebateStmt):
                    stmt.body.ctrl_name = value
                    for alt in stmt.unlesses:
                        alt.body.ctrl_name = value
        else:
            super().__setattr__(name, value)

    def __repr__(self):
        return '{}({}, {!r})'.format(
            self.__class__.__name__, self.stmt_list, self.ctrl_name
            )

    def __getitem__(self, itemidx):
        return self.stmt_list.__getitem__(itemidx)

    def __len__(self):
        return len(self.stmt_list)

    def __iter__(self):
        """Initializes iteration state."""
        self.index = 0
        return self

    def __next__(self):
        """Obtain the next statement from this list."""
        try:
            node = self.stmt_list[self.index]
        except IndexError:
            raise StopIteration
        self.index += 1
        return node

    def flatten(self):
        """Converts DEBATE/UNLESS constructs into conditional jumps."""
        for stmt in self:
            if isinstance(stmt, DebateStmt):
                # Create two lists of statements before and after this one.
                topslice = self.stmt_list[:self.index-1]
                botslice = self.stmt_list[self.index:]
                # Flatten the body of the DEBATE suite.
                stmt.body.flatten()
                # Create a new list of flattened statements.
                bodylen = len(stmt.body)+1 if stmt.unlesses else len(stmt.body)
                midslice = [CondJumpStmt(stmt.clause, bodylen)]
                midslice.extend(stmt.body.stmt_list)
                # For each UNLESS suite that follows:
                unless_idx = 0
                for unless in stmt.unlesses:
                    # Flatten the body.
                    unless.body.flatten()
                    bodylen = len(unless.body) + 1
                    # Add the jump that allows the previous suites to skip this one.
                    midslice.append(CondJumpStmt(None, bodylen))
                    # If this is the last suite, there will be no jump at the end.
                    if unless_idx == len(stmt.unlesses) - 1:
                        bodylen -= 1
                    # Add this suite.
                    midslice.append(CondJumpStmt(unless.clause, bodylen))
                    midslice.extend(unless.body.stmt_list)
                    # Increment enumerate counter.
                    unless_idx += 1
                # Recombine the flattened DEBATE/UNLESS construct with the script.
                self.stmt_list = topslice + midslice + botslice
                # Compensate for the increased length.
                self.index += len(midslice) - 1
            elif (isinstance(stmt, TildeAthLoop)
                or isinstance(stmt, FabricateStmt)):
                stmt.body.flatten()


class ReplicateStmt(Statement):
    __slots__ = ('name', 'expr')

    def __init__(self, name, expr):
        self.name = name
        self.expr = expr

    def eval(self, fsm):
        yield self.expr, None
        if isinstance(self.return_val, AthSymbol):
            symbol = self.return_val.copy()
            # symbol.alive = True
        elif isAthValue(self.return_val):
            symbol = AthSymbol(left=self.return_val.left)
        fsm.assign_name(self.name.name, symbol)
        yield None, symbol


class ProcreateStmt(Statement):
    __slots__ = ('name', 'expr')

    def __init__(self, name, expr):
        self.name = name
        self.expr = expr

    def eval(self, fsm):
        if not self.expr:
            # If there is no expression, assign an empty living symbol.
            symbol = AthSymbol()
            fsm.assign_name(self.name.name, symbol)
        else:
            yield self.expr, None
            try:
                symbol = fsm.lookup_name(self.name.name)
            except NameError:
                # If this symbol's name doesn't exist yet, make it.
                symbol = AthSymbol(left=self.return_val)
                fsm.assign_name(self.name.name, symbol)  
            else:
                if isAthValue(self.return_val):
                    # If the result evaluates to a bare value, assign it directly.
                    symbol.assign_left(self.return_val)
                elif isinstance(self.return_val, AthSymbol):
                    if isinstance(self.expr, VarExpr) and self.expr.name == 'NULL':
                        # If NULL is assigned, empty the left value.
                        symbol.assign_left(None)
                    else:
                        # Otherwise, the value is a symbol, so point the left value to it.
                        symbol.assign_left(self.return_val.left)
                else:
                    raise TypeError('Invalid assignment: {}'.format(result))
        yield None, symbol


class BifurcateStmt(Statement):
    __slots__ = ('name', 'lexpr', 'rexpr')

    def __init__(self, name, lexpr, rexpr):
        self.name = name
        self.lexpr = lexpr
        self.rexpr = rexpr

    def assign_half(self, fsm, name, value, left):
        if isinstance(value, AthSymbol):
            if name != 'NULL':
                # If symbol is not NULL, copy its reference.
                fsm.assign_name(name, value)
        elif value is None:
            # If symbol is empty on that side, create dead symbol.
            fsm.assign_name(name, AthSymbol(False))
        else:
            if left:
                fsm.assign_name(name, AthSymbol(left=value))
            else:
                fsm.assign_name(name, AthSymbol(right=value))

    def eval(self, fsm):
        symbol = fsm.lookup_name(self.name.name)
        self.assign_half(fsm, self.lexpr.name, symbol.left, True)
        self.assign_half(fsm, self.rexpr.name, symbol.right, False)
        yield None, AthSymbol(False)


class AggregateStmt(Statement):
    __slots__ = ('lexpr', 'rexpr', 'name')

    def __init__(self, lexpr, rexpr, name):
        self.lexpr = lexpr
        self.rexpr = rexpr
        self.name = name

    def eval(self, fsm):
        yield self.lexpr, None
        lsym = self.return_val
        yield self.rexpr, None
        rsym = self.return_val
        try:
            result = fsm.lookup_name(self.name.name)
        except NameError:
            result = AthSymbol()
            result.assign_left(lsym)
            result.assign_right(rsym)
            fsm.assign_name(self.name.name, result)
        else:
            result.assign_left(lsym.refcopy(result))
            result.assign_right(rsym.refcopy(result))
        yield None, result


class EnumerateStmt(Statement):
    __slots__ = ('string', 'stack')

    def __init__(self, string, stack):
        self.string = string
        self.stack = stack

    def eval(self, fsm):
        yield self.string, None
        string = self.return_val
        if isinstance(self.return_val, AthSymbol):
            string = self.return_val.left
        if not isinstance(string, str):
            raise TypeError('ENUMERATE only takes strings')

        charlist = [AthSymbol(left=char) for char in string]
        for i in range(len(charlist) - 1):
            charlist[i].assign_right(charlist[i + 1])
        charlist[-1].assign_right(AthSymbol(False))

        fsm.assign_name(self.stack.name, charlist[0])
        yield None, charlist[0]


class ImportStmt(Statement):
    __slots__ = ('module', 'alias')

    def __init__(self, module, alias):
        self.module = module
        self.alias = alias

    def eval(self, fsm):
        try:
            module_vars = fsm.modules[self.module.name]
        except KeyError:
            module = fsm.__class__()
            try:
                module.interpret(self.module.name + '.~ATH')
            except SystemExit as exitexec:
                if exitexec.args[0]:
                    raise exitexec
            module_vars = {
                key: value for key, value in module.stack[0].scope_vars.items()
                }
            fsm.modules[self.module.name] = module_vars
        try:
            symbol = module_vars[self.alias.name]
        except KeyError:
            raise NameError(
                'symbol {} not found in module {}'.format(
                    self.alias.name, self.module.name
                    )
                )
        fsm.assign_name(self.alias.name, symbol.copy())
        yield None, symbol


class InputStmt(Statement):
    __slots__ = ('name', 'prompt')

    def __init__(self, name, prompt):
        self.name = name
        self.prompt = prompt if prompt is not None else StringExpr('')

    def eval(self, fsm):
        yield self.prompt, None
        if isAthValue(self.return_val):
            prompt = self.return_val
        elif isinstance(self.return_val, AthSymbol):
            if isAthValue(self.return_val.left):
                prompt = self.return_val.left
            elif prompt.left is None:
                prompt = ''
            raise SymbolError('Invalid prompt!')
        value = input(prompt)
        try:
            value = int(value)
        except ValueError:
            try:
                value = float(value)
            except ValueError:
                pass
        try:
            symbol = fsm.lookup_name(self.name.name)
        except NameError:
            symbol = AthSymbol(left=value)
            fsm.assign_name(self.name.name, symbol)
        else:
            symbol.left = value
        yield None, symbol


class PrintFunc(Statement):
    """Echoes a string to sys.stdout."""
    __slots__ = ('args',)

    def __init__(self, args):
        self.args = args

    def get_string(self, fsm, args):
        if isinstance(args[0], str):
            return args[0]
        elif isinstance(args[0], AthSymbol) and isinstance(args[0].left, str):
            return args[0].left
        raise TypeError(
            'print must take string or symbol with string as first argument'
            )

    def format(self, fsm, args):
        frmtstr = self.get_string(fsm, args)
        frmtstr = re.sub(r'(?<!\\)~s', '{!s}', frmtstr)
        frmtstr = re.sub(r'(?<!\\)~d', '{:.0f}', frmtstr)
        frmtstr = re.sub(r'(?<!\\)~((?:\d)?\.\d)?f', '{:\\1f}', frmtstr)
        frmtstr = re.sub(r'\\~', '~', frmtstr)
        # Replace special character escapes
        frmtstr = re.sub(r'\\a', '\a', frmtstr) # Bell
        frmtstr = re.sub(r'\\b', '\b', frmtstr) # Backspace
        frmtstr = re.sub(r'\\f', '\f', frmtstr) # Line-feed
        frmtstr = re.sub(r'\\r', '\r', frmtstr) # Carriage Return
        frmtstr = re.sub(r'\\n', '\n', frmtstr) # Newline
        frmtstr = re.sub(r'\\t', '\t', frmtstr) # H-Tab
        frmtstr = re.sub(r'\\v', '\v', frmtstr) # V-Tab
        # Grab the format arguments
        frmtargs = []
        if len(args) > 1:
            for arg in args[1:]:
                if isAthValue(arg):
                    frmtargs.append(arg)
                elif isinstance(arg, AthSymbol):
                    if isAthValue(arg.left):
                        frmtargs.append(arg.left)
                        continue
                    raise TypeError(
                        'Invalid symbol value {}!'.format(
                            arg.left.__class__.__name__
                            )
                        )
        return frmtstr.format(*frmtargs)

    def eval(self, fsm):
        args = []
        for arg in self.args:
            yield arg, None
            args.append(self.return_val)
        string = self.format(fsm, args) if args else ''
        print(string, end='')
        yield None, string


class KillFunc(Statement):
    """Kills a ~ATH symbol."""
    __slots__ = ('name', 'args')

    def __init__(self, name, args):
        self.name = name
        self.args = args

    def eval(self, fsm):
        if self.args:
            raise TypeError(
                'DIE() expects 0 arguments, got: {}'.format(len(self.args))
                )
        fsm.lookup_name(self.name.name).kill()
        raise SymbolDeath
        # To ensure that this is also a function that returns a generator.
        yield None, None


class ExecuteStmt(Statement):
    __slots__ = ('args',)

    def __init__(self, args):
        self.args = args

    def eval(self, fsm):
        # Execute must have at least one argument.
        if not self.args:
            raise TypeError('execute statement missing symbol argument')
        # Split the name and the function arguments.
        name = self.args[0]
        args = self.args[1:]        
        # EXECUTE(NULL) will return NULL if called and returned from.
        if isinstance(name, VarExpr) and name.name == 'NULL':
            yield None, AthSymbol(False)
            # Just in case something makes this move past here.
            while True:
                return
        # Evaluate the name symbol, whatever it returns must have a function.
        yield name, None  
        func = self.return_val.right
        if not isinstance(func, AthFunction):
            raise TypeError('symbol executed must have been fabricated')
        # Check if the number of passed arguments matches the intended format.
        if len(args) != len(func.argfmt):
            raise TypeError(
                'expected {} arguments, got {}'.format(
                    len(func.argfmt) + 1, len(args) + 1
                    )
                )
        # Build the scope dictionary.
        arg_dict = {}
        if len(args):
            for name, argexpr in zip(func.argfmt, args):
                yield argexpr, None
                if isAthValue(arg):
                    arg_dict[name] = AthSymbol(left=self.return_val)
                else:
                    arg_dict[name] = self.return_val
        yield func, arg_dict


class DivulgateStmt(ControlStmt):
    __slots__ = ('expr',)

    def __init__(self, expr):
        self.expr = expr

    def eval(self, fsm):
        yield self.expr, None
        yield None, self.return_val


class FabricateStmt(Statement):
    __slots__ = ('name', 'argfmt', 'body')

    def __init__(self, name, argfmt, body):
        body.ctrl_name = name.name
        self.name = name
        self.argfmt = [arg.name for arg in argfmt]
        self.body = body

    def eval(self, fsm):
        try:
            symbol = fsm.lookup_name(self.name.name)
        except NameError:
            symbol = AthSymbol(
                right=AthFunction(self.name.name, self.argfmt, self.body)
                )
            fsm.assign_name(self.name.name, symbol)
        else:
            symbol.right = AthFunction(self.name.name, self.argfmt, self.body)
        yield None, symbol


class LambdaFunc(Statement):
    __slots__ = ('argfmt', 'expr')

    def __init__(self, argfmt, expr):
        self.argfmt = [arg.name for arg in argfmt]
        self.expr = expr


class TildeAthLoop(ControlStmt):
    __slots__ = ('grave', 'body', 'state')

    def __init__(self, grave, body, state=None):
        if state is None:
            if isinstance(grave, UnaryArithExpr):
                if grave.op == '!' and isinstance(grave.expr, VarExpr):
                    self.state = True
                    grave = grave.expr
            elif isinstance(grave, VarExpr):
                self.state = False
                body.ctrl_name = grave.name
            else:
                raise SyntaxError('Invalid ~ATH expression')
        else:
            self.state = state
        self.grave = grave
        self.body = body


class DebateStmt(ControlStmt):
    __slots__ = ('clause', 'body', 'unlesses')

    def __init__(self, clause, body, unlesses):
        self.clause = clause
        self.body = body
        self.unlesses = unlesses


class UnlessStmt(ControlStmt):
    __slots__ = ('clause', 'body')

    def __init__(self, clause, body):
        self.clause = clause
        self.body = body


class InspectStack(Statement):
    __slots__ = ('args',)

    def __init__(self, args):
        self.args = args

    def eval(self, fsm):
        if not self.args:
            print(fsm.bltin_vars)
            for frame in fsm.stack:
                print(frame.scope_vars)
            yield None, None
            while True:
                return

        index = self.args[0].eval(fsm)
        if isinstance(index, AthSymbol):
            index = index.left
        if len(self.args) > 1 and not isinstance(index, int):
            raise ValueError('may only call stack frame index')
        if not index:
            print(fsm.bltin_vars)
        print(fsm.stack[index].scope_vars)
        yield None, None
