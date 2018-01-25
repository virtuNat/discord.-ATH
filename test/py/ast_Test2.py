#!/usr/bin/env python
from athast import *
from tildeath import TildeAthInterp

interp = TildeAthInterp()
interp.ast = AthAstList([ProcreateStmt(VarExpr('LOOP'), None), ProcreateStmt(VarExpr('CTR'), IntExpr(1)), FabricateStmt(AthFunction('CTR', ['COUNT'], AthAstList([DivulgateStmt(BinaryExpr('+', VarExpr('COUNT'), IntExpr(1)))], 'CTR'))), BifurcateStmt(VarExpr('CTR'), VarExpr('ctr'), VarExpr('cnt')), InputStmt(VarExpr('MAX'), StringExpr('Count to how many? :')), TildeAthLoop(False, VarExpr('LOOP'), AthAstList([PrintStmt([StringExpr('Count: ~d\\n'), VarExpr('CTR')]), ReplicateStmt(VarExpr('CTR'), ExecuteStmt([VarExpr('CTR'), VarExpr('CTR')])), CondJumpStmt(BinaryExpr('>', VarExpr('CTR'), VarExpr('MAX')), 3), InspectStack([]), KillStmt(VarExpr('LOOP')), CondJumpStmt(None, 1), PrintStmt([StringExpr('Next...\\n')])], 'LOOP'), ExecuteStmt([VarExpr('NULL')])), KillStmt(VarExpr('THIS'))], 'THIS')
interp.execute()
