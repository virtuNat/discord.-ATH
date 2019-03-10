#!/usr/bin/env python
from athstmt import *
from athinterpreter import TildeAthInterp

stmts = AthStatementList([
    AthTokenStatement('PROCREATE', [IdentifierToken('LOOP'), None]),
    AthTokenStatement('PROCREATE', [IdentifierToken('QUEUE'), None]),
    AthTokenStatement('PROCREATE', [IdentifierToken('FLAG'), None]),
    TildeAthLoop(False, AthStatementList([
        AthTokenStatement('print', [LiteralToken('Select action:\\n', str)]),
        AthTokenStatement('print', [LiteralToken('[1] Add an item to queue\\n', str)]),
        AthTokenStatement('print', [LiteralToken('[2] View queue\\n', str)]),
        AthTokenStatement('print', [LiteralToken('[3] Exit\\n', str)]),
        AthTokenStatement('input', [IdentifierToken('CHOICE'), LiteralToken('', str)]),
        CondiJump([BnaryExpr(['==', IdentifierToken('CHOICE'), LiteralToken(3, int)]), 2]),
        AthTokenStatement('DIE', [IdentifierToken('LOOP')]),
        CondiJump([None, 22]),
        CondiJump([BnaryExpr(['==', IdentifierToken('CHOICE'), LiteralToken(2, int)]), 11]),
        CondiJump([UnaryExpr(['!', IdentifierToken('FLAG')]), 8]),
        AthTokenStatement('PROCREATE', [IdentifierToken('STACK'), None]),
        AthTokenStatement('REPLICATE', [IdentifierToken('TEMP'), IdentifierToken('QUEUE')]),
        AthTokenStatement('BIFURCATE', [IdentifierToken('TEMP'), IdentifierToken('HEAD'), IdentifierToken('TEMP')]),
        AthTokenStatement('AGGREGATE', [IdentifierToken('STACK'), IdentifierToken('HEAD'), IdentifierToken('NULL')]),
        TildeAthLoop(False, AthStatementList([
            AthTokenStatement('BIFURCATE', [IdentifierToken('TEMP'), IdentifierToken('HEAD'), IdentifierToken('TEMP')]),
            AthTokenStatement('AGGREGATE', [IdentifierToken('STACK'), IdentifierToken('HEAD'), IdentifierToken('STACK')]),
            ], pendant='TEMP'),
            AthTokenStatement('EXECUTE', [IdentifierToken('NULL')])),
        TildeAthLoop(False, AthStatementList([
            AthTokenStatement('BIFURCATE', [IdentifierToken('STACK'), IdentifierToken('HEAD'), IdentifierToken('STACK')]),
            AthTokenStatement('print', [LiteralToken('~s\\n', str), IdentifierToken('HEAD')]),
            ], pendant='STACK'),
            AthTokenStatement('EXECUTE', [IdentifierToken('NULL')])),
        AthTokenStatement('print', [LiteralToken('Queue print done.\\n', str)]),
        CondiJump([None, 12]),
        AthTokenStatement('print', [LiteralToken('Queue is empty.\\n', str)]),
        CondiJump([None, 10]),
        CondiJump([BnaryExpr(['==', IdentifierToken('CHOICE'), LiteralToken(1, int)]), 8]),
        AthTokenStatement('REPLICATE', [IdentifierToken('ITEM'), LiteralToken('', str)]),
        AthTokenStatement('input', [IdentifierToken('ITEM'), LiteralToken('Input string to add: ', str)]),
        CondiJump([IdentifierToken('FLAG'), 3]),
        AthTokenStatement('AGGREGATE', [IdentifierToken('QUEUE'), IdentifierToken('ITEM'), IdentifierToken('NULL')]),
        AthTokenStatement('DIE', [IdentifierToken('FLAG')]),
        CondiJump([None, 3]),
        AthTokenStatement('AGGREGATE', [IdentifierToken('QUEUE'), IdentifierToken('ITEM'), IdentifierToken('QUEUE')]),
        CondiJump([None, 1]),
        AthTokenStatement('print', [LiteralToken('Invalid input.', str)]),
        ], pendant='LOOP'),
        AthTokenStatement('EXECUTE', [IdentifierToken('NULL')])),
    AthTokenStatement('DIE', [IdentifierToken('THIS')])
    ], pendant='THIS')

if __name__ == '__main__':
    TildeAthInterp().exec_stmts('QueueTest.~ATH', stmts)
