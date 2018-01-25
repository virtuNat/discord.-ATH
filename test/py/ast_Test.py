#!/usr/bin/env python
from athast import *
from tildeath import TildeAthInterp

interp = TildeAthInterp()
interp.ast = AthAstList([PrintStmt([StringExpr('Welcome to ~ATH.\\n')]), InputStmt(VarExpr('TEST'), StringExpr('Input name: ')), PrintStmt([StringExpr('Thank you, ~s for inputting.\\n'), VarExpr('TEST')]), ProcreateStmt(VarExpr('CTR'), IntExpr(5)), ReplicateStmt(VarExpr('CT2'), VarExpr('CTR')), BifurcateStmt(VarExpr('CTR'), VarExpr('CT3'), VarExpr('CT2')), AggregateStmt(VarExpr('CTR'), VarExpr('CT3'), VarExpr('CT2')), ReplicateStmt(VarExpr('CTR'), VarExpr('NULL')), TildeAthLoop(False, VarExpr('CTR'), AthAstList([PrintStmt([StringExpr('Print ~d times.\\n'), IntExpr(1)]), KillStmt(VarExpr('CTR')), PrintStmt([StringExpr('This should not print.')])], 'CTR'), ExecuteStmt([VarExpr('NULL')])), PrintStmt([StringExpr('I wish you a peaceful death, ~s.\\n'), VarExpr('TEST')]), KillStmt(VarExpr('THIS'))], 'THIS')
interp.execute()
