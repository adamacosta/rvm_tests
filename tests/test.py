import unittest
from subprocess import call
from os import chdir, devnull


class TestRVM(unittest.TestCase):

	def test_all(self):
		prepend = 'Failed a test that '
		msgs = ['tests for consistency across processes',
		        'tests that aborting a transaction undoes the changes',
		        'tests for consistency across processes w/ multiple segments',
		        'tests that aborting undoes changes in multiple segments',
		        'tests a commit, abort, commit sequence',
		        'tests that unlogged modification is lost on process termination',
		        'tests that a segment may only be involved in one transaction']
		FNULL = open(devnull, 'w')
		call(['make', 'tests'], stdout=FNULL)
		chdir('tests')
		for i in range(1, 8):
			t = call('./rvm_test' + str(i))
			self.assertEqual(t, 0, msg=prepend + msgs[i - 1])
			call(['rm', '-r', 'rvm_segments'])
		chdir('..')
		call(['make', 'clean'], stdout=FNULL)
		FNULL.close()

if __name__ == '__main__':
	unittest.main()