#!/usr/bin/env python
from athast import *
from tildeath import TildeAthInterp

interp = TildeAthInterp()
interp.ast = AthAstList([
    TildeAthLoop(False, AthAstList([
        PrintStmt([StringExpr('Hello World!\\n')]),
        PrintStmt([StringExpr('This is the script ~s!\\n'), VarExpr('THIS')]),
        KillStmt(VarExpr('THIS'))
        ], 'THIS'),
    ExecuteStmt([VarExpr('NULL')])
    )
    ], 'THIS')
interp.execute()
