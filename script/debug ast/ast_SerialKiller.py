#!/usr/bin/env python
from athast import *
from symbol import ThisSymbol
from tildeath import TildeAthInterp

ast = AthAstList([
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
    KillStmt(['THIS'])
    ], 'THIS')
interp = TildeAthInterp()
interp.bltin_vars['THIS'] = ThisSymbol('SerialKiller.~ATH', ast)
interp.execute(ast)
