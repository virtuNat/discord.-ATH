#!/usr/bin/env python
from athstmt import *
from athinterpreter import TildeAthInterp

stmts = AthStatementList([
    AthTokenStatement('PROCREATE', [IdentifierToken('FOO'), None]),
    AthTokenStatement('PROCREATE', [IdentifierToken('BAR'), None]),
    TildeAthLoop(False, AthStatementList([
        TildeAthLoop(False, AthStatementList([
            AthTokenStatement('print', [LiteralToken('Oof.\\n', str)]),
            AthTokenStatement('DIE', [IdentifierToken('FOO'), IdentifierToken('BAR')]),
            ], pendant='BAR'),
            AthTokenStatement('EXECUTE', [IdentifierToken('NULL')])),
        AthTokenStatement('print', [LiteralToken('Well hello there.\\n', str)]),
        ], pendant='FOO'),
        AthTokenStatement('EXECUTE', [IdentifierToken('NULL')])),
    AthTokenStatement('DIE', [IdentifierToken('THIS')])
    ], pendant='THIS')

if __name__ == '__main__':
    TildeAthInterp().exec_stmts('SerialKiller.~ATH', stmts)
