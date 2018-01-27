#!/usr/bin/env python
from athast import *
from tildeath import TildeAthInterp

interp = TildeAthInterp()
interp.ast = AthAstList([
    ProcreateStmt('LOOP', VarExpr('NULL')),
    TildeAthLoop(False, AthAstList([
        PrintStmt([StringExpr('Are you there.\\n')]),
        KillStmt(VarExpr('LOOP'))
        ], 'LOOP'),
    ExecuteStmt([VarExpr('NULL')])
    ),
    KillStmt(VarExpr('THIS'))
    ], 'THIS')
interp.execute()
