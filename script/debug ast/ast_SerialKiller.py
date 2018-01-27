#!/usr/bin/env python
from athast import *
from tildeath import TildeAthInterp

interp = TildeAthInterp()
interp.ast = AthAstList([
    ProcreateStmt('FOO', None),
    ProcreateStmt('BAR', None),
    TildeAthLoop(False, AthAstList([
        TildeAthLoop(False, AthAstList([
            PrintStmt([StringExpr('Oof.\\n')]),
            KillStmt(['FOO', 'BAR'])
            ], 'BAR'),
        ExecuteStmt([VarExpr('NULL')])
        ),
        PrintStmt([StringExpr('Well hello there.\\n')])
        ], 'FOO'),
    ExecuteStmt([VarExpr('NULL')])
    ),
    KillStmt('THIS')
    ], 'THIS')
interp.execute()
