#!/usr/bin/env python
from athstmt import *
from athinterpreter import TildeAthInterp

stmts = AthStatementList([
    AthTokenStatement('PROCREATE', [IdentifierToken('LOOP'), LiteralToken(0, int)]),
    TildeAthLoop(False, AthStatementList([
        AthTokenStatement('print', [LiteralToken('Enter the coefficients of the cubic equation ax^3 + bx^2 + cx + d = 0\\n', str)]),
        AthTokenStatement('input', [IdentifierToken('A'), LiteralToken('a: ', str)]),
        AthTokenStatement('input', [IdentifierToken('B'), LiteralToken('b: ', str)]),
        AthTokenStatement('input', [IdentifierToken('C'), LiteralToken('c: ', str)]),
        AthTokenStatement('input', [IdentifierToken('D'), LiteralToken('d: ', str)]),
        AthTokenStatement('PROCREATE', [IdentifierToken('J'), BnaryExpr(['+', BnaryExpr(['*', IdentifierToken('A'), BnaryExpr(['-', BnaryExpr(['*', IdentifierToken('C'), BnaryExpr(['-', BnaryExpr(['*', BnaryExpr(['*', LiteralToken(18, int), IdentifierToken('B')]), IdentifierToken('D')]), BnaryExpr(['*', BnaryExpr(['*', LiteralToken(4, int), IdentifierToken('C')]), IdentifierToken('C')])])]), BnaryExpr(['*', BnaryExpr(['*', BnaryExpr(['*', LiteralToken(27, int), IdentifierToken('A')]), IdentifierToken('D')]), IdentifierToken('D')])])]), BnaryExpr(['*', BnaryExpr(['*', IdentifierToken('B'), IdentifierToken('B')]), BnaryExpr(['-', BnaryExpr(['*', IdentifierToken('C'), IdentifierToken('C')]), BnaryExpr(['*', BnaryExpr(['*', LiteralToken(4, int), IdentifierToken('B')]), IdentifierToken('D')])])])])]),
        AthTokenStatement('PROCREATE', [IdentifierToken('K'), BnaryExpr(['-', BnaryExpr(['*', IdentifierToken('B'), IdentifierToken('B')]), BnaryExpr(['*', BnaryExpr(['*', LiteralToken(3, int), IdentifierToken('A')]), IdentifierToken('C')])])]),
        CondiJump([BnaryExpr(['==', IdentifierToken('J'), LiteralToken(0, int)]), 9]),
        CondiJump([BnaryExpr(['==', IdentifierToken('K'), LiteralToken(0, int)]), 4]),
        AthTokenStatement('PROCREATE', [IdentifierToken('X1'), BnaryExpr(['/', UnaryExpr(['-', IdentifierToken('B')]), BnaryExpr(['*', LiteralToken(3, int), IdentifierToken('A')])])]),
        AthTokenStatement('PROCREATE', [IdentifierToken('X2'), IdentifierToken('X1')]),
        AthTokenStatement('PROCREATE', [IdentifierToken('X3'), IdentifierToken('X1')]),
        CondiJump([None, 16]),
        AthTokenStatement('PROCREATE', [IdentifierToken('X1'), BnaryExpr(['/', BnaryExpr(['-', BnaryExpr(['*', IdentifierToken('B'), BnaryExpr(['-', BnaryExpr(['*', BnaryExpr(['*', LiteralToken(4, int), IdentifierToken('A')]), IdentifierToken('C')]), BnaryExpr(['*', IdentifierToken('B'), IdentifierToken('B')])])]), BnaryExpr(['*', BnaryExpr(['*', BnaryExpr(['*', LiteralToken(9, int), IdentifierToken('A')]), IdentifierToken('A')]), IdentifierToken('D')])]), BnaryExpr(['*', IdentifierToken('A'), IdentifierToken('K')])])]),
        AthTokenStatement('PROCREATE', [IdentifierToken('X2'), BnaryExpr(['/', BnaryExpr(['-', BnaryExpr(['*', BnaryExpr(['*', LiteralToken(9, int), IdentifierToken('A')]), IdentifierToken('D')]), BnaryExpr(['*', IdentifierToken('B'), IdentifierToken('C')])]), BnaryExpr(['*', LiteralToken(2, int), IdentifierToken('K')])])]),
        AthTokenStatement('PROCREATE', [IdentifierToken('X3'), IdentifierToken('X2')]),
        CondiJump([None, 12]),
        AthTokenStatement('PROCREATE', [IdentifierToken('R'), BnaryExpr(['+', UnaryExpr(['-', LiteralToken(0.5, float)]), BnaryExpr(['*', BnaryExpr(['^', LiteralToken(0.75, float), LiteralToken(0.5, float)]), LiteralToken(1j, complex)])])]),
        AthTokenStatement('PROCREATE', [IdentifierToken('L'), BnaryExpr(['+', BnaryExpr(['*', BnaryExpr(['*', BnaryExpr(['*', LiteralToken(2, int), IdentifierToken('B')]), IdentifierToken('B')]), IdentifierToken('B')]), BnaryExpr(['*', BnaryExpr(['*', LiteralToken(9, int), IdentifierToken('A')]), BnaryExpr(['-', BnaryExpr(['*', BnaryExpr(['*', LiteralToken(3, int), IdentifierToken('A')]), IdentifierToken('D')]), BnaryExpr(['*', IdentifierToken('B'), IdentifierToken('C')])])])])]),
        AthTokenStatement('PROCREATE', [IdentifierToken('M'), BnaryExpr(['^', BnaryExpr(['*', BnaryExpr(['*', BnaryExpr(['*', UnaryExpr(['-', LiteralToken(27, int)]), IdentifierToken('A')]), IdentifierToken('A')]), IdentifierToken('J')]), LiteralToken(0.5, float)])]),
        CondiJump([BnaryExpr(['==', IdentifierToken('L'), IdentifierToken('M')]), 2]),
        AthTokenStatement('PROCREATE', [IdentifierToken('C1'), BnaryExpr(['^', BnaryExpr(['/', BnaryExpr(['+', IdentifierToken('L'), IdentifierToken('M')]), LiteralToken(2, int)]), BnaryExpr(['/', LiteralToken(1, int), LiteralToken(3, int)])])]),
        CondiJump([None, 1]),
        AthTokenStatement('PROCREATE', [IdentifierToken('C1'), BnaryExpr(['^', BnaryExpr(['/', BnaryExpr(['-', IdentifierToken('L'), IdentifierToken('M')]), LiteralToken(2, int)]), BnaryExpr(['/', LiteralToken(1, int), LiteralToken(3, int)])])]),
        AthTokenStatement('PROCREATE', [IdentifierToken('C2'), BnaryExpr(['*', IdentifierToken('C1'), IdentifierToken('R')])]),
        AthTokenStatement('PROCREATE', [IdentifierToken('C3'), BnaryExpr(['/', IdentifierToken('C1'), IdentifierToken('R')])]),
        AthTokenStatement('PROCREATE', [IdentifierToken('X1'), BnaryExpr(['/', UnaryExpr(['-', BnaryExpr(['+', BnaryExpr(['+', IdentifierToken('B'), IdentifierToken('C1')]), BnaryExpr(['/', IdentifierToken('K'), IdentifierToken('C1')])])]), BnaryExpr(['*', LiteralToken(3, int), IdentifierToken('A')])])]),
        AthTokenStatement('PROCREATE', [IdentifierToken('X2'), BnaryExpr(['/', UnaryExpr(['-', BnaryExpr(['+', BnaryExpr(['+', IdentifierToken('B'), IdentifierToken('C2')]), BnaryExpr(['/', IdentifierToken('K'), IdentifierToken('C2')])])]), BnaryExpr(['*', LiteralToken(3, int), IdentifierToken('A')])])]),
        AthTokenStatement('PROCREATE', [IdentifierToken('X3'), BnaryExpr(['/', UnaryExpr(['-', BnaryExpr(['+', BnaryExpr(['+', IdentifierToken('B'), IdentifierToken('C3')]), BnaryExpr(['/', IdentifierToken('K'), IdentifierToken('C3')])])]), BnaryExpr(['*', LiteralToken(3, int), IdentifierToken('A')])])]),
        AthTokenStatement('print', [LiteralToken('The three roots are ~.4f, ~.4f, ~.4f\\n', str), IdentifierToken('X1'), IdentifierToken('X2'), IdentifierToken('X3')]),
        AthTokenStatement('DIE', [IdentifierToken('LOOP')]),
        ], pendant='LOOP'),
        AthTokenStatement('EXECUTE', [IdentifierToken('NULL')])),
    AthTokenStatement('DIE', [IdentifierToken('THIS')])
    ], pendant='THIS')

if __name__ == '__main__':
    TildeAthInterp().exec_stmts('CubicRoots.~ATH', stmts)
