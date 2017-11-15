#!/usr/bin/env python
from athast import *
from athparser import TildeAthInterp

ath_script = Serialize([ProcreateStmt(VarExpr('LOOP'), IntExpr(1)), TildeAthLoop(VarExpr('LOOP'), Serialize([InputStmt(VarExpr('NAME'), StringExpr("What's your name? ")), PrintFunc([StringExpr('Hello, ~s\\n!'), VarExpr('NAME')]), KillFunc(VarExpr('LOOP'), [])], LOOP)), KillFunc(VarExpr('THIS'), [])], THIS)
TildeAthInterp().execute(ath_script)
