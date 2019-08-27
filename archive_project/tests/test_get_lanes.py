import unittest
from get_lanes import get_lanes

class TestGet_lanes(unittest.TestCase):

	def test_pf_data(self):
		#mock that data comes back and mock that it doesn't
mock = Mock(side_effect=KeyError('foo'))


if __name__ == '__main__':
	unittest.main()

