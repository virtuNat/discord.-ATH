#!/usr/bin/env python
from athast import *
from symbol import ThisSymbol
from tildeath import TildeAthInterp

ast = AthAstList([
    ImportStmt('ModuleTest', 'FIB'),
    ProcreateStmt('MAIN', None),
    ProcreateStmt('COUNT', IntExpr(1)),
    TildeAthLoop(False, AthAstList([
        PrintStmt([StringExpr('F~d = ~d\\n'), VarExpr('COUNT'), ExecuteStmt([VarExpr('FIB'), VarExpr('COUNT')])]),
        CondJumpStmt(BinaryExpr('>=', VarExpr('COUNT'), IntExpr(10)), 1),
        KillStmt(['MAIN']),
        ProcreateStmt('COUNT', BinaryExpr('+', VarExpr('COUNT'), IntExpr(1)))
        ], 'MAIN'),
    ExecuteStmt([VarExpr('NULL')])
    ),
    KillStmt(['THIS'])
    ], 'THIS')
interp = TildeAthInterp()
interp.bltin_vars['THIS'] = ThisSymbol('ImportTest.~ATH', ast)
interp.execute(ast)
