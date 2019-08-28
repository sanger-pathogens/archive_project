import unittest
from unittest import mock
from unittest.mock import mock_open, patch, Mock
from archive_project import get_lanes as GL


class TestGet_lanes(unittest.TestCase):

	@mock.patch('archive_project.get_lanes.check_output')
	def test_pf_data(self,mock_query: unittest.mock.Mock):
		lane_class = GL.get_lanes("study")
		actual = lane_class.pf_data()
		mock_query.assert_called_once_with(['pf', 'data', '-t', 'study', '-i', 'study'])
		'''
		actual = lane_class.check_output.return_value = ['data']
		self.assertEqual(['data'],actual)
		'''
		
'''

GL.get_lanes.pf = Mock()
GL.get_lanes.check_output = Mock()
lane_class = GL.get_lanes('study')

actual = lane_class.check_output.return_value = ['data']
self.assertEqual(['data'],actual)

'''
if __name__ == '__main__':
        unittest.main()
dbxref
