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
			actual, message = get_studies(self.prok_path)
		_file.assert_called_once_with(self.prok_path) 
		expected = ['data1', 'data2', 'data3']
		self.assertEqual(expected,actual)
		self.assertEqual("Studies extracted from file",message)

	def test_get_studies_from_list(self):
		mock_open.return_value = FileNotFoundError 
		actual, message = get_studies(self.list_of_studies)
		expected = self.list_of_studies
		assert isinstance(actual, object)
		self.assertEqual(expected, actual)
		self.assertEqual("Studies extracted from list", message)

	def test_get_studies_integer(self):
		mock_open.return_value = FileNotFoundError
		actual, message = get_studies(47)
		self.assertEqual([], actual)
		self.assertEqual((type(47), "is not a valid input type. Nothing will be uploaded. Please enter path to a file or a list of study names"), message)

	def test_get_studies_empty_list(self):
		mock_open.return_value = FileNotFoundError
		actual, message = get_studies([])
		self.assertEqual([], actual)
		self.assertEqual("Studies extracted from list", message)

	def test_file_and_fail(self):
		mock_open.return_value = FileNotFoundError
		actual, message = get_studies(self.prok_path)
		#archive_project.GetStudies.open.assert_called_once_with(self.prok_path)
		expected = list(self.prok_path.split(','))
		self.assertEqual(expected,actual)
		self.assertEqual("This file can't be found. Attempt will be made to interpret as a list. If this is not intended then please enter a valid path to a file or a list of study names.",message)

if __name__ == '__main__':
	unittest.main()
