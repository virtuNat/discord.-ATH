#!/usr/bin/env python
from athast import *
from tildeath import TildeAthInterp

interp = TildeAthInterp()
interp.ast = AthAstList([ProcreateStmt(VarExpr('LOOP'), IntExpr(0)), TildeAthLoop(False, VarExpr('LOOP'), AthAstList([PrintStmt([StringExpr('~d'), VarExpr('LOOP')]), CondJumpStmt(BinaryExpr('>', VarExpr('LOOP'), IntExpr(9)), 1), KillStmt(VarExpr('LOOP')), ProcreateStmt(VarExpr('LOOP'), BinaryExpr('+', VarExpr('LOOP'), IntExpr(1))), PrintStmt([StringExpr(', ')])], 'LOOP'), ExecuteStmt([VarExpr('NULL')])), PrintStmt([StringExpr('\\n~d\\n'), VarExpr('LOOP')]), TildeAthLoop(True, VarExpr('LOOP'), AthAstList([PrintStmt([StringExpr('~d'), VarExpr('LOOP')]), CondJumpStmt(BinaryExpr('>', VarExpr('LOOP'), IntExpr(0)), 3), ReplicateStmt(VarExpr('LOOP'), BinaryExpr('-', VarExpr('LOOP'), IntExpr(1))), PrintStmt([StringExpr(', ')]), KillStmt(VarExpr('LOOP')), ReplicateStmt(VarExpr('LOOP'), UnaryExpr('!', VarExpr('LOOP'))), PrintStmt([StringExpr('\\n')])], 'LOOP'), ExecuteStmt([VarExpr('NULL')])), KillStmt(VarExpr('THIS'))], 'THIS')
interp.execute()
