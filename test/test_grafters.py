import unittest
from grafter import *
from athparser import ath_lexer, bltinparser, intparser, nameparser


class GrafterTester(unittest.TestCase):
	def graft_test(self, code, grafter, expected):
		tokens = ath_lexer.lex(code)
		graft = grafter(tokens, 0)
		self.assertNotEqual(None, graft)
		self.assertEqual(expected, graft.value)

	def test_tag(self):
		self.graft_test('NULL', nameparser, 'NULL')

	def test_keyword(self):
		self.graft_test('~ATH', bltinparser('~ATH'), '~ATH')

	def test_concatenate(self):
		parser = Concatenator(bltinparser('input'), nameparser)
		self.graft_test('input CHOICE', parser, ('input', 'CHOICE'))

	def test_concatenate_sugar(self):
		parser = bltinparser('input') + nameparser
		self.graft_test('input CHOICE', parser, ('input', 'CHOICE'))

	def test_concatenate_stack(self):
		parser = bltinparser('BIRTH') + nameparser + bltinparser(';')
		self.graft_test('BIRTH BLAH;', parser, (('BIRTH', 'BLAH'), ';'))

	def test_ipevaluator(self):
		parser = Evaluator(intparser, int)
		self.graft_test('413', parser, 413)

	def test_ipevaluator_sugar(self):
		parser = intparser ^ int
		self.graft_test('413', parser, 413)

	def test_lrexpression(self):
		grouper = bltinparser('+') ^ (lambda _: lambda l, r: int(l) + int(r))
		parser = ExprParser(intparser, grouper)
		self.graft_test('4', parser, '4')
		self.graft_test('4 + 5', parser, 9)
		self.graft_test('4 + 5 + 6', parser, 15)

	def test_lrexpression_sugar(self):
		grouper = bltinparser('*') ^ (lambda _: lambda l, r: int(l) * int(r))
		parser = intparser * grouper
		self.graft_test('4 * 3 * 2 * 1', parser, 24)

	def test_selector(self):
		parser = Selector(intparser, nameparser)
		self.graft_test('VAR', parser, 'VAR')
		self.graft_test('413', parser, '413')

	def test_selector_sugar(self):
		parser = intparser | nameparser
		self.graft_test('VAR', parser, 'VAR')
		self.graft_test('413', parser, '413')

	def test_ensuregraft(self):
		parser = EnsureGraft(bltinparser('UNLESS'))
		self.graft_test('BIRTH', parser, None)
		self.graft_test('UNLESS', parser, 'UNLESS')

	def test_repeater(self):
		parser = Repeater(nameparser)
		self.graft_test('VAR1 VAR2 VAR3', parser, ['VAR1', 'VAR2', 'VAR3'])

	def test_lazygrafter(self):
		def get_parser():
			return bltinparser('BIFURCATE')
		parser = LazyGrafter(get_parser)
		self.graft_test('BIFURCATE', parser, 'BIFURCATE')

	def test_strictgrafter(self):
		parser = EnsureGraft(StrictGrafter(nameparser))
		self.graft_test('abc d_ef ghi4', parser, None)
		self.graft_test('GRAVE', parser, 'GRAVE')


if __name__ == '__main__':
	unittest.main()
