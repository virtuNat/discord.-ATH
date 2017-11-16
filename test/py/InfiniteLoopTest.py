#!/usr/bin/env python
from athast import *
from athparser import TildeAthInterp

ath_script = Serialize([ProcreateStmt(VarExpr('LOOP'), IntExpr(0)), TildeAthLoop(VarExpr('LOOP'), Serialize([PrintFunc([StringExpr('Hi.')]), KillFunc(VarExpr('LOOP'), [])], LOOP))], THIS)
TildeAthInterp().execute(ath_script)
