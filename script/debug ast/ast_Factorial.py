#!/usr/bin/env python
from athast import *
from tildeath import TildeAthInterp

interp = TildeAthInterp()
interp.ast = AthAstList([
    FabricateStmt(AthFunction('FACT', ['PROD', 'NUM'], AthAstList([
        CondJumpStmt(BinaryExpr('>', VarExpr('NUM'), IntExpr(1)), 1),
        DivulgateStmt(ExecuteStmt([VarExpr('FACT'), BinaryExpr('*', VarExpr('PROD'), VarExpr('NUM')), BinaryExpr('-', VarExpr('NUM'), IntExpr(1))])),
        DivulgateStmt(VarExpr('PROD'))
        ], 'FACT')
    )),
    TildeAthLoop(False, AthAstList([
        InputStmt('NUM', StringExpr('Get the factorial of: ')),
        PrintStmt([StringExpr('The factorial is ~d.\\n'), ExecuteStmt([VarExpr('FACT'), IntExpr(1), VarExpr('NUM')])]),
        KillStmt(VarExpr('THIS'))
        ], 'THIS'),
    ExecuteStmt([VarExpr('NULL')])
    )
    ], 'THIS')
interp.execute()
