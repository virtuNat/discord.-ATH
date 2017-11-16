#!/usr/bin/env python
from athast import *
from athparser import TildeAthInterp

ath_script = Serialize([ProcreateStmt(VarExpr('LOOP'), IntExpr(0)), ProcreateStmt(VarExpr('A'), IntExpr(0)), FabricateStmt(VarExpr('ADDONE'), [], Serialize([ReplicateStmt(VarExpr('A'), BinaryExpr('+', VarExpr('A'), IntExpr(1)))], THIS)), TildeAthLoop(VarExpr('LOOP'), Serialize([ExecuteStmt([VarExpr('ADDONE')]), PrintFunc([StringExpr('~s '), VarExpr('A')]), DebateStmt(BinaryExpr('==', VarExpr('A'), IntExpr(256)), Serialize([PrintFunc([StringExpr('\\n')]), KillFunc(VarExpr('LOOP'), [])], LOOP), [])], LOOP)), KillFunc(VarExpr('THIS'), [])], THIS)
TildeAthInterp().execute(ath_script)
