#!/usr/bin/env python
from athast import *
from symbol import ThisSymbol
from tildeath import TildeAthInterp

ast = AthAstList([
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
        KillStmt(['LOOP'])
        ], 'LOOP'),
    ExecuteStmt([VarExpr('NULL')])
    ),
    KillStmt(['THIS'])
    ], 'THIS')
interp = TildeAthInterp()
interp.bltin_vars['THIS'] = ThisSymbol('AddOneFunc.~ATH', ast)
interp.execute(ast)
