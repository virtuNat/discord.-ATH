#!/usr/bin/env python
from athstmt import *
from athinterpreter import TildeAthInterp

stmts = AthStatementList([
    AthTokenStatement('FABRICATE', [AthCustomFunction('FACT', ['PROD', 'NUM'], AthStatementList([
        CondiJump([BnaryExpr(['>', IdentifierToken('NUM'), LiteralToken(1, int)]), 1]),
        AthTokenStatement('DIVULGATE', [AthTokenStatement('EXECUTE', [IdentifierToken('FACT'), BnaryExpr(['*', IdentifierToken('PROD'), IdentifierToken('NUM')]), BnaryExpr(['-', IdentifierToken('NUM'), LiteralToken(1, int)])])]),
        AthTokenStatement('DIVULGATE', [IdentifierToken('PROD')])
        ], pendant='FACT'))]),
    TildeAthLoop(False, AthStatementList([
        AthTokenStatement('input', [IdentifierToken('NUM'), LiteralToken('Get the factorial of: ', str)]),
        AthTokenStatement('print', [LiteralToken('The factorial is ~d.\\n', str), AthTokenStatement('EXECUTE', [IdentifierToken('FACT'), LiteralToken(1, int), IdentifierToken('NUM')])]),
        AthTokenStatement('DIE', [IdentifierToken('THIS')]),
        ], pendant='THIS'),
        AthTokenStatement('EXECUTE', [IdentifierToken('NULL')]))
    ], pendant='THIS')

if __name__ == '__main__':
    TildeAthInterp().exec_stmts('Factorial.~ATH', stmts)
