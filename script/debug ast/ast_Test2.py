#!/usr/bin/env python
from athast import *
from symbol import ThisSymbol
from tildeath import TildeAthInterp

ast = AthAstList([
    ProcreateStmt('LOOP', None),
    ProcreateStmt('CTR', IntExpr(1)),
    FabricateStmt(AthFunction('CTR', ['COUNT'], AthAstList([
        DivulgateStmt(BinaryExpr('+', VarExpr('COUNT'), IntExpr(1)))
        ], 'CTR')
    )),
    BifurcateStmt('CTR', 'ctr', 'cnt'),
    InputStmt('MAX', StringExpr('Count to how many? :')),
    TildeAthLoop(False, AthAstList([
        PrintStmt([StringExpr('Count: ~d\\n'), VarExpr('CTR')]),
        ReplicateStmt('CTR', ExecuteStmt([VarExpr('CTR'), VarExpr('CTR')])),
        CondJumpStmt(BinaryExpr('>', VarExpr('CTR'), VarExpr('MAX')), 3),
        InspectStack([]),
        KillStmt(['LOOP']),
        CondJumpStmt(None, 1),
        PrintStmt([StringExpr('Next...\\n')])
        ], 'LOOP'),
    ExecuteStmt([VarExpr('NULL')])
    ),
    KillStmt(['THIS'])
    ], 'THIS')
interp = TildeAthInterp()
interp.bltin_vars['THIS'] = ThisSymbol('Test2.~ATH', ast)
interp.execute(ast)
