#!/usr/bin/env python
from athast import *
from athparser import TildeAthInterp

ath_script = Serialize([ProcreateStmt(VarExpr('B'), IntExpr(5)), FabricateStmt(VarExpr('FOO'), [], Serialize([ReplicateStmt(VarExpr('A'), BinaryExpr('+', VarExpr('B'), IntExpr(5))), DivulgateStmt(VarExpr('A'))], THIS)), FabricateStmt(VarExpr('BAR'), [], Serialize([ProcreateStmt(VarExpr('B'), IntExpr(2)), ReplicateStmt(VarExpr('A'), ExecuteStmt([VarExpr('FOO')])), DivulgateStmt(VarExpr('A'))], THIS)), ProcreateStmt(VarExpr('LOOP'), IntExpr(1)), TildeAthLoop(False, VarExpr('LOOP'), Serialize([ReplicateStmt(VarExpr('ANS'), ExecuteStmt([VarExpr('FOO')])), PrintFunc([StringExpr('Foo: ~d\\n'), VarExpr('ANS')]), ReplicateStmt(VarExpr('ANS'), ExecuteStmt([VarExpr('BAR')])), PrintFunc([StringExpr('Bar: ~d\\n'), VarExpr('ANS')]), KillFunc(VarExpr('LOOP'), [])], LOOP)), KillFunc(VarExpr('THIS'), [])], THIS)
TildeAthInterp().execute(ath_script)
