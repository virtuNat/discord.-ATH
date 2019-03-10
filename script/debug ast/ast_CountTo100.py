#!/usr/bin/env python
from athstmt import *
from athinterpreter import TildeAthInterp

stmts = AthStatementList([
    AthTokenStatement('PROCREATE', [IdentifierToken('A'), LiteralToken(0, int)]),
    AthTokenStatement('FABRICATE', [AthCustomFunction('COUNT', [], AthStatementList([
        CondiJump([BnaryExpr(['<', IdentifierToken('A'), LiteralToken(100, int)]), 3]),
        AthTokenStatement('PROCREATE', [IdentifierToken('A'), BnaryExpr(['+', IdentifierToken('A'), LiteralToken(1, int)])]),
        AthTokenStatement('print', [LiteralToken('~s ', str), IdentifierToken('A')]),
        AthTokenStatement('EXECUTE', [IdentifierToken('COUNT')])
        ], pendant='COUNT'))]),
    AthTokenStatement('PROCREATE', [IdentifierToken('LOOP'), LiteralToken(0, int)]),
    TildeAthLoop(False, AthStatementList([
        AthTokenStatement('EXECUTE', [IdentifierToken('COUNT')]),
        AthTokenStatement('DIE', [IdentifierToken('LOOP')]),
        ], pendant='LOOP'),
        AthTokenStatement('EXECUTE', [IdentifierToken('NULL')])),
    AthTokenStatement('DIE', [IdentifierToken('THIS')])
    ], pendant='THIS')

if __name__ == '__main__':
    TildeAthInterp().exec_stmts('CountTo100.~ATH', stmts)
