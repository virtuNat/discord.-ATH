#!/usr/bin/env python
from athast import *
from symbol import ThisSymbol
from tildeath import TildeAthInterp

ast = AthAstList([
    ProcreateStmt('LOOP', IntExpr(0)),
    TildeAthLoop(False, AthAstList([
        PrintStmt([StringExpr('Which of the following is not a French word?\\n')]),
        PrintStmt([StringExpr('[A] sale\\n')]),
        PrintStmt([StringExpr('[B] mode\\n')]),
        PrintStmt([StringExpr('[C] grand\\n')]),
        PrintStmt([StringExpr('[D] chat\\n')]),
        PrintStmt([StringExpr('[E] A, B, C, and D are all French words\\n')]),
        PrintStmt([StringExpr('[F] A, B, C, and D are all not French words\\n')]),
        InputStmt('CHOICE', StringExpr('')),
        EnumerateStmt(VarExpr('CHOICE'), VarExpr('CHARS')),
        BifurcateStmt('CHARS', 'HEAD', 'TAIL'),
        CondJumpStmt(UnaryExpr('!', VarExpr('TAIL')), 5),
        CondJumpStmt(BinaryExpr('||', BinaryExpr('&&', BinaryExpr('>=', VarExpr('CHOICE'), StringExpr('A')), BinaryExpr('<=', VarExpr('CHOICE'), StringExpr('F'))), BinaryExpr('&&', BinaryExpr('<=', VarExpr('CHOICE'), StringExpr('f')), BinaryExpr('>=', VarExpr('CHOICE'), StringExpr('a')))), 2),
        PrintStmt([StringExpr('Wrong! Try again, idiot.\\n')]),
        CondJumpStmt(None, 10),
        PrintStmt([StringExpr("Are you blind? That's not even a choice.\\n")]),
        CondJumpStmt(None, 8),
        CondJumpStmt(BinaryExpr('||', BinaryExpr('==', VarExpr('CHOICE'), StringExpr('THE CHEAT CODE')), BinaryExpr('==', VarExpr('CHOICE'), StringExpr('the cheat code'))), 2),
        PrintStmt([StringExpr("Damn, you caught me. It's a trick question.\\n")]),
        CondJumpStmt(None, 5),
        CondJumpStmt(BinaryExpr('||', BinaryExpr('==', VarExpr('CHOICE'), StringExpr('DIE')), BinaryExpr('==', VarExpr('CHOICE'), StringExpr('die'))), 3),
        PrintStmt([StringExpr('Hmph. Ninny.\\n')]),
        KillStmt(['LOOP']),
        CondJumpStmt(None, 1),
        PrintStmt([StringExpr("HA! Loser can't even guess the cheat code.\\n")]),
        PrintStmt([StringExpr('\\n')])
        ], 'LOOP'),
    ExecuteStmt([VarExpr('NULL')])
    ),
    KillStmt(['THIS'])
    ], 'THIS')
interp = TildeAthInterp()
interp.bltin_vars['THIS'] = ThisSymbol('1ItemTest.~ATH', ast)
interp.execute(ast)
