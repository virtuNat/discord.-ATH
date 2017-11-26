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
    AthExpr, AthSymbol, BuiltinSymbol, AthFunction,
    SymbolDeath, DivulgateBack, EndTilDeath, BreakUnless
    )


class ArithExpr(AthExpr):
    """Superclass to all arithmetic-based syntax."""
    __slots__ = ()


class NumExpr(ArithExpr):
    """Superclass of both integers and floats."""
    __slots__ = ('num',)

    def __repr__(self):
        return '{}({})'.format(self.__class__.__name__, self.num)

    def eval(self, fsm):
        return self.num


class FloatExpr(NumExpr):
    """Holds float number values.

    Arithmetic operators handle float and int values differently;
    for addition, subtraction, and multiplication, return a float
    if at least one operand is float otherwise return int.

    For true division, return type is always float.
    For floor division, return type is int if both operands are int.
    """
    __slots__ = ()

    def __init__(self, num):
        self.num = float(num)


class IntExpr(NumExpr):
    """Holds integer number values."""
    __slots__ = ()

    def __init__(self, num):
        self.num = int(num)


class VarExpr(ArithExpr):
    """Contains a symbol name."""
    __slots__ = ('name',)

    def __init__(self, name):
        self.name = name

    def eval(self, fsm):
        return fsm.lookup_name(self.name)


class StringExpr(ArithExpr):
    """Holds string values."""
    __slots__ = ('string',)

    def __init__(self, string):
        self.string = string

    def eval(self, fsm):
        return self.string


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
    else:
        raise SyntaxError('Invalid comparison operator: {}', op)


def symbol_opr(lval, rval, op):
    if not (isinstance(lval, AthSymbol) and isinstance(rval, AthSymbol)):
        raise TypeError('May only perform living assertions on symbols')
    try:
        if op == '!=!':
            value = (lval.left.alive == rval.left.alive
                and lval.right.alive == rval.right.alive)
        elif op == '!=?':
            value = lval.left.alive == rval.left.alive
        elif op == '?=!':
            value = lval.right.alive == rval.right.alive
        elif op == '~=!':
            value = (lval.left.alive != rval.left.alive
                and lval.right.alive == rval.right.alive)
        elif op == '!=~':
            value = (lval.left.alive == rval.left.alive
                and lval.right.alive != rval.right.alive)
        elif op == '~=~':
            value = (lval.left.alive != rval.left.alive
                and lval.right.alive != rval.right.alive)
        else:
            raise SyntaxError('Invalid comparison operator: {}', op)
    except AttributeError:
        raise SymbolError('The relevant side(s) must be symbols')
    else:
        return AthSymbol(value)


class UnaryArithExpr(ArithExpr):
    """Handles unary arithmetic expressions."""
    __slots__ = ('op', 'expr')
    ops = {
        '+': operator.pos,
        '-': operator.neg,
        '~': operator.inv,
        '!': bool_not,
    }

    def __init__(self, op, expr):
        self.op = op
        self.expr = expr

    def eval(self, fsm):
        try:
            result = self.ops[self.op](self.expr.eval(fsm))
            if isinstance(result, AthSymbol):
                return result
            elif isAthValue(result):
                return AthSymbol(left=result)
            else:
                raise ValueError('Invalid result: {}'.format(result))
        except KeyError:
            raise SyntaxError('Unknown operator: {}', self.op)


class BinaryExpr(ArithExpr):
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
        '!=?': partial(symbol_opr, op='!=?'),
        '?=!': partial(symbol_opr, op='?=!'),
        '~=!': partial(symbol_opr, op='~=!'),
        '!=~': partial(symbol_opr, op='!=~'),
        '~=~': partial(symbol_opr, op='~=~'),
    }

    def __init__(self, op, lexpr, rexpr):
        self.op = op
        self.lexpr = lexpr
        self.rexpr = rexpr

    def eval(self, fsm):
        lval = self.lexpr.eval(fsm)
        rval = self.rexpr.eval(fsm)
        try:
            result = self.ops[self.op](lval, rval)
            if isinstance(result, AthSymbol):
                return result
            elif isAthValue(result):
                return AthSymbol(left=result)
            else:
                raise ValueError('Invalid result: {}'.format(result))
        except KeyError:
            raise SyntaxError('Invalid operator: {}'.format(self.op))


class BinaryIPExpr(ArithExpr):
    """Handles in-place binary arithmetic operators."""
    __slots__ = ('op', 'name', 'expr')

    def __init__(self, op, name, expr):
        self.op = op
        self.name = name
        self.expr = expr

    def eval(self, fsm):
        raise NotImplementedError(
            '{} has not been implemented.'.format(self.__class__.__name__)
            )


class Statement(AthExpr):
    """Superclass to all builtin statements."""
    __slots__ = ()


class Serialize(Statement):
    __slots__ = ('stmt_list', 'ctrl_name', 'value')

    def __init__(self, stmt_list):
        self.stmt_list = stmt_list
        self.value = None
        super().__setattr__('ctrl_name', 'THIS')

    def __repr__(self):
        return '{}({}, {!r})'.format(
            self.__class__.__name__, self.stmt_list, self.ctrl_name
            )

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

    def eval(self, fsm):
        for stmt in self.stmt_list:
            try:
                stmt.eval(fsm)
            except SymbolDeath:
                if not fsm.lookup_name('THIS').alive:
                    raise EndTilDeath
                elif not fsm.lookup_name(self.ctrl_name):
                    raise
            except DivulgateBack:
                self.value = stmt.value
                raise


class ReplicateStmt(Statement):
    __slots__ = ('name', 'expr')

    def __init__(self, name, expr):
        self.name = name
        self.expr = expr

    def eval(self, fsm):
        result = self.expr.eval(fsm)
        if isinstance(result, AthSymbol):
            symbol = result.copy()
            symbol.alive = True
        elif isAthValue(result):
            symbol = AthSymbol(left=result.left)
        else:
            raise SymbolError('Bad copy: {}'.format(result))
        fsm.assign_name(self.name.name, symbol)


class ProcreateStmt(Statement):
    __slots__ = ('name', 'expr')

    def __init__(self, name, expr):
        self.name = name
        self.expr = expr

    def eval(self, fsm):
        try:
            result = self.expr.eval(fsm)
        except AttributeError:
            fsm.assign_name(self.name.name, AthSymbol())
        else:
            try:
                symbol = fsm.lookup_name(self.name.name)
            except NameError:
                fsm.assign_name(self.name.name, AthSymbol(left=result))   
            else:
                if isAthValue(result):
                    symbol.assign_left(result)
                elif isinstance(result, AthSymbol):
                    if isinstance(self.expr, VarExpr) and self.expr.name == 'NULL':
                        symbol.assign_left(None)
                    else:
                        symbol.assign_left(result.left)
                else:
                    raise TypeError('Invalid assignment: {}'.format(result))            


class BifurcateStmt(Statement):
    __slots__ = ('name', 'lexpr', 'rexpr')

    def __init__(self, name, lexpr, rexpr):
        self.name = name
        self.lexpr = lexpr
        self.rexpr = rexpr

    def assign_half(self, fsm, name, value, left):
        if isinstance(value, AthSymbol):
            if name != 'NULL':
                fsm.assign_name(name, value)
        elif value is None:
            fsm.assign_name(name, AthSymbol(False))
        else:
            if left:
                fsm.assign_name(name, AthSymbol(left=value))
            else:
                fsm.assign_name(name, AthSymbol(right=value))

    def eval(self, fsm):
        symbol = fsm.lookup_name(self.name.name)
        if isinstance(symbol, AthSymbol):
            self.assign_half(fsm, self.lexpr.name, symbol.left, True)
            self.assign_half(fsm, self.rexpr.name, symbol.right, False)
        else:
            raise SymbolError('May not bifurcate non-symbol')


class AggregateStmt(Statement):
    __slots__ = ('lexpr', 'rexpr', 'name')

    def __init__(self, lexpr, rexpr, name):
        self.lexpr = lexpr
        self.rexpr = rexpr
        self.name = name

    def eval(self, fsm):
        try:
            result = fsm.lookup_name(self.name.name)
        except NameError:
            result = AthSymbol()
            lsym = self.lexpr.eval(fsm)
            rsym = self.rexpr.eval(fsm)
        else:
            lsym = self.lexpr.eval(fsm).refcopy(result)
            rsym = self.rexpr.eval(fsm).refcopy(result)

        result.assign_left(lsym)
        result.assign_right(rsym)
        fsm.assign_name(self.name.name, result)


class EnumerateStmt(Statement):
    __slots__ = ('string', 'stack')

    def __init__(self, string, stack):
        self.string = string
        self.stack = stack

    def eval(self, fsm):
        string = self.string.eval(fsm)
        if isinstance(string, AthSymbol):
            string = string.left
        if not isinstance(string, str):
            raise TypeError('ENUMERATE only takes strings')

        charlist = [AthSymbol(left=char) for char in string]
        for i in range(len(charlist) - 1):
            charlist[i].assign_right(charlist[i + 1])
        charlist[-1].assign_right(AthSymbol(False))
        fsm.assign_name(self.stack.name, charlist[0])


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
                key: value for key, value in module.global_vars.items()
                if not isinstance(value, BuiltinSymbol)
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
        fsm.assign_name(self.alias.name, symbol)


class InputStmt(Statement):
    __slots__ = ('name', 'prompt')

    def __init__(self, name, prompt):
        self.name = name
        self.prompt = prompt if prompt is not None else StringExpr('')

    def eval(self, fsm):
        prompt = self.prompt.eval(fsm)
        if isinstance(prompt, AthSymbol):
            if isAthValue(prompt.left):
                prompt = prompt.left
            elif prompt.left is None:
                prompt = ''
            else:
                raise SymbolError('Invalid prompt!')
        value = input(prompt)
        try:
            value = int(value)
        except ValueError:
            try:
                value = float(value)
            except ValueError:
                pass
        fsm.assign_name(self.name.name, AthSymbol(left=value))


class PrintFunc(Statement):
    """Echoes a string to sys.stdout."""
    __slots__ = ('args',)

    def __init__(self, args):
        self.args = args

    def get_string(self, fsm):
        if isinstance(self.args[0], StringExpr):
            return self.args[0].string
        elif isinstance(self.args[0], VarExpr):
            symbol = self.args[0].eval(fsm)
            if isinstance(symbol.left, str):
                return symbol.left
        raise TypeError(
            'print must take string or symbol with string as first argument'
            )

    def format(self, frmtstr, fsm):
        frmtstr = re.sub(r'(?<!\\)~s', '{!s}', frmtstr)
        frmtstr = re.sub(r'(?<!\\)~d', '{:.0f}', frmtstr)
        frmtstr = re.sub(r'(?<!\\)~((?:\d)?\.\d)?f', '{:\\1f}', frmtstr)
        frmtstr = re.sub(r'\\~', '~', frmtstr)
        # Replace whitespace character escapes
        frmtstr = re.sub(r'\\a', '\a', frmtstr)
        frmtstr = re.sub(r'\\b', '\b', frmtstr)
        frmtstr = re.sub(r'\\f', '\f', frmtstr)
        frmtstr = re.sub(r'\\r', '\r', frmtstr)
        frmtstr = re.sub(r'\\n', '\n', frmtstr)
        frmtstr = re.sub(r'\\t', '\t', frmtstr)
        frmtstr = re.sub(r'\\v', '\v', frmtstr)
        # Grab the format arguments
        if len(self.args) > 1:
            frmtargs = []
            for arg in self.args[1:]:
                result = arg.eval(fsm)
                if isAthValue(result):
                    frmtargs.append(result)
                elif isinstance(result, AthSymbol):
                    if isAthValue(result.left):
                        frmtargs.append(result.left)
                    else:
                        raise TypeError('Invalid symbol value!')
        else:
            frmtargs = tuple()
        return frmtstr.format(*frmtargs)

    def eval(self, fsm):
        if self.args:
            frmtstr = self.get_string(fsm)
            frmtedstr = self.format(frmtstr, fsm)
        else:
            frmtedstr = ''
        print(frmtedstr, end='')


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


class ExecuteStmt(Statement):
    __slots__ = ('args',)

    def __init__(self, args):
        self.args = args

    def eval(self, fsm):
        if not self.args:
            raise TypeError('execute statement missing symbol argument')

        name = self.args[0]
        args = self.args[1:]
        if not isinstance(name, VarExpr):
            raise TypeError('execute must have symbol as first argument')

        if name.name == 'NULL':
            return AthSymbol(False)

        func = name.eval(fsm).right
        if not isinstance(func, AthFunction):
            raise TypeError('symbol executed must have been fabricated')

        argnames = [arg.name for arg in func.argfmt]
        if len(args) != len(argnames):
            raise TypeError(
                'expected {} arguments, got {}'.format(
                    len(argnames) + 1, len(args) + 1
                    )
                )

        arg_dict = {}
        if len(args):
            for name, argexpr in zip(argnames, args):
                arg = argexpr.eval(fsm)
                if isAthValue(arg):
                    arg_dict[name] = AthSymbol(left=arg)
                else:
                    arg_dict[name] = arg

        return func.execute(fsm, arg_dict)


class DivulgateStmt(Statement):
    __slots__ = ('expr', 'value')

    def __init__(self, expr):
        self.expr = expr
        self.value = None

    def __repr__(self):
        return '{}({})'.format(self.__class__.__name__, self.expr)

    def eval(self, fsm):
        self.value = self.expr.eval(fsm)
        raise DivulgateBack


class FabricateStmt(Statement):
    __slots__ = ('name', 'argfmt', 'body')

    def __init__(self, name, argfmt, body):
        body.ctrl_name = name.name
        self.name = name
        self.argfmt = argfmt
        self.body = body

    def eval(self, fsm):
        newflag = False
        try:
            symbol = fsm.lookup_name(self.name.name)
        except NameError:
            newflag = True
            symbol = AthSymbol()
        symbol.right = AthFunction(self.name.name, self.argfmt, self.body)
        if newflag:
            fsm.assign_name(self.name.name, symbol)


class TildeAthLoop(Statement):
    __slots__ = ('state', 'grave', 'body')

    def __init__(self, grave, body):
        if isinstance(grave, UnaryArithExpr):
            if grave.op == '!' and isinstance(grave.expr, VarExpr):
                self.state = True
                grave = grave.expr
        elif isinstance(grave, VarExpr):
            self.state = False
            body.ctrl_name = grave.name
        else:
            raise TypeError('Invalid ~ATH expression')
        self.grave = grave
        self.body = body

    def eval(self, fsm):
        dying = self.grave.eval(fsm)
        with fsm.push_stack():
            while dying.alive != self.state:
                self.body.eval(fsm)
                dying = self.grave.eval(fsm)


class DebateStmt(Statement):
    __slots__ = ('clause', 'body', 'unlesses')

    def __init__(self, clause, body, unlesses):
        self.clause = clause
        self.body = body
        self.unlesses = unlesses

    def eval(self, fsm):
        if self.clause.eval(fsm):
            try:
                self.body.eval(fsm)
            except SymbolDeath:
                raise
        elif self.unlesses:
            for unless in self.unlesses:
                try:
                    unless.eval(fsm)
                except BreakUnless:
                    break
                except SymbolDeath:
                    raise
                except DivulgateBack:
                    self.body.value = unless.body.value
                    raise


class UnlessStmt(Statement):
    __slots__ = ('clause', 'body')

    def __init__(self, clause, body):
        self.clause = clause
        self.body = body

    def eval(self, fsm):
        if self.clause is None or self.clause.eval(fsm):
            self.body.eval(fsm)
            raise BreakUnless


class InspectStack(Statement):
    __slots__ = ('args',)

    def __init__(self, args):
        self.args = args

    def eval(self, fsm):
        if not self.args:
            print(fsm.global_vars)
            for frame in fsm.stack:
                print(frame.scope_vars)
            return None

        index = self.args[0].eval(fsm)
        if isinstance(index, AthSymbol):
            index = index.left
        if len(self.args) > 1 and not isinstance(index, int):
            raise ValueError('may only call stack frame index')

        if not index:
            # 0, globals
            print(fsm.global_vars)
        elif abs(index) > len(fsm.stack):
            # out of bounds, top stack
            print(fsm.stack[-1].scope_vars)
        elif index > 0:
            # positive, adjust to index notation
            print(fsm.stack[index - 1].scope_vars)
        else:
            # negative, as is
            print(fsm.stack[index].scope_vars)
