#!/usr/bin/env python
from athast import *
from symbol import ThisSymbol
from tildeath import TildeAthInterp

ast = AthAstList([
    FabricateStmt(AthFunction('ACK', ['M', 'N'], AthAstList([
        CondJumpStmt(BinaryExpr('==', VarExpr('M'), IntExpr(0)), 2),
        DivulgateStmt(BinaryExpr('+', VarExpr('N'), IntExpr(1))),
        CondJumpStmt(None, 4),
        CondJumpStmt(BinaryExpr('==', VarExpr('N'), IntExpr(0)), 2),
        DivulgateStmt(ExecuteStmt([VarExpr('ACK'), BinaryExpr('-', VarExpr('M'), IntExpr(1)), IntExpr(1)])),
        CondJumpStmt(None, 1),
        DivulgateStmt(ExecuteStmt([VarExpr('ACK'), BinaryExpr('-', VarExpr('M'), IntExpr(1)), ExecuteStmt([VarExpr('ACK'), VarExpr('M'), BinaryExpr('-', VarExpr('N'), IntExpr(1))])]))
        ], 'ACK')
    )),
    TildeAthLoop(False, AthAstList([
        InputStmt('NUM', StringExpr('Get the ackermann function of: ')),
        PrintStmt([StringExpr('The value of A(n, n) is ~d.\\n'), ExecuteStmt([VarExpr('ACK'), VarExpr('NUM'), VarExpr('NUM')])]),
        KillStmt(['THIS'])
        ], 'THIS'),
    ExecuteStmt([VarExpr('NULL')])
    )
    ], 'THIS')
interp = TildeAthInterp()
interp.bltin_vars['THIS'] = ThisSymbol('Ackermann.~ATH', ast)
interp.execute(ast)
