import math
import operator
from athsymbol import AthSymbol, BuiltinSymbol
from athbuiltins_default import AthBuiltinsDict, NULL

def math_builtin(func, dtypes):
    def math_proxy_func(*values):
        args = []
        for value in values:
            if isinstance(value, AthSymbol):
                value = value.left
            if isinstance(value, dtypes):
                args.append(value)
            raise TypeError('invalid numerical type')
        return AthSymbol(left=func(*args))
    return BuiltinSymbol.from_builtin(
        math_proxy_func(func, dtypes), 0
        )

math_builtins = AthBuiltinsDict()
math_builtins.update(
    # Basic arithmetic
    ADDTN=math_builtin(operator.add, (int, float, complex)),
    SUBTN=math_builtin(operator.sub, (int, float, complex)),
    MULTP=math_builtin(operator.mul, (int, float, complex)),
    INDIV=math_builtin(operator.floordiv, (int, float, complex)),
    FLDIV=math_builtin(operator.truediv, (int, float, complex)),
    INMOD=math_builtin(operator.mod, (int, float, complex)),
    # Simple relational functions
    FNABS=math_builtin(abs, (int, float, complex)),
    FLOOR=math_builtin(math.floor, (int, float)),
    CEILN=math_builtin(math.ceil, (int, float)),
    FLMOD=math_builtin(math.fmod, (int, float)),
    MANT2=math_builtin(lambda x: math.frexp(x)[0], (int, float)),
    CHAR2=math_builtin(lambda x: math.frexp(x)[1], (int, float)),
    LDEXP=math_builtin(math.ldexp, (int, float)),
    FRACT=math_builtin(lambda x: modf(x)[1], (int, float)),
    TRUNC=math_builtin(math.trunc, (int, float)),
    # Power and logarithm functions
    POWER=math_builtin(operator.pow, (int, float, complex)),
    EXPNP=math_builtin(math.exp, (int, float)),
    EXPM1=math_builtin(math.expm1, (int, float)),
    LOGP1=math_builtin(math.log1p, (int, float)),
    LOGNP=math_builtin(math.log, (int, float)),
    LOGDC=math_builtin(math.log10, (int, float)),
    LOGBN=math_builtin(math.log2, (int, float)),
    SQRRT=math_builtin(math.sqrt, (int, float)),
    # Angular conversion functions
    # R2DEG=math_builtin(math.degrees, (int, float)),
    # D2RAD=math_builtin(math.radians, (int, float)),
    # Circular trig functions
    SINCR=math_builtin(math.sin, (int, float)),
    COSCR=math_builtin(math.cos, (int, float)),
    TANCR=math_builtin(math.tan, (int, float)),
    ASINC=math_builtin(math.asin, (int, float)),
    ACOSC=math_builtin(math.acon, (int, float)),
    ATANC=math_builtin(math.atan, (int, float)),
    ATAN2=math_builtin(math.atan2, (int, float)),
    HYPOT=math_builtin(math.hypot, (int, float)),
    # Hyperbolic trig functions
    SINHY=math_builtin(math.sinh, (int, float)),
    COSHY=math_builtin(math.cosh, (int, float)),
    TANHY=math_builtin(math.tanh, (int, float)),
    ASINH=math_builtin(math.asinh, (int, float)),
    ACOSH=math_builtin(math.acosh, (int, float)),
    ATANH=math_builtin(math.atanh, (int, float)),
    # Other math functions
    ERRFN=math_builtin(math.erf, (int, float)),
    CPERF=math_builtin(math.cerf, (int, float)),
    GAMMA=math_builtin(math.gamma, (int, float)),
    LOGGM=math_builtin(math.lgamma, (int, float)),
    # Constants
    CMPLX_CONST=BuiltinSymbol(left=1j),
    NAPER_CONST=BuiltinSymbol(left=math.e),
    ARCHI_CONST=BuiltinSymbol(left=math.pi),
    RADIA_CONST=BuiltinSymbol(left=math.tau),
    # Inf and NaN
    INF=BuiltinSymbol(left=math.inf),
    NAN=BuiltinSymbol(left=math.nan),
    ISFIN=math_builtin(math.isfinite, (int, float)),
    ISINF=math_builtin(math.isinf, (int, float)),
    ISNAN=math_builtin(math.isnan, (int, float)),
    )
