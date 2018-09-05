import re
from athsymbol import (
    AthSymbol, SymbolDeath,
    BuiltinSymbol, NullSymbol,
    )


def import_statement(env, module, symbol):
    pass


def execute_statement(env, *args):
    pass


def inspect_statement(env, frame):
    pass


def input_statement(env, dst, ech):
    pass


format_strings = (
    (r'(?<![\\])~s', '{!s}'),
    (r'(?<![\\])~d', '{:0.0f}'),
    (r'(?<![\\])~((?:\d)?\.\d)?f', '{:\\1f}'),
    )

escapes = (
    (r'\\a', '\a'),
    (r'\\b', '\b'),
    (r'\\r', '\r'),
    (r'\\n', '\n'),
    (r'\\f', '\f'),
    (r'\\t', '\t'),
    (r'\\v', '\v'),
    (r'\\~', '~'),
    )

def print_statement(env, *args):
    if not args:
        raise TypeError('print statement empty')
    frmtstr = args[0]
    fmtargs = args[1:]
    if isinstance(frmtstr, AthSymbol):
        frmtstr = frmtstr.left
    elif not isinstance(frmtstr, str):
        raise TypeError(
            'First argument must be string or symbol containing string'
            )
    if fmtargs:
        for fmtseq in format_strings:
            frmtstr = re.sub(*fmtseq, frmtstr)
        for escape in escapes:
            frmtstr = re.sub(*escape, frmtstr)
        fmtargv = []
        for arg in fmtargs:
            if isinstance(arg, AthSymbol):
                arg = arg.left
            if isinstance(arg, (int, float, complex, str)):
                fmtargv.append(arg)
            else:
                raise ValueError('print symbol left values must be primitive')
        frmtstr.format(*fmtargv)
    else:
        for escape in escapes:
            frmtstr = re.sub(*escape, frmtstr)
    print(frmtstr)
    return frmtstr


def death_statement(env, *syms):
    for grave in syms:
        env.get_symbol(grave.name).kill()
    raise SymbolDeath((sym.name for sym in syms))


def replicate_statement(env, dst, src):
    pass


def procreate_statement(env, dst, src):
    pass


def enumerate_statement(env, src, dst):
    pass


def bifurcate_statement(env, src, lft, rht):
    pass


def aggregate_statement(env, dst, lft, rht):
    pass


def fabricate_statement(env, func):
    pass


def divulgate_statement(env, expr):
    pass


def debate_function(env, *args):
    pass


def unless_function(env, *args):
    pass


class AthBuiltinsDict(dict):
    __slots__ = ()
    instance = None

    def __new__(cls, *args, **kwargs):
        if cls.instance is None:
            cls.instance = super().__new__(cls, *args, **kwargs)
        return cls.instance

    def add_builtin(self, name, item):
        self.__setitem__(name, BuiltinSymbol.from_builtin(name, *item))

    def add_builtins(self, **kwargs):
        self.update(
            {name: BuiltinSymbol.from_builtin(name, *kwargs[name])
             for name in kwargs}
            )

ath_builtins = AthBuiltinsDict(NULL=NullSymbol())
# Putting import token in python call expression is a syntax error
ath_builtins.add_builtin('import', (import_statement, 1, 2))
ath_builtins.add_builtins(
    EXECUTE=(execute_statement, 1, -1),
    INSPECT=(inspect_statement, 1),
    input=(input_statement, 0, 1),
    print=(print_statement, 1, -1),
    DIE=(death_statement, 1, -1),
    REPLICATE=(replicate_statement, 1, 2),
    PROCREATE=(procreate_statement, 1, 2),
    ENUMERATE=(enumerate_statement, 2),
    BIFURCATE=(bifurcate_statement, 3),
    AGGREGATE=(aggregate_statement, 3),
    FABRICATE=(fabricate_statement, 1),
    DIVULGATE=(divulgate_statement, 1),
    DEBATE=(debate_function, 1, -1),
    UNLESS=(unless_function, 1, -1),
    )
