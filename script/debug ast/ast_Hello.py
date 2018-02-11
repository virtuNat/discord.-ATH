#!/usr/bin/env python
from athast import *
from symbol import ThisSymbol
from tildeath import TildeAthInterp

ast = AthAstList([
    TildeAthLoop(False, AthAstList([
        PrintStmt([StringExpr('Hello World!\\n')]),
        PrintStmt([StringExpr('This is the script ~s!\\n'), VarExpr('THIS')]),
        KillStmt(['THIS'])
        ], 'THIS'),
    ExecuteStmt([VarExpr('NULL')])
    )
    ], 'THIS')
interp = TildeAthInterp()
interp.bltin_vars['THIS'] = ThisSymbol('Hello.~ATH', ast)
interp.execute(ast)
