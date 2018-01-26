#!/usr/bin/env python
from athast import *
from tildeath import TildeAthInterp

interp = TildeAthInterp()
interp.ast = AthAstList([ProcreateStmt(VarExpr('B'), IntExpr(5)), FabricateStmt(AthFunction('FOO', [], AthAstList([ReplicateStmt(VarExpr('A'), BinaryExpr('+', VarExpr('B'), IntExpr(5))), DivulgateStmt(VarExpr('A'))], 'FOO'))), FabricateStmt(AthFunction('BAR', [], AthAstList([ProcreateStmt(VarExpr('B'), IntExpr(2)), DivulgateStmt(ExecuteStmt([VarExpr('FOO')]))], 'BAR'))), ProcreateStmt(VarExpr('LOOP'), IntExpr(1)), TildeAthLoop(False, VarExpr('LOOP'), AthAstList([PrintStmt([StringExpr('Foo: ~d\\n'), ExecuteStmt([VarExpr('FOO')])]), PrintStmt([StringExpr('Bar: ~d\\n'), ExecuteStmt([VarExpr('BAR')])]), KillStmt(VarExpr('LOOP'))], 'LOOP'), ExecuteStmt([VarExpr('NULL')])), KillStmt(VarExpr('THIS'))], 'THIS')
interp.execute()
