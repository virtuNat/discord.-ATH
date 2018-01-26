#!/usr/bin/env python
from athast import *
from tildeath import TildeAthInterp

interp = TildeAthInterp()
interp.ast = AthAstList([ProcreateStmt(VarExpr('LOOP'), IntExpr(0)), TildeAthLoop(True, VarExpr('LOOP'), AthAstList([PrintStmt([StringExpr("This shouldn't print.\\n")])], 'LOOP'), ExecuteStmt([VarExpr('NULL')])), PrintStmt([StringExpr('Yay.\\n')]), KillStmt(VarExpr('THIS'))], 'THIS')
interp.execute()
