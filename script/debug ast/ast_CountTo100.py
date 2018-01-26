#!/usr/bin/env python
from athast import *
from tildeath import TildeAthInterp

interp = TildeAthInterp()
interp.ast = AthAstList([ProcreateStmt(VarExpr('A'), IntExpr(0)), FabricateStmt(AthFunction('COUNT', [], AthAstList([CondJumpStmt(BinaryExpr('<', VarExpr('A'), IntExpr(100)), 3), ProcreateStmt(VarExpr('A'), BinaryExpr('+', VarExpr('A'), IntExpr(1))), PrintStmt([StringExpr('~s '), VarExpr('A')]), ExecuteStmt([VarExpr('COUNT')])], 'COUNT'))), ProcreateStmt(VarExpr('LOOP'), IntExpr(0)), TildeAthLoop(False, VarExpr('LOOP'), AthAstList([ExecuteStmt([VarExpr('COUNT')]), KillStmt(VarExpr('LOOP'))], 'LOOP'), ExecuteStmt([VarExpr('NULL')])), KillStmt(VarExpr('THIS'))], 'THIS')
interp.execute()
