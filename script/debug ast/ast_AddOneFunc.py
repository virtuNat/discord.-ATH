#!/usr/bin/env python
from athast import *
from tildeath import TildeAthInterp

interp = TildeAthInterp()
interp.ast = AthAstList([
    ProcreateStmt('LOOP', IntExpr(0)),
    ProcreateStmt('A', IntExpr(0)),
    FabricateStmt(AthFunction('ADDONE', [], AthAstList([
        AggregateStmt('A', BinaryExpr('+', VarExpr('A'), IntExpr(1)), VarExpr('NULL')),
        BifurcateStmt('A', 'A', 'NULL')
        ], 'ADDONE')
    )),
    TildeAthLoop(False, AthAstList([
        ExecuteStmt([VarExpr('ADDONE')]),
        PrintStmt([StringExpr('~s '), VarExpr('A')]),
        CondJumpStmt(BinaryExpr('==', VarExpr('A'), IntExpr(256)), 2),
        PrintStmt([StringExpr('\\n')]),
        KillStmt(VarExpr('LOOP'))
        ], 'LOOP'),
    ExecuteStmt([VarExpr('NULL')])
    ),
    KillStmt(VarExpr('THIS'))
    ], 'THIS')
interp.execute()
