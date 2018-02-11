#!/usr/bin/env python
from athast import *
from symbol import ThisSymbol
from tildeath import TildeAthInterp

ast = AthAstList([
    ProcreateStmt('LOOP', None),
    ProcreateStmt('QUEUE', None),
    ProcreateStmt('FLAG', None),
    TildeAthLoop(False, AthAstList([
        PrintStmt([StringExpr('Select action:\\n')]),
        PrintStmt([StringExpr('[1] Add an item to queue\\n')]),
        PrintStmt([StringExpr('[2] View queue\\n')]),
        PrintStmt([StringExpr('[3] Exit\\n')]),
        InputStmt('CHOICE', StringExpr('')),
        CondJumpStmt(BinaryExpr('==', VarExpr('CHOICE'), IntExpr(3)), 2),
        KillStmt(['LOOP']),
        CondJumpStmt(None, 22),
        CondJumpStmt(BinaryExpr('==', VarExpr('CHOICE'), IntExpr(2)), 11),
        CondJumpStmt(UnaryExpr('!', VarExpr('FLAG')), 8),
        ProcreateStmt('STACK', None),
        ReplicateStmt('TEMP', VarExpr('QUEUE')),
        BifurcateStmt('TEMP', 'HEAD', 'TEMP'),
        AggregateStmt('STACK', VarExpr('HEAD'), VarExpr('NULL')),
        TildeAthLoop(False, AthAstList([
            BifurcateStmt('TEMP', 'HEAD', 'TEMP'),
            AggregateStmt('STACK', VarExpr('HEAD'), VarExpr('STACK'))
            ], 'TEMP'),
        ExecuteStmt([VarExpr('NULL')])
        ),
        TildeAthLoop(False, AthAstList([
            BifurcateStmt('STACK', 'HEAD', 'STACK'),
            PrintStmt([StringExpr('~s\\n'), VarExpr('HEAD')])
            ], 'STACK'),
        ExecuteStmt([VarExpr('NULL')])
        ),
        PrintStmt([StringExpr('Queue print done.\\n')]),
        CondJumpStmt(None, 12),
        PrintStmt([StringExpr('Queue is empty.\\n')]),
        CondJumpStmt(None, 10),
        CondJumpStmt(BinaryExpr('==', VarExpr('CHOICE'), IntExpr(1)), 8),
        ReplicateStmt('ITEM', StringExpr('')),
        InputStmt('ITEM', StringExpr('Input string to add: ')),
        CondJumpStmt(VarExpr('FLAG'), 3),
        AggregateStmt('QUEUE', VarExpr('ITEM'), VarExpr('NULL')),
        KillStmt(['FLAG']),
        CondJumpStmt(None, 3),
        AggregateStmt('QUEUE', VarExpr('ITEM'), VarExpr('QUEUE')),
        CondJumpStmt(None, 1),
        PrintStmt([StringExpr('Invalid input.')])
        ], 'LOOP'),
    ExecuteStmt([VarExpr('NULL')])
    ),
    KillStmt(['THIS'])
    ], 'THIS')
interp = TildeAthInterp()
interp.bltin_vars['THIS'] = ThisSymbol('QueueTest.~ATH', ast)
interp.execute(ast)
