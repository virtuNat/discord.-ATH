#!/usr/bin/env python
from athast import *
from athparser import TildeAthInterp

ath_script = Serialize([ProcreateStmt(VarExpr('LOOP'), VarExpr('NULL')), TildeAthLoop(False, VarExpr('LOOP'), Serialize([PrintFunc([StringExpr('Are you there.\\n')]), KillFunc(VarExpr('LOOP'), [])], LOOP)), KillFunc(VarExpr('THIS'), [])], THIS)
TildeAthInterp().execute(ath_script)
