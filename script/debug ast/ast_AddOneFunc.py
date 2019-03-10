#!/usr/bin/env python
from athstmt import *
from athinterpreter import TildeAthInterp

stmts = AthStatementList([
    AthTokenStatement('PROCREATE', [IdentifierToken('LOOP'), LiteralToken(0, int)]),
    AthTokenStatement('PROCREATE', [IdentifierToken('A'), LiteralToken(0, int)]),
    AthTokenStatement('FABRICATE', [AthCustomFunction('ADDONE', [], AthStatementList([
        AthTokenStatement('AGGREGATE', [IdentifierToken('A'), BnaryExpr(['+', IdentifierToken('A'), LiteralToken(1, int)]), IdentifierToken('NULL')]),
        AthTokenStatement('BIFURCATE', [IdentifierToken('A'), IdentifierToken('A'), IdentifierToken('NULL')])
        ], pendant='ADDONE'))]),
    TildeAthLoop(False, AthStatementList([
        AthTokenStatement('EXECUTE', [IdentifierToken('ADDONE')]),
        AthTokenStatement('print', [LiteralToken('~s ', str), IdentifierToken('A')]),
        CondiJump([BnaryExpr(['==', IdentifierToken('A'), LiteralToken(256, int)]), 2]),
        AthTokenStatement('print', [LiteralToken('\\n', str)]),
        AthTokenStatement('DIE', [IdentifierToken('LOOP')]),
        ], pendant='LOOP'),
        AthTokenStatement('EXECUTE', [IdentifierToken('NULL')])),
    AthTokenStatement('DIE', [IdentifierToken('THIS')])
    ], pendant='THIS')

if __name__ == '__main__':
    TildeAthInterp().exec_stmts('AddOneFunc.~ATH', stmts)
