import unittest
from unittest.mock import mock_open, patch  
from archive_project.GetStudies import get_studies

class TestGetStudies(unittest.TestCase):

	def setUp(self):
		self.prok_path = 'fake_path/prokaryotes.ilm.studies'
		self.list_of_studies = ['mock_study_1','mock_study_3','mock_study_5']

	def tearDown(self):
		pass 
	
	def test_get_studies_from_file(self):
		with patch("archive_project.GetStudies.open".format(__name__), mock_open(read_data="data1\ndata2\ndata3"), create=True) as _file:
			actual = get_studies(self.prok_path) 
		_file.assert_called_once_with(self.prok_path) 
		expected = ['data1', 'data2', 'data3']
		self.assertEqual(expected,actual) 

	def test_get_studies_from_list(self):
		mock_open.return_value = FileNotFoundError 
		actual = get_studies(self.list_of_studies)
		expected = self.list_of_studies
		assert isinstance(actual, object)
		self.assertEqual(expected, actual)

	def test_get_studies_integer(self):
		mock_open.return_value = FileNotFoundError
		actual = get_studies(47)
		self.assertEqual([], actual)

	def test_get_studies_empty_list(self):
		mock_open.return_value = FileNotFoundError
		actual = get_studies([])
		self.assertEqual([], actual)

if __name__ == '__main__':
	unittest.main()
