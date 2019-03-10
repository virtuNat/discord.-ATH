#!/usr/bin/env python
from athstmt import *
from athinterpreter import TildeAthInterp

stmts = AthStatementList([
    AthTokenStatement('PROCREATE', [IdentifierToken('X'), LiteralToken(10, int)]),
    AthTokenStatement('PROCREATE', [IdentifierToken('Y'), LiteralToken(11, int)]),
    AthTokenStatement('PROCREATE', [IdentifierToken('Z'), LiteralToken(12, int)]),
    AthTokenStatement('FABRICATE', [AthCustomFunction('F', [], AthStatementList([
        AthTokenStatement('REPLICATE', [IdentifierToken('Y'), LiteralToken(2, int)]),
        AthTokenStatement('PROCREATE', [IdentifierToken('X'), BnaryExpr(['+', IdentifierToken('Z'), LiteralToken(1, int)])]),
        AthTokenStatement('PROCREATE', [IdentifierToken('Z'), BnaryExpr(['+', IdentifierToken('Y'), LiteralToken(2, int)])])
        ], pendant='F'))]),
    AthTokenStatement('FABRICATE', [AthCustomFunction('G', [], AthStatementList([
        AthTokenStatement('REPLICATE', [IdentifierToken('Z'), LiteralToken(5, int)]),
        AthTokenStatement('FABRICATE', [AthCustomFunction('H', [], AthStatementList([
            AthTokenStatement('REPLICATE', [IdentifierToken('X'), BnaryExpr(['+', IdentifierToken('Z'), LiteralToken(1, int)])]),
            AthTokenStatement('PROCREATE', [IdentifierToken('Y'), BnaryExpr(['+', IdentifierToken('X'), LiteralToken(1, int)])]),
            AthTokenStatement('EXECUTE', [IdentifierToken('F')]),
            AthTokenStatement('EXECUTE', [IdentifierToken('NULL')])
            ], pendant='H'))]),
        AthTokenStatement('EXECUTE', [IdentifierToken('H')]),
        AthTokenStatement('EXECUTE', [IdentifierToken('NULL')])
        ], pendant='G'))]),
    TildeAthLoop(False, AthStatementList([
        AthTokenStatement('EXECUTE', [IdentifierToken('G')]),
        AthTokenStatement('print', [LiteralToken('~d, ~d, ~d', str), IdentifierToken('X'), IdentifierToken('Y'), IdentifierToken('Z')]),
        AthTokenStatement('DIE', [IdentifierToken('G')]),
        ], pendant='G'),
        AthTokenStatement('EXECUTE', [IdentifierToken('NULL')])),
    AthTokenStatement('DIE', [IdentifierToken('THIS')])
    ], pendant='THIS')

if __name__ == '__main__':
    TildeAthInterp().exec_stmts('ScopeTest3.~ATH', stmts)
