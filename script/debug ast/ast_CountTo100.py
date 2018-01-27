#!/usr/bin/env python
from athast import *
from tildeath import TildeAthInterp

interp = TildeAthInterp()
interp.ast = AthAstList([
    ProcreateStmt('A', IntExpr(0)),
    FabricateStmt(AthFunction('COUNT', [], AthAstList([
        CondJumpStmt(BinaryExpr('<', VarExpr('A'), IntExpr(100)), 3),
        ProcreateStmt('A', BinaryExpr('+', VarExpr('A'), IntExpr(1))),
        PrintStmt([StringExpr('~s '), VarExpr('A')]),
        ExecuteStmt([VarExpr('COUNT')])
        ], 'COUNT')
    )),
    ProcreateStmt('LOOP', IntExpr(0)),
    TildeAthLoop(False, AthAstList([
        ExecuteStmt([VarExpr('COUNT')]),
        KillStmt(VarExpr('LOOP'))
        ], 'LOOP'),
    ExecuteStmt([VarExpr('NULL')])
    ),
    KillStmt(VarExpr('THIS'))
    ], 'THIS')
interp.execute()
