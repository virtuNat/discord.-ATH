#!/usr/bin/env python
from athast import *
from symbol import ThisSymbol
from tildeath import TildeAthInterp

ast = AthAstList([
    ProcreateStmt('LOOP', IntExpr(0)),
    TildeAthLoop(True, AthAstList([
        PrintStmt([StringExpr("This shouldn't print.\\n")])
        ], 'LOOP'),
    ExecuteStmt([VarExpr('NULL')])
    ),
    PrintStmt([StringExpr('Yay.\\n')]),
    KillStmt(['THIS'])
    ], 'THIS')
interp = TildeAthInterp()
interp.bltin_vars['THIS'] = ThisSymbol('Negation.~ATH', ast)
interp.execute(ast)
