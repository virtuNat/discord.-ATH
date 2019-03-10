#!/usr/bin/env python
from athstmt import *
from athinterpreter import TildeAthInterp

stmts = AthStatementList([
    AthTokenStatement('PROCREATE', [IdentifierToken('LOOP'), None]),
    AthTokenStatement('PROCREATE', [IdentifierToken('STACK'), None]),
    AthTokenStatement('PROCREATE', [IdentifierToken('FLAG'), None]),
    TildeAthLoop(False, AthStatementList([
        AthTokenStatement('print', [LiteralToken('Select action:\\n', str)]),
        AthTokenStatement('print', [LiteralToken('[1] Add an item to stack\\n', str)]),
        AthTokenStatement('print', [LiteralToken('[2] View stack\\n', str)]),
        AthTokenStatement('print', [LiteralToken('[3] Exit\\n', str)]),
        AthTokenStatement('input', [IdentifierToken('CHOICE'), LiteralToken('', str)]),
        CondiJump([BnaryExpr(['==', IdentifierToken('CHOICE'), LiteralToken(3, int)]), 2]),
        AthTokenStatement('DIE', [IdentifierToken('LOOP')]),
        CondiJump([None, 14]),
        CondiJump([BnaryExpr(['==', IdentifierToken('CHOICE'), LiteralToken(2, int)]), 3]),
        AthTokenStatement('REPLICATE', [IdentifierToken('TEMP'), IdentifierToken('STACK')]),
        TildeAthLoop(False, AthStatementList([
            AthTokenStatement('BIFURCATE', [IdentifierToken('TEMP'), IdentifierToken('HEAD'), IdentifierToken('TEMP')]),
            AthTokenStatement('print', [LiteralToken('~s\\n', str), IdentifierToken('HEAD')]),
            ], pendant='TEMP'),
            AthTokenStatement('EXECUTE', [IdentifierToken('NULL')])),
        CondiJump([None, 10]),
        CondiJump([BnaryExpr(['==', IdentifierToken('CHOICE'), LiteralToken(1, int)]), 8]),
        AthTokenStatement('REPLICATE', [IdentifierToken('ITEM'), LiteralToken('', str)]),
        AthTokenStatement('input', [IdentifierToken('ITEM'), LiteralToken('Input string to add: ', str)]),
        CondiJump([IdentifierToken('FLAG'), 3]),
        AthTokenStatement('AGGREGATE', [IdentifierToken('STACK'), IdentifierToken('ITEM'), IdentifierToken('NULL')]),
        AthTokenStatement('DIE', [IdentifierToken('FLAG')]),
        CondiJump([None, 3]),
        AthTokenStatement('AGGREGATE', [IdentifierToken('STACK'), IdentifierToken('ITEM'), IdentifierToken('STACK')]),
        CondiJump([None, 1]),
        AthTokenStatement('print', [LiteralToken('Invalid input.', str)]),
        ], pendant='LOOP'),
        AthTokenStatement('EXECUTE', [IdentifierToken('NULL')])),
    AthTokenStatement('DIE', [IdentifierToken('THIS')])
    ], pendant='THIS')

if __name__ == '__main__':
    TildeAthInterp().exec_stmts('StackTest.~ATH', stmts)
