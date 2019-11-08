import unittest
from unittest import mock
from unittest.mock import call
from archive_project.GetLanes import get_lanes
from testfixtures import TempDirectory

class TestGetLanes(unittest.TestCase):
	
	def setUp(self):
		self.tempdir = TempDirectory() 
		self.tempdir.write('fake_file1.txt', b'some foo thing') 
		self.tempdir.write('fake_tmp_files/folder/afile.txt', b'the text')
		self.tempdir.write('fake_directory/fake_file2.txt', b'the text') 
		self.tempdir.write('fake_directory/afile.bam', b'the text') 
		self.tempdir.write('fake_directory/afile.sam', b'the text') 
		self.tempdir.write('fake_directory/afile.fastq.gz', b'the text') 
		self.tempdir.makedir('empty_directory') 
		self.tempdir_path = self.tempdir.path

	def tearDown(self):
		self.tempdir.cleanup()
		pass 
		
	def test_get_lanes_returns_data(self):
		data_list = bytes(str(self.tempdir.path + '/fake_tmp_files/folder/afile.txt\n'+self.tempdir.path + '/fake_directory/fake_file2.txt\n' + 'fake_path\n'),'ascii')
		with mock.patch('archive_project.GetLanes.check_output', return_value=data_list) as co:
			actual, message = get_lanes("study")
		co.assert_called_once_with(['pf', 'data', '-t', 'study', '-i', 'study'])
		calls = [call(self.tempdir.path + '/fake_tmp_files/folder/afile.txt'), call(self.tempdir.path + '/fake_directory/fake_file2.txt')]
		expected = [str(self.tempdir.path + '/fake_tmp_files/folder/afile.txt'), str(self.tempdir.path + '/fake_directory/fake_file2.txt')]
		self.assertEqual(expected,actual)
		self.assertEqual(('These paths were returned by pf, but do not actually exist', ['fake_path'], '\n'),message)

	def test_get_lanes_returns_nodata(self):
		with mock.patch('archive_project.GetLanes.check_output', return_value=b'') as co:
			with mock.patch('os.path.exists', return_value=True) as pe:
				actual, message = get_lanes("study")
		self.assertEqual([],actual)
		pe.assert_not_called()
		self.assertEqual(('Unknown study or no data associated with study: ', "study", '\n'),message)


		
if __name__ == '__main__':
        unittest.main()
