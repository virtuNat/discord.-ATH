#!/usr/bin/env python
from athstmt import *
from athinterpreter import TildeAthInterp

stmts = AthStatementList([
    AthTokenStatement('print', [LiteralToken('Welcome to ~ATH.\\n', str)]),
    AthTokenStatement('input', [IdentifierToken('TEST'), LiteralToken('Input name: ', str)]),
    AthTokenStatement('print', [LiteralToken('Thank you, ~s for inputting.\\n', str), IdentifierToken('TEST')]),
    AthTokenStatement('PROCREATE', [IdentifierToken('CTR'), LiteralToken(5, int)]),
    AthTokenStatement('REPLICATE', [IdentifierToken('CT2'), IdentifierToken('CTR')]),
    AthTokenStatement('BIFURCATE', [IdentifierToken('CTR'), IdentifierToken('CT3'), IdentifierToken('CT2')]),
    AthTokenStatement('AGGREGATE', [IdentifierToken('CT2'), IdentifierToken('CTR'), IdentifierToken('CT3')]),
    TildeAthLoop(False, AthStatementList([
        AthTokenStatement('print', [LiteralToken('Print ~d times.\\n', str), LiteralToken(1, int)]),
        AthTokenStatement('DIE', [IdentifierToken('CTR')]),
        AthTokenStatement('print', [LiteralToken('This should not print.', str)]),
        ], pendant='CTR'),
        AthTokenStatement('EXECUTE', [IdentifierToken('NULL')])),
    AthTokenStatement('print', [LiteralToken('I wish you a peaceful death, ~s.\\n', str), IdentifierToken('TEST')]),
    AthTokenStatement('DIE', [IdentifierToken('THIS')])
    ], pendant='THIS')

if __name__ == '__main__':
    TildeAthInterp().exec_stmts('Test.~ATH', stmts)
