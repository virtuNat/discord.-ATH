"""Functions that link tokens together based on defined criteria and behavior."""
from lexer import Token


class Graft(object):
    """As the name implies, a graft of the AST's leaves."""
    __slots__ = ('value', 'index')

    def __init__(self, value, index):
        self.value = value
        self.index = index

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return (self.value, self.index) == (other.value, other.index)
        else:
            raise TypeError('May not comapre Grafts to non-Grafts.')

    def __hash__(self):
        return object.__hash__((self.value, self.index))

    def __repr__(self):
        return f'{self.__class__.__name__}({self.value}, {self.index})'


class BaseParser(object):
    """Grafts tokens together. Primitive."""
    __slots__ = ()

    def __repr__(self):
        attr_list = tuple(repr(getattr(self, slot)) for slot in self.__slots__)
        return f'{self.__class__.__name__}{attr_list}'

    def __call__(self, *args):
        raise NotImplementedError(
            'Override BaseParser call when subclassing.'
            )

    def __add__(self, other):
        """Overload + operator to do concantenation"""
        return ConcatParser(self, other)

    def __mul__(self, other):
        """Overload * operator to do L-R evaluation"""
        return ExprsnParser(self, other)

    def __pow__(self, other):
        """Overload ** operator to do strict eval"""
        return StrictParser(self, other)

    def __or__(self, other):
        """Overload | operator to do alt selection"""
        return SelectParser(self, other)

    def __xor__(self, other):
        """Overload ^ operator to do I-P evaluation"""
        return WrapprParser(self, other)

    def format(self, other):
        if (
            not isinstance(other, self.__class__)
            and isinstance(other, (
                ConcatParser,
                SelectParser,
                ExprsnParser,
                StrictParser,
                WrapprParser,
                ))
            ):
            return f'({other!r})'
        return repr(other)


class ConcatParser(BaseParser):
    """Takes two grafters, the left and the right.

    It will evaluate the left grafter first, then the right grafter.
    If both succeed it will return a tuple of the results, otherwise
    it will return None.
    """
    __slots__ = ('leval', 'reval')

    def __init__(self, left, right):
        self.leval = left
        self.reval = right

    def __repr__(self):
        return f'{self.format(self.leval)} + {self.format(self.reval)}'

    def __call__(self, tokens, index):
        lvalue = self.leval(tokens, index)
        if not lvalue:
            return None
        rvalue = self.reval(tokens, lvalue.index)
        if not rvalue:
            return None
        if isinstance(lvalue.value, list): # Avoid recursive lists.
            return Graft(lvalue.value + [rvalue.value], rvalue.index)
        return Graft([lvalue.value, rvalue.value], rvalue.index)


class SelectParser(BaseParser):
    """Takes two grafters, the left and the right.

    It will evaluate the left grafter first. If the left grafter is
    successful, it will return from that. Otherwise it will evaluate
    and return from the right grafter.
    """
    __slots__ = ('leval', 'reval')

    def __init__(self, left, right):
        self.leval = left
        self.reval = right

    def __repr__(self):
        return f'{self.format(self.leval)} | {self.format(self.reval)}'

    def __call__(self, tokens, index):
        return self.leval(tokens, index) or self.reval(tokens, index)


class WrapprParser(BaseParser):
    """Takes a grafter and a function.

    It will evaluate the grafter as arguments for the function,
    and return the result of the function's evaluation as a graft.
    """
    __slots__ = ('graft', 'apply')

    def __init__(self, grafter, func):
        self.graft = grafter
        self.apply = func

    def __repr__(self):
        return f'{self.format(self.grafy)} ^ {self.format(self.apply)}'

    def __call__(self, tokens, index):
        graft = self.graft(tokens, index)
        if graft:
            graft.value = self.apply(graft.value)
            return graft
        return None


class ExprsnParser(BaseParser):
    """A grafter that evaluates expressions using two grafters.

    The first grafter returns a list of items, while the
    second grafter returns a list of separators (operators).
    The grafter will evaluate the items left to right, using
    the separators to reference the operations that need to
    be applied to the items. Returns a graft of the result.
    """
    __slots__ = ('graft', 'group', 'tokens', 'result')

    def __init__(self, grafter, grouper):
        self.graft = grafter
        self.group = grouper

    def __repr__(self):
        return f'{self.format(self.graft)} * {self.format(self.group)}'

    def graft_next(self):
        """Concatenate the separator function and the next item
        and return the graft result of applying eval_next to
        both. If the separator matches but the next item does not,
        increment the index and return None.
        """
        sepmatch = self.group(self.tokens, self.result.index)
        if sepmatch:
            item = self.graft(self.tokens, sepmatch.index)
            if item:
                item.value = sepmatch.value(self.result.value, item.value)
                return item
            else:
                self.result.index += 1
        return None

    def __call__(self, tokens, index):
        self.tokens = tokens
        self.result = self.graft(tokens, index)
        newresult = self.result
        while newresult:
            newresult = self.graft_next()
            if newresult:
                self.result = newresult
        return self.result


class StrictParser(BaseParser):
    """ExprsnParser, but strict and doesn't allow dangling separators."""
    __slots__ = ('graft', 'group', 'result', 'graft_next')

    def __init__(self, grafter, grouper):
        self.graft = grafter
        self.group = grouper
        self.graft_next = self.group + self.graft ^ self.eval_next

    def __repr__(self):
        return f'{self.format(self.graft)} ** {self.format(self.group)}'

    def eval_next(self, graft):
        """Using the function bound to the separator, and the
        item currently being looked at, evaluate the function
        on the current expression result and the item.
        """
        sep_func, next_item = graft
        return sep_func(self.result.value, next_item)

    def __call__(self, tokens, index):
        self.result = self.graft(tokens, index)
        newresult = self.result
        while newresult:
            newresult = self.graft_next(tokens, self.result.index)
            if newresult:
                self.result = newresult
        return self.result


class ItemParser(Token, BaseParser):
    """A grafter wrapper around a representative token value.

    It will return a Graft object if it can pull a token of the
    exact same type as the one represented by it, otherwise it will
    return None.
    """
    __slots__ = ()

    def __repr__(self):
        return f'{self.__class__.__name__}({self.token!r}, {self.tag!r})'

    def __eq__(self, other):
        try:
            return (self.token, self.tag) == (other.token, other.tag)
        except AttributeError:
            raise TypeError(
                f'can\'t compare Token to {other.__class__.__name__}'
                )

    def __hash__(self):
        """Don't break hashability, at least not yet."""
        return object.__hash__(self)

    def __call__(self, tokens, index):
        if index < len(tokens) and self == tokens[index]:
            return Graft(self.token, index + 1)
        return None


class TagsParser(BaseParser):
    """ItemParser, but only matches tags."""
    __slots__ = ('tag',)

    def __init__(self, tag):
        self.tag = tag

    def __eq__(self, other):
        try:
            return self.tag == other.tag
        except AttributeError:
            raise TypeError(
                f'Can\'t compare tag of {other.__class__.__name__}'
                )

    def __hash__(self):
        """Don't break hashability, at least not yet."""
        return object.__hash__(self)

    def __call__(self, tokens, index):
        if index < len(tokens) and self.tag == tokens[index].tag:
            return Graft(tokens[index].token, index + 1)
        return None


class OptionParser(BaseParser):
    """Guarantees that the result of a graft evaluation is a Graft object;
    if the evaluation fails the graft object's value is set to None.

    Used when some syntax is optional in a statement or clause.
    """
    __slots__ = ('graft',)

    def __init__(self, grafter):
        self.graft = grafter

    def __call__(self, tokens, index):
        return self.graft(tokens, index) or Graft(None, index)


class RepeatParser(BaseParser):
    """A grafter that will apply itself repeatedly until failure,
    returning the list of all grafts created from iteration.

    Used to build a list of arguments, tokens, and the like.
    """
    __slots__ = ('graft',)

    def __init__(self, grafter):
        self.graft = grafter

    def __call__(self, tokens, index):
        grafts = []
        graft = self.graft(tokens, index)
        while graft:
            grafts.append(graft.value)
            index = graft.index
            graft = self.graft(tokens, index)
        return Graft(grafts, index)


class LazierParser(BaseParser):
    """A grafter wrapper that takes a function returning a grafter,
    instead of a grafter itself. When called the first time, it will
    create its grafter from the function.

    Used to prevent stack overflow from recursive parsing.
    """
    __slots__ = ('grafter_func', 'grafter')

    def __init__(self, grafter_func):
        self.grafter_func = grafter_func
        self.grafter = None

    def __repr__(self):
        return f'{self.__class__.__name__}({self.grafter_func})'

    def __call__(self, tokens, index):
        if not self.grafter:
            self.grafter = self.grafter_func()
        return self.grafter(tokens, index)


class ScriptParser(BaseParser):
    """A grafter that must evaluate every token in the token list
    provided to it in order to return a graft, otherwise returns None.

    Used to prevent partially matching garbage code.
    """
    __slots__ = ('grafter',)

    def __init__(self, grafter):
        self.grafter = grafter

    def __call__(self, tokens, index):
        graft = self.grafter(tokens, index)
        if graft.index == len(tokens):
            # print('Final:\n', graft.value, '\n', sep='')
            return graft
        token = tokens[graft.index]
        raise SyntaxError(
            f'Starting from {token.token} on line {token.line}\n'
            )
