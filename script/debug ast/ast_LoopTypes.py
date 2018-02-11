#!/usr/bin/env python
from athast import *
from symbol import ThisSymbol
from tildeath import TildeAthInterp

ast = AthAstList([
    ProcreateStmt('LOOP', IntExpr(0)),
    TildeAthLoop(False, AthAstList([
        PrintStmt([StringExpr('~d'), VarExpr('LOOP')]),
        CondJumpStmt(BinaryExpr('>', VarExpr('LOOP'), IntExpr(9)), 1),
        KillStmt(['LOOP']),
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
        KillStmt(['LOOP']),
        ReplicateStmt('LOOP', UnaryExpr('!', VarExpr('LOOP'))),
        PrintStmt([StringExpr('\\n')])
        ], 'LOOP'),
    ExecuteStmt([VarExpr('NULL')])
    ),
    KillStmt(['THIS'])
    ], 'THIS')
interp = TildeAthInterp()
interp.bltin_vars['THIS'] = ThisSymbol('LoopTypes.~ATH', ast)
interp.execute(ast)
