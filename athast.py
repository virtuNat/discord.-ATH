"""~ATH's Abstract Syntax Tree definition.

This contains the data structure of ~ATH syntax and its variables,
as well as their implementations. This does not, however, contain
the literals used for lexing.
"""
import operator

def isAthValue(self, obj):
    return (isinstance(obj, int)
        or isinstance(obj, float)
        or isinstance(obj, str))


class SymbolError(Exception):
    """Raised when a symbol-specific exception occurs."""


class AthExpr(object):
    """Base class of all ~ATH AST nodes."""
    __slots__ = ()

    def __eq__(self, othr):
        if isinstance(othr, self.__class__):
            self_attrs = {slot: getattr(self, slot) for slot in self.__slots__}
            othr_attrs = {slot: getattr(othr, slot) for slot in othr.__slots__}
            return self_attrs == othr_attrs
        return False

    def __hash__(self):
        return object.__hash__(self)

    def __repr__(self):
        attr_list = tuple([repr(getattr(self, slot)) for slot in self.__slots__])
        attr_str = ', '.join(attr_list)
        return '{}({})'.format(self.__class__.__name__, attr_str)

    def eval(self, fsm):
        raise NotImplementedError(
            '{} has not been implemented.'.format(self.__class__.__name__)
            )


class AthSymbol(AthExpr):
    """~ATH Variable data structure."""
    __slots__ = ('alive', 'left', 'right')

    def __init__(self, alive=True, left=None, right=None):
        self.alive = alive
        self.left = left
        self.right = right

    def copy(self):
        newsymbol = AthSymbol(self.alive)
        if isinstance(self.left, AthSymbol):
            newsymbol.left = self.left.copy()
        else:
            newsymbol.left = self.left
        if isinstance(self.right, AthSymbol):
            newsymbol.right = self.right.copy()
        else:
            newsymbol.right = self.right
        return newsymbol

    def assign_left(self, value):
        if (isAthValue(value)
            or isinstance(value, AthSymbol)):
            self.left = value
        else:
            raise TypeError(
                'May only assign constants or symbols to left'
                )

    def assign_right(self, value):
        if (isinstance(value, AthFunction)
            or isinstance(value, AthSymbol)):
            self.right = value
        else:
            raise TypeError(
                'May only assign functions or symbols to right'
                )

    def kill(self):
        self.alive = False


class ArithExpr(AthExpr):
    """Superclass to all arithmetic-based syntax."""
    __slots__ = ()


class NumExpr(ArithExpr):
    """Superclass of both integers and floats."""
    __slots__ = ('num',)

    def __init__(self, num):
        self.num = num

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


class IntExpr(NumExpr):
    """Holds integer number values."""
    __slots__ = ()


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
        self.string = string[1:-1]

    def eval(self, fsm):
        return self.string


class AthFunction(AthExpr):
    """Superclass of all ~ATH functions."""
    __slots__ = ()


class PrintFunc(AthFunction):
    """Echoes a string to sys.stdout."""
    __slots__ = ('args',)

    def __init__(self, args):
        self.args = args

    def eval(self, fsm):
        if len(self.args):
            if isinstance(self.args[0], StringExpr):
                frmtstr = self.args[0].string
            elif isinstance(self.args[0], AthSymbol) and isinstance(self.args[0].left, StringExpr):
                frmtstr = self.args[0].left.string
            else:
                raise TypeError(
                    'print must take string or symbol with string as first argument'
                    )
            print(frmtstr)
        else:
            print('')


class KillFunc(AthFunction):
    """Kills a ~ATH symbol."""
    __slots__ = ('name',)

    def __init__(self, name):
        self.name = name

    def eval(self, fsm):
        fsm.lookup_name(self.name).kill()


class BoolExpr(AthExpr):
    """Superclass to all boolean syntax."""
    __slots__ = ()


class ValueBoolExpr(BoolExpr):
    """Superclass to all value-based boolean syntax."""
    __slots__ = ()


class ValueCmpExpr(ValueBoolExpr):
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
            return AthSymbol(self.ops[self.op](lval, rval))
        except KeyError:
            raise SyntaxError('Invalid comparison operator: {}', self.op)


class NotExpr(ValueBoolExpr):
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


class AndExpr(ValueBoolExpr):
    __slots__ = ('lexpr', 'rexpr')

    def __init__(self, lexpr, rexpr):
        self.lexpr = lexpr
        self.rexpr = rexpr

    def eval(self, fsm):
        lval = self.lexpr.eval(fsm)
        rval = self.rexpr.eval(fsm)
        if isinstance(lval, AthSymbol) and isinstance(rval, AthSymbol):
            return lval if not lval.alive else rval
        else:
            msg = 'May only perform boolean operations on symbols, not {}'
            raise TypeError(msg.format(value.__class__.__name__))


class OrExpr(ValueBoolExpr):
    __slots__ = ('lexpr', 'rexpr')

    def __init__(self, lexpr, rexpr):
        self.lexpr = lexpr
        self.rexpr = rexpr

    def eval(self, fsm):
        lval = self.lexpr.eval(fsm)
        rval = self.rexpr.eval(fsm)
        if isinstance(lval, AthSymbol) and isinstance(rval, AthSymbol):
            return rval if not lval.alive else lval
        else:
            msg = 'May only perform boolean operations on symbols, not {}'
            raise TypeError(msg.format(value.__class__.__name__))


class XorExpr(ValueBoolExpr):
    __slots__ = ('lexpr', 'rexpr')

    def __init__(self, lexpr, rexpr):
        self.lexpr = lexpr
        self.rexpr = rexpr

    def eval(self, fsm):
        lval = self.lexpr.eval(fsm)
        rval = self.rexpr.eval(fsm)
        if isinstance(lval, AthSymbol) and isinstance(rval, AthSymbol):
            if lval.alive and not rval.alive:
                return lval
            elif not lval.alive and rval.alive:
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


class Serialize(AthExpr):
    __slots__ = ('lexpr', 'rexpr')

    def __init__(self, lexpr, rexpr):
        self.lexpr = lexpr
        self.rexpr = rexpr

    def eval(self, fsm):
        self.lexpr.eval(fsm)
        self.rexpr.eval(fsm)


class Statement(AthExpr):
    """Superclass to all builtin statements."""
    __slots__ = ()


class ProcreateStmt(Statement):
    __slots__ = ('name', 'expr')

    def __init__(self, name, expr):
        self.name = name
        self.expr = expr

    def eval(self, fsm):
        result = AthSymbol(left=self.expr.eval(fsm))
        fsm.assign_name(self.name, result)


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


class ReplicateStmt(Statement):
    __slots__ = ('name', 'expr')

    def __init__(self, name, expr):
        self.name = name
        self.expr = expr

    def eval(self, fsm):
        result = self.expr.eval(fsm)
        if isinstance(result, AthSymbol):
            symbol = result.copy()
        elif isinstance(result, AthFunction):
            symbol = AthSymbol(result.alive, right=result.right)
        elif isAthValue(result):
            symbol = AthSymbol(result.alive, left=result.left)
        fsm.assign_name(self.name, symbol)


class BifurcateStmt(Statement):
    __slots__ = ('name', 'lexpr', 'rexpr')

    def __init__(self, name, lexpr, rexpr):
        self.name = name
        self.lname = lname
        self.rname = rname

    def eval(self, fsm):
        symbol = fsm.lookup_name(self.name)
        if isinstance(symbol, AthSymbol):
            lval = AthSymbol(left=symbol.left)
            rval = AthSymbol(right=symbol.right)

            fsm.assign_name(self.lname, lval)
            fsm.assign_name(self.rname, rval)
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
        fsm.assign_name(self.name, result)


class WhenStmt(Statement):
    __slots__ = ('clause', 'when_suite', 'unless_suite')

    def __init__(self, clause, when_suite, unless_suite):
        self.clause = clause
        self.when_suite = when_suite
        self.unless_suite = unless_suite

    def eval(self, fsm):
        if self.clause.eval(fsm):
            self.when_suite.eval(fsm)
        elif self.unless_suite:
            self.unless_suite.eval(fsm)


class UnlessStmt(Statement):
    __slots__ = ('clause', 'this_suite', 'next_suite')

    def __init__(self, clause, this_suite, next_suite):
        self.clause = clause
        self.this_suite = this_suite
        self.next_suite = next_suite

    def eval(self, fsm):
        if self.clause is None or self.clause.eval(fsm):
            self.this_suite.eval(fsm)
        elif self.next_suite:
            self.next_suite.eval(fsm)


class TernaryStmt(Statement):
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


class InputStmt(Statement):
    __slots__ = ('name', 'prompt')

    def __init__(self, name, prompt):
        self.name = name
        self.prompt = prompt

    def eval(self, fsm):
        result = AthSymbol(left=input(self.prompt.string))
        fsm.assign_name(self.name, result)
        print([frame.scope_vars for frame in fsm.stack])


class TildeAthLoop(Statement):
    __slots__ = ('grave', 'body')

    def __init__(self, grave, body):
        self.grave = grave
        self.body = body

    def eval(self, fsm):
        dying = fsm.lookup_name(self.grave)
        try:
            while dying.alive:
                self.body.eval(fsm)
                dying = fsm.lookup_name(self.grave)
        except AttributeError:
            raise RuntimeError('Illegal ~ATH loop grave: {!r}'.format(dying))
