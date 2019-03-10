import math
import operator
from athsymbol import AthSymbol, BuiltinSymbol

def math_builtin(name, func, dtypes):
    def math_proxy_func(env, *values):
        args = []
        for value in values:
            if isinstance(value, AthSymbol):
                value = value.left
            if isinstance(value, dtypes):
                args.append(value)
            else:
                raise TypeError('invalid numerical type')
        return AthSymbol(left=func(*args))
    return BuiltinSymbol.from_builtin(name, math_proxy_func, 0)

builtins_dict = {
    # Basic arithmetic
    'ADDTN': math_builtin('ADDTN', operator.add, (int, float, complex)),
    'SUBTN': math_builtin('SUBTN', operator.sub, (int, float, complex)),
    'MULTP': math_builtin('MULTP', operator.mul, (int, float, complex)),
    'INDIV': math_builtin('INDIV', operator.floordiv, (int, float, complex)),
    'FLDIV': math_builtin('FLDIV', operator.truediv, (int, float, complex)),
    'INMOD': math_builtin('INMOD', operator.mod, (int, float, complex)),
    # Simple relational functions
    'FNABS': math_builtin('FNABS', abs, (int, float, complex)),
    'FLOOR': math_builtin('FLOOR', math.floor, (int, float)),
    'CEILN': math_builtin('CEILN', math.ceil, (int, float)),
    'FLMOD': math_builtin('FLMOD', math.fmod, (int, float)),
    'MANT2': math_builtin('MANT2', lambda x: math.frexp(x)[0], (int, float)),
    'CHAR2': math_builtin('CHAR2', lambda x: math.frexp(x)[1], (int, float)),
    'LDEXP': math_builtin('LDEXP', math.ldexp, (int, float)),
    'FRACT': math_builtin('FRACT', lambda x: modf(x)[1], (int, float)),
    'TRUNC': math_builtin('TRUNC', math.trunc, (int, float)),
    # Power and logarithm functions
    'POWER': math_builtin('POWER', operator.pow, (int, float, complex)),
    'EXPNP': math_builtin('EXPNP', math.exp, (int, float)),
    'EXPM1': math_builtin('EXPM1', math.expm1, (int, float)),
    'LOGP1': math_builtin('LOGP1', math.log1p, (int, float)),
    'LOGNP': math_builtin('LOGNP', math.log, (int, float)),
    'LOGDC': math_builtin('LOGDC', math.log10, (int, float)),
    'LOGBN': math_builtin('LOGBN', math.log2, (int, float)),
    'SQRRT': math_builtin('SQRRT', math.sqrt, (int, float)),
    # Angular conversion functions
    # 'R2DEG': math_builtin('R2DEG', math.degrees, (int, float)),
    # 'D2RAD': math_builtin('D2RAD', math.radians, (int, float)),
    # Circular trig functions
    'SINCR': math_builtin('SINCR', math.sin, (int, float)),
    'COSCR': math_builtin('COSCR', math.cos, (int, float)),
    'TANCR': math_builtin('TANCR', math.tan, (int, float)),
    'ASINC': math_builtin('ASINC', math.asin, (int, float)),
    'ACOSC': math_builtin('ACOSC', math.acos, (int, float)),
    'ATANC': math_builtin('ATANC', math.atan, (int, float)),
    'ATAN2': math_builtin('ATAN2', math.atan2, (int, float)),
    'HYPOT': math_builtin('HYPOT', math.hypot, (int, float)),
    # Hyperbolic trig functions
    'SINHY': math_builtin('SINHY', math.sinh, (int, float)),
    'COSHY': math_builtin('COSHY', math.cosh, (int, float)),
    'TANHY': math_builtin('TANHY', math.tanh, (int, float)),
    'ASINH': math_builtin('ASINH', math.asinh, (int, float)),
    'ACOSH': math_builtin('ACOSH', math.acosh, (int, float)),
    'ATANH': math_builtin('ATANH', math.atanh, (int, float)),
    # Other math functions
    'ERRFN': math_builtin('ERRFN', math.erf, (int, float)),
    'CPERF': math_builtin('CPERF', math.erfc, (int, float)),
    'GAMMA': math_builtin('GAMMA', math.gamma, (int, float)),
    'LOGGM': math_builtin('LOGGM', math.lgamma, (int, float)),
    # Constants
    'CMPLX_CONST': BuiltinSymbol(left=1j),
    'NAPER_CONST': BuiltinSymbol(left=math.e),
    'ARCHI_CONST': BuiltinSymbol(left=math.pi),
    'RADIA_CONST': BuiltinSymbol(left=math.tau),
    # Inf and NaN
    'INF': BuiltinSymbol(left=math.inf),
    'NAN': BuiltinSymbol(left=math.nan),
    'ISFIN': math_builtin('ISFIN', math.isfinite, (int, float)),
    'ISINF': math_builtin('ISINF', math.isinf, (int, float)),
    'ISNAN': math_builtin('ISNAN', math.isnan, (int, float)),
    }
