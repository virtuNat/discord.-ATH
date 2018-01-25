#!/usr/bin/env python
from athast import *
from tildeath import TildeAthInterp

interp = TildeAthInterp()
interp.ast = AthAstList([ProcreateStmt(VarExpr('LOOP'), IntExpr(0)), TildeAthLoop(False, VarExpr('LOOP'), AthAstList([PrintStmt([StringExpr('Hi.')]), KillStmt(VarExpr('LOOP'))], 'LOOP'), ExecuteStmt([VarExpr('NULL')]))], 'THIS')
interp.execute()
