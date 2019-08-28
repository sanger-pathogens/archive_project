import unittest
from unittest.mock import mock_open, patch  
from archive_project import get_studies as GS
'''
class TestGet_studies(unittest.TestCase):

	def setUp(self):
		self.database1 = GS.get_studies('prokaryotes')
		self.database2 = GS.get_studies('fake')
		self.prok_path = '/nfs/pathnfs05/conf/prokaryotes/prokaryotes.ilm.studies'
	
	def tearDown(self):
		pass 

	def test_make_path(self):
		self.assertEqual(self.database1.make_path(),self.prok_path) #check correct path made
	
	def test_read_studies(self):
		
		#test valid file will open and read studies correctly 
		with patch("archive_project.get_studies.open".format(__name__), 
					new=mock_open(read_data="data1\ndata2\ndata3")) as _file:
			actual = self.database1.read_studies() #Run the function to read studies with prokaryotes as database 
		_file.assert_called_once_with(self.prok_path) #Check was run with correct file path
		expected = ['data1', 'data2', 'data3']
		self.assertEqual(expected,actual) #check output as expected

		#test file that doesn't exist returns correct error 
		mock_open.return_value = FileNotFoundError 
		actual = self.database2.read_studies()
		self.assertEqual(None, actual)
		
if __name__ == '__main__':
	unittest.main()

'''
