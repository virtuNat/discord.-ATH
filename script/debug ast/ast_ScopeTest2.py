#!/usr/bin/env python
from athast import *
from tildeath import TildeAthInterp

interp = TildeAthInterp()
interp.ast = AthAstList([
    ProcreateStmt('X', IntExpr(1)),
    FabricateStmt(AthFunction('F', ['I'], AthAstList([
        ReplicateStmt('X', VarExpr('I')),
        AggregateStmt('I', BinaryExpr('+', VarExpr('I'), IntExpr(1)), VarExpr('NULL')),
        BifurcateStmt('I', 'I', 'NULL'),
        ExecuteStmt([VarExpr('G'), VarExpr('I')]),
        ProcreateStmt('VAR', None)
        ], 'F')
    )),
    FabricateStmt(AthFunction('G', ['J'], AthAstList([
        AggregateStmt('J', BinaryExpr('+', VarExpr('J'), VarExpr('X')), VarExpr('NULL')),
        BifurcateStmt('J', 'J', 'NULL')
        ], 'G')
    )),
    TildeAthLoop(False, AthAstList([
        ExecuteStmt([VarExpr('F'), VarExpr('X')]),
        PrintStmt([StringExpr('~d\\n'), VarExpr('X')]),
        KillStmt(VarExpr('THIS'))
        ], 'THIS'),
    ExecuteStmt([VarExpr('NULL')])
    )
    ], 'THIS')
interp.execute()
