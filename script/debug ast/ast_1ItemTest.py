#!/usr/bin/env python
from athstmt import *
from athinterpreter import TildeAthInterp

stmts = AthStatementList([
    AthTokenStatement('PROCREATE', [IdentifierToken('LOOP'), LiteralToken(0, int)]),
    TildeAthLoop(False, AthStatementList([
        AthTokenStatement('print', [LiteralToken('Which of the following is not a French word?\\n', str)]),
        AthTokenStatement('print', [LiteralToken('[A] sale\\n', str)]),
        AthTokenStatement('print', [LiteralToken('[B] mode\\n', str)]),
        AthTokenStatement('print', [LiteralToken('[C] grand\\n', str)]),
        AthTokenStatement('print', [LiteralToken('[D] chat\\n', str)]),
        AthTokenStatement('print', [LiteralToken('[E] A, B, C, and D are all French words\\n', str)]),
        AthTokenStatement('print', [LiteralToken('[F] A, B, C, and D are all not French words\\n', str)]),
        AthTokenStatement('input', [IdentifierToken('CHOICE'), LiteralToken('', str)]),
        AthTokenStatement('ENUMERATE', [IdentifierToken('CHOICE'), IdentifierToken('CHARS')]),
        AthTokenStatement('BIFURCATE', [IdentifierToken('CHARS'), IdentifierToken('HEAD'), IdentifierToken('TAIL')]),
        CondiJump([UnaryExpr(['!', IdentifierToken('TAIL')]), 5]),
        CondiJump([BnaryExpr(['l|', BnaryExpr(['l&', BnaryExpr(['>=', IdentifierToken('CHOICE'), LiteralToken('A', str)]), BnaryExpr(['<=', IdentifierToken('CHOICE'), LiteralToken('F', str)])]), BnaryExpr(['l&', BnaryExpr(['<=', IdentifierToken('CHOICE'), LiteralToken('f', str)]), BnaryExpr(['>=', IdentifierToken('CHOICE'), LiteralToken('a', str)])])]), 2]),
        AthTokenStatement('print', [LiteralToken('Wrong! Try again, idiot.\\n', str)]),
        CondiJump([None, 10]),
        AthTokenStatement('print', [LiteralToken("Are you blind? That's not even a choice.\\n", str)]),
        CondiJump([None, 8]),
        CondiJump([BnaryExpr(['l|', BnaryExpr(['==', IdentifierToken('CHOICE'), LiteralToken('THE CHEAT CODE', str)]), BnaryExpr(['==', IdentifierToken('CHOICE'), LiteralToken('the cheat code', str)])]), 2]),
        AthTokenStatement('print', [LiteralToken("Damn, you caught me. It's a trick question.\\n", str)]),
        CondiJump([None, 5]),
        CondiJump([BnaryExpr(['l|', BnaryExpr(['==', IdentifierToken('CHOICE'), LiteralToken('DIE', str)]), BnaryExpr(['==', IdentifierToken('CHOICE'), LiteralToken('die', str)])]), 3]),
        AthTokenStatement('print', [LiteralToken('Hmph. Ninny.\\n', str)]),
        AthTokenStatement('DIE', [IdentifierToken('LOOP')]),
        CondiJump([None, 1]),
        AthTokenStatement('print', [LiteralToken("HA! Loser can't even guess the cheat code.\\n", str)]),
        AthTokenStatement('print', [LiteralToken('\\n', str)]),
        ], pendant='LOOP'),
        AthTokenStatement('EXECUTE', [IdentifierToken('NULL')])),
    AthTokenStatement('DIE', [IdentifierToken('THIS')])
    ], pendant='THIS')

if __name__ == '__main__':
    TildeAthInterp().exec_stmts('1ItemTest.~ATH', stmts)
