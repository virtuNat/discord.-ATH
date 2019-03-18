#!/usr/bin/env python
from athstmt import *
from athinterpreter import TildeAthInterp

stmts = AthStatementList([
    TildeAthLoop(False, AthStatementList([
        AthTokenStatement('input', [IdentifierToken('NUM'), LiteralToken('Enter number: ', str)]),
        AthTokenStatement('print', [LiteralToken('Log base 2 of ~0.3f is ~0.3f.\\n', str), IdentifierToken('NUM'), AthTokenStatement('EXECUTE', [AthTokenStatement('EXECUTE', [IdentifierToken('import'), LiteralToken('MATH', str), LiteralToken('LOGBN', str)]), IdentifierToken('NUM')])]),
        AthTokenStatement('DIE', [IdentifierToken('THIS')]),
        ], pendant='THIS'),
        AthTokenStatement('EXECUTE', [IdentifierToken('NULL')]))
    ], pendant='THIS')

if __name__ == '__main__':
    TildeAthInterp().exec_stmts('StatementFuncTest.~ATH', stmts)
