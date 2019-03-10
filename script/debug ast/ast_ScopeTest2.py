#!/usr/bin/env python
from athstmt import *
from athinterpreter import TildeAthInterp

stmts = AthStatementList([
    AthTokenStatement('PROCREATE', [IdentifierToken('X'), LiteralToken(1, int)]),
    AthTokenStatement('FABRICATE', [AthCustomFunction('F', ['I'], AthStatementList([
        AthTokenStatement('REPLICATE', [IdentifierToken('X'), IdentifierToken('I')]),
        AthTokenStatement('PROCREATE', [IdentifierToken('I'), BnaryExpr(['+', IdentifierToken('I'), LiteralToken(1, int)])]),
        AthTokenStatement('EXECUTE', [IdentifierToken('G'), IdentifierToken('I')]),
        AthTokenStatement('PROCREATE', [IdentifierToken('VAR'), None])
        ], pendant='F'))]),
    AthTokenStatement('FABRICATE', [AthCustomFunction('G', ['J'], AthStatementList([
        AthTokenStatement('PROCREATE', [IdentifierToken('J'), BnaryExpr(['+', IdentifierToken('J'), LiteralToken(1, int)])])
        ], pendant='G'))]),
    TildeAthLoop(False, AthStatementList([
        AthTokenStatement('EXECUTE', [IdentifierToken('F'), IdentifierToken('X')]),
        AthTokenStatement('print', [LiteralToken('~d\\n', str), IdentifierToken('X')]),
        AthTokenStatement('DIE', [IdentifierToken('THIS')]),
        ], pendant='THIS'),
        AthTokenStatement('EXECUTE', [IdentifierToken('NULL')]))
    ], pendant='THIS')

if __name__ == '__main__':
    TildeAthInterp().exec_stmts('ScopeTest2.~ATH', stmts)
