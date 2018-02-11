#!/usr/bin/env python
from athast import *
from symbol import ThisSymbol
from tildeath import TildeAthInterp

ast = AthAstList([
    ProcreateStmt('LOOP', IntExpr(1)),
    TildeAthLoop(False, AthAstList([
        ProcreateStmt('X', IntExpr(1)),
        ProcreateStmt('Y', IntExpr(2)),
        AggregateStmt('Z', VarExpr('X'), VarExpr('Y')),
        ProcreateStmt('A', IntExpr(3)),
        ReplicateStmt('Y', VarExpr('A')),
        BifurcateStmt('Z', 'B', 'C'),
        PrintStmt([StringExpr('~s, ~s'), VarExpr('B'), VarExpr('C')]),
        KillStmt(['LOOP'])
        ], 'LOOP'),
    ExecuteStmt([VarExpr('NULL')])
    ),
    KillStmt(['THIS'])
    ], 'THIS')
interp = TildeAthInterp()
interp.bltin_vars['THIS'] = ThisSymbol('Aggregate-BifurcateTest.~ATH', ast)
interp.execute(ast)
