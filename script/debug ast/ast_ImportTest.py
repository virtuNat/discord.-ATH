#!/usr/bin/env python
from athast import *
from tildeath import TildeAthInterp

interp = TildeAthInterp()
interp.ast = AthAstList([
    ImportStmt('ModuleTest', 'FIB'),
    ProcreateStmt('MAIN', None),
    ProcreateStmt('COUNT', IntExpr(1)),
    TildeAthLoop(False, AthAstList([
        PrintStmt([StringExpr('F~d = ~d\\n'), VarExpr('COUNT'), ExecuteStmt([VarExpr('FIB'), VarExpr('COUNT')])]),
        CondJumpStmt(BinaryExpr('>=', VarExpr('COUNT'), IntExpr(10)), 1),
        KillStmt(VarExpr('MAIN')),
        ProcreateStmt('COUNT', BinaryExpr('+', VarExpr('COUNT'), IntExpr(1)))
        ], 'MAIN'),
    ExecuteStmt([VarExpr('NULL')])
    ),
    KillStmt(VarExpr('THIS'))
    ], 'THIS')
interp.execute()
