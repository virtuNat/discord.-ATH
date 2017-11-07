import operator

class AthExpr(object):
    __slots__ = ()

    def __eq__(self, othr):
        if isinstance(othr, self.__class__):
            try:
                self_attrs = self.__dict__
                othr_attrs = othr.__dict__
            except AttributeError:
                self_attrs = {slot: getattr(self, slot) for slot in self.__slots__}
                othr_attrs = {slot: getattr(othr, slot) for slot in othr.__slots__}
            return self_attrs == othr_attrs
        return False

    def __hash__(self):
        return object.__hash__(self)


class ArithExpr(AthExpr):
    """Superclass to all arithmetic-based syntax."""
    __slots__ = ()


class NumExpr(ArithExpr):
    """Superclass of both integers and floats."""
    __slots__ = ('num')

    def __init__(self, num):
        self.num = num

    def __repr__(self):
        return '{}({})'.format(self.__class__.__name__, self.num)


class FloatExpr(NumExpr):
    pass


class IntExpr(NumExpr):
    pass


class UnaryArithExpr(ArithExpr):
    pass


class BinaryArithExpr(ArithExpr):
    pass


class StringExpr(AthExpr):
    pass


class AthFunction(AthExpr):
    """Superclass of all ~ATH functions."""
    __slots__ = ()


class PrintFunc(AthFunction):
    pass


class KillFunc(AthFunction):
    pass


class AthSymbol(AthExpr):
    """~ATH Variable data structure."""
    __slots__ = ()


class BoolExpr(AthExpr):
    """Superclass to all boolean syntax."""
    __slots__ = ()


class ValueBoolExpr(BoolExpr):
    """Superclass to all value-based boolean syntax."""
    __slots__ = ()


class NotExpr(ValueBoolExpr):
    pass


class AndExpr(ValueBoolExpr):
    pass


class OrExpr(ValueBoolExpr):
    pass


class XorExpr(ValueBoolExpr):
    pass


class SymBoolExpr(BoolExpr):
    """Superclass to all symbol-based boolean syntax."""
    __slots__ = ()


class BothSymBool(SymBoolExpr):
    pass


class LeftSymBool(SymBoolExpr):
    pass


class RightSymBool(SymBoolExpr):
    pass


class NegLeftSymBool(SymBoolExpr):
    pass


class NegRightSymBool(SymBoolExpr):
    pass


class NegBothSymBool(SymBoolExpr):
    pass


class Statement(AthExpr):
    """Superclass to all builtin statements."""
    __slots__ = ()


class BirthStmt(Statement):
    pass


class BifurcateStmt(Statement):
    pass


class AggregateStmt(Statement):
    pass


class WhenStmt(Statement):
    pass


class UnlessStmt(Statement):
    pass


class TernaryStmt(Statement):
    pass


class InputStmt(Statement):
    pass


class TilDeathLoop(Statement):
    pass
