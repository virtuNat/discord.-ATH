import operator
from functools import partialmethod

def isAthValue(obj):
    """True if an object is a number or string."""
    return (isinstance(obj, int)
        or isinstance(obj, float)
        or isinstance(obj, str))


class SymbolError(Exception):
    """Raised when a symbol-specific exception occurs."""


class SymbolDeath(Exception):
    """Raised when a symbol dies."""


class EndTilDeath(Exception):
    """Raised when the THIS symbol dies."""


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


class AthSymbol(AthExpr):
    """~ATH Variable data structure."""
    __slots__ = ('alive', 'left', 'right')

    def __init__(self, alive=True, left=None, right=None):
        self.alive = alive
        self.left = left
        self.right = right

    def cmpop(self, other, op):
        if not isAthValue(self.left):
            raise SymbolError('symbol left is not a value')
        if isinstance(other, AthSymbol):
            return AthSymbol(op(self.left, other.left))
        else:
            return AthSymbol(op(self.left, other), self.left, self.right)

    def unoop(self, op):
        if not isAthValue(self.left):
            raise SymbolError('symbol left is not a value')
        return AthSymbol(left=op(self.left))

    def binop(self, other, op):
        if not isAthValue(self.left):
            raise SymbolError('symbol left is not a value')
        if isinstance(other, AthSymbol):
            return AthSymbol(left=op(self.left, other.left))
        else:
            return AthSymbol(left=op(self.left, other), right=self.right)
    
    def reop(self, other, op):
        if not isAthValue(self.left):
            raise SymbolError('symbol left is not a value')
        if isinstance(other, AthSymbol):
            return AthSymbol(left=op(other.left, self.left))
        else:
            return AthSymbol(left=op(other, self.left), right=self.right)

    def inop(self, other, op):
        if not isAthValue(self.left):
            raise SymbolError('symbol left is not a value')
        self.left = op(self.left, other)
        return self

    def __bool__(self):
        return self.alive

    __add__ = partialmethod(binop, op=operator.add)
    __radd__ = partialmethod(reop, op=operator.add)
    __iadd__ = partialmethod(inop, op=operator.add)

    __sub__ = partialmethod(binop, op=operator.sub)
    __rsub__ = partialmethod(reop, op=operator.sub)
    __isub__ = partialmethod(inop, op=operator.sub)

    __mul__ = partialmethod(binop, op=operator.mul)
    __rmul__ = partialmethod(reop, op=operator.mul)
    __imul__ = partialmethod(inop, op=operator.mul)

    __truediv__ = partialmethod(binop, op=operator.truediv)
    __rtruediv__ = partialmethod(reop, op=operator.truediv)
    __itruediv__ = partialmethod(inop, op=operator.truediv)

    __floordiv__ = partialmethod(binop, op=operator.floordiv)
    __rfloordiv__ = partialmethod(reop, op=operator.floordiv)
    __ifloordiv__ = partialmethod(inop, op=operator.floordiv)

    __mod__ = partialmethod(binop, op=operator.mod)
    __rmod__ = partialmethod(reop, op=operator.mod)
    __imod__ = partialmethod(inop, op=operator.mod)

    __pow__ = partialmethod(binop, op=operator.pow)
    __rpow__ = partialmethod(reop, op=operator.pow)
    __ipow__ = partialmethod(inop, op=operator.pow)

    __lshift__ = partialmethod(binop, op=operator.lshift)
    __rlshift__ = partialmethod(reop, op=operator.lshift)
    __ilshift__ = partialmethod(inop, op=operator.lshift)

    __rshift__ = partialmethod(binop, op=operator.rshift)
    __rrshift__ = partialmethod(reop, op=operator.rshift)
    __irshift__ = partialmethod(inop, op=operator.rshift)

    __and__ = partialmethod(binop, op=operator.and_)
    __rand__ = partialmethod(reop, op=operator.and_)
    __iand__ = partialmethod(inop, op=operator.and_)

    __or__ = partialmethod(binop, op=operator.or_)
    __ror__ = partialmethod(reop, op=operator.or_)
    __ior__ = partialmethod(inop, op=operator.or_)

    __xor__ = partialmethod(binop, op=operator.xor)
    __rxor__ = partialmethod(reop, op=operator.xor)
    __ixor__ = partialmethod(inop, op=operator.xor)

    __invert__ = partialmethod(unoop, op=operator.invert)
    __pos__ = partialmethod(unoop, op=operator.pos)
    __neg__ = partialmethod(unoop, op=operator.neg)

    __eq__ = partialmethod(cmpop, op=operator.eq)
    __ne__ = partialmethod(cmpop, op=operator.ne)
    __gt__ = partialmethod(cmpop, op=operator.gt)
    __ge__ = partialmethod(cmpop, op=operator.ge)
    __lt__ = partialmethod(cmpop, op=operator.lt)
    __le__ = partialmethod(cmpop, op=operator.le)

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
