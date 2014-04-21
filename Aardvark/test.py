import unittest
import db

class TestResearch(unittest.TestCase):

	@classmethod
	def setUpClass(cls):
		cls.a = cls.something

	def test_value(self):
		print 'hello'
		self.assertEqual(self.a, 'b')

# def gen_test(a, b):
#     def test(self):
#         self.assertEqual(a, b)
#     return test

# Fetch test cases from database
examples = db.find('research')

# for doc in examples:
	# print doc

# for t in l:
# 	test_name = 'test_%s' % t[0]
# 	test = test_generator(t[0], t[1])
# 	setattr(TestResearch, test_name, test);

def suite():
	suite = unittest.TestSuite()
	
	test = TestResearch('test_value')
	test.something ='s'
	suite.addTest(test)

	test2 = TestResearch('test_value')
	test.something = 'l'
	suite.addTest(test)

	return suite

if __name__ == '__main__':
	suite = suite()
	res = unittest.TextTestRunner(verbosity=2).run(suite)

# import vark

# p = 'examples/wef2'

# text = vark.get_text(p)

# acronyms = vark.get_acronyms(text)
# table = {}

# print acronyms

# for acronym in acronyms:
# 	table[acronym] = vark.expand(acronym, text)

# print json.dumps(table)