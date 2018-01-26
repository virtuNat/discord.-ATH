#!/usr/bin/env python
from athast import *
from tildeath import TildeAthInterp

interp = TildeAthInterp()
interp.ast = AthAstList([FabricateStmt(AthFunction('ACK', ['M', 'N'], AthAstList([CondJumpStmt(BinaryExpr('==', VarExpr('M'), IntExpr(0)), 2), DivulgateStmt(BinaryExpr('+', VarExpr('N'), IntExpr(1))), CondJumpStmt(None, 4), CondJumpStmt(BinaryExpr('==', VarExpr('N'), IntExpr(0)), 2), DivulgateStmt(ExecuteStmt([VarExpr('ACK'), BinaryExpr('-', VarExpr('M'), IntExpr(1)), IntExpr(1)])), CondJumpStmt(None, 1), DivulgateStmt(ExecuteStmt([VarExpr('ACK'), BinaryExpr('-', VarExpr('M'), IntExpr(1)), ExecuteStmt([VarExpr('ACK'), VarExpr('M'), BinaryExpr('-', VarExpr('N'), IntExpr(1))])]))], 'ACK'))), TildeAthLoop(False, VarExpr('THIS'), AthAstList([InputStmt(VarExpr('NUM'), StringExpr('Get the ackermann function of: ')), PrintStmt([StringExpr('The value of A(n, n) is ~d.\\n'), ExecuteStmt([VarExpr('ACK'), VarExpr('NUM'), VarExpr('NUM')])]), KillStmt(VarExpr('THIS'))], 'THIS'), ExecuteStmt([VarExpr('NULL')]))], 'THIS')
interp.execute()
