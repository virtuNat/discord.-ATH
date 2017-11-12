from athast import *
from athparser import TildeAthInterp

ath_script = Serialize([PrintFunc([StringExpr('Welcome to ~ATH.\\n')]), InputStmt(VarExpr('TEST'), StringExpr('Input name: ')), PrintFunc([StringExpr('Thank you, ~s for inputting.\\n'), VarExpr('TEST')]), ProcreateStmt(VarExpr('CTR'), IntExpr(5)), ReplicateStmt(VarExpr('CT2'), VarExpr('CTR')), BifurcateStmt(VarExpr('CTR'), VarExpr('CT3'), VarExpr('CT2')), AggregateStmt(VarExpr('CTR'), VarExpr('CT3'), VarExpr('CT2')), ReplicateStmt(VarExpr('CTR'), VarExpr('NULL')), TildeAthLoop(VarExpr('CTR'), Serialize([PrintFunc([StringExpr('Print ~d times.\\n'), IntExpr(1)]), KillFunc(VarExpr('CTR'), []), PrintFunc([StringExpr('This should not print.')])], 'THIS')), PrintFunc([StringExpr('I wish you a peaceful death, ~s.\\n'), VarExpr('TEST')]), KillFunc(VarExpr('THIS'), [])], 'THIS')
TildeAthInterp().execute(ath_script)
