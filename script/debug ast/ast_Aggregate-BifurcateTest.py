#!/usr/bin/env python
from athast import *
from tildeath import TildeAthInterp

interp = TildeAthInterp()
interp.ast = AthAstList([
    ProcreateStmt('LOOP', IntExpr(1)),
    TildeAthLoop(False, AthAstList([
        ProcreateStmt('X', IntExpr(1)),
        ProcreateStmt('Y', IntExpr(2)),
        AggregateStmt('Z', VarExpr('X'), VarExpr('Y')),
        ProcreateStmt('A', IntExpr(3)),
        ReplicateStmt('Y', VarExpr('A')),
        BifurcateStmt('Z', 'B', 'C'),
        PrintStmt([StringExpr('~s, ~s'), VarExpr('B'), VarExpr('C')]),
        KillStmt(VarExpr('LOOP'))
        ], 'LOOP'),
    ExecuteStmt([VarExpr('NULL')])
    ),
    KillStmt(VarExpr('THIS'))
    ], 'THIS')
interp.execute()
