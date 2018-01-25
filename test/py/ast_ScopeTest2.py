#!/usr/bin/env python
from athast import *
from tildeath import TildeAthInterp

interp = TildeAthInterp()
interp.ast = AthAstList([ProcreateStmt(VarExpr('X'), IntExpr(1)), FabricateStmt(AthFunction('F', ['I'], AthAstList([ReplicateStmt(VarExpr('X'), VarExpr('I')), AggregateStmt(BinaryExpr('+', VarExpr('I'), IntExpr(1)), VarExpr('NULL'), VarExpr('I')), BifurcateStmt(VarExpr('I'), VarExpr('I'), VarExpr('NULL')), ExecuteStmt([VarExpr('G'), VarExpr('I')]), ProcreateStmt(VarExpr('VAR'), None)], 'F'))), FabricateStmt(AthFunction('G', ['J'], AthAstList([AggregateStmt(BinaryExpr('+', VarExpr('J'), VarExpr('X')), VarExpr('NULL'), VarExpr('J')), BifurcateStmt(VarExpr('J'), VarExpr('J'), VarExpr('NULL'))], 'G'))), TildeAthLoop(False, VarExpr('THIS'), AthAstList([ExecuteStmt([VarExpr('F'), VarExpr('X')]), PrintStmt([StringExpr('~d\\n'), VarExpr('X')]), KillStmt(VarExpr('THIS'))], 'THIS'), ExecuteStmt([VarExpr('NULL')]))], 'THIS')
interp.execute()
