from athast import *
from athparser import TildeAthInterp

ath_script = Serialize([ProcreateStmt(VarExpr('LOOP'), VarExpr('NULL')), TildeAthLoop(VarExpr('LOOP'), Serialize([PrintFunc([StringExpr('Hi.')]), KillFunc(VarExpr('LOOP'), [])], 'THIS')), KillFunc(VarExpr('THIS'), [])], 'THIS')
TildeAthInterp().execute(ath_script)
