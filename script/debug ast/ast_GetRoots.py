#!/usr/bin/env python
from athstmt import *
from athinterpreter import TildeAthInterp

stmts = AthStatementList([
    AthTokenStatement('PROCREATE', [IdentifierToken('LOOP'), LiteralToken(0, int)]),
    TildeAthLoop(False, AthStatementList([
        AthTokenStatement('input', [IdentifierToken('A'), LiteralToken('A: ', str)]),
        AthTokenStatement('input', [IdentifierToken('B'), LiteralToken('B: ', str)]),
        AthTokenStatement('input', [IdentifierToken('C'), LiteralToken('C: ', str)]),
        AthTokenStatement('REPLICATE', [IdentifierToken('R'), BnaryExpr(['/', UnaryExpr(['-', IdentifierToken('B')]), BnaryExpr(['*', LiteralToken(2, int), IdentifierToken('A')])])]),
        AthTokenStatement('REPLICATE', [IdentifierToken('I'), BnaryExpr(['/', BnaryExpr(['^', BnaryExpr(['-', BnaryExpr(['*', IdentifierToken('B'), IdentifierToken('B')]), BnaryExpr(['*', BnaryExpr(['*', LiteralToken(4, int), IdentifierToken('A')]), IdentifierToken('C')])]), LiteralToken(0.5, float)]), BnaryExpr(['*', LiteralToken(2, int), IdentifierToken('A')])])]),
        AthTokenStatement('print', [LiteralToken('The roots of the quadratic equation ~dx^2 + ~dx + ~d are ~.4f and ~.4f.', str), IdentifierToken('A'), IdentifierToken('B'), IdentifierToken('C'), BnaryExpr(['+', IdentifierToken('R'), IdentifierToken('I')]), BnaryExpr(['-', IdentifierToken('R'), IdentifierToken('I')])]),
        AthTokenStatement('DIE', [IdentifierToken('LOOP')]),
        ], pendant='LOOP'),
        AthTokenStatement('EXECUTE', [IdentifierToken('NULL')])),
    AthTokenStatement('DIE', [IdentifierToken('THIS')])
    ], pendant='THIS')

if __name__ == '__main__':
    TildeAthInterp().exec_stmts('GetRoots.~ATH', stmts)
