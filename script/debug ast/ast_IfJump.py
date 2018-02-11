#!/usr/bin/env python
from athast import *
from symbol import ThisSymbol
from tildeath import TildeAthInterp

ast = AthAstList([
    ProcreateStmt('TEST', None),
    TildeAthLoop(False, AthAstList([
        CondJumpStmt(VarExpr('TEST'), 3),
        PrintStmt([StringExpr('Test!\\n')]),
        ReplicateStmt('TEST', UnaryExpr('!', VarExpr('TEST'))),
        CondJumpStmt(None, 5),
        CondJumpStmt(UnaryExpr('!', VarExpr('TEST')), 3),
        PrintStmt([StringExpr('Test died\\n')]),
        KillStmt(['THIS']),
        CondJumpStmt(None, 1),
        PrintStmt([StringExpr('should not print\\n')])
        ], 'THIS'),
    ExecuteStmt([VarExpr('NULL')])
    )
    ], 'THIS')
interp = TildeAthInterp()
interp.bltin_vars['THIS'] = ThisSymbol('IfJump.~ATH', ast)
interp.execute(ast)
