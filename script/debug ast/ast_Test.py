#!/usr/bin/env python
from athast import *
from symbol import ThisSymbol
from tildeath import TildeAthInterp

ast = AthAstList([
    PrintStmt([StringExpr('Welcome to ~ATH.\\n')]),
    InputStmt('TEST', StringExpr('Input name: ')),
    PrintStmt([StringExpr('Thank you, ~s for inputting.\\n'), VarExpr('TEST')]),
    ProcreateStmt('CTR', IntExpr(5)),
    ReplicateStmt('CT2', VarExpr('CTR')),
    BifurcateStmt('CTR', 'CT3', 'CT2'),
    AggregateStmt('CT2', VarExpr('CTR'), VarExpr('CT3')),
    ReplicateStmt('CTR', VarExpr('NULL')),
    TildeAthLoop(False, AthAstList([
        PrintStmt([StringExpr('Print ~d times.\\n'), IntExpr(1)]),
        KillStmt(['CTR']),
        PrintStmt([StringExpr('This should not print.')])
        ], 'CTR'),
    ExecuteStmt([VarExpr('NULL')])
    ),
    PrintStmt([StringExpr('I wish you a peaceful death, ~s.\\n'), VarExpr('TEST')]),
    KillStmt(['THIS'])
    ], 'THIS')
interp = TildeAthInterp()
interp.bltin_vars['THIS'] = ThisSymbol('Test.~ATH', ast)
interp.execute(ast)
