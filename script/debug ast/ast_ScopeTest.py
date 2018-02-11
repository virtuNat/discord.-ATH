#!/usr/bin/env python
from athast import *
from symbol import ThisSymbol
from tildeath import TildeAthInterp

ast = AthAstList([
    ProcreateStmt('B', IntExpr(5)),
    FabricateStmt(AthFunction('FOO', [], AthAstList([
        ReplicateStmt('A', BinaryExpr('+', VarExpr('B'), IntExpr(5))),
        DivulgateStmt(VarExpr('A'))
        ], 'FOO')
    )),
    FabricateStmt(AthFunction('BAR', [], AthAstList([
        ProcreateStmt('B', IntExpr(2)),
        DivulgateStmt(ExecuteStmt([VarExpr('FOO')]))
        ], 'BAR')
    )),
    ProcreateStmt('LOOP', IntExpr(1)),
    TildeAthLoop(False, AthAstList([
        PrintStmt([StringExpr('Foo: ~d\\n'), ExecuteStmt([VarExpr('FOO')])]),
        PrintStmt([StringExpr('Bar: ~d\\n'), ExecuteStmt([VarExpr('BAR')])]),
        KillStmt(['LOOP'])
        ], 'LOOP'),
    ExecuteStmt([VarExpr('NULL')])
    ),
    KillStmt(['THIS'])
    ], 'THIS')
interp = TildeAthInterp()
interp.bltin_vars['THIS'] = ThisSymbol('ScopeTest.~ATH', ast)
interp.execute(ast)
