import operator
from functools import partial
from athsymbol import (
    isAthValue, AthExpr, AthSymbol,
    BuiltinSymbol, AthBuiltinFunction, AthCustomFunction,
    SymbolError,
    )
from athbuiltins_default import ath_builtins

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
    raise SyntaxError(f'Invalid comparison operator: {op}')

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

unops = {
    '+': operator.pos,
    '-': operator.neg,
    '~': operator.inv,
    '!': bool_not,
}

biops = {
    '^': operator.pow,
    '*': operator.mul,
    '/': operator.truediv,
    '/_': operator.floordiv,
    '%': operator.mod,
    '+': operator.add,
    '-': operator.sub,
    '<<': operator.lshift,
    '>>': operator.rshift,
    'b&': operator.and_,
    'b|': operator.or_,
    'b^': operator.xor,
    '<': partial(cmp_opr, op=operator.lt),
    '<=': partial(cmp_opr, op=operator.le),
    '>': partial(cmp_opr, op=operator.gt),
    '>=': partial(cmp_opr, op=operator.ge),
    '==': partial(cmp_opr, op=operator.eq),
    '~=': partial(cmp_opr, op=operator.ne),
    'l&': partial(bool_opr, op='&&'),
    'l|': partial(bool_opr, op='||'),
    'l^': partial(bool_opr, op='^^'),
    '!=!': partial(symbol_opr, op='!=!'),
    '?=!': partial(symbol_opr, op='?=!'),
    '!=?': partial(symbol_opr, op='!=?'),
    '~=!': partial(symbol_opr, op='~=!'),
    '!=~': partial(symbol_opr, op='!=~'),
    '~=~': partial(symbol_opr, op='~=~'),
}

def unopr_expression(env, opr, val):
    ans = unops[opr](val)
    if isAthValue(ans):
        return AthSymbol(left=ans)
    return ans

def biopr_expression(env, opr, lft, rht):
    ans = biops[opr](lft, rht)
    if isAthValue(ans):
        return AthSymbol(left=ans)
    return ans

def on_dead_jump(env, expr, jlen):
    if not expr:
        env.stack[-1].iter_nodes.index += jlen
    return AthSymbol(False)


class ThisSymbol(BuiltinSymbol):
    __slots__ = ()

    def __init__(self, fname, ast):
        self.alive = True
        self.left = fname
        self.right = AthCustomFunction(fname[:-5], [], ast)


class BaseToken(AthExpr):
    pass


class LiteralToken(BaseToken):
    __slots__ = ('value',)

    def __init__(self, token, vtype=str):
        if not isinstance(token, vtype):
            self.value = vtype(token)
        else:
            self.value = token

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return '{}({!r}, {})'.format(
            self.__class__.__name__,
            self.value,
            type(self.value).__name__,
            )


class IdentifierToken(BaseToken):
    __slots__ = ('name',)

    def __init__(self, token):
        self.name = token

    def __str__(self):
        return self.name


class AthExecutor(object):
    """TBD"""
    __slots__ = ('stmt', 'argv')

    def __init__(self, stmt):
        # The statement attached to this object.
        self.stmt = stmt
        # The expression values.
        self.argv = []

    def __repr__(self):
        return f'<Executor for {self.stmt} with values {self.argv}>'

    def is_ready(self):
        return len(self.argv) == len(self.stmt.args)

    def is_name_arg(self):
        bitmask = self.stmt.func.bitmask
        return bitmask < 0 or bitmask & (1 << len(self.argv))

    def get_arg(self):
        return self.stmt.args[len(self.argv)]

    def get_args(self):
        self.argv.clear()
        return self.stmt.args

    def set_argv(self, arg):
        self.argv.append(arg)

    def set_args(self, args):
        self.argv.extend(args)

    def execute(self, env):
        return self.stmt.func(env, *self.argv)


class AthStatement(AthExpr):
    """TBD"""
    __slots__ = ('args', 'name', 'func')

    def __init__(self, args, name, func):
        self.args = args
        self.name = name
        self.func = func

    def __str__(self):
        return f'<{self.name} statement>'

    def __repr__(self):
        return f'{self.__class__.__name__}({self.args})'

    def prepare(self):
        return AthExecutor(self)


class AthTokenStatement(AthStatement):
    """TBD"""
    __slots__ = ()

    def __init__(self, name, args):
        self.name = name
        self.args = args
        self.func = ath_builtins[name].right

    def __repr__(self):
        return f'{self.__class__.__name__}({self.name!r}, {self.args!r})'


class TildeAthLoop(AthStatement):
    __slots__ = ('state', 'body', 'coro')

    def __init__(self, state, body, coro):
        self.name = self.__class__.__name__
        self.state = state
        self.body = body
        self.coro = coro

    def __repr__(self):
        return '{}({}, {}, {})'.format(
            self.__class__.__name__,
            self.state,
            self.body,
            self.coro,
            )

    def prepare(self):
        return self


# Special Statements that do not have tokens associated with them.
class UnaryExpr(AthStatement):
    __slots__ = ()

    def __init__(self, args):
        super().__init__(
            args,
            self.__class__.__name__,
            AthBuiltinFunction(self.__class__.__name__, unopr_expression, 0)
            )


class BnaryExpr(AthStatement):
    __slots__ = ()

    def __init__(self, args):
        super().__init__(
            args,
            self.__class__.__name__,
            AthBuiltinFunction(self.__class__.__name__, biopr_expression, 0)
            )


class CondiJump(AthStatement):
    __slots__ = ()

    def __init__(self, args):
        super().__init__(
            args,
            self.__class__.__name__,
            AthBuiltinFunction(self.__class__.__name__, on_dead_jump, 0)
            )


class AthStatementIter(object):
    __slots__ = ('stmts', 'index', 'pendant')

    def __init__(self, stmts):
        self.stmts = stmts
        self.pendant = stmts.pendant
        self.index = 0

    def __repr__(self):
        return '<{} on stmt {}: {}>'.format(
            self.__class__.__name__,
            self.index,
            self.get_current().name,
            )

    def __iter__(self):
        return self

    def __next__(self):
        try:
            stmt = self.stmts[self.index]
        except IndexError:
            raise StopIteration
        self.index += 1
        return stmt

    def get_current(self):
        return self.stmts[self.index - 1 if self.index > 0 else 0]

    def reset(self):
        self.index = 0


class StmtPrintFrame(object):
    __slots__ = (
        'node', 'nodegen', 'iterlen', 'iterctr', 'useindent',
        )

    def __init__(self, node, attr=None, useindent=True):
        if attr is None:
            iterobj = node
        else:
            iterobj = getattr(node, attr)
        self.node = node
        self.nodegen = iter(iterobj)
        self.iterlen = len(iterobj)
        self.iterctr = 0
        self.useindent = useindent

    def __repr__(self):
        return '<StmtPrintFrame object iterating {} of {} on {}>'.format(
            self.iterctr,
            self.iterlen,
            self.node.__class__.__name__,
            )

    def __iter__(self):
        return self.nodegen

    def __next__(self):
        return next(self.nodegen)

    def __len__(self):
        return self.iterlen

    def add_indent(self, level):
        return self.useindent * level * '    '


class AthStatementList(list):
    __slots__ = ('pendant',)

    def __init__(self, *stmtlist, pendant='THIS'):
        super().__init__(*stmtlist)
        self.pendant = pendant

    def __repr__(self):
        return '{}({}, pendant={!r})'.format(
            self.__class__.__name__,
            super().__repr__(),
            self.pendant,
            )

    def iter_nodes(self):
        return AthStatementIter(self)

    def __eq__(self, other):
        if not isinstance(self, other.__class__):
            return False
        if self.pendant != other.pendant:
            return False
        return all(map(operator.eq, self, other))

    def format(self):
        ident = 1
        stack = [StmtPrintFrame(self)]
        slist = [f'{self.__class__.__name__}([\n']
        while True:
            try:
                item = next(stack[-1])
            except StopIteration:
                item = stack[-1].node
                if len(stack) == 1:
                    slist.append('\n{}], pendant={!r})'.format(
                        stack[-1].add_indent(ident),
                        item.pendant
                        ))
                    return ''.join(slist)
                if isinstance(item, AthStatementList):
                    slist.append('{}], pendant={!r})\n'.format(
                        stack[-1].add_indent(ident),
                        item.pendant,
                        ))
                    ident -= 1
                elif isinstance(item, TildeAthLoop):
                    if stack[-1].iterctr < stack[-1].iterlen:
                        slist.append('{}], pendant={!r}),\n{}{}({!r}, ['.format(
                            stack[-1].add_indent(ident),
                            item.body.pendant,
                            stack[-1].add_indent(ident),
                            item.coro.__class__.__name__,
                            item.coro.name
                            ))
                        stack[-1].nodegen = iter(item.coro.args)
                        stack[-1].useindent = False
                        stack[-1].iterctr += 1
                        continue
                    else:
                        slist[-1] = ']))'
                        ident -= 1
                elif isinstance(item, AthStatement):
                    if slist[-1][-2] == ',':
                        slist[-1] = '])'
                    else:
                        slist.append('])')
                elif isinstance(item, AthCustomFunction):
                    slist.append('\n{}], pendant={!r}))'.format(
                        stack[-1].add_indent(ident),
                        item.body.pendant,
                        ))
                    ident -= 1
                stack.pop()
                if stack[-1].iterctr < stack[-1].iterlen - 1:
                    if isinstance(stack[-1].node,
                        (AthStatementList, AthCustomFunction, TildeAthLoop)
                        ):
                        slist.append(',\n')
                    else:
                        slist.append(', ')
                    stack[-1].iterctr += 1
                continue
            if isinstance(item, AthStatementList):
                slist.append('{}([\n'.format(
                    stack[-1].add_indent(ident),
                    item.__class__.__name__,
                    ))
                stack.append(StmtPrintFrame(item))
                ident += 1
            elif isinstance(item, AthTokenStatement):
                slist.append('{}{}({!r}, ['.format(
                    stack[-1].add_indent(ident),
                    item.__class__.__name__,
                    item.name,
                    ))
                stack.append(StmtPrintFrame(item, 'args', False))
            elif isinstance(item, TildeAthLoop):
                slist.append('{}{}({}, {}([\n'.format(
                    stack[-1].add_indent(ident),
                    item.__class__.__name__,
                    item.state,
                    item.body.__class__.__name__,
                    ))
                stack.append(StmtPrintFrame(item, 'body'))
                stack[-1].iterlen += len(item.coro.args)
                ident += 1
            elif isinstance(item, AthCustomFunction):
                slist.append('{}({!r}, {!r}, {}([\n'.format(
                    item.__class__.__name__,
                    item.name,
                    item.argfmt,
                    item.body.__class__.__name__,
                    ))
                stack.append(StmtPrintFrame(item, 'body'))
                ident += 1
            elif isinstance(item, AthStatement):
                slist.append('{}{}(['.format(
                    stack[-1].add_indent(ident),
                    item.__class__.__name__,
                    ))
                stack.append(StmtPrintFrame(item, 'args', False))
            else:
                slist.append(repr(item))
                stack[-1].iterctr += 1
            if 0 < stack[-1].iterctr:
                if isinstance(stack[-1].node, AthStatementList):
                    slist.append(',\n')
                else:
                    slist.append(', ')
