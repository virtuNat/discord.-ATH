from athast import *
from athparser import TildeAthInterp

ath_script = Serialize([ProcreateStmt(VarExpr('LOOP'), IntExpr(1)), TildeAthLoop(VarExpr('LOOP'), Serialize([ProcreateStmt(VarExpr('X'), IntExpr(1)), ProcreateStmt(VarExpr('Y'), IntExpr(2)), AggregateStmt(VarExpr('X'), VarExpr('Y'), VarExpr('Z')), ProcreateStmt(VarExpr('A'), IntExpr(3)), ReplicateStmt(VarExpr('Y'), VarExpr('A')), BifurcateStmt(VarExpr('Z'), VarExpr('B'), VarExpr('C')), PrintFunc([StringExpr('~s, ~s'), VarExpr('B'), VarExpr('C')]), KillFunc(VarExpr('LOOP'), [])], 'THIS')), KillFunc(VarExpr('THIS'), [])], 'THIS')
TildeAthInterp().execute(ath_script)
