#!/usr/bin/env python
from athstmt import *
from athinterpreter import TildeAthInterp

stmts = AthStatementList([
    TildeAthLoop(False, AthStatementList([
        AthTokenStatement('input', [IdentifierToken('CARDSTR'), LiteralToken('Enter the shorthand string for your card, ex. 5H, 10S, QD: ', str)]),
        AthTokenStatement('ENUMERATE', [IdentifierToken('CARDSTR'), IdentifierToken('CARD')]),
        AthTokenStatement('REPLICATE', [IdentifierToken('TEMP'), IdentifierToken('CARD')]),
        AthTokenStatement('PROCREATE', [IdentifierToken('CARDLEN'), LiteralToken(0, int)]),
        AthTokenStatement('PROCREATE', [IdentifierToken('SUIT'), None]),
        TildeAthLoop(False, AthStatementList([
            AthTokenStatement('BIFURCATE', [IdentifierToken('TEMP'), IdentifierToken('LVAL'), IdentifierToken('TEMP')]),
            AthTokenStatement('PROCREATE', [IdentifierToken('CARDLEN'), BnaryExpr(['+', IdentifierToken('CARDLEN'), LiteralToken(1, int)])]),
            AthTokenStatement('PROCREATE', [IdentifierToken('SUIT'), IdentifierToken('LVAL')]),
            ], pendant='TEMP'),
            AthTokenStatement('EXECUTE', [IdentifierToken('NULL')])),
        AthTokenStatement('BIFURCATE', [IdentifierToken('CARD'), IdentifierToken('FACE'), IdentifierToken('NULL')]),
        AthTokenStatement('REPLICATE', [IdentifierToken('VALID'), BnaryExpr(['l|', BnaryExpr(['<', IdentifierToken('CARDLEN'), LiteralToken(2, int)]), BnaryExpr(['>', IdentifierToken('CARDLEN'), LiteralToken(3, int)])])]),
        TildeAthLoop(False, AthStatementList([
            AthTokenStatement('print', [LiteralToken("That doesn't even LOOK like a card string!\\n", str)]),
            AthTokenStatement('DIE', [IdentifierToken('THIS')]),
            ], pendant='VALID'),
            AthTokenStatement('EXECUTE', [IdentifierToken('NULL')])),
        AthTokenStatement('PROCREATE', [IdentifierToken('FACENAME'), LiteralToken('', str)]),
        AthTokenStatement('REPLICATE', [IdentifierToken('FACECHECK'), BnaryExpr(['==', IdentifierToken('CARDLEN'), LiteralToken(3, int)])]),
        TildeAthLoop(False, AthStatementList([
            AthTokenStatement('PROCREATE', [IdentifierToken('FACENAME'), LiteralToken('Ten', str)]),
            AthTokenStatement('DIE', [IdentifierToken('FACECHECK')]),
            ], pendant='FACECHECK'),
            AthTokenStatement('EXECUTE', [IdentifierToken('NULL')])),
        AthTokenStatement('REPLICATE', [IdentifierToken('FACECHECK'), BnaryExpr(['==', IdentifierToken('FACE'), LiteralToken('2', str)])]),
        TildeAthLoop(False, AthStatementList([
            AthTokenStatement('PROCREATE', [IdentifierToken('FACENAME'), LiteralToken('Two', str)]),
            AthTokenStatement('DIE', [IdentifierToken('FACECHECK')]),
            ], pendant='FACECHECK'),
            AthTokenStatement('EXECUTE', [IdentifierToken('NULL')])),
        AthTokenStatement('REPLICATE', [IdentifierToken('FACECHECK'), BnaryExpr(['==', IdentifierToken('FACE'), LiteralToken('3', str)])]),
        TildeAthLoop(False, AthStatementList([
            AthTokenStatement('PROCREATE', [IdentifierToken('FACENAME'), LiteralToken('Three', str)]),
            AthTokenStatement('DIE', [IdentifierToken('FACECHECK')]),
            ], pendant='FACECHECK'),
            AthTokenStatement('EXECUTE', [IdentifierToken('NULL')])),
        AthTokenStatement('REPLICATE', [IdentifierToken('FACECHECK'), BnaryExpr(['==', IdentifierToken('FACE'), LiteralToken('4', str)])]),
        TildeAthLoop(False, AthStatementList([
            AthTokenStatement('PROCREATE', [IdentifierToken('FACENAME'), LiteralToken('Four', str)]),
            AthTokenStatement('DIE', [IdentifierToken('FACECHECK')]),
            ], pendant='FACECHECK'),
            AthTokenStatement('EXECUTE', [IdentifierToken('NULL')])),
        AthTokenStatement('REPLICATE', [IdentifierToken('FACECHECK'), BnaryExpr(['==', IdentifierToken('FACE'), LiteralToken('5', str)])]),
        TildeAthLoop(False, AthStatementList([
            AthTokenStatement('PROCREATE', [IdentifierToken('FACENAME'), LiteralToken('Five', str)]),
            AthTokenStatement('DIE', [IdentifierToken('FACECHECK')]),
            ], pendant='FACECHECK'),
            AthTokenStatement('EXECUTE', [IdentifierToken('NULL')])),
        AthTokenStatement('REPLICATE', [IdentifierToken('FACECHECK'), BnaryExpr(['==', IdentifierToken('FACE'), LiteralToken('6', str)])]),
        TildeAthLoop(False, AthStatementList([
            AthTokenStatement('PROCREATE', [IdentifierToken('FACENAME'), LiteralToken('Six', str)]),
            AthTokenStatement('DIE', [IdentifierToken('FACECHECK')]),
            ], pendant='FACECHECK'),
            AthTokenStatement('EXECUTE', [IdentifierToken('NULL')])),
        AthTokenStatement('REPLICATE', [IdentifierToken('FACECHECK'), BnaryExpr(['==', IdentifierToken('FACE'), LiteralToken('7', str)])]),
        TildeAthLoop(False, AthStatementList([
            AthTokenStatement('PROCREATE', [IdentifierToken('FACENAME'), LiteralToken('Seven', str)]),
            AthTokenStatement('DIE', [IdentifierToken('FACECHECK')]),
            ], pendant='FACECHECK'),
            AthTokenStatement('EXECUTE', [IdentifierToken('NULL')])),
        AthTokenStatement('REPLICATE', [IdentifierToken('FACECHECK'), BnaryExpr(['==', IdentifierToken('FACE'), LiteralToken('8', str)])]),
        TildeAthLoop(False, AthStatementList([
            AthTokenStatement('PROCREATE', [IdentifierToken('FACENAME'), LiteralToken('Eight', str)]),
            AthTokenStatement('DIE', [IdentifierToken('FACECHECK')]),
            ], pendant='FACECHECK'),
            AthTokenStatement('EXECUTE', [IdentifierToken('NULL')])),
        AthTokenStatement('REPLICATE', [IdentifierToken('FACECHECK'), BnaryExpr(['==', IdentifierToken('FACE'), LiteralToken('9', str)])]),
        TildeAthLoop(False, AthStatementList([
            AthTokenStatement('PROCREATE', [IdentifierToken('FACENAME'), LiteralToken('Nine', str)]),
            AthTokenStatement('DIE', [IdentifierToken('FACECHECK')]),
            ], pendant='FACECHECK'),
            AthTokenStatement('EXECUTE', [IdentifierToken('NULL')])),
        AthTokenStatement('REPLICATE', [IdentifierToken('FACECHECK'), BnaryExpr(['==', IdentifierToken('FACE'), LiteralToken('J', str)])]),
        TildeAthLoop(False, AthStatementList([
            AthTokenStatement('PROCREATE', [IdentifierToken('FACENAME'), LiteralToken('Jack', str)]),
            AthTokenStatement('DIE', [IdentifierToken('FACECHECK')]),
            ], pendant='FACECHECK'),
            AthTokenStatement('EXECUTE', [IdentifierToken('NULL')])),
        AthTokenStatement('REPLICATE', [IdentifierToken('FACECHECK'), BnaryExpr(['==', IdentifierToken('FACE'), LiteralToken('Q', str)])]),
        TildeAthLoop(False, AthStatementList([
            AthTokenStatement('PROCREATE', [IdentifierToken('FACENAME'), LiteralToken('Queen', str)]),
            AthTokenStatement('DIE', [IdentifierToken('FACECHECK')]),
            ], pendant='FACECHECK'),
            AthTokenStatement('EXECUTE', [IdentifierToken('NULL')])),
        AthTokenStatement('REPLICATE', [IdentifierToken('FACECHECK'), BnaryExpr(['==', IdentifierToken('FACE'), LiteralToken('K', str)])]),
        TildeAthLoop(False, AthStatementList([
            AthTokenStatement('PROCREATE', [IdentifierToken('FACENAME'), LiteralToken('King', str)]),
            AthTokenStatement('DIE', [IdentifierToken('FACECHECK')]),
            ], pendant='FACECHECK'),
            AthTokenStatement('EXECUTE', [IdentifierToken('NULL')])),
        AthTokenStatement('REPLICATE', [IdentifierToken('FACECHECK'), BnaryExpr(['==', IdentifierToken('FACE'), LiteralToken('A', str)])]),
        TildeAthLoop(False, AthStatementList([
            AthTokenStatement('PROCREATE', [IdentifierToken('FACENAME'), LiteralToken('Ace', str)]),
            AthTokenStatement('DIE', [IdentifierToken('FACECHECK')]),
            ], pendant='FACECHECK'),
            AthTokenStatement('EXECUTE', [IdentifierToken('NULL')])),
        AthTokenStatement('REPLICATE', [IdentifierToken('FACECHECK'), BnaryExpr(['==', IdentifierToken('FACENAME'), LiteralToken('', str)])]),
        TildeAthLoop(False, AthStatementList([
            AthTokenStatement('PROCREATE', [IdentifierToken('FACENAME'), LiteralToken('WRONG', str)]),
            AthTokenStatement('print', [LiteralToken("This isn't a real card face!\\n", str)]),
            AthTokenStatement('DIE', [IdentifierToken('FACECHECK')]),
            ], pendant='FACECHECK'),
            AthTokenStatement('EXECUTE', [IdentifierToken('NULL')])),
        AthTokenStatement('PROCREATE', [IdentifierToken('SUITNAME'), LiteralToken('', str)]),
        AthTokenStatement('REPLICATE', [IdentifierToken('SUITCHECK'), BnaryExpr(['==', IdentifierToken('SUIT'), LiteralToken('S', str)])]),
        TildeAthLoop(False, AthStatementList([
            AthTokenStatement('PROCREATE', [IdentifierToken('SUITNAME'), LiteralToken('Spades', str)]),
            AthTokenStatement('DIE', [IdentifierToken('SUITCHECK')]),
            ], pendant='SUITCHECK'),
            AthTokenStatement('EXECUTE', [IdentifierToken('NULL')])),
        AthTokenStatement('REPLICATE', [IdentifierToken('SUITCHECK'), BnaryExpr(['==', IdentifierToken('SUIT'), LiteralToken('H', str)])]),
        TildeAthLoop(False, AthStatementList([
            AthTokenStatement('PROCREATE', [IdentifierToken('SUITNAME'), LiteralToken('Hearts', str)]),
            AthTokenStatement('DIE', [IdentifierToken('SUITCHECK')]),
            ], pendant='SUITCHECK'),
            AthTokenStatement('EXECUTE', [IdentifierToken('NULL')])),
        AthTokenStatement('REPLICATE', [IdentifierToken('SUITCHECK'), BnaryExpr(['==', IdentifierToken('SUIT'), LiteralToken('D', str)])]),
        TildeAthLoop(False, AthStatementList([
            AthTokenStatement('PROCREATE', [IdentifierToken('SUITNAME'), LiteralToken('Diamonds', str)]),
            AthTokenStatement('DIE', [IdentifierToken('SUITCHECK')]),
            ], pendant='SUITCHECK'),
            AthTokenStatement('EXECUTE', [IdentifierToken('NULL')])),
        AthTokenStatement('REPLICATE', [IdentifierToken('SUITCHECK'), BnaryExpr(['==', IdentifierToken('SUIT'), LiteralToken('C', str)])]),
        TildeAthLoop(False, AthStatementList([
            AthTokenStatement('PROCREATE', [IdentifierToken('SUITNAME'), LiteralToken('Clubs', str)]),
            AthTokenStatement('DIE', [IdentifierToken('SUITCHECK')]),
            ], pendant='SUITCHECK'),
            AthTokenStatement('EXECUTE', [IdentifierToken('NULL')])),
        AthTokenStatement('REPLICATE', [IdentifierToken('SUITCHECK'), BnaryExpr(['==', IdentifierToken('SUITNAME'), LiteralToken('', str)])]),
        TildeAthLoop(False, AthStatementList([
            AthTokenStatement('PROCREATE', [IdentifierToken('SUITNAME'), LiteralToken('WRONG', str)]),
            AthTokenStatement('print', [LiteralToken("This isn't a real card suit!\\n", str)]),
            AthTokenStatement('DIE', [IdentifierToken('SUITCHECK')]),
            ], pendant='SUITCHECK'),
            AthTokenStatement('EXECUTE', [IdentifierToken('NULL')])),
        AthTokenStatement('REPLICATE', [IdentifierToken('VALID'), BnaryExpr(['l&', BnaryExpr(['~=', IdentifierToken('SUITNAME'), LiteralToken('WRONG', str)]), BnaryExpr(['~=', IdentifierToken('FACENAME'), LiteralToken('WRONG', str)])])]),
        TildeAthLoop(False, AthStatementList([
            AthTokenStatement('print', [LiteralToken('Your card is the ~s of ~s.\\n', str), IdentifierToken('FACENAME'), IdentifierToken('SUITNAME')]),
            AthTokenStatement('DIE', [IdentifierToken('THIS')]),
            ], pendant='VALID'),
            AthTokenStatement('EXECUTE', [IdentifierToken('NULL')])),
        AthTokenStatement('print', [LiteralToken('Go back and try again with a REAL deck of cards!\\n', str)]),
        AthTokenStatement('DIE', [IdentifierToken('THIS')]),
        ], pendant='THIS'),
        AthTokenStatement('EXECUTE', [IdentifierToken('NULL')]))
    ], pendant='THIS')

if __name__ == '__main__':
    TildeAthInterp().exec_stmts('LoopHell.~ATH', stmts)
