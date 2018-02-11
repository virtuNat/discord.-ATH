#!/usr/bin/env python
from athast import *
from symbol import ThisSymbol
from tildeath import TildeAthInterp

ast = AthAstList([
    ProcreateStmt('LOOP', None),
    ProcreateStmt('STACK', None),
    ProcreateStmt('FLAG', None),
    TildeAthLoop(False, AthAstList([
        PrintStmt([StringExpr('Select action:\\n')]),
        PrintStmt([StringExpr('[1] Add an item to stack\\n')]),
        PrintStmt([StringExpr('[2] View stack\\n')]),
        PrintStmt([StringExpr('[3] Exit\\n')]),
        InputStmt('CHOICE', StringExpr('')),
        CondJumpStmt(BinaryExpr('==', VarExpr('CHOICE'), IntExpr(3)), 2),
        KillStmt(['LOOP']),
        CondJumpStmt(None, 14),
        CondJumpStmt(BinaryExpr('==', VarExpr('CHOICE'), IntExpr(2)), 3),
        ReplicateStmt('TEMP', VarExpr('STACK')),
        TildeAthLoop(False, AthAstList([
            BifurcateStmt('TEMP', 'HEAD', 'TEMP'),
            PrintStmt([StringExpr('~s\\n'), VarExpr('HEAD')])
            ], 'TEMP'),
        ExecuteStmt([VarExpr('NULL')])
        ),
        CondJumpStmt(None, 10),
        CondJumpStmt(BinaryExpr('==', VarExpr('CHOICE'), IntExpr(1)), 8),
        ReplicateStmt('ITEM', StringExpr('')),
        InputStmt('ITEM', StringExpr('Input string to add: ')),
        CondJumpStmt(VarExpr('FLAG'), 3),
        AggregateStmt('STACK', VarExpr('ITEM'), VarExpr('NULL')),
        KillStmt(['FLAG']),
        CondJumpStmt(None, 3),
        AggregateStmt('STACK', VarExpr('ITEM'), VarExpr('STACK')),
        CondJumpStmt(None, 1),
        PrintStmt([StringExpr('Invalid input.')])
        ], 'LOOP'),
    ExecuteStmt([VarExpr('NULL')])
    ),
    KillStmt(['THIS'])
    ], 'THIS')
interp = TildeAthInterp()
interp.bltin_vars['THIS'] = ThisSymbol('StackTest.~ATH', ast)
interp.execute(ast)
