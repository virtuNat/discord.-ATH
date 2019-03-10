#!/usr/bin/env python
from athstmt import *
from athinterpreter import TildeAthInterp

stmts = AthStatementList([
    AthTokenStatement('import', ['MATH', 'LOGBN']),
    TildeAthLoop(False, AthStatementList([
        AthTokenStatement('input', [IdentifierToken('NUM'), LiteralToken('Enter number: ', str)]),
        AthTokenStatement('print', [LiteralToken('Log base 2 of ~0.3f is ~0.3f.\\n', str), IdentifierToken('NUM'), AthTokenStatement('EXECUTE', [IdentifierToken('LOGBN'), IdentifierToken('NUM')])]),
        AthTokenStatement('DIE', [IdentifierToken('THIS')]),
        ], pendant='THIS'),
        AthTokenStatement('EXECUTE', [IdentifierToken('NULL')]))
    ], pendant='THIS')

if __name__ == '__main__':
    TildeAthInterp().exec_stmts('MathTest.~ATH', stmts)
