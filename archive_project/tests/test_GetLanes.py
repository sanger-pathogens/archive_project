import unittest
from unittest import mock
from archive_project.GetLanes import get_lanes
from testfixtures import TempDirectory

class TestGetLanes(unittest.TestCase):
	
	def setUp(self):
		self.tempdir = TempDirectory() 
		self.tempdir.write('fake_file1.txt', b'some foo thing') #this file should be kept 
		self.tempdir.write('fake_tmp_files/folder/afile.txt', b'the text') #directory to be removed
		self.tempdir.write('fake_directory/fake_file2.txt', b'the text') #this file kept
		self.tempdir.write('fake_directory/afile.bam', b'the text') #this file removed 
		self.tempdir.write('fake_directory/afile.sam', b'the text') #this file removed 
		self.tempdir.write('fake_directory/afile.fastq.gz', b'the text') #this file removed
		self.tempdir.makedir('empty_directory') #this directory should be removed 
		self.tempdir_path = self.tempdir.path

	def tearDown(self):
		self.tempdir.cleanup()
		pass 
		
	def test_get_lanes_returns_data(self):
		data_list = bytes(str(self.tempdir.path + '/fake_tmp_files/folder/afile.txt\n'+self.tempdir.path + '/fake_directory/fake_file2.txt\n' + 'fake_path\n'),'ascii')
		with mock.patch('archive_project.GetLanes.check_output', return_value=data_list) as co:
			actual = get_lanes("study")
		co.assert_called_once_with(['pf', 'data', '-t', 'study', '-i', 'study']) #check_output called correctly 
		expected = [str(self.tempdir.path + '/fake_tmp_files/folder/afile.txt'), str(self.tempdir.path + '/fake_directory/fake_file2.txt')]
		print(actual)
		print(expected)
		self.assertEqual(expected,actual) #output of function as expected
		
	def test_pf_data_nodata(self):
		#For study that doesn't exits or had no data
		with mock.patch('archive_project.GetLanes.check_output', return_value=b'') as co:
			actual = get_lanes("study")
		self.assertEqual(None,actual) #output as expected 
		
if __name__ == '__main__':
        unittest.main()
