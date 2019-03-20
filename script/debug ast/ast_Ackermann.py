#!/usr/bin/env python
from athstmt import *
from athinterpreter import TildeAthInterp

stmts = AthStatementList([
    AthTokenStatement('FABRICATE', [AthCustomFunction('ACK', ['M', 'N'], AthStatementList([
        CondiJump([BnaryExpr(['==', IdentifierToken('M'), LiteralToken(0, int)]), 2]),
        AthTokenStatement('DIVULGATE', [BnaryExpr(['+', IdentifierToken('N'), LiteralToken(1, int)])]),
        CondiJump([None, 2]),
        CondiJump([BnaryExpr(['==', IdentifierToken('N'), LiteralToken(0, int)]), 3]),
        AthTokenStatement('DIVULGATE', [AthTokenStatement('EXECUTE', [IdentifierToken('ACK'), BnaryExpr(['-', IdentifierToken('M'), LiteralToken(1, int)]), LiteralToken(1, int)])]),
        AthTokenStatement('DIVULGATE', [AthTokenStatement('EXECUTE', [IdentifierToken('ACK'), BnaryExpr(['-', IdentifierToken('M'), LiteralToken(1, int)]), AthTokenStatement('EXECUTE', [IdentifierToken('ACK'), IdentifierToken('M'), BnaryExpr(['-', IdentifierToken('N'), LiteralToken(1, int)])])])])
        ], pendant='ACK'))]),
    TildeAthLoop(False, AthStatementList([
        AthTokenStatement('input', [IdentifierToken('NUM'), LiteralToken('Get the ackermann function of: ', str)]),
        AthTokenStatement('print', [LiteralToken('The value of A(~d, ~d) is ~d.\\n', str), IdentifierToken('NUM'), IdentifierToken('NUM'), AthTokenStatement('EXECUTE', [IdentifierToken('ACK'), IdentifierToken('NUM'), IdentifierToken('NUM')])]),
        AthTokenStatement('DIE', [IdentifierToken('THIS')]),
        ], pendant='THIS'),
        AthTokenStatement('EXECUTE', [IdentifierToken('NULL')]))
    ], pendant='THIS')

if __name__ == '__main__':
    TildeAthInterp().exec_stmts('Ackermann.~ATH', stmts)
