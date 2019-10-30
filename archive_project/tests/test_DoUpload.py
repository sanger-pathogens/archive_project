import unittest
from unittest.mock import patch, MagicMock
from archive_project import DoUpload as DU
from testfixtures import TempDirectory


class TestDoUpload(unittest.TestCase):

	def setUp(self):
		self.test_path = '/lustre/scratch118/infgen/pathogen/pathpipe/prokaryotes/seq-pipelines/Salmonella/enterica_subsp_enterica_serovar_Typhi_str_Ty2/TRACKING/5798/4316STDY6559668/SLX/17718553/20953_1#1'
		self.database = 'prokaryotes'
		self.s3_path = 's3://prokaryotes/Salmonella/enterica_subsp_enterica_serovar_Typhi_str_Ty2/TRACKING/5798/4316STDY6559668/SLX/17718553/20953_1#1'
		self.root = '/lustre/scratch118/infgen/pathogen/pathpipe/prokaryotes/seq-pipelines/'
		self.output_file = "failed_uploads_%s.txt"%self.database
		with patch("archive_project.DoUpload.open".format(__name__), create=True) as _file1:
			self.sync_class = DU.DoUpload(self.database,self.database,self.root,self.output_file)
			self.bad_path_class = DU.DoUpload(self.database,self.database,self.root, self.output_file)
		self.bad_path = 'fake/path/'
		self.tempdir = TempDirectory() 
		self.tempdir.write('fake_file1.txt', b'some foo thing') 
		self.tempdir.write('fake_tmp_files/folder/afile.txt', b'the text') 
		self.tempdir.write('fake_directory/fake_file2.txt', b'the text')
		self.tempdir.write('fake_directory/afile.bam', b'the text')  
		self.tempdir.write('fake_directory/afile.sam', b'the text') 
		self.tempdir.write('fake_directory/afile.fastq.gz', b'the text') 
		self.tempdir.makedir('empty_directory') 
		self.tempdir_path = self.tempdir.path
		self.mock_runrealcmd = MagicMock()

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
		with patch("archive_project.DoUpload.open".format(__name__), create=True) as _file1:
			temp_dir_class = DU.DoUpload(self.database,self.database,self.root,self.output_file)
			file_paths = temp_dir_class.get_filepaths(self.tempdir.path,)	
			expected = [str(self.tempdir.path +'/fake_file1.txt'), str(self.tempdir.path +'/fake_directory/fake_file2.txt')]
			self.assertEqual(file_paths, expected)
	
	def test_boto3_upload_true(self):
		session = MagicMock()
		s3 = MagicMock()
		bucket = MagicMock() 
		return_paths = [str(self.tempdir.path + '/fake_file1.txt')]
		with patch("boto3.Session", return_value=session) as sesh:
			with patch("archive_project.DoUpload.DoUpload.get_filepaths", return_value=return_paths) as get_fp:
				with patch("archive_project.DoUpload.DoUpload.make_s3path", return_value=return_paths) as make_newpath: 
					session.resource.return_value = s3
					s3.Bucket.return_value = bucket
					with patch("archive_project.DoUpload.open".format(__name__), create=True) as _file1:
						temp_dir_class = DU.DoUpload(self.database,self.database,self.root,self.output_file)
						_file1.assert_called_once_with(self.output_file,"a+")
						with patch("archive_project.DoUpload.open".format(__name__), create=True) as _file2:
							actual = temp_dir_class.boto3_upload(self.tempdir.path)
		session.resource.assert_called_once_with('s3', endpoint_url="https://cog.sanger.ac.uk")
		_file2.assert_called_once_with(str(self.tempdir.path+'/fake_file1.txt'), 'rb')
		make_newpath.assert_called_once_with(str(self.tempdir.path+'/fake_file1.txt'))
		get_fp.assert_called_once_with(self.tempdir.path)
		self.assertEqual([],actual)
	
	def test_boto3_upload_None(self):
		session = MagicMock()
		s3 = MagicMock()
		bucket = MagicMock() 
		return_paths = [str(self.tempdir.path + '/fake_file1.txt')]
		with patch("boto3.Session", return_value=session) as sesh:
			with patch("archive_project.DoUpload.DoUpload.get_filepaths", return_value=return_paths) as get_fp:
				with patch("archive_project.DoUpload.DoUpload.make_s3path", return_value=None) as make_newpath: 
					session.resource.return_value = s3
					s3.Bucket.return_value = bucket
					with patch("archive_project.DoUpload.open".format(__name__), create=True) as _file:
						temp_dir_class = DU.DoUpload(self.database,self.database,self.root,self.output_file)
						_file.assert_called_once_with(self.output_file,"a+")
						actual = temp_dir_class.boto3_upload(self.tempdir.path)
		session.resource.assert_called_once_with('s3', endpoint_url="https://cog.sanger.ac.uk")
		make_newpath.assert_called_once_with(str(self.tempdir.path+'/fake_file1.txt'))
		get_fp.assert_called_once_with(self.tempdir.path)
		self.assertEqual(return_paths,actual)

	def test_s3cmd_upload(self):
		return_path = [str(self.tempdir.path + '/fake_file1.txt')]
		with patch("archive_project.DoUpload.DoUpload.make_s3path", return_value=return_path) as make_newpath:
					temp_dir_class = DU.DoUpload(self.database, self.database, self.root, self.output_file)
					temp_dir_class.s3_sync(self.tempdir.path, command_runner=self.mock_runrealcmd)
		make_newpath.assert_called_once_with(str(self.tempdir.path))
		self.mock_runrealcmd.assert_called_once_with('s3cmd --verbose --no-preserve --exclude="*/*.fastq.gz" --exclude="*/*.bam" --exclude="*/*.sam" --exclude="*/*.bam.bai" --no-check-md5 sync' + str(self.tempdir.path) + str(return_path) + '--progress')

if __name__ == '__main__':
        unittest.main()

