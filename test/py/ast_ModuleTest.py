#!/usr/bin/env python
from athast import *
from tildeath import TildeAthInterp

interp = TildeAthInterp()
interp.ast = AthAstList([FabricateStmt(AthFunction('FIB', ['LENGTH'], AthAstList([ProcreateStmt(VarExpr('N1'), IntExpr(0)), ProcreateStmt(VarExpr('N2'), IntExpr(0)), ProcreateStmt(VarExpr('N3'), IntExpr(1)), ProcreateStmt(VarExpr('LOOP'), None), TildeAthLoop(False, VarExpr('LOOP'), AthAstList([CondJumpStmt(BinaryExpr('<=', VarExpr('LENGTH'), IntExpr(1)), 1), KillStmt(VarExpr('LOOP')), ProcreateStmt(VarExpr('N1'), VarExpr('N2')), ProcreateStmt(VarExpr('N2'), VarExpr('N3')), ProcreateStmt(VarExpr('N3'), BinaryExpr('+', VarExpr('N1'), VarExpr('N2'))), ReplicateStmt(VarExpr('LENGTH'), BinaryExpr('-', VarExpr('LENGTH'), IntExpr(1)))], 'LOOP'), ExecuteStmt([VarExpr('NULL')])), DivulgateStmt(VarExpr('N3'))], 'FIB'))), TildeAthLoop(False, VarExpr('THIS'), AthAstList([KillStmt(VarExpr('THIS'))], 'THIS'), ExecuteStmt([VarExpr('NULL')]))], 'THIS')
interp.execute()
