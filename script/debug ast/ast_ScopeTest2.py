#!/usr/bin/env python
from athast import *
from symbol import ThisSymbol
from tildeath import TildeAthInterp

ast = AthAstList([
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
        KillStmt(['THIS'])
        ], 'THIS'),
    ExecuteStmt([VarExpr('NULL')])
    )
    ], 'THIS')
interp = TildeAthInterp()
interp.bltin_vars['THIS'] = ThisSymbol('ScopeTest2.~ATH', ast)
interp.execute(ast)
