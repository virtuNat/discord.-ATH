#!/usr/bin/env python
from athstmt import *
from athinterpreter import TildeAthInterp

stmts = AthStatementList([
    AthTokenStatement('PROCREATE', [IdentifierToken('LOOP'), LiteralToken(1, int)]),
    TildeAthLoop(False, AthStatementList([
        AthTokenStatement('PROCREATE', [IdentifierToken('X'), LiteralToken(1, int)]),
        AthTokenStatement('PROCREATE', [IdentifierToken('Y'), LiteralToken(2, int)]),
        AthTokenStatement('AGGREGATE', [IdentifierToken('Z'), IdentifierToken('X'), IdentifierToken('Y')]),
        AthTokenStatement('PROCREATE', [IdentifierToken('A'), LiteralToken(3, int)]),
        AthTokenStatement('REPLICATE', [IdentifierToken('Y'), IdentifierToken('A')]),
        AthTokenStatement('BIFURCATE', [IdentifierToken('Z'), IdentifierToken('B'), IdentifierToken('C')]),
        AthTokenStatement('print', [LiteralToken('~s, ~s', str), IdentifierToken('B'), IdentifierToken('C')]),
        AthTokenStatement('DIE', [IdentifierToken('LOOP')]),
        ], pendant='LOOP'),
        AthTokenStatement('EXECUTE', [IdentifierToken('NULL')])),
    AthTokenStatement('DIE', [IdentifierToken('THIS')])
    ], pendant='THIS')

if __name__ == '__main__':
    TildeAthInterp().exec_stmts('Aggregate-BifurcateTest.~ATH', stmts)
