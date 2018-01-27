#!/usr/bin/env python
from athast import *
from tildeath import TildeAthInterp

interp = TildeAthInterp()
interp.ast = AthAstList([
    ProcreateStmt('LOOP', IntExpr(0)),
    TildeAthLoop(False, AthAstList([
        PrintStmt([StringExpr('~d'), VarExpr('LOOP')]),
        CondJumpStmt(BinaryExpr('>', VarExpr('LOOP'), IntExpr(9)), 1),
        KillStmt(VarExpr('LOOP')),
        ProcreateStmt('LOOP', BinaryExpr('+', VarExpr('LOOP'), IntExpr(1))),
        PrintStmt([StringExpr(', ')])
        ], 'LOOP'),
    ExecuteStmt([VarExpr('NULL')])
    ),
    PrintStmt([StringExpr('\\n~d\\n'), VarExpr('LOOP')]),
    TildeAthLoop(True, AthAstList([
        PrintStmt([StringExpr('~d'), VarExpr('LOOP')]),
        CondJumpStmt(BinaryExpr('>', VarExpr('LOOP'), IntExpr(0)), 3),
        ReplicateStmt('LOOP', BinaryExpr('-', VarExpr('LOOP'), IntExpr(1))),
        PrintStmt([StringExpr(', ')]),
        KillStmt(VarExpr('LOOP')),
        ReplicateStmt('LOOP', UnaryExpr('!', VarExpr('LOOP'))),
        PrintStmt([StringExpr('\\n')])
        ], 'LOOP'),
    ExecuteStmt([VarExpr('NULL')])
    ),
    KillStmt(VarExpr('THIS'))
    ], 'THIS')
interp.execute()
