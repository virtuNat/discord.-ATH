"""Contains ~ATH's AST and data structure primitives for easier access."""
import operator
from functools import partialmethod


def isAthValue(obj):
    """True if an object is a number or string."""
    return (isinstance(obj, int)
        or isinstance(obj, float)
        or isinstance(obj, complex)
        or isinstance(obj, str))


class SymbolError(Exception):
    """Raised when a symbol-specific exception occurs."""


class SymbolDeath(Exception):
    """Raised when a symbol dies."""


class DivulgateBack(Exception):
    """Raised when Divulgate is called."""


class EndTilDeath(Exception):
    """Raised when the THIS symbol dies."""


class BreakUnless(Exception):
    """Raised when an Unless clause successfuly executes."""


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


class AthFunction(AthExpr):
    """Function objects in ~ATH."""
    __slots__ = ('name', 'argfmt', 'body')

    def __init__(self, name, argfmt, body):
        self.name = name
        self.argfmt = argfmt
        self.body = body

    def execute(self, fsm, args):
        value = AthSymbol(False)
        with fsm.push_stack(args):
            for stmt in self.body.stmt_list:
                try:
                    stmt.eval(fsm)
                except DivulgateBack:
                    try:
                        value = stmt.value
                    except AttributeError:
                        value = stmt.body.value
                    break
                except SymbolDeath:
                    if not fsm.lookup_name('THIS').alive:
                        raise EndTilDeath
                    elif not fsm.lookup_name(self.name).alive:
                        break
        return value


# class AthRefList(list):
#     """A list of symbols can't use __eq__ to compare values in lists."""

#     def __contains__(self, obj):
#         """Force in checks to use identity comparisons."""
#         for item in self:
#             if item is obj:
#                 return True
#         return False

#     def remove(self, obj):
#         """Force removals to use identity comparisons."""
#         idx = 0
#         for item in self:
#             if item is obj:
#                 self.pop(idx)
#                 return None
#             idx += 1


class AthSymbol(AthExpr):
    """~ATH Variable data structure."""
    __slots__ = ('alive', 'left', 'right') #, 'leftof', 'rightof')

    def __init__(self, alive=True, left=None, right=None):
        self.alive = alive
        self.left = None
        self.right = None
        self.assign_left(left)
        self.assign_right(right)
        # self.leftof = AthRefList()
        # self.rightof = AthRefList()

    def __repr__(self):
        """Represent this symbol."""
        return '{}({}, {!r}, {!r})'.format(
            self.__class__.__name__,
            self.alive, self.left, self.right
            )

    def cmpop(self, other, op):
        """Base function for comparison operators."""
        if not isAthValue(self.left):
            raise SymbolError('symbol left is not a value')
        if isinstance(other, AthSymbol):
            return AthSymbol(op(self.left, other.left))
        else:
            return AthSymbol(op(self.left, other), self.left, self.right)

    def unoop(self, op):
        """Base function for unary operators."""
        if not isAthValue(self.left):
            raise SymbolError('symbol left is not a value')
        return AthSymbol(left=op(self.left))

    def binop(self, other, op):
        """Base function for binary operators."""
        if not isAthValue(self.left):
            raise SymbolError('symbol left is not a value')
        if isinstance(other, AthSymbol):
            return AthSymbol(left=op(self.left, other.left))
        else:
            return AthSymbol(left=op(self.left, other), right=self.right)

    def reop(self, other, op):
        """Base function for reverse binary operators."""
        if not isAthValue(self.left):
            raise SymbolError('symbol left is not a value')
        return AthSymbol(left=op(other, self.left), right=self.right)

    def inop(self, other, op):
        """Base function for in-place binary operators."""
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

    def __contains__(self, symbol):
        """Returns True if this symbol contains the given symbol as
        one of its left or right values, or the left or right values
        of those values if they're also symbols.

        Note that this performs the test recursively, and might be slow
        for large-scale binary symbol heaps.
        """
        if self.left is symbol or self.right is symbol:
            # If either side is the symbol, return True.
            return True
        elif isinstance(self.left, AthSymbol):
            if isinstance(self.right, AthSymbol):
                # If both values are symbols, return True
                # if at least one value contains the symbol
                return (
                    self.left.__contains__(symbol) or 
                    self.right.__contains__(symbol)
                    )
            else:
                # If only left is a symbol, check that one
                return self.left.__contains__(symbol)
        elif isinstance(self.right, AthSymbol):
            # If only right is a symbol, check that one
            return self.right.__contains__(symbol)
        else:
            # If neither are symbols, return False.
            return False


    def copy(self):
        """Deep copies this symbol and returns the result."""
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

    def refcopy(self, ref):
        """Replaces all instances of a reference symbol in
        this symbol with deep copies of that reference symbol.
        """
        if ref is self:
            return self.copy()
        if isinstance(self.left, AthSymbol):
            self.assign_left(self.left.refcopy(ref))
        if isinstance(self.right, AthSymbol):
            self.assign_right(self.right.refcopy(ref))
        return self

    def assign_left(self, value):
        if not (isAthValue(value)
            or isinstance(value, AthSymbol)
            or value is None
            ):
            raise TypeError(
                'May only assign constants or symbols to left'
                )
        # if isinstance(self.left, AthSymbol):
        #     self.left.leftof.remove(self)
        self.left = value
        # if isinstance(value, AthSymbol) and self not in value.leftof:
        #     self.left.leftof.append(self)


    def assign_right(self, value):
        if not (isinstance(value, AthFunction)
            or isinstance(value, AthSymbol)
            or value is None
            ):
            raise TypeError(
                'May only assign functions or symbols to right'
                )
        # if isinstance(self.right, AthSymbol):
        #     self.right.rightof.remove(self)
        self.right = value
        # if isinstance(value, AthSymbol) and self not in value.rightof:
        #     self.right.rightof.append(self)

    def kill(self):
        """THIS.DIE()"""
        self.alive = False


class BuiltinSymbol(AthSymbol):
    __slots__ = ()

    def __init__(self, alive=True):
        self.alive = alive
        self.left = None
        self.right = None
        # self.leftof = AthRefList()
        # self.rightof = AthRefList()

    def assign_left(self, value):
        echo_error('SymbolError: Builtins cannot be assigned to!')

    def assign_right(self, value):
        echo_error('SymbolError: Builtins cannot be assigned to!')

    def inop(self, other, op):
        echo_error('SymbolError: Builtins cannot be assigned to!')
