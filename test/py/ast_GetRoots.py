#!/usr/bin/env python
from athast import *
from tildeath import TildeAthInterp

interp = TildeAthInterp()
interp.ast = AthAstList([ProcreateStmt(VarExpr('LOOP'), IntExpr(0)), TildeAthLoop(False, VarExpr('LOOP'), AthAstList([InputStmt(VarExpr('A'), StringExpr('A: ')), InputStmt(VarExpr('B'), StringExpr('B: ')), InputStmt(VarExpr('C'), StringExpr('C: ')), ReplicateStmt(VarExpr('R'), BinaryExpr('/', BinaryExpr('+', UnaryExpr('-', VarExpr('B')), BinaryExpr('**', BinaryExpr('-', BinaryExpr('**', VarExpr('B'), IntExpr(2)), BinaryExpr('*', BinaryExpr('*', IntExpr(4), VarExpr('A')), VarExpr('C'))), BinaryExpr('/', IntExpr(1), IntExpr(2)))), BinaryExpr('*', IntExpr(2), VarExpr('A')))), ReplicateStmt(VarExpr('S'), BinaryExpr('/', BinaryExpr('-', UnaryExpr('-', VarExpr('B')), BinaryExpr('**', BinaryExpr('-', BinaryExpr('**', VarExpr('B'), IntExpr(2)), BinaryExpr('*', BinaryExpr('*', IntExpr(4), VarExpr('A')), VarExpr('C'))), BinaryExpr('/', IntExpr(1), IntExpr(2)))), BinaryExpr('*', IntExpr(2), VarExpr('A')))), PrintStmt([StringExpr('The roots of the quadratic equation ~dx^2 + ~dx + ~d are ~.4f and ~.4f.'), VarExpr('A'), VarExpr('B'), VarExpr('C'), VarExpr('R'), VarExpr('S')]), KillStmt(VarExpr('LOOP'))], 'LOOP'), ExecuteStmt([VarExpr('NULL')])), KillStmt(VarExpr('THIS'))], 'THIS')
interp.execute()
