#!/usr/bin/env python
from athast import *
from symbol import ThisSymbol
from tildeath import TildeAthInterp

ast = AthAstList([
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
        KillStmt(['LOOP'])
        ], 'LOOP'),
    ExecuteStmt([VarExpr('NULL')])
    ),
    KillStmt(['THIS'])
    ], 'THIS')
interp = TildeAthInterp()
interp.bltin_vars['THIS'] = ThisSymbol('CountTo100.~ATH', ast)
interp.execute(ast)
