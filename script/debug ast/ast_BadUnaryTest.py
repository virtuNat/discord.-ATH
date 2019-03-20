#!/usr/bin/env python
from athstmt import *
from athinterpreter import TildeAthInterp

stmts = AthStatementList([
    TildeAthLoop(False, AthStatementList([
        AthTokenStatement('print', [LiteralToken('~d is twelve.', str), BnaryExpr(['+', LiteralToken(5, int), UnaryExpr(['+', LiteralToken(7, int)])])]),
        AthTokenStatement('DIE', [IdentifierToken('THIS')]),
        ], pendant='THIS'),
        AthTokenStatement('EXECUTE', [IdentifierToken('NULL')]))
    ], pendant='THIS')

if __name__ == '__main__':
    TildeAthInterp().exec_stmts('BadUnaryTest.~ATH', stmts)
