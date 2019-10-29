import unittest
from unittest.mock import mock_open, patch  
from archive_project.GetStudies import get_studies

class TestGetStudies(unittest.TestCase):

	def setUp(self):
		self.prok_path = 'fake_path/prokaryotes.ilm.studies'
	
	def tearDown(self):
		pass 
	
	def test_get_studies_success(self):
		with patch("archive_project.GetStudies.open".format(__name__), mock_open(read_data="data1\ndata2\ndata3"), create=True) as _file:
			actual = get_studies(self.prok_path) 
		_file.assert_called_once_with(self.prok_path) 
		expected = ['data1', 'data2', 'data3']
		self.assertEqual(expected,actual) 

	def test_get_studies_fail(self):
		mock_open.return_value = FileNotFoundError 
		actual = get_studies(self.prok_path)
		self.assertEqual([], actual)
		
if __name__ == '__main__':
	unittest.main()
