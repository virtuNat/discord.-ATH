#!/usr/bin/env python
from athast import *
from tildeath import TildeAthInterp

interp = TildeAthInterp()
interp.ast = AthAstList([
    ProcreateStmt('LOOP', IntExpr(0)),
    TildeAthLoop(False, AthAstList([
        InputStmt('A', StringExpr('A: ')),
        InputStmt('B', StringExpr('B: ')),
        InputStmt('C', StringExpr('C: ')),
        ReplicateStmt('R', BinaryExpr('/', BinaryExpr('+', UnaryExpr('-', VarExpr('B')), BinaryExpr('**', BinaryExpr('-', BinaryExpr('**', VarExpr('B'), IntExpr(2)), BinaryExpr('*', BinaryExpr('*', IntExpr(4), VarExpr('A')), VarExpr('C'))), BinaryExpr('/', IntExpr(1), IntExpr(2)))), BinaryExpr('*', IntExpr(2), VarExpr('A')))),
        ReplicateStmt('S', BinaryExpr('/', BinaryExpr('-', UnaryExpr('-', VarExpr('B')), BinaryExpr('**', BinaryExpr('-', BinaryExpr('**', VarExpr('B'), IntExpr(2)), BinaryExpr('*', BinaryExpr('*', IntExpr(4), VarExpr('A')), VarExpr('C'))), BinaryExpr('/', IntExpr(1), IntExpr(2)))), BinaryExpr('*', IntExpr(2), VarExpr('A')))),
        PrintStmt([StringExpr('The roots of the quadratic equation ~dx^2 + ~dx + ~d are ~.4f and ~.4f.'), VarExpr('A'), VarExpr('B'), VarExpr('C'), VarExpr('R'), VarExpr('S')]),
        KillStmt(VarExpr('LOOP'))
        ], 'LOOP'),
    ExecuteStmt([VarExpr('NULL')])
    ),
    KillStmt(VarExpr('THIS'))
    ], 'THIS')
interp.execute()
