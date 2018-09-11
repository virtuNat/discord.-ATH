import math
import operator
from athsymbol import AthSymbol, BuiltinSymbol
from athbuiltins_default import AthBuiltinsDict, NULL

def math_builtin(func, dtypes, argsmin, argsmax, bitmask):
    def math_proxy_wrapper(func, dtypes):
        def math_proxy_func(*values):
            args = []
            for value in values:
                if isinstance(value, dtypes):
                    args.append(value)
                elif (isinstance(value, AthSymbol)
                    and isinstance(value.left, dtypes)
                    ):
                    args.append(value.left)
                raise TypeError('invalid numerical type')
            return func(*args)
        return math_proxy_func
    return BuiltinSymbol.from_builtin(
        math_proxy_wrapper(func, dtypes), argsmin, argsmax, bitmask
        )

math_builtins = AthBuiltinsDict()
math_builtins.update(
    # Basic arithmetic
    ADDTN=math_builtin(operator.add, (int, float, complex), 2, 2, 0),
    SUBTN=math_builtin(operator.sub, (int, float, complex), 2, 2, 0),
    MULTP=math_builtin(operator.mul, (int, float, complex), 2, 2, 0),
    INDIV=math_builtin(operator.floordiv, (int, float, complex), 2, 2, 0),
    FLDIV=math_builtin(operator.truediv, (int, float, complex), 2, 2, 0),
    INMOD=math_builtin(operator.mod, (int, float, complex), 2, 2, 0),
    # Simple relational functions
    FNABS=math_builtin(abs, (int, float, complex), 1, 1, 0),
    FLOOR=math_builtin(math.floor, (int, float), 1, 1, 0),
    CEILN=math_builtin(math.ceil, (int, float), 1, 1, 0),
    FLMOD=math_builtin(math.fmod, (int, float), 2, 2, 0),
    MANT2=math_builtin(lambda x: math.frexp(x)[0], (int, float), 1, 1, 0),
    CHAR2=math_builtin(lambda x: math.frexp(x)[1], (int, float), 1, 1, 0),
    LDEXP=math_builtin(math.ldexp, (int, float), 2, 2, 0),
    FRACT=math_builtin(lambda x: modf(x)[1], (int, float), 1, 1, 0),
    TRUNC=math_builtin(math.trunc, (int, float), 1, 1, 0),
    # Power and logarithm functions
    POWER=math_builtin(operator.pow, (int, float, complex), 2, 2, 0),
    EXPNP=math_builtin(math.exp, (int, float), 1, 1, 0),
    EXPM1=math_builtin(math.expm1, (int, float), 1, 1, 0),
    LOGP1=math_builtin(math.log1p, (int, float), 1, 1, 0),
    LOGNP=math_builtin(math.log, (int, float), 1, 2, 0),
    LOGDC=math_builtin(math.log10, (int, float), 1, 1, 0),
    LOGBN=math_builtin(math.log2, (int, float), 1, 1, 0),
    SQRRT=math_builtin(math.sqrt, (int, float), 1, 1, 0),
    # Angular conversion functions
    # R2DEG=math_builtin(math.degrees, (int, float), 1, 1, 0),
    # D2RAD=math_builtin(math.radians, (int, float), 1, 1, 0),
    # Circular trig functions
    SINCR=math_builtin(math.sin, (int, float), 1, 1, 0),
    COSCR=math_builtin(math.cos, (int, float), 1, 1, 0),
    TANCR=math_builtin(math.tan, (int, float), 1, 1, 0),
    ASINC=math_builtin(math.asin, (int, float), 1, 1, 0),
    ACOSC=math_builtin(math.acon, (int, float), 1, 1, 0),
    ATANC=math_builtin(math.atan, (int, float), 1, 1, 0),
    ATAN2=math_builtin(math.atan2, (int, float), 2, 2, 0),
    HYPOT=math_builtin(math.hypot, (int, float), 2, 2, 0),
    # Hyperbolic trig functions
    SINHY=math_builtin(math.sinh, (int, float), 1, 1, 0),
    COSHY=math_builtin(math.cosh, (int, float), 1, 1, 0),
    TANHY=math_builtin(math.tanh, (int, float), 1, 1, 0),
    ASINH=math_builtin(math.asinh, (int, float), 1, 1, 0),
    ACOSH=math_builtin(math.acosh, (int, float), 1, 1, 0),
    ATANH=math_builtin(math.atanh, (int, float), 1, 1, 0),
    # Other math functions
    ERRFN=math_builtin(math.erf, (int, float), 1, 1, 0),
    CPERF=math_builtin(math.cerf, (int, float), 1, 1, 0),
    GAMMA=math_builtin(math.gamma, (int, float), 1, 1, 0),
    LOGGM=math_builtin(math.lgamma, (int, float), 1, 1, 0),
    # Constants
    CMPLX_CONST=BuiltinSymbol(left=1j),
    NAPER_CONST=BuiltinSymbol(left=math.e),
    ARCHI_CONST=BuiltinSymbol(left=math.pi),
    CIRCL_CONST=BuiltinSymbol(left=math.tau),
    # Inf and NaN
    INF=BuiltinSymbol(left=math.inf),
    NAN=BuiltinSymbol(left=math.nan),
    ISFIN=math_builtin(math.isfinite, (int, float), 1, 1, 0),
    ISINF=math_builtin(math.isinf, (int, float), 1, 1, 0),
    ISNAN=math_builtin(math.isnan, (int, float), 1, 1, 0),
    )
