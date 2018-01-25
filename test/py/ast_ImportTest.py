#!/usr/bin/env python
from athast import *
from tildeath import TildeAthInterp

interp = TildeAthInterp()
interp.ast = AthAstList([ImportStmt(VarExpr('ModuleTest'), VarExpr('FIB')), ProcreateStmt(VarExpr('MAIN'), None), ProcreateStmt(VarExpr('COUNT'), IntExpr(1)), TildeAthLoop(False, VarExpr('MAIN'), AthAstList([PrintStmt([StringExpr('F~d = ~d\\n'), VarExpr('COUNT'), ExecuteStmt([VarExpr('FIB'), VarExpr('COUNT')])]), CondJumpStmt(BinaryExpr('>=', VarExpr('COUNT'), IntExpr(10)), 1), KillStmt(VarExpr('MAIN')), ProcreateStmt(VarExpr('COUNT'), BinaryExpr('+', VarExpr('COUNT'), IntExpr(1)))], 'MAIN'), ExecuteStmt([VarExpr('NULL')])), KillStmt(VarExpr('THIS'))], 'THIS')
interp.execute()
