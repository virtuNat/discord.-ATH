import re
from itertools import filterfalse
from athsymbol import (
    AthSymbol, AthFunction, AthCustomFunction, SymbolDeath,
    BuiltinSymbol, NullSymbol, isAthValue,
    )

NULL = NullSymbol()

class AthBuiltinsDict(dict):
    __slots__ = ()

    def add_builtin(self, name, args):
        self.__setitem__(name, BuiltinSymbol.from_builtin(name, *args))

    def add_builtins(self, **kwargs):
        self.update(
            {name: BuiltinSymbol.from_builtin(name, *kwargs[name])
             for name in kwargs}
            )

ath_builtins = AthBuiltinsDict(NULL=NULL)
ath_modules = {'MATH'}

def pull_name(arg):
    if isinstance(arg, AthSymbol):
        arg = arg.left
    if isinstance(arg, str):
        return arg
    raise TypeError('cannot pull grave from non-string')

def import_statement(env, module, symbol):
    module = pull_name(module)
    symbol = pull_name(symbol)
    try:
        module_vars = env.modules[module]
    except KeyError:
        if module in ath_modules:
            module_vars = __import__(f'athbuiltins_{module.lower()}').builtins_dict
        else:
            subproc = env.__class__()
            try:
                subproc.interpret(module + '.~ATH', True)
            except SystemExit as exit_state:
                if exit_state.args[0]:
                    raise exit_state
            module_vars = subproc.stack[0].scope_vars
        env.modules[module] = module_vars
    try:
        backref = module_vars[symbol]
    except KeyError:
        raise NameError(
            f'symbol {symbol} not found in module {module}'
            )
    env.set_symbol(symbol, backref)
    return backref

def execute_statement(env, *args):
    # Evaluates the validity of a function call before passing to stack.
    # Execute must have at least one argument.
    if not args:
        raise TypeError('execute statement missing function argument')
    argc = len(args) - 1
    # Split the name and the function arguments.
    name, *argv = args
    # EXECUTE(NULL) will return NULL if called and returned from.
    if name is NULL:
        return NULL
    # The name symbol must have a function.
    func = name.right
    if not isinstance(func, AthFunction):
        raise TypeError('first argument must reference a function')
    if isinstance(func, AthCustomFunction):
        # Check if the number of passed arguments matches the intended format.
        if argc != len(func.argfmt):
            raise TypeError(
                f'expected {func.argsmin + 1} arguments, got {argc + 1}'
                )
        # Build the scope dictionary.
        arg_dict = {
            name: (AthSymbol(left=value) if isAthValue(value) else value)
            for name, value in zip(func.argfmt, argv)
            } 
        return func, arg_dict
    # For builtin functions, just pass the arguments as is.
    return func, argv

def inspect_statement(env, index=None):
    if index is None:
        print(ath_builtins)
        for frame in env.stack:
            print(frame.scope_vars)
        return NULL
    if isinstance(index, AthSymbol):
        index = index.left
    if not isinstance(index, int):
        raise TypeError('frame index must be integer')
    print(env.stack[index].scope_vars)
    return NULL

def input_statement(env, dst, ech=None):
    # Takes input from stdin and saves it to a symbol.
    dst = pull_name(dst)
    if ech is None:
        prompt = ''
    elif isAthValue(ech):
        prompt = ech
    elif isinstance(ech, AthSymbol):
        if ech.left is None:
            prompt = ''
        elif isAthValue(ech.left):
            prompt = ech.left
        else:
            raise SymbolError('invalid prompt type')
    else:
        raise SymbolError('invalid prompt type')
    value = input(prompt)
    try:
        value = int(value)
    except ValueError:
        try:
            value = float(value)
        except ValueError:
            try:
                value = complex(value)
            except ValueError:
                pass
    try:
        sym = env.get_symbol(dst)
    except NameError:
        sym = AthSymbol(left=value)
        env.set_symbol(dst, sym)
    else:
        sym.left = value
    return sym

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
    # Echoes a formatted string to stdout.
    if not args:
        raise TypeError('print statement empty')
    frmtstr, fmtargs = args[0], args[1:]
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
            if isAthValue(arg):
                fmtargv.append(arg)
            else:
                raise ValueError('print symbol left values must be primitive')
        frmtstr = frmtstr.format(*fmtargv)
    else:
        for escape in escapes:
            frmtstr = re.sub(*escape, frmtstr)
    print(frmtstr, end='', flush=True)
    return frmtstr

def death_statement(env, *syms):
    # Kills one or a group of symbols, which may change control state.
    graves = []
    for sym in syms:
        grave = pull_name(sym)
        graves.append(grave)
        env.get_symbol(grave).kill()
    raise SymbolDeath(graves)

def replicate_statement(env, dst, src=None):
    dst = pull_name(dst)
    if src is not None:
        if src is NULL:
            # If NULL is replicated, create a new dead symbol.
            sym = AthSymbol(False)
        elif isinstance(src, AthSymbol):
            # If a symbol is replicated, copy it.
            sym = src.copy()
        elif isAthValue(src):
            # If a value is replicated, set it to left.
            sym = AthSymbol(left=src)
        else:
            raise ValueError(f'tried to copy {src!r}')
    else:
        # If there is no expression, assign an empty living symbol.
        sym = AthSymbol()
    env.set_symbol(dst, sym)
    return sym

def procreate_value(sym, src):
    if src is NULL:
        # If NULL is assigned, kill the symbol and empty it.
        sym.copyfrom(NULL)
    elif isAthValue(src):
        # If the result evaluates to a bare value, assign it directly.
        sym.assign_left(src)
    elif isinstance(src, AthSymbol):
        # Otherwise, the value is a symbol, so point the left value to it.
        sym.assign_left(src.left)
    else:
        raise ValueError(f'tried to assign {src!r}')

def procreate_statement(env, dst, src=None):
    dst = pull_name(dst)
    if src is None:
        # If there is no expression, assign an empty living symbol.
        sym = AthSymbol()
        env.set_symbol(dst, sym)
    else:
        try:
            sym = env.get_symbol(dst)
        except NameError:
            # If this symbol's name doesn't exist yet, make it.
            sym = AthSymbol()
            procreate_value(sym, src)
            env.set_symbol(dst, sym)
        else:
            procreate_value(sym, src)
    return sym

def enumerate_statement(env, src, dst):
    if isinstance(src, AthSymbol):
        val = src.left
    else:
        val = src
    if not isinstance(val, str):
        raise TypeError('ENUMERATE only takes strings')

    charlist = [AthSymbol(left=char) for char in val]
    for i in range(len(charlist) - 1):
        charlist[i].assign_right(charlist[i + 1])
    charlist[-1].assign_right(AthSymbol(False))

    env.set_symbol(pull_name(dst), charlist[0])
    return charlist[0]

def bifurcate_statement(env, src, lft, rht):
    # Split a symbol and assign the values to the two names given.
    lft = pull_name(lft)
    rht = pull_name(rht)
    syms = env.get_symbol(pull_name(src))
    syml = symr = None
    if lft != 'NULL':
        if isinstance(syms.left, AthSymbol):
            if lft != src:
                env.set_symbol(lft, syms.left)
            else:
                syml = syms.left
        elif syms.left is None:
            env.set_symbol(lft, AthSymbol(False))
        else:
            env.set_symbol(lft, AthSymbol(left=syms.left))
    if rht != 'NULL':
        if isinstance(syms.right, AthSymbol):
            if rht != src:
                env.set_symbol(rht, syms.right)
            else:
                symr = syms.right
        elif syms.right is None:
            env.set_symbol(rht, AthSymbol(False))
        else:
            env.set_symbol(rht, AthSymbol(right=syms.right))
    if syml is not None:
        syms.copyfrom(syml)
    elif symr is not None:
        syms.copyfrom(symr)
    return NULL

def aggregate_statement(env, dst, lft, rht):
    # Merge two symbols or values together.
    dst = pull_name(dst)
    if lft is NULL:
        lft = NULL.copy()
    if rht is NULL:
        rht = NULL.copy()
    try:
        syms = env.get_symbol(dst)
    except NameError:
        syms = AthSymbol(True, lft, rht)
        env.set_symbol(dst, syms)
    else:
        if isinstance(lft, AthSymbol):
            lft = lft.refcopy(syms)
        if isinstance(rht, AthSymbol):
            rht = rht.refcopy(syms)
        syms.assign_left(lft)
        syms.assign_right(rht)
    return syms

def fabricate_statement(env, func):
    # Attach user-made function object to a symbol.
    try:
        sym = env.get_symbol(func.name)
    except NameError:
        sym = AthSymbol(right=func)
        env.set_symbol(func.name, sym)
    else:
        sym.right = func
    return sym

def divulgate_statement(env, expr):
    # Bring symbol outside function. This should not execute.
    return expr

def debate_function(env, *args):
    # Returns the first dead symbol.
    try:
        return next(filterfalse(None, args))
    except StopIteration:
        return NULL

def unless_function(env, *args):
    # Returns the first living symbol.
    try:
        return next(filter(None, args))
    except StopIteration:
        return NULL

# Putting import token in python call expression is a syntax error
ath_builtins.add_builtin('import', (import_statement, 3))
ath_builtins.add_builtins(
    EXECUTE=(execute_statement, 0),
    INSPECT=(inspect_statement, 0),
    input=(input_statement, 1),
    print=(print_statement, 0),
    DIE=(death_statement, -1),
    REPLICATE=(replicate_statement, 1),
    PROCREATE=(procreate_statement, 1),
    ENUMERATE=(enumerate_statement, 2),
    BIFURCATE=(bifurcate_statement, 7),
    AGGREGATE=(aggregate_statement, 1),
    FABRICATE=(fabricate_statement, 0),
    DIVULGATE=(divulgate_statement, 0),
    DEBATE=(debate_function, 0),
    UNLESS=(unless_function, 0),
    )
