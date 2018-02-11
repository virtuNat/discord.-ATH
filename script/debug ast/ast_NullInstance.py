#!/usr/bin/env python
from athast import *
from symbol import ThisSymbol
from tildeath import TildeAthInterp

ast = AthAstList([
    ProcreateStmt('LOOP', VarExpr('NULL')),
    TildeAthLoop(False, AthAstList([
        PrintStmt([StringExpr('Are you there.\\n')]),
        KillStmt(['LOOP'])
        ], 'LOOP'),
    ExecuteStmt([VarExpr('NULL')])
    ),
    KillStmt(['THIS'])
    ], 'THIS')
interp = TildeAthInterp()
interp.bltin_vars['THIS'] = ThisSymbol('NullInstance.~ATH', ast)
interp.execute(ast)
