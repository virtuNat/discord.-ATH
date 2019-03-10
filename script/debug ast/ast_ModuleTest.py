#!/usr/bin/env python
from athstmt import *
from athinterpreter import TildeAthInterp

stmts = AthStatementList([
    AthTokenStatement('FABRICATE', [AthCustomFunction('FIB', ['LENGTH'], AthStatementList([
        AthTokenStatement('PROCREATE', [IdentifierToken('N1'), LiteralToken(0, int)]),
        AthTokenStatement('PROCREATE', [IdentifierToken('N2'), LiteralToken(0, int)]),
        AthTokenStatement('PROCREATE', [IdentifierToken('N3'), LiteralToken(1, int)]),
        AthTokenStatement('PROCREATE', [IdentifierToken('LOOP'), None]),
        TildeAthLoop(False, AthStatementList([
            CondiJump([BnaryExpr(['<=', IdentifierToken('LENGTH'), LiteralToken(1, int)]), 1]),
            AthTokenStatement('DIE', [IdentifierToken('LOOP')]),
            AthTokenStatement('PROCREATE', [IdentifierToken('N1'), IdentifierToken('N2')]),
            AthTokenStatement('PROCREATE', [IdentifierToken('N2'), IdentifierToken('N3')]),
            AthTokenStatement('PROCREATE', [IdentifierToken('N3'), BnaryExpr(['+', IdentifierToken('N1'), IdentifierToken('N2')])]),
            AthTokenStatement('REPLICATE', [IdentifierToken('LENGTH'), BnaryExpr(['-', IdentifierToken('LENGTH'), LiteralToken(1, int)])]),
            ], pendant='LOOP'),
            AthTokenStatement('EXECUTE', [IdentifierToken('NULL')])),
        AthTokenStatement('DIVULGATE', [IdentifierToken('N3')])
        ], pendant='FIB'))]),
    TildeAthLoop(False, AthStatementList([
        AthTokenStatement('DIE', [IdentifierToken('THIS')]),
        ], pendant='THIS'),
        AthTokenStatement('EXECUTE', [IdentifierToken('NULL')]))
    ], pendant='THIS')

if __name__ == '__main__':
    TildeAthInterp().exec_stmts('ModuleTest.~ATH', stmts)
