"""~ATH's Abstract Syntax Tree definition.

This contains the data structure of ~ATH syntax and its variables,
as well as their implementations. This does not, however, contain
the literals used for lexing.
"""
import re
import operator
from functools import partial
from symbol import (
    isAthValue, SymbolError, SymbolDeath,
    AthExpr, AthSymbol, AthFunction,
    BuiltinSymbol, NULL,
    )


class AstExpr(AthExpr):
    """Base class for AST expressions."""
    __slots__ = ()


class EvalExpr(AstExpr):
    """Superclass to all expressions that are not statements."""
    __slots__ = ()


class PrimitiveExpr(EvalExpr):
    """Superclass to primitives."""
    __slots__ = ()


class NumExpr(PrimitiveExpr):
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


class StringExpr(PrimitiveExpr):
    """Holds string values."""
    __slots__ = ('string',)

    def __init__(self, string):
        self.string = string

    def eval(self, fsm):
        yield None, self.string



class VarExpr(PrimitiveExpr):
    """Contains a symbol name."""
    __slots__ = ('name',)

    def __init__(self, name):
        self.name = name

    def __hash__(self):
        return hash(self.name)

    def eval(self, fsm):
        yield None, fsm.lookup_name(self.name)


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


class UnaryExpr(EvalExpr):
    """Handles unary arithmetic expressions."""
    __slots__ = ('op', 'expr')
    ops = {
        '+': operator.pos,
        '-': operator.neg,
        '~': operator.inv,
        '!': bool_not,
    }

    def __init__(self, args, expr=None):
        if isinstance(args, tuple):
            self.op, self.expr = args
        else:
            self.op = args
            self.expr = expr

    def eval(self, fsm):
        result = self.ops[self.op]((yield self.expr, None))
        if isinstance(result, AthSymbol):
            yield None, result
        elif isAthValue(result):
            yield None, AthSymbol(left=result)
        else:
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
        result = self.ops[self.op](
            (yield self.lexpr, None), (yield self.rexpr, None)
            )
        if isinstance(result, AthSymbol):
            yield None, result
        elif isAthValue(result):
            yield None, AthSymbol(left=result)
        else:
            raise ValueError('Invalid result: {}'.format(result))


class Statement(AstExpr):
    """Superclass to all statements."""
    __slots__ = ()

    def __repr__(self, level=0):
        return (' ' * 4 * level) + super().__repr__()


class ControlStmt(Statement):
    """Superclass to all control flow statements."""
    __slots__ = ()


class AthAstList(ControlStmt):
    __slots__ = ('stmt_list', 'ctrl_name', 'index')

    def __init__(self, stmt_list, ctrl_name=None):
        self.stmt_list = stmt_list
        self.ctrl_name = ctrl_name or 'THIS'
        self.index = 0

    def __repr__(self, level=0):
        return (
            self.__class__.__name__
            + '([\n'
            + ',\n'.join(
                stmt.__repr__(level+1)
                for stmt in self.stmt_list
                )
            + '\n' + (' ' * 4 * (level+1))
            + '], {!r})'.format(self.ctrl_name)
            )

    def __len__(self):
        return len(self.stmt_list)

    def __getitem__(self, key):
        return self.stmt_list.__getitem__(key)

    def __setitem__(self, key, val):
        raise TypeError('The AST List is not mutable!')

    def __delitem__(self, key):
        raise TypeError('The AST List is not mutable!')

    def __iter__(self):
        """Initializes iteration state."""
        return AstListIterator(self.stmt_list, self.ctrl_name)

    def __reversed__(self):
        self.index = len(self.stmt_list)
        while self.index >= 0:
            self.index -= 1
            yield self.stmt_list[self.index]

    def __contains__(self, item):
        return self.stmt_list.__contains__(item)

    def eval(self, fsm):
        raise NotImplementedError(
            'The AST list is to be directly evaluated by the interpreter.'
            )


class AstListIterator(AthAstList):
    """Iterator objects instantiated by AthAstLists when iterated over."""
    __slots__ = ()

    def __init__(self, stmt_list, ctrl_name):
        self.stmt_list = stmt_list
        self.ctrl_name = ctrl_name
        self.index = 0

    def __repr__(self):
        return '<AST Iterator at index {}>'.format(self.index)

    def __iter__(self):
        self.index = 0
        return self

    def __next__(self):
        try:
            node = self.stmt_list[self.index]
        except IndexError:
            raise StopIteration
        self.index += 1
        return node


class PropagateStmt(Statement):
    """Unused."""
    __slots__ = ('source', 'target')

    def __init__(self, source, target):
        self.source = source
        self.target = target

    def eval(self, fsm):
        try:
            symbol = fsm.lookup_name(self.source.name)
        except NameError:
            raise NameError('Symbol {} not found!'.format(self.source.name))
        if self.target:
            fsm.assign_name(self.target.name, symbol)
        else:
            fsm.assign_name(self.source.name, symbol)
        yield None, symbol


class ReplicateStmt(Statement):
    __slots__ = ('name', 'expr')

    def __init__(self, name, expr):
        self.name = name
        self.expr = expr

    def eval(self, fsm):
        if self.expr:
            value = (yield self.expr, None)
            if value is NULL:
                symbol = AthSymbol(False)
            elif isinstance(value, AthSymbol):
                symbol = value.copy()
            elif isAthValue(value):
                symbol = AthSymbol(left=value)
            else:
                raise ValueError(repr(value))
        else:
            symbol = AthSymbol()
        fsm.assign_name(self.name, symbol)
        yield None, symbol


class ProcreateStmt(Statement):
    __slots__ = ('name', 'expr')

    def __init__(self, name, expr):
        self.name = name
        self.expr = expr

    def assign_value(self, symbol, value):
        if isAthValue(value):
            # If the result evaluates to a bare value, assign it directly.
            symbol.assign_left(value)
        elif isinstance(value, AthSymbol):
            if value is NULL:
                # If NULL is assigned, kill the symbol and empty it.
                symbol.alive = False
                symbol.left = None
                symbol.right = None
            else:
                # Otherwise, the value is a symbol, so point the left value to it.
                symbol.assign_left(value.left)
        else:
            raise TypeError('Invalid assignment: {}'.format(value))

    def eval(self, fsm):
        if not self.expr:
            # If there is no expression, assign an empty living symbol.
            symbol = AthSymbol()
            fsm.assign_name(self.name, symbol)
        else:
            value = (yield self.expr, None)
            try:
                symbol = fsm.lookup_name(self.name)
            except NameError:
                # If this symbol's name doesn't exist yet, make it.
                symbol = AthSymbol()
                self.assign_value(symbol, value)
                fsm.assign_name(self.name, symbol)
            else:
                self.assign_value(symbol, value)
        yield None, symbol


class BifurcateStmt(Statement):
    __slots__ = ('name', 'lexpr', 'rexpr')

    def __init__(self, name, lexpr, rexpr):
        self.name = name
        self.lexpr = lexpr
        self.rexpr = rexpr

    def eval(self, fsm):
        syml = None
        symr = None
        symbol = fsm.lookup_name(self.name)
        if self.lexpr != 'NULL':
            if isinstance(symbol.left, AthSymbol):
                if self.lexpr != self.name:
                    fsm.assign_name(self.lexpr, symbol.left)
                else:
                    syml = symbol.left
            elif symbol.left is None:
                fsm.assign_name(self.lexpr, AthSymbol(False))
            else:
                fsm.assign_name(self.lexpr, AthSymbol(left=symbol.left))
        if self.rexpr != 'NULL':
            if isinstance(symbol.right, AthSymbol):
                if self.rexpr != self.name:
                    fsm.assign_name(self.rexpr, symbol.right)
                else:
                    symr = symbol.right
            elif symbol.right is None:
                fsm.assign_name(self.rexpr, AthSymbol(False))
            else:
                fsm.assign_name(self.rexpr, AthSymbol(right=symbol.right))
        if syml is not None:
            symbol.alive = syml.alive
            symbol.left = syml.left
            symbol.right = syml.right
        elif symr is not None:
            symbol.alive = symr.alive
            symbol.left = symr.left
            symbol.right = symr.right
        yield None, AthSymbol(False)


class AggregateStmt(Statement):
    __slots__ = ('name', 'lexpr', 'rexpr')

    def __init__(self, name, lexpr, rexpr):
        self.name = name
        self.lexpr = lexpr
        self.rexpr = rexpr

    def eval(self, fsm):
        if isinstance(self.lexpr, VarExpr) and self.lexpr.name == 'NULL':
            lsym = AthSymbol(False)
        else:
            lsym = (yield self.lexpr, None)
        if isinstance(self.rexpr, VarExpr) and self.rexpr.name == 'NULL':
            rsym = AthSymbol(False)
        else:
            rsym = (yield self.rexpr, None)
        try:
            result = fsm.lookup_name(self.name)
        except NameError:
            result = AthSymbol()
            result.assign_left(lsym)
            result.assign_right(rsym)
            fsm.assign_name(self.name, result)
        else:
            if isinstance(lsym, AthSymbol):
                lsym = lsym.refcopy(result)
            if isinstance(rsym, AthSymbol):
                rsym = rsym.refcopy(result)
            result.assign_left(lsym)
            result.assign_right(rsym)
        yield None, result


class EnumerateStmt(Statement):
    __slots__ = ('string', 'stack')

    def __init__(self, string, stack):
        self.string = string
        self.stack = stack

    def eval(self, fsm):
        string = (yield self.string, None)
        if isinstance(string, AthSymbol):
            string = string.left
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
            module_vars = fsm.modules[self.module]
        except KeyError:
            module = fsm.__class__()
            try:
                module.interpret(self.module + '.~ATH')
            except SystemExit as exitexec:
                if exitexec.args[0]:
                    raise exitexec
            module_vars = module.stack[0].scope_vars
            fsm.modules[self.module] = module_vars
        try:
            symbol = module_vars[self.alias]
        except KeyError:
            raise NameError(
                'symbol {} not found in module {}'.format(
                    self.alias, self.module
                    )
                )
        fsm.assign_name(self.alias, symbol.copy())
        yield None, symbol


class InputStmt(Statement):
    __slots__ = ('name', 'prompt')

    def __init__(self, name, prompt):
        self.name = name
        self.prompt = prompt

    def eval(self, fsm):
        prompt = (yield self.prompt, None)
        if isinstance(prompt, AthSymbol):
            if isAthValue(prompt.left):
                prompt = prompt.left
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
            symbol = fsm.lookup_name(self.name)
        except NameError:
            symbol = AthSymbol(left=value)
            fsm.assign_name(self.name, symbol)
        else:
            symbol.left = value
        yield None, symbol


class PrintStmt(Statement):
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
        frmtstr = re.sub(r'(?<!\\)~[s|d]', '{!s}', frmtstr)
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
            args.append((yield arg, None))
        string = self.format(fsm, args) if args else ''
        print(string, end='')
        yield None, string


class KillStmt(ControlStmt):
    """Kills a ~ATH symbol."""
    __slots__ = ('graves',)

    def __init__(self, graves):
        self.graves = graves

    def eval(self, fsm):
        for symbol in self.graves:
            fsm.lookup_name(symbol).kill()
        raise SymbolDeath(self.graves)
        # To ensure that this is also a function that returns a generator.
        yield


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
        func = (yield name, None).right
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
                value = (yield argexpr, None)
                if isAthValue(value):
                    arg_dict[name] = AthSymbol(left=value)
                else:
                    arg_dict[name] = value
        yield func, arg_dict


class DivulgateStmt(ControlStmt):
    __slots__ = ('expr',)

    def __init__(self, expr):
        self.expr = expr

    def eval(self, fsm):
        yield None, (yield self.expr, None)


class FabricateStmt(Statement):
    __slots__ = ('func',)

    def __init__(self, func):
        self.func = func

    def __repr__(self, level=0):
        return (
            (' ' * 4 * level)
            + '{}({}({!r}, {!r}, '.format(
                self.__class__.__name__,
                self.func.__class__.__name__,
                self.func.name,
                self.func.argfmt,
                )
            + self.func.body.__repr__(level)
            + '\n' + (' ' * 4 * level) + '))'
            )

    def eval(self, fsm):
        try:
            symbol = fsm.lookup_name(self.func.name)
        except NameError:
            symbol = AthSymbol(right=self.func)
            fsm.assign_name(self.func.name, symbol)
        else:
            symbol.right = self.func
        yield None, symbol


class TildeAthLoop(ControlStmt):
    __slots__ = ('state', 'body', 'coro')

    def __init__(self, state, body, coro):
        self.state = state
        self.body = body
        self.coro = coro

    def __repr__(self, level=0):
        return (
            (' ' * 4 * level)
            + '{}({}, '.format(
                self.__class__.__name__,
                self.state,
                )
            + self.body.__repr__(level)
            + ',\n'
            + self.coro.__repr__(level)
            + '\n' + (' ' * 4 * level) + ')'
            )

    def eval(self, fsm):
        raise NotImplementedError(
            'Loops are to be directly evaluated by the interpreter.'
            )


class CondJumpStmt(ControlStmt):
    """Statement that signals the execution to skip a number
    of statements equivalent to its height if the clause is
    evaluated to a dead symbol.
    """
    __slots__ = ('clause', 'height')

    def __init__(self, clause, height):
        self.clause = clause
        self.height = height

    def eval(self, fsm):
        # Unconditional jumps have no clause and force the jump.
        if self.clause:
            # Evaluate clause, jump only if value is dead.
            if (yield self.clause, None):
                yield None, NULL
                # Raise Stopiteration repeatedly.
                while True:
                    return
        fsm.ast.index += self.height
        yield None, NULL


class InspectStack(Statement):
    __slots__ = ('args',)

    def __init__(self, args):
        self.args = args

    def eval(self, fsm):
        if not self.args:
            print(fsm.bltin_vars)
            for frame in fsm.stack:
                print(frame.scope_vars)
            yield None, NULL
            # Raise Stopiteration repeatedly.
            while True:
                return
        index = (yield self.args[0], None)
        if isinstance(index, AthSymbol):
            index = index.left
        if len(self.args) > 1 and not isinstance(index, int):
            raise ValueError('may only call stack frame index')
        print(fsm.stack[index].scope_vars)
        yield None, NULL
