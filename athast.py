import operator

class AthExpr(object):
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
        attr_list = tuple([getattr(self, slot) for slot in self.__slots__])
        if len(attr_list) == 1:
            attr_str = repr(attr_list)[:-2] + ')'
        else:
            attr_str = repr(attr_list)
        return '{}{}'.format(self.__class__.__name__, attr_str)


class ArithExpr(AthExpr):
    """Superclass to all arithmetic-based syntax."""
    __slots__ = ()


class NumExpr(ArithExpr):
    """Superclass of both integers and floats."""
    __slots__ = ('num')


class FloatExpr(NumExpr):
    """Holds float number values. 

    Arithmetic operators handle float and int values differently;
    for addition, subtraction, and multiplication, return a float
    if at least one operand is float otherwise return int.

    For true division, return type is always float.
    For floor division, return type is always int.
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
    __slots__ = ('op', 'value')

    def __init__(self, op, value):
        self.op = op
        self.value = value


class BinaryArithExpr(ArithExpr):
    __slots__ = ('op', 'lval', 'rval')

    def __init__(self, op, lval, rval):
        self.op = op
        self.lval = lval
        self.rval = rval


class StringExpr(AthExpr):
    """Holds string values."""
    __slots__ = ('string')

    def __init__(self, string):
        self.string = string


class AthFunction(AthExpr):
    """Superclass of all ~ATH functions."""
    __slots__ = ()


class PrintFunc(AthFunction):
    """Echoes a string to sys.stdout."""
    __slots__ = ('args')

    def __init__(self, *args):
        self.args = args


class KillFunc(AthFunction):
    """Kills a ~ATH symbol."""
    __slots__ = ('symbol')

    def __init__(self, symbol):
        self.symbol = symbol


class AthSymbol(AthExpr):
    """~ATH Variable data structure."""
    __slots__ = ()


class BoolExpr(AthExpr):
    """Superclass to all boolean syntax."""
    __slots__ = ()


class ValueBoolExpr(BoolExpr):
    """Superclass to all value-based boolean syntax."""
    __slots__ = ()


class ValueCmpExpr(ValueBoolExpr):
    __slots__ = ('op', 'lval', 'rval')

    def __init__(self, op, lval, rval):
        self.op = op
        self.lval = lval
        self.rval = rval


class NotExpr(ValueBoolExpr):
    __slots__ = ('value')

    def __init__(self, value):
        self.value = value


class AndExpr(ValueBoolExpr):
    __slots__ = ('lval', 'rval')

    def __init__(self, lval, rval):
        self.lval = lval
        self.rval = rval


class OrExpr(ValueBoolExpr):
    __slots__ = ('lval', 'rval')

    def __init__(self, lval, rval):
        self.lval = lval
        self.rval = rval


class XorExpr(ValueBoolExpr):
    __slots__ = ('lval', 'rval')

    def __init__(self, lval, rval):
        self.lval = lval
        self.rval = rval


class SymBoolExpr(BoolExpr):
    """Superclass to all symbol-based boolean syntax."""
    __slots__ = ('op', 'lval', 'rval')

    def __init__(self, op, lval, rval):
        self.op = op
        self.lval = lval
        self.rval = rval


class Statement(AthExpr):
    """Superclass to all builtin statements."""
    __slots__ = ()


class BirthStmt(Statement):
    __slots__ = ('name', 'expr')

    def __init__(self, name, expr):
        self.name = name
        self.expr = expr


class BirthFuncStmt(Statement):
    __slots__ = ('name', 'argfmt', 'body')

    def __init__(self, name, argfmt, body):
        self.name = name
        self.argfmt = argfmt
        self.body = body


class BifurcateStmt(Statement):
    __slots__ = ('name', 'lname', 'rname')

    def __init__(self, name, lname, rname):
        self.name = name
        self.lname = lname
        self.rname = rname


class AggregateStmt(Statement):
    __slots__ = ('lname', 'rname', 'name')

    def __init__(self, lname, rname, name):
        self.lname = lname
        self.rname = rname
        self.name = name


class WhenStmt(Statement):
    __slots__ = ('clause', 'when_suite', 'unless_suite')

    def __init__(self, clause, when_suite, unless_suite):
        self.clause = clause
        self.when_suite = when_suite
        self.unless_suite = unless_suite


class UnlessStmt(Statement):
    __slots__ = ('clause', 'this_suite', 'next_suite')

    def __init__(self, clause, this_suite, next_suite):
        self.clause = clause
        self.this_suite = this_suite
        self.next_suite = next_suite


class TernaryStmt(Statement):
    __slots__ = ('when_suite', 'clause', 'unless_suite')

    def __init__(self, when_suite, clause, unless_suite):
        self.when_suite = when_suite
        self.clause = clause
        self.unless_suite = unless_suite


class InputStmt(Statement):
    __slots__ = ('name', 'prompt')

    def __init__(self, name, prompt):
        self.name = name
        self.prompt = prompt


class TildeAthLoop(Statement):
    __slots__ = ('clause', 'body')

    def __init__(self, clause, body):
        self.clause = clause
        self.body = body
