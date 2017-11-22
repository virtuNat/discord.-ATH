#!/usr/bin/env python
from athast import *
from athparser import TildeAthInterp

ath_script = Serialize([ProcreateStmt(VarExpr('A'), IntExpr(0)), FabricateStmt(VarExpr('COUNT'), [], Serialize([DebateStmt(BinaryExpr('<', VarExpr('A'), IntExpr(100)), Serialize([ReplicateStmt(VarExpr('A'), BinaryExpr('+', VarExpr('A'), IntExpr(1))), PrintFunc([StringExpr('~s '), VarExpr('A')]), ExecuteStmt([VarExpr('COUNT')])], THIS), [])], THIS)), ProcreateStmt(VarExpr('LOOP'), IntExpr(0)), TildeAthLoop(False, VarExpr('LOOP'), Serialize([ExecuteStmt([VarExpr('COUNT')]), KillFunc(VarExpr('LOOP'), [])], LOOP)), KillFunc(VarExpr('THIS'), [])], THIS)
TildeAthInterp().execute(ath_script)
