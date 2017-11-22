#!/usr/bin/env python
from athast import *
from athparser import TildeAthInterp

ath_script = Serialize([ProcreateStmt(VarExpr('LOOP'), IntExpr(0)), TildeAthLoop(True, VarExpr('LOOP'), Serialize([PrintFunc([StringExpr("This shouldn't print.\\n")])], THIS)), PrintFunc([StringExpr('Yay.\\n')]), KillFunc(VarExpr('THIS'), [])], THIS)
TildeAthInterp().execute(ath_script)
