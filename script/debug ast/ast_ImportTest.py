#!/usr/bin/env python
from athstmt import *
from athinterpreter import TildeAthInterp

stmts = AthStatementList([
    AthTokenStatement('import', ['ModuleTest', 'FIB']),
    AthTokenStatement('PROCREATE', [IdentifierToken('MAIN'), None]),
    AthTokenStatement('PROCREATE', [IdentifierToken('COUNT'), LiteralToken(1, int)]),
    TildeAthLoop(False, AthStatementList([
        AthTokenStatement('print', [LiteralToken('F~d = ~d\\n', str), IdentifierToken('COUNT'), AthTokenStatement('EXECUTE', [IdentifierToken('FIB'), IdentifierToken('COUNT')])]),
        CondiJump([BnaryExpr(['>=', IdentifierToken('COUNT'), LiteralToken(10, int)]), 1]),
        AthTokenStatement('DIE', ['MAIN']),
        AthTokenStatement('PROCREATE', [IdentifierToken('COUNT'), BnaryExpr(['+', IdentifierToken('COUNT'), LiteralToken(1, int)])]),
        ], pendant='MAIN'),
        AthTokenStatement('EXECUTE', [IdentifierToken('NULL')])),
    AthTokenStatement('DIE', ['THIS'])
    ], pendant='THIS')
TildeAthInterp().exec_stmts('ImportTest.~ATH', stmts)
