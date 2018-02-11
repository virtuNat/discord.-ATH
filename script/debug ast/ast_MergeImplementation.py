#!/usr/bin/env python
from athast import *
from symbol import ThisSymbol
from tildeath import TildeAthInterp

ast = AthAstList([
    FabricateStmt(AthFunction('REVERSE', ['STRUCT'], AthAstList([
        ReplicateStmt('QUEUE', None),
        ReplicateStmt('STACK', VarExpr('STRUCT')),
        BifurcateStmt('STACK', 'HEAD', 'STACK'),
        AggregateStmt('QUEUE', VarExpr('HEAD'), VarExpr('NULL')),
        TildeAthLoop(False, AthAstList([
            BifurcateStmt('STACK', 'HEAD', 'STACK'),
            AggregateStmt('QUEUE', VarExpr('HEAD'), VarExpr('QUEUE'))
            ], 'STACK'),
        ExecuteStmt([VarExpr('NULL')])
        ),
        DivulgateStmt(VarExpr('QUEUE'))
        ], 'REVERSE')
    )),
    FabricateStmt(AthFunction('MERGESORT', ['STRUCT', 'LEN'], AthAstList([
        CondJumpStmt(BinaryExpr('<', VarExpr('LEN'), IntExpr(2)), 1),
        DivulgateStmt(VarExpr('STRUCT')),
        ReplicateStmt('LENL', BinaryExpr('/_', VarExpr('LEN'), IntExpr(2))),
        ReplicateStmt('LENR', BinaryExpr('-', VarExpr('LEN'), VarExpr('LENL'))),
        ReplicateStmt('TEMPL', None),
        ReplicateStmt('TEMPR', VarExpr('STRUCT')),
        ReplicateStmt('IDX', IntExpr(1)),
        BifurcateStmt('TEMPR', 'HEAD', 'TEMPR'),
        AggregateStmt('TEMPL', VarExpr('HEAD'), VarExpr('NULL')),
        TildeAthLoop(False, AthAstList([
            CondJumpStmt(BinaryExpr('>=', VarExpr('IDX'), VarExpr('LENL')), 1),
            KillStmt(['IDX']),
            BifurcateStmt('TEMPR', 'HEAD', 'TEMPR'),
            AggregateStmt('TEMPL', VarExpr('HEAD'), VarExpr('TEMPL')),
            ProcreateStmt('IDX', BinaryExpr('+', VarExpr('IDX'), IntExpr(1)))
            ], 'IDX'),
        ExecuteStmt([VarExpr('NULL')])
        ),
        ReplicateStmt('TEMPL', ExecuteStmt([VarExpr('REVERSE'), VarExpr('TEMPL')])),
        CondJumpStmt(BinaryExpr('>', VarExpr('LENL'), IntExpr(1)), 1),
        ReplicateStmt('TEMPL', ExecuteStmt([VarExpr('MERGESORT'), VarExpr('TEMPL'), VarExpr('LENL')])),
        CondJumpStmt(BinaryExpr('>', VarExpr('LENR'), IntExpr(1)), 1),
        ReplicateStmt('TEMPR', ExecuteStmt([VarExpr('MERGESORT'), VarExpr('TEMPR'), VarExpr('LENR')])),
        ReplicateStmt('MERGED', None),
        ReplicateStmt('FLAG', None),
        ReplicateStmt('LOOP', None),
        TildeAthLoop(False, AthAstList([
            CondJumpStmt(BinaryExpr('&&', BinaryExpr('>', VarExpr('LENL'), IntExpr(0)), BinaryExpr('>', VarExpr('LENR'), IntExpr(0))), 21),
            BifurcateStmt('TEMPL', 'HEADL', 'NEXTL'),
            BifurcateStmt('TEMPR', 'HEADR', 'NEXTR'),
            CondJumpStmt(BinaryExpr('>', VarExpr('HEADL'), VarExpr('HEADR')), 9),
            CondJumpStmt(VarExpr('FLAG'), 3),
            AggregateStmt('MERGED', VarExpr('HEADR'), VarExpr('NULL')),
            KillStmt(['FLAG']),
            CondJumpStmt(None, 1),
            AggregateStmt('MERGED', VarExpr('HEADR'), VarExpr('MERGED')),
            ProcreateStmt('LENR', BinaryExpr('-', VarExpr('LENR'), IntExpr(1))),
            BifurcateStmt('NEXTR', 'L', 'R'),
            AggregateStmt('TEMPR', VarExpr('L'), VarExpr('R')),
            CondJumpStmt(None, 20),
            CondJumpStmt(VarExpr('FLAG'), 3),
            AggregateStmt('MERGED', VarExpr('HEADL'), VarExpr('NULL')),
            KillStmt(['FLAG']),
            CondJumpStmt(None, 1),
            AggregateStmt('MERGED', VarExpr('HEADL'), VarExpr('MERGED')),
            ProcreateStmt('LENL', BinaryExpr('-', VarExpr('LENL'), IntExpr(1))),
            BifurcateStmt('NEXTL', 'L', 'R'),
            AggregateStmt('TEMPL', VarExpr('L'), VarExpr('R')),
            CondJumpStmt(None, 11),
            CondJumpStmt(BinaryExpr('>', VarExpr('LENL'), IntExpr(0)), 4),
            BifurcateStmt('TEMPL', 'HEADL', 'TEMPL'),
            AggregateStmt('MERGED', VarExpr('HEADL'), VarExpr('MERGED')),
            ProcreateStmt('LENL', BinaryExpr('-', VarExpr('LENL'), IntExpr(1))),
            CondJumpStmt(None, 6),
            CondJumpStmt(BinaryExpr('>', VarExpr('LENR'), IntExpr(0)), 4),
            BifurcateStmt('TEMPR', 'HEADR', 'TEMPR'),
            AggregateStmt('MERGED', VarExpr('HEADR'), VarExpr('MERGED')),
            ProcreateStmt('LENR', BinaryExpr('-', VarExpr('LENR'), IntExpr(1))),
            CondJumpStmt(None, 1),
            KillStmt(['LOOP'])
            ], 'LOOP'),
        ExecuteStmt([VarExpr('NULL')])
        ),
        DivulgateStmt(ExecuteStmt([VarExpr('REVERSE'), VarExpr('MERGED')]))
        ], 'MERGESORT')
    )),
    ProcreateStmt('LLEN', IntExpr(0)),
    ProcreateStmt('LIST', None),
    TildeAthLoop(False, AthAstList([
        PrintStmt([StringExpr('Select action:\\n')]),
        PrintStmt([StringExpr('[1] Add an integer to the list\\n')]),
        PrintStmt([StringExpr('[2] Sort and print list\\n')]),
        PrintStmt([StringExpr('[3] Exit\\n')]),
        InputStmt('CHOICE', StringExpr('')),
        CondJumpStmt(BinaryExpr('==', VarExpr('CHOICE'), IntExpr(3)), 2),
        KillStmt(['THIS']),
        CondJumpStmt(None, 23),
        CondJumpStmt(BinaryExpr('==', VarExpr('CHOICE'), IntExpr(2)), 12),
        BifurcateStmt('LIST', 'L', 'R'),
        CondJumpStmt(VarExpr('L'), 8),
        ReplicateStmt('SORTED', ExecuteStmt([VarExpr('MERGESORT'), VarExpr('LIST'), VarExpr('LLEN')])),
        BifurcateStmt('SORTED', 'L', 'R'),
        AggregateStmt('LIST', VarExpr('L'), VarExpr('R')),
        ReplicateStmt('TEMP', VarExpr('LIST')),
        PrintStmt([StringExpr('The items in sorted ascending order are:\\n[')]),
        TildeAthLoop(False, AthAstList([
            BifurcateStmt('TEMP', 'HEAD', 'TEMP'),
            PrintStmt([StringExpr('~s'), VarExpr('HEAD')]),
            CondJumpStmt(VarExpr('TEMP'), 1),
            PrintStmt([StringExpr(', ')])
            ], 'TEMP'),
        ExecuteStmt([VarExpr('NULL')])
        ),
        PrintStmt([StringExpr(']\\n')]),
        CondJumpStmt(None, 12),
        PrintStmt([StringExpr('List is empty, oops.\\n')]),
        CondJumpStmt(None, 10),
        CondJumpStmt(BinaryExpr('==', VarExpr('CHOICE'), IntExpr(1)), 8),
        ReplicateStmt('ITEM', StringExpr('')),
        InputStmt('ITEM', StringExpr('Input string to add: ')),
        CondJumpStmt(BinaryExpr('==', VarExpr('LLEN'), IntExpr(0)), 2),
        AggregateStmt('LIST', VarExpr('ITEM'), VarExpr('NULL')),
        CondJumpStmt(None, 1),
        AggregateStmt('LIST', VarExpr('ITEM'), VarExpr('LIST')),
        ProcreateStmt('LLEN', BinaryExpr('+', VarExpr('LLEN'), IntExpr(1))),
        CondJumpStmt(None, 1),
        PrintStmt([StringExpr('Invalid choice, try again.\\n')])
        ], 'THIS'),
    ExecuteStmt([VarExpr('NULL')])
    )
    ], 'THIS')
interp = TildeAthInterp()
interp.bltin_vars['THIS'] = ThisSymbol('MergeImplementation.~ATH', ast)
interp.execute(ast)
