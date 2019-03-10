#!/usr/bin/env python
from athstmt import *
from athinterpreter import TildeAthInterp

stmts = AthStatementList([
    AthTokenStatement('FABRICATE', [AthCustomFunction('COUNTER', ['NUM', 'DIGITS'], AthStatementList([
        CondiJump([BnaryExpr(['<', IdentifierToken('NUM'), LiteralToken(0, int)]), 2]),
        AthTokenStatement('DIVULGATE', [AthTokenStatement('EXECUTE', [IdentifierToken('COUNTER'), UnaryExpr(['-', IdentifierToken('NUM')]), LiteralToken(0, int)])]),
        CondiJump([None, 2]),
        CondiJump([BnaryExpr(['<', IdentifierToken('NUM'), LiteralToken(10, int)]), 3]),
        AthTokenStatement('DIVULGATE', [BnaryExpr(['+', IdentifierToken('DIGITS'), LiteralToken(1, int)])]),
        AthTokenStatement('DIVULGATE', [AthTokenStatement('EXECUTE', [IdentifierToken('COUNTER'), BnaryExpr(['/_', IdentifierToken('NUM'), LiteralToken(10, int)]), BnaryExpr(['+', IdentifierToken('DIGITS'), LiteralToken(1, int)])])])
        ], pendant='COUNTER'))]),
    TildeAthLoop(False, AthStatementList([
        AthTokenStatement('input', [IdentifierToken('NUM'), LiteralToken('Give an integer to count the digits of: ', str)]),
        AthTokenStatement('print', [LiteralToken('There are ~d digits in that integer.\\n', str), AthTokenStatement('EXECUTE', [IdentifierToken('COUNTER'), IdentifierToken('NUM'), LiteralToken(0, int)])]),
        AthTokenStatement('DIE', [IdentifierToken('THIS')]),
        ], pendant='THIS'),
        AthTokenStatement('EXECUTE', [IdentifierToken('NULL')]))
    ], pendant='THIS')

if __name__ == '__main__':
    TildeAthInterp().exec_stmts('DigitCounter.~ATH', stmts)
