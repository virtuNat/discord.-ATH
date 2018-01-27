#!/usr/bin/env python
from athast import *
from tildeath import TildeAthInterp

interp = TildeAthInterp()
interp.ast = AthAstList([
    ProcreateStmt('TEST', None),
    TildeAthLoop(False, AthAstList([
        CondJumpStmt(VarExpr('TEST'), 3),
        PrintStmt([StringExpr('Test!\\n')]),
        ReplicateStmt('TEST', UnaryExpr('!', VarExpr('TEST'))),
        CondJumpStmt(None, 5),
        CondJumpStmt(UnaryExpr('!', VarExpr('TEST')), 3),
        PrintStmt([StringExpr('Test died\\n')]),
        KillStmt(VarExpr('THIS')),
        CondJumpStmt(None, 1),
        PrintStmt([StringExpr('should not print\\n')])
        ], 'THIS'),
    ExecuteStmt([VarExpr('NULL')])
    )
    ], 'THIS')
interp.execute()
