#!/usr/bin/env python
from athast import *
from athparser import TildeAthInterp

ath_script = Serialize([FabricateStmt(VarExpr('FACTORIAL'), [VarExpr('NUM')], Serialize([DebateStmt(BinaryExpr('>', VarExpr('NUM'), IntExpr(1)), Serialize([DivulgateStmt(BinaryExpr('*', VarExpr('NUM'), ExecuteStmt([VarExpr('FACTORIAL'), BinaryExpr('-', VarExpr('NUM'), IntExpr(1))])))], THIS), []), DivulgateStmt(IntExpr(1))], THIS)), TildeAthLoop(False, VarExpr('THIS'), Serialize([InputStmt(VarExpr('NUM'), StringExpr('Get the factorial of: ')), PrintFunc([StringExpr('~d! is ~d\\n'), VarExpr('NUM'), ExecuteStmt([VarExpr('FACTORIAL'), VarExpr('NUM')])]), KillFunc(VarExpr('THIS'), [])], THIS)), ExecuteStmt([VarExpr('NULL')])], THIS)
TildeAthInterp().execute(ath_script)
