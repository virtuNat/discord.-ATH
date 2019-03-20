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
        attr_list = tuple(getattr(self, slot) for slot in self.__slots__)
        return f'{self.__class__.__name__}{attr_list}'

    def __call__(self, *args):
        raise NotImplementedError(
            'Override BaseParser call when subclassing.'
            )

    def __add__(self, other):
        """Overload + operator to do concantenation"""
        return ConcatParser(self, other)

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
    """Takes any number of grafters.

    It will only return a graft if all the grafters parse consecutively
    in the order presented.
    """
    __slots__ = ('parsers')

    def __init__(self, left, right):
        if isinstance(left, self.__class__):
            self.parsers = [*left.parsers, right]
        else:
            self.parsers = [left, right]

    def __add__(self, other):
        if isinstance(other, self.__class__):
            self.parsers.extend(other.parsers)
        else:
            self.parsers.append(other)
        return self

    def __radd__(self, other):
        self.parsers.append(other)
        return self

    def __repr__(self):
        return ' + '.join(map(self.format, self.parsers))

    def __call__(self, tokens, index):
        value = []
        for parser in self.parsers:
            graft = parser(tokens, index)
            if not graft:
                return None
            value.append(graft.value)
            index = graft.index
        return Graft(value, index)


class SelectParser(BaseParser):
    """Takes any number of grafters.

    It will evaluate the grafters in the order presented. The first
    grafter to fully match will be returned.
    """
    __slots__ = ('parsers')

    def __init__(self, left, right):
        if isinstance(left, self.__class__):
            self.parsers = [*left.parsers, right]
        else:
            self.parsers = [left, right]

    def __or__(self, other):
        if isinstance(other, self.__class__):
            self.parsers.extend(other.parsers)
        else:
            self.parsers.append(other)
        return self

    def __ror__(self, other):
        self.parsers.append(other)
        return self

    def __repr__(self):
        return ' | '.join(map(self.format, self.parsers))

    def __call__(self, tokens, index):
        for parser in self.parsers:
            graft = parser(tokens, index)
            if graft:
                return graft
        return None


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
        return f'{self.format(self.graft)} ^ {self.format(self.apply)}'

    def __call__(self, tokens, index):
        graft = self.graft(tokens, index)
        if graft:
            graft.value = self.apply(graft.value)
        return graft


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
    __slots__ = ('caller', 'grafter')

    def __init__(self, caller):
        self.caller = caller
        self.grafter = None

    def __repr__(self):
        return f'{self.__class__.__name__}({self.caller})'

    def __call__(self, tokens, index):
        if not self.grafter:
            self.grafter = self.caller()
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
            return graft
        token = tokens[graft.index]
        raise SyntaxError(
            f'Starting from {token.token} on line {token.line}\n'
            )
