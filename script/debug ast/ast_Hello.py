#!/usr/bin/env python
from athast import *
from tildeath import TildeAthInterp

interp = TildeAthInterp()
interp.ast = AthAstList([TildeAthLoop(False, VarExpr('THIS'), AthAstList([PrintStmt([StringExpr('Hello World!')]), KillStmt(VarExpr('THIS'))], 'THIS'), ExecuteStmt([VarExpr('NULL')]))], 'THIS')
interp.execute()
