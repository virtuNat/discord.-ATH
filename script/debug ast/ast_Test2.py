#!/usr/bin/env python
from athstmt import *
from athinterpreter import TildeAthInterp

stmts = AthStatementList([
    AthTokenStatement('PROCREATE', [IdentifierToken('LOOP'), None]),
    AthTokenStatement('PROCREATE', [IdentifierToken('CTR'), LiteralToken(1, int)]),
    AthTokenStatement('FABRICATE', [AthCustomFunction('CTR', ['COUNT'], AthStatementList([
        AthTokenStatement('DIVULGATE', [BnaryExpr(['+', IdentifierToken('COUNT'), LiteralToken(1, int)])])
        ], pendant='CTR'))]),
    AthTokenStatement('BIFURCATE', [IdentifierToken('CTR'), IdentifierToken('ctr'), IdentifierToken('cnt')]),
    AthTokenStatement('input', [IdentifierToken('MAX'), LiteralToken('Count to how many? :', str)]),
    TildeAthLoop(False, AthStatementList([
        AthTokenStatement('print', [LiteralToken('Count: ~d\\n', str), IdentifierToken('CTR')]),
        AthTokenStatement('REPLICATE', [IdentifierToken('CTR'), AthTokenStatement('EXECUTE', [IdentifierToken('CTR'), IdentifierToken('CTR')])]),
        CondiJump([BnaryExpr(['>', IdentifierToken('CTR'), IdentifierToken('MAX')]), 3]),
        AthTokenStatement('INSPECT', []),
        AthTokenStatement('DIE', [IdentifierToken('LOOP')]),
        CondiJump([None, 1]),
        AthTokenStatement('print', [LiteralToken('Next...\\n', str)]),
        ], pendant='LOOP'),
        AthTokenStatement('EXECUTE', [IdentifierToken('NULL')])),
    AthTokenStatement('DIE', [IdentifierToken('THIS')])
    ], pendant='THIS')

if __name__ == '__main__':
    TildeAthInterp().exec_stmts('Test2.~ATH', stmts)
