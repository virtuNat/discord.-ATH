#!/usr/bin/env python
from athstmt import *
from athinterpreter import TildeAthInterp

stmts = AthStatementList([
    AthTokenStatement('PROCREATE', [IdentifierToken('LOOP'), LiteralToken(0, int)]),
    TildeAthLoop(False, AthStatementList([
        AthTokenStatement('print', [LiteralToken('~d', str), IdentifierToken('LOOP')]),
        CondiJump([BnaryExpr(['>', IdentifierToken('LOOP'), LiteralToken(9, int)]), 1]),
        AthTokenStatement('DIE', [IdentifierToken('LOOP')]),
        AthTokenStatement('PROCREATE', [IdentifierToken('LOOP'), BnaryExpr(['+', IdentifierToken('LOOP'), LiteralToken(1, int)])]),
        AthTokenStatement('print', [LiteralToken(', ', str)]),
        ], pendant='LOOP'),
        AthTokenStatement('EXECUTE', [IdentifierToken('NULL')])),
    AthTokenStatement('print', [LiteralToken('\\n~d\\n', str), IdentifierToken('LOOP')]),
    TildeAthLoop(True, AthStatementList([
        AthTokenStatement('print', [LiteralToken('~d', str), IdentifierToken('LOOP')]),
        CondiJump([BnaryExpr(['>', IdentifierToken('LOOP'), LiteralToken(0, int)]), 3]),
        AthTokenStatement('REPLICATE', [IdentifierToken('LOOP'), BnaryExpr(['-', IdentifierToken('LOOP'), LiteralToken(1, int)])]),
        AthTokenStatement('print', [LiteralToken(', ', str)]),
        AthTokenStatement('DIE', [IdentifierToken('LOOP')]),
        AthTokenStatement('REPLICATE', [IdentifierToken('LOOP'), UnaryExpr(['!', IdentifierToken('LOOP')])]),
        AthTokenStatement('print', [LiteralToken('\\n', str)]),
        ], pendant='LOOP'),
        AthTokenStatement('EXECUTE', [IdentifierToken('NULL')])),
    AthTokenStatement('DIE', [IdentifierToken('THIS')])
    ], pendant='THIS')

if __name__ == '__main__':
    TildeAthInterp().exec_stmts('LoopTypes.~ATH', stmts)
