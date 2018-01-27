#!/usr/bin/env python
from athast import *
from tildeath import TildeAthInterp

interp = TildeAthInterp()
interp.ast = AthAstList([
    FabricateStmt(AthFunction('FIB', ['LENGTH'], AthAstList([
        ProcreateStmt('N1', IntExpr(0)),
        ProcreateStmt('N2', IntExpr(0)),
        ProcreateStmt('N3', IntExpr(1)),
        ProcreateStmt('LOOP', None),
        TildeAthLoop(False, AthAstList([
            CondJumpStmt(BinaryExpr('<=', VarExpr('LENGTH'), IntExpr(1)), 1),
            KillStmt(VarExpr('LOOP')),
            ProcreateStmt('N1', VarExpr('N2')),
            ProcreateStmt('N2', VarExpr('N3')),
            ProcreateStmt('N3', BinaryExpr('+', VarExpr('N1'), VarExpr('N2'))),
            ReplicateStmt('LENGTH', BinaryExpr('-', VarExpr('LENGTH'), IntExpr(1)))
            ], 'LOOP'),
        ExecuteStmt([VarExpr('NULL')])
        ),
        DivulgateStmt(VarExpr('N3'))
        ], 'FIB')
    )),
    TildeAthLoop(False, AthAstList([
        KillStmt(VarExpr('THIS'))
        ], 'THIS'),
    ExecuteStmt([VarExpr('NULL')])
    )
    ], 'THIS')
interp.execute()
