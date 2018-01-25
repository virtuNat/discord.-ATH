#!/usr/bin/env python
from athast import *
from tildeath import TildeAthInterp

interp = TildeAthInterp()
interp.ast = AthAstList([ProcreateStmt(VarExpr('LOOP'), IntExpr(1)), TildeAthLoop(False, VarExpr('LOOP'), AthAstList([ProcreateStmt(VarExpr('X'), IntExpr(1)), ProcreateStmt(VarExpr('Y'), IntExpr(2)), AggregateStmt(VarExpr('X'), VarExpr('Y'), VarExpr('Z')), ProcreateStmt(VarExpr('A'), IntExpr(3)), ReplicateStmt(VarExpr('Y'), VarExpr('A')), BifurcateStmt(VarExpr('Z'), VarExpr('B'), VarExpr('C')), PrintStmt([StringExpr('~s, ~s'), VarExpr('B'), VarExpr('C')]), KillStmt(VarExpr('LOOP'))], 'LOOP'), ExecuteStmt([VarExpr('NULL')])), KillStmt(VarExpr('THIS'))], 'THIS')
interp.execute()
