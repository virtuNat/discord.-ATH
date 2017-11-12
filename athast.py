"""~ATH's Abstract Syntax Tree definition.

This contains the data structure of ~ATH syntax and its variables,
as well as their implementations. This does not, however, contain
the literals used for lexing.
"""
import re
import operator
from symbol import isAthValue, AthExpr, AthSymbol, AthFunction
from symbol import SymbolError, SymbolDeath, EndTilDeath


class VarExpr(AthExpr):
    """Contains a symbol name."""
    __slots__ = ('name',)

    def __init__(self, name):
        self.name = name

    def eval(self, fsm):
        return fsm.lookup_name(self.name)


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


class UnaryArithExpr(ArithExpr):
    """Handles unary arithmetic expressions."""
    __slots__ = ('op', 'expr')
    ops = {
        '+': operator.pos,
        '-': operator.neg,
        '~': operator.inv,
    }

    def __init__(self, op, expr):
        self.op = op
        self.expr = expr

    def eval(self, fsm):
        try:
            return self.ops[self.op](self.expr.eval(fsm))
        except KeyError:
            raise SyntaxError('Unknown operator: {}', self.op)


class BinaryArithExpr(ArithExpr):
    """Handles binary arithmetic expressions."""
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
    }

    def __init__(self, op, lexpr, rexpr):
        self.op = op
        self.lexpr = lexpr
        self.rexpr = rexpr

    def eval(self, fsm):
        lval = self.lexpr.eval(fsm)
        rval = self.rexpr.eval(fsm)
        try:
            return self.ops[self.op](lval, rval)
        except KeyError:
            raise SyntaxError('Invalid arithmetic operator: {}', self.op)


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


class StringExpr(AthExpr):
    """Holds string values."""
    __slots__ = ('string',)

    def __init__(self, string):
        self.string = string

    def eval(self, fsm):
        return self.string


class BoolExpr(AthExpr):
    """Superclass to all boolean syntax."""
    __slots__ = ()


class ValueCmpExpr(BoolExpr):
    """Handles value comparison expressions."""
    __slots__ = ('op', 'lexpr', 'rexpr')
    ops = {
        '<': operator.lt,
        '<=': operator.le,
        '>': operator.gt,
        '>=': operator.ge,
        '==': operator.eq,
        '~=': operator.ne,
    }

    def __init__(self, op, lexpr, rexpr):
        self.op = op
        self.lexpr = lexpr
        self.rexpr = rexpr

    def eval(self, fsm):
        lval = self.lexpr.eval(fsm)
        rval = self.rexpr.eval(fsm)
        try:
            return AthSymbol(self.ops[self.op](lval, rval).alive)
        except KeyError:
            raise SyntaxError('Invalid comparison operator: {}', self.op)


class NotExpr(BoolExpr):
    __slots__ = ('expr',)

    def __init__(self, expr):
        self.expr = expr

    def eval(self, fsm):
        value = self.expr.eval(fsm)
        if isinstance(value, AthSymbol):
            return AthSymbol(not value.alive)
        else:
            msg = 'May only perform boolean operations on symbols, not {}'
            raise TypeError(msg.format(value.__class__.__name__))


class AndExpr(BoolExpr):
    __slots__ = ('lexpr', 'rexpr')

    def __init__(self, lexpr, rexpr):
        self.lexpr = lexpr
        self.rexpr = rexpr

    def eval(self, fsm):
        lval = self.lexpr.eval(fsm)
        rval = self.rexpr.eval(fsm)
        if isinstance(lval, AthSymbol) and isinstance(rval, AthSymbol):
            return lval and rval
        else:
            msg = 'May only perform boolean operations on symbols, not {}'
            raise TypeError(msg.format(value.__class__.__name__))


class OrExpr(BoolExpr):
    __slots__ = ('lexpr', 'rexpr')

    def __init__(self, lexpr, rexpr):
        self.lexpr = lexpr
        self.rexpr = rexpr

    def eval(self, fsm):
        lval = self.lexpr.eval(fsm)
        rval = self.rexpr.eval(fsm)
        if isinstance(lval, AthSymbol) and isinstance(rval, AthSymbol):
            return lval or rval
        else:
            msg = 'May only perform boolean operations on symbols, not {}'
            raise TypeError(msg.format(value.__class__.__name__))


class XorExpr(BoolExpr):
    __slots__ = ('lexpr', 'rexpr')

    def __init__(self, lexpr, rexpr):
        self.lexpr = lexpr
        self.rexpr = rexpr

    def eval(self, fsm):
        lval = self.lexpr.eval(fsm)
        rval = self.rexpr.eval(fsm)
        if isinstance(lval, AthSymbol) and isinstance(rval, AthSymbol):
            if lval and not rval:
                return lval
            elif not lval and rval:
                return rval
            else:
                return AthSymbol(False)
        else:
            msg = 'May only perform boolean operations on symbols, not {}'
            raise TypeError(msg.format(value.__class__.__name__))


class SymBoolExpr(BoolExpr):
    """Handles all symbol-based boolean syntax."""
    __slots__ = ('op', 'lexpr', 'rexpr')

    def __init__(self, op, lexpr, rexpr):
        self.op = op
        self.lexpr = lexpr
        self.rexpr = rexpr

    def eval(self):
        lval = self.lexpr.eval(fsm)
        rval = self.rexpr.eval(fsm)
        if isinstance(lval, AthSymbol) and isinstance(rval, AthSymbol):
            try:
                if self.op == '!=!':
                    value = (lval.left.alive == rval.left.alive
                        and lval.right.alive == rval.right.alive)
                elif self.op == '!=?':
                    value = lval.left.alive == rval.left.alive
                elif self.op == '?=!':
                    value = lval.right.alive == rval.right.alive
                elif self.op == '~=!':
                    value = (lval.left.alive != rval.left.alive
                        and lval.right.alive == rval.right.alive)
                elif self.op == '!=~':
                    value = (lval.left.alive == rval.left.alive
                        and lval.right.alive != rval.right.alive)
                elif self.op == '~=~':
                    value = (lval.left.alive != rval.left.alive
                        and lval.right.alive != rval.right.alive)
                else:
                    raise SyntaxError('Invalid comparison operator: {}', self.op)
            except AttributeError:
                raise SymbolError('The relevant side(s) must be symbols')
            else:
                return AthSymbol(value)
        else:
            raise TypeError('May only perform living assertions on symbols')


class TernaryExpr(ArithExpr):
    __slots__ = ('when_suite', 'clause', 'unless_suite')

    def __init__(self, when_suite, clause, unless_suite):
        self.when_suite = when_suite
        self.clause = clause
        self.unless_suite = unless_suite

    def eval(self, fsm):
        if self.clause.eval(fsm):
            return self.when_suite.eval(fsm)
        else:
            return self.unless_suite.eval(fsm)


class Serialize(AthExpr):
    __slots__ = ('stmt_list', 'ctrl_name')

    def __init__(self, stmt_list, ctrl_name='THIS'):
        self.stmt_list = stmt_list
        self.ctrl_name = 'THIS'

    def eval(self, fsm):
        for stmt in self.stmt_list:
            try:
                stmt.eval(fsm)
            except SymbolDeath:
                raise


class Statement(AthExpr):
    """Superclass to all builtin statements."""
    __slots__ = ()


class TildeAthLoop(Statement):
    __slots__ = ('grave', 'body')

    def __init__(self, grave, body):
        self.grave = grave
        self.body = body

    def eval(self, fsm):
        dying = self.grave.eval(fsm)
        fsm.push_stack()
        while True:
            try:
                self.body.eval(fsm)
            except SymbolDeath:
                dying = self.grave.eval(fsm)
                if not dying:
                    break
        fsm.pop_stack()


class InputStmt(Statement):
    __slots__ = ('name', 'prompt')

    def __init__(self, name, prompt):
        self.name = name
        self.prompt = prompt if prompt is not None else StringExpr('')

    def eval(self, fsm):
        prompt = self.prompt.eval(fsm)
        if isinstance(prompt, AthSymbol):
            prompt = promp.left
        value = input(prompt)
        try:
            value = int(value)
        except ValueError:
            try:
                value = float(value)
            except ValueError:
                pass
        fsm.assign_name(self.name.name, AthSymbol(left=value))


class ProcreateStmt(Statement):
    __slots__ = ('name', 'expr')

    def __init__(self, name, expr):
        self.name = name
        self.expr = expr

    def eval(self, fsm):
        result = self.expr.eval(fsm)
        if not isinstance(result, AthSymbol):
            symbol = AthSymbol()
            symbol.assign_left(result)
            result = symbol
        elif self.expr.name == 'NULL':
            result = AthSymbol()
        fsm.assign_name(self.name.name, result)


class FabricateStmt(Statement):
    __slots__ = ('name', 'argfmt', 'body')

    def __init__(self, name, argfmt, body):
        self.name = name
        self.argfmt = argfmt
        self.body = body

    def eval(self, fsm):
        raise NotImplementedError(
            '{} has not been implemented.'.format(self.__class__.__name__)
            )


class ExecuteStmt(Statement):
    __slots__ = ('args',)

    def __init__(self, args):
        self.args = args

    def eval(self, fsm):
        raise NotImplementedError(
            '{} has not been implemented.'.format(self.__class__.__name__)
            )


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
        frmtstr = re.sub(r'(?<!\\)~((?:\d)?\.\d)?f', '{:\1f}', frmtstr)
        frmtstr = re.sub(r'(?<=\\)~', '~', frmtstr)
        # Replace whitespace character escapes
        frmtstr = re.sub(r'\\t', '\t', frmtstr)
        frmtstr = re.sub(r'\\t', '\v', frmtstr)
        frmtstr = re.sub(r'\\t', '\f', frmtstr)
        frmtstr = re.sub(r'\\r', '\r', frmtstr)
        frmtstr = re.sub(r'\\n', '\n', frmtstr)
        # Grab the format arguments
        if len(self.args) > 1:
            frmtargs = []
            for arg in self.args[1:]:
                result = arg.eval(fsm)
                if isAthValue(result):
                    frmtargs.append(result)
                elif isinstance(result, AthSymbol):
                    # print(result)
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
        if self.name.name == 'THIS':
            raise EndTilDeath
        self.name.eval(fsm).kill()
        raise SymbolDeath


class ReplicateStmt(Statement):
    __slots__ = ('name', 'expr')

    def __init__(self, name, expr):
        self.name = name
        self.expr = expr

    def eval(self, fsm):
        result = self.expr.eval(fsm)
        if isinstance(result, AthSymbol):
            symbol = result.copy()
        elif isAthValue(result):
            symbol = AthSymbol(result.alive, left=result.left)
        else:
            raise SymbolError('Bad copy: {}'.format(result))
        fsm.assign_name(self.name.name, symbol)


class BifurcateStmt(Statement):
    __slots__ = ('name', 'lexpr', 'rexpr')

    def __init__(self, name, lexpr, rexpr):
        self.name = name
        self.lexpr = lexpr
        self.rexpr = rexpr

    def assign_half(self, fsm, name, value):
        if isinstance(value, AthSymbol):
            fsm.assign_name(name, value)
        elif value is None:
            fsm.assign_name(name, AthSymbol(False))
        else:
            fsm.assign_name(name, AthSymbol(left=value))

    def eval(self, fsm):
        symbol = self.name.eval(fsm)
        if isinstance(symbol, AthSymbol):
            self.assign_half(fsm, self.lexpr.name, symbol.left)
            self.assign_half(fsm, self.rexpr.name, symbol.right)
        else:
            raise SymbolError('May not bifurcate non-symbol')


class AggregateStmt(Statement):
    __slots__ = ('lexpr', 'rexpr', 'name')

    def __init__(self, lexpr, rexpr, name):
        self.lexpr = lexpr
        self.rexpr = rexpr
        self.name = name

    def eval(self, fsm):
        result = AthSymbol()
        lval = self.lexpr.eval(fsm)
        rval = self.rexpr.eval(fsm)

        result.assign_left(lval)
        result.assign_right(rval)
        fsm.assign_name(self.name.name, result)


class BreakUnless(Exception):
    """Raised when an Unless clause successfuly executes."""


class WhenStmt(Statement):
    __slots__ = ('clause', 'suite', 'unlesses')

    def __init__(self, clause, suite, unlesses):
        self.clause = clause
        self.suite = suite
        self.unlesses = unlesses

    def eval(self, fsm):
        if self.clause.eval(fsm):
            self.suite.eval(fsm)
        elif self.unlesses:
            for unless in self.unlesses:
                try:
                    unless.eval(fsm)
                except BreakUnless:
                    break


class UnlessStmt(Statement):
    __slots__ = ('clause', 'body')

    def __init__(self, clause, body):
        self.clause = clause
        self.body = body

    def eval(self, fsm):
        if self.clause is None or self.clause.eval(fsm):
            self.body.eval(fsm)
            raise BreakUnless
