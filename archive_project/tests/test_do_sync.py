import unittest
from unittest import mock
from unittest.mock import mock_open, patch, Mock, MagicMock
from archive_project import do_sync as DS
import os
from testfixtures import TempDirectory


class TestDo_sync(unittest.TestCase):

	def setUp(self):
		self.test_path = '/lustre/scratch118/infgen/pathogen/pathpipe/prokaryotes/seq-pipelines/Salmonella/enterica_subsp_enterica_serovar_Typhi_str_Ty2/TRACKING/5798/4316STDY6559668/SLX/17718553/20953_1#1'
		self.database = 'prokaryotes'
		self.s3_path = 's3://prokaryotes/Salmonella/enterica_subsp_enterica_serovar_Typhi_str_Ty2/TRACKING/5798/4316STDY6559668/SLX/17718553/20953_1#1'
		self.sync_class = DS.do_sync(self.test_path,self.database)
		self.bad_path = 'fake/path/'
		self.bad_path_class = DS.do_sync(self.bad_path,self.database)
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
		
	def test_make_s3path(self):
		self.assertEqual(self.sync_class.make_s3path(self.test_path),self.s3_path)
		self.assertEqual(self.sync_class.make_s3path(self.bad_path),None)
		
	def test_exclusions(self):
		dirs = ['fake_tmp_files', 'fake_directory1', 'fake_directory2']
		files = ['fake_file1.txt', 'fake_file2.txt', 'fake_file.fastq.gz', 'fake_file.bam', 'fake_file.sam']
		output_dirs, output_files = self.sync_class.exclusions(dirs,files)
		self.assertEqual(output_dirs, ['fake_directory1', 'fake_directory2'])
		self.assertEqual(output_files, ['fake_file1.txt', 'fake_file2.txt'])
	
	def test_get_filepaths(self):
		temp_dir_class = DS.do_sync(self.tempdir.path,self.database)
		file_paths = temp_dir_class.get_filepaths()	
		expected = [str(self.tempdir.path +'/fake_file1.txt'), str(self.tempdir.path +'/fake_directory/fake_file2.txt')]
		self.assertEqual(file_paths, expected)
		
	def test_boto3_upload_true(self):
		session = MagicMock()
		s3 = MagicMock()
		bucket = MagicMock() 
		return_paths = [str(self.tempdir.path + '/fake_file1.txt')]
		with patch("boto3.Session", return_value=session) as sesh:
			with patch("archive_project.do_sync.do_sync.get_filepaths", return_value=return_paths) as get_fp:
				with patch("archive_project.do_sync.do_sync.make_s3path", return_value=return_paths) as make_newpath: 
					session.resource.return_value = s3
					s3.Bucket.return_value = bucket
					with patch("archive_project.do_sync.open".format(__name__), new=mock_open(read_data="data1\ndata2\ndata3")) as _file:
						temp_dir_class = DS.do_sync(self.tempdir.path,self.database)
						actual = temp_dir_class.boto3_upload()
		session.resource.assert_called_once_with('s3', endpoint_url="https://cog.sanger.ac.uk")
		_file.assert_called_once_with(str(self.tempdir.path+'/fake_file1.txt'), 'rb')
		make_newpath.assert_called_once_with(str(self.tempdir.path+'/fake_file1.txt'))
		get_fp.assert_called_once_with()
		self.assertEqual([],actual)
		
	def test_boto3_upload_None(self):
		session = MagicMock()
		s3 = MagicMock()
		bucket = MagicMock() 
		return_paths = [str(self.tempdir.path + '/fake_file1.txt')]
		with patch("boto3.Session", return_value=session) as sesh:
			with patch("archive_project.do_sync.do_sync.get_filepaths", return_value=return_paths) as get_fp:
				with patch("archive_project.do_sync.do_sync.make_s3path", return_value=None) as make_newpath: 
					session.resource.return_value = s3
					s3.Bucket.return_value = bucket
					temp_dir_class = DS.do_sync(self.tempdir.path,self.database)
					actual = temp_dir_class.boto3_upload()
		session.resource.assert_called_once_with('s3', endpoint_url="https://cog.sanger.ac.uk")
		make_newpath.assert_called_once_with(str(self.tempdir.path+'/fake_file1.txt'))
		get_fp.assert_called_once_with()
		self.assertEqual(return_paths,actual)

if __name__ == '__main__':
        unittest.main()

