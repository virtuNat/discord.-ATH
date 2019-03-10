#!/usr/bin/env python
from athstmt import *
from athinterpreter import TildeAthInterp

stmts = AthStatementList([
    AthTokenStatement('PROCREATE', [IdentifierToken('TEST'), None]),
    TildeAthLoop(False, AthStatementList([
        CondiJump([IdentifierToken('TEST'), 3]),
        AthTokenStatement('print', [LiteralToken('Test!\\n', str)]),
        AthTokenStatement('REPLICATE', [IdentifierToken('TEST'), UnaryExpr(['!', IdentifierToken('TEST')])]),
        CondiJump([None, 5]),
        CondiJump([UnaryExpr(['!', IdentifierToken('TEST')]), 3]),
        AthTokenStatement('print', [LiteralToken('Test died\\n', str)]),
        AthTokenStatement('DIE', [IdentifierToken('THIS')]),
        CondiJump([None, 1]),
        AthTokenStatement('print', [LiteralToken('should not print\\n', str)]),
        ], pendant='THIS'),
        AthTokenStatement('EXECUTE', [IdentifierToken('NULL')]))
    ], pendant='THIS')

if __name__ == '__main__':
    TildeAthInterp().exec_stmts('IfJump.~ATH', stmts)
