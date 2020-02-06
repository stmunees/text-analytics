class SanityTest():
	""" Sanity Test """
	def test_addition_sanity(self):
		''' Basic Sanity Test '''
		assert(1 + 1 == 2)

SanityVar = SanityTest()
SanityVar.test_addition_sanity()