#!/usr/bin/env python
from athast import *
from tildeath import TildeAthInterp

interp = TildeAthInterp()
interp.ast = AthAstList([ProcreateStmt(VarExpr('LOOP'), IntExpr(0)), TildeAthLoop(False, VarExpr('LOOP'), AthAstList([InputStmt(VarExpr('RATE'), StringExpr('On a scale of A to AAAAA, how do you rate your suffering? ')), EnumerateStmt(VarExpr('RATE'), VarExpr('RATE')), ProcreateStmt(VarExpr('A'), IntExpr(0)), ProcreateStmt(VarExpr('B'), IntExpr(0)), ProcreateStmt(VarExpr('C'), IntExpr(0)), ProcreateStmt(VarExpr('D'), IntExpr(0)), ProcreateStmt(VarExpr('E'), IntExpr(0)), ProcreateStmt(VarExpr('F'), IntExpr(0)), BifurcateStmt(VarExpr('RATE'), VarExpr('RATE'), VarExpr('END')), TildeAthLoop(False, VarExpr('END'), AthAstList([KillStmt(VarExpr('A')), BifurcateStmt(VarExpr('END'), VarExpr('RATE'), VarExpr('END')), TildeAthLoop(False, VarExpr('END'), AthAstList([KillStmt(VarExpr('B')), BifurcateStmt(VarExpr('END'), VarExpr('RATE'), VarExpr('END')), TildeAthLoop(False, VarExpr('END'), AthAstList([KillStmt(VarExpr('C')), BifurcateStmt(VarExpr('END'), VarExpr('RATE'), VarExpr('END')), TildeAthLoop(False, VarExpr('END'), AthAstList([KillStmt(VarExpr('D')), BifurcateStmt(VarExpr('END'), VarExpr('RATE'), VarExpr('END')), TildeAthLoop(False, VarExpr('END'), AthAstList([KillStmt(VarExpr('E')), BifurcateStmt(VarExpr('END'), VarExpr('RATE'), VarExpr('END')), TildeAthLoop(False, VarExpr('END'), AthAstList([KillStmt(VarExpr('F')), BifurcateStmt(VarExpr('END'), VarExpr('RATE'), VarExpr('END'))], 'END'), ExecuteStmt([VarExpr('NULL')]))], 'END'), ExecuteStmt([VarExpr('NULL')]))], 'END'), ExecuteStmt([VarExpr('NULL')]))], 'END'), ExecuteStmt([VarExpr('NULL')]))], 'END'), ExecuteStmt([VarExpr('NULL')]))], 'END'), ExecuteStmt([VarExpr('NULL')])), CondJumpStmt(VarExpr('A'), 2), PrintStmt([StringExpr('Aw, you wee bab. Do you want me to kiss your booboos away?')]), CondJumpStmt(None, 13), CondJumpStmt(VarExpr('B'), 2), PrintStmt([StringExpr('Fortify!')]), CondJumpStmt(None, 10), CondJumpStmt(VarExpr('C'), 2), PrintStmt([StringExpr(':wackyZany:')]), CondJumpStmt(None, 7), CondJumpStmt(VarExpr('D'), 2), PrintStmt([StringExpr('Have you tried mixing coffee and energy drinks yet.')]), CondJumpStmt(None, 4), CondJumpStmt(VarExpr('E'), 2), PrintStmt([StringExpr('Same.')]), CondJumpStmt(None, 1), PrintStmt([StringExpr("You're overreacting. Calm your shit.")]), PrintStmt([StringExpr('\\n')]), InspectStack([UnaryExpr('-', IntExpr(1))]), KillStmt(VarExpr('LOOP'))], 'LOOP'), ExecuteStmt([VarExpr('NULL')])), KillStmt(VarExpr('THIS'))], 'THIS')
interp.execute()
