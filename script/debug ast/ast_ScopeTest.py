#!/usr/bin/env python
from athstmt import *
from athinterpreter import TildeAthInterp

stmts = AthStatementList([
    AthTokenStatement('PROCREATE', [IdentifierToken('B'), LiteralToken(5, int)]),
    AthTokenStatement('FABRICATE', [AthCustomFunction('FOO', [], AthStatementList([
        AthTokenStatement('REPLICATE', [IdentifierToken('A'), BnaryExpr(['+', IdentifierToken('B'), LiteralToken(5, int)])]),
        AthTokenStatement('DIVULGATE', [IdentifierToken('A')])
        ], pendant='FOO'))]),
    AthTokenStatement('FABRICATE', [AthCustomFunction('BAR', [], AthStatementList([
        AthTokenStatement('PROCREATE', [IdentifierToken('B'), LiteralToken(2, int)]),
        AthTokenStatement('DIVULGATE', [AthTokenStatement('EXECUTE', [IdentifierToken('FOO')])])
        ], pendant='BAR'))]),
    AthTokenStatement('PROCREATE', [IdentifierToken('LOOP'), LiteralToken(1, int)]),
    TildeAthLoop(False, AthStatementList([
        AthTokenStatement('print', [LiteralToken('Foo: ~d\\n', str), AthTokenStatement('EXECUTE', [IdentifierToken('FOO')])]),
        AthTokenStatement('print', [LiteralToken('Bar: ~d\\n', str), AthTokenStatement('EXECUTE', [IdentifierToken('BAR')])]),
        AthTokenStatement('DIE', [IdentifierToken('LOOP')]),
        ], pendant='LOOP'),
        AthTokenStatement('EXECUTE', [IdentifierToken('NULL')])),
    AthTokenStatement('DIE', [IdentifierToken('THIS')])
    ], pendant='THIS')

if __name__ == '__main__':
    TildeAthInterp().exec_stmts('ScopeTest.~ATH', stmts)
