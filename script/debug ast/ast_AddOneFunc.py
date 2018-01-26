#!/usr/bin/env python
from athast import *
from tildeath import TildeAthInterp

interp = TildeAthInterp()
interp.ast = AthAstList([ProcreateStmt(VarExpr('LOOP'), IntExpr(0)), ProcreateStmt(VarExpr('A'), IntExpr(0)), FabricateStmt(AthFunction('ADDONE', [], AthAstList([AggregateStmt(BinaryExpr('+', VarExpr('A'), IntExpr(1)), VarExpr('NULL'), VarExpr('A')), BifurcateStmt(VarExpr('A'), VarExpr('A'), VarExpr('NULL'))], 'ADDONE'))), TildeAthLoop(False, VarExpr('LOOP'), AthAstList([ExecuteStmt([VarExpr('ADDONE')]), PrintStmt([StringExpr('~s '), VarExpr('A')]), CondJumpStmt(BinaryExpr('==', VarExpr('A'), IntExpr(256)), 2), PrintStmt([StringExpr('\\n')]), KillStmt(VarExpr('LOOP'))], 'LOOP'), ExecuteStmt([VarExpr('NULL')])), KillStmt(VarExpr('THIS'))], 'THIS')
interp.execute()
