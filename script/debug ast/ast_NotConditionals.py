#!/usr/bin/env python
from athstmt import *
from athinterpreter import TildeAthInterp

stmts = AthStatementList([
    AthTokenStatement('PROCREATE', [IdentifierToken('LOOP'), LiteralToken(0, int)]),
    TildeAthLoop(False, AthStatementList([
        AthTokenStatement('input', [IdentifierToken('RATE'), LiteralToken('On a scale of A to AAAAA, how do you rate your suffering? ', str)]),
        AthTokenStatement('ENUMERATE', [IdentifierToken('RATE'), IdentifierToken('RATE')]),
        AthTokenStatement('PROCREATE', [IdentifierToken('A'), LiteralToken(0, int)]),
        AthTokenStatement('PROCREATE', [IdentifierToken('B'), LiteralToken(0, int)]),
        AthTokenStatement('PROCREATE', [IdentifierToken('C'), LiteralToken(0, int)]),
        AthTokenStatement('PROCREATE', [IdentifierToken('D'), LiteralToken(0, int)]),
        AthTokenStatement('PROCREATE', [IdentifierToken('E'), LiteralToken(0, int)]),
        AthTokenStatement('PROCREATE', [IdentifierToken('F'), LiteralToken(0, int)]),
        AthTokenStatement('BIFURCATE', [IdentifierToken('RATE'), IdentifierToken('RATE'), IdentifierToken('END')]),
        TildeAthLoop(False, AthStatementList([
            AthTokenStatement('DIE', [IdentifierToken('A')]),
            AthTokenStatement('BIFURCATE', [IdentifierToken('END'), IdentifierToken('RATE'), IdentifierToken('END')]),
            TildeAthLoop(False, AthStatementList([
                AthTokenStatement('DIE', [IdentifierToken('B')]),
                AthTokenStatement('BIFURCATE', [IdentifierToken('END'), IdentifierToken('RATE'), IdentifierToken('END')]),
                TildeAthLoop(False, AthStatementList([
                    AthTokenStatement('DIE', [IdentifierToken('C')]),
                    AthTokenStatement('BIFURCATE', [IdentifierToken('END'), IdentifierToken('RATE'), IdentifierToken('END')]),
                    TildeAthLoop(False, AthStatementList([
                        AthTokenStatement('DIE', [IdentifierToken('D')]),
                        AthTokenStatement('BIFURCATE', [IdentifierToken('END'), IdentifierToken('RATE'), IdentifierToken('END')]),
                        TildeAthLoop(False, AthStatementList([
                            AthTokenStatement('DIE', [IdentifierToken('E')]),
                            AthTokenStatement('BIFURCATE', [IdentifierToken('END'), IdentifierToken('RATE'), IdentifierToken('END')]),
                            TildeAthLoop(False, AthStatementList([
                                AthTokenStatement('DIE', [IdentifierToken('F')]),
                                AthTokenStatement('BIFURCATE', [IdentifierToken('END'), IdentifierToken('RATE'), IdentifierToken('END')]),
                                ], pendant='END'),
                                AthTokenStatement('EXECUTE', [IdentifierToken('NULL')])),
                            ], pendant='END'),
                            AthTokenStatement('EXECUTE', [IdentifierToken('NULL')])),
                        ], pendant='END'),
                        AthTokenStatement('EXECUTE', [IdentifierToken('NULL')])),
                    ], pendant='END'),
                    AthTokenStatement('EXECUTE', [IdentifierToken('NULL')])),
                ], pendant='END'),
                AthTokenStatement('EXECUTE', [IdentifierToken('NULL')])),
            ], pendant='END'),
            AthTokenStatement('EXECUTE', [IdentifierToken('NULL')])),
        CondiJump([IdentifierToken('A'), 2]),
        AthTokenStatement('print', [LiteralToken('Aw, you wee bab. Do you want me to kiss your booboos away?', str)]),
        CondiJump([None, 13]),
        CondiJump([IdentifierToken('B'), 2]),
        AthTokenStatement('print', [LiteralToken('Fortify!', str)]),
        CondiJump([None, 10]),
        CondiJump([IdentifierToken('C'), 2]),
        AthTokenStatement('print', [LiteralToken(':wackyZany:', str)]),
        CondiJump([None, 7]),
        CondiJump([IdentifierToken('D'), 2]),
        AthTokenStatement('print', [LiteralToken('Have you tried mixing coffee and energy drinks yet.', str)]),
        CondiJump([None, 4]),
        CondiJump([IdentifierToken('E'), 2]),
        AthTokenStatement('print', [LiteralToken('Same.', str)]),
        CondiJump([None, 1]),
        AthTokenStatement('print', [LiteralToken("You're overreacting. Calm your shit.", str)]),
        AthTokenStatement('print', [LiteralToken('\\n', str)]),
        AthTokenStatement('INSPECT', [UnaryExpr(['-', LiteralToken(1, int)])]),
        AthTokenStatement('DIE', [IdentifierToken('LOOP')]),
        ], pendant='LOOP'),
        AthTokenStatement('EXECUTE', [IdentifierToken('NULL')])),
    AthTokenStatement('DIE', [IdentifierToken('THIS')])
    ], pendant='THIS')

if __name__ == '__main__':
    TildeAthInterp().exec_stmts('NotConditionals.~ATH', stmts)
