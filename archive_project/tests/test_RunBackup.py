import unittest
from unittest.mock import Mock, call, patch
from archive_project.RunBackup import RunBackup


class TestRunBackup(unittest.TestCase):
	
	def setUp(self):
		self.database_1 = 'database1'
		self.database_2 = 'database2'
		self.database_3 = 'database3'
		self.mock_study_1 = ['mock_study_1']
		self.mock_study_2 = ['mock_study_2']
		self.mock_study_3 = [] 
		self.mock_study_4 = ['mock_study_1','mock_study_3','mock_study_5']
		self.mock_study_5 = 47
		self.mock_lane_1 = ['mock_lane_1']
		self.mock_lane_2 = []
		self.mock_lane_3 = ['mock_lane_2.1','mock_lane_2.2']
		self.do_sync = Mock() 
		self.studies_file_path_1 = '/nfs/pathnfs05/conf/database1/database1.ilm.studies'
		self.studies_file_path_2 = '/nfs/pathnfs05/conf/database2/database2.ilm.studies'
		self.studies_file_path_3 = '/nfs/pathnfs05/conf/database3/database3.ilm.studies'
		self.root = '/lustre/scratch118/infgen/pathogen/pathpipe/prokaryotes/seq-pipelines/'
		self.type1 = 'file' 
		self.type2 = 'studies'
		self.output_file = "output.txt"
		self.studies_from_file_message="Studies extracted from file"
		self.file_not_found_message="This file can't be found. Attempt will be made to interpret as a list. If this is not intended then please enter a valid path to a file or a list of study names."
		self.studies_from_list_message="Studies extracted from list"
		self.study_is_int_message=(type(self.mock_study_5),"is not a valid input type. Nothing will be uploaded. Please enter path to a file or a list of study names")
		self.no_data_found_message = ('Unknown study or no data associated with study: ', self.mock_study_3)
		self.all_paths_exist_massage = ''

	def tearDown(self):
		pass 

	def mock_make_bucket_ifnone(self,database):
		if database == self.database_1:
			return ('New bucket created: {}'.format(database))
		if database == self.database_2:
			return ("New bucket, {}, failed to be created".format(database))
		if database ==self.database_3:
			return ('{} bucket already exists'.format(database))
		
	def mock_get_study(self,input_studies):
		if input_studies == self.studies_file_path_1:
			return self.mock_study_1,self.studies_from_file_message
		elif input_studies == self.studies_file_path_2:
			return self.mock_study_2,self.studies_from_file_message
		elif input_studies == self.studies_file_path_3:
			return self.mock_study_3, self.studies_from_file_message
		elif input_studies == self.mock_study_1:
			return self.mock_study_1, self.studies_from_list_message
		elif input_studies == self.mock_study_2:
			return self.mock_study_2, self.file_not_found_message
		elif input_studies == self.mock_study_3:
			return self.mock_study_3, self.studies_from_list_message
		elif input_studies == self.mock_study_4:
			return self.mock_study_4,self.studies_from_list_message
		elif input_studies == self.mock_study_5:
			return [], self.study_is_int_message
		else:
			return [], 'message'
			
	def mock_lane_for_study(self,study):
		if study == self.mock_study_1[0] or study == self.mock_study_2[0]:
			return self.mock_lane_1, self.all_paths_exist_massage
		if study == self.mock_study_3: 
			return self.mock_lane_2, self.all_paths_exist_massage
		if study == self.mock_study_4[2]:
			return self.mock_lane_3, self.no_data_found_message
		else: return [],'message'
	
	def test_run_make_new_database_with_file_as_upload(self):
		with patch("archive_project.RunBackup.open".format(__name__),create=True) as _file:
			actual = RunBackup(self.studies_file_path_1, self.database_1, self.database_1, self.root, self.mock_make_bucket_ifnone, self.mock_get_study, self.mock_lane_for_study, uploader=self.do_sync, upload_mode='upload')
			actual.run()
		calls = [call(self.database_1,self.database_1,self.root, 'output.txt'),call().boto3_upload(self.mock_lane_1[0])]
		self.do_sync.assert_has_calls(calls)
		
	def test_run_database_already_exists_with_file_upload(self):
		with patch("archive_project.RunBackup.open".format(__name__), create=True) as _file:
			actual = RunBackup(self.studies_file_path_2, self.database_2, self.database_2, self.root, self.mock_make_bucket_ifnone, self.mock_get_study, self.mock_lane_for_study, uploader=self.do_sync, upload_mode='upload')
			actual.run()
		calls = [call(self.database_2, self.database_2, self.root, 'output.txt'),call().boto3_upload(self.mock_lane_1[0])]
		self.do_sync.assert_has_calls(calls)
		
	def test_run_database_study_is_none_with_file_upload(self):
		with patch("archive_project.RunBackup.open".format(__name__), create=True) as _file:
			actual = RunBackup(self.studies_file_path_3, self.database_3, self.database_3, self.root, self.mock_make_bucket_ifnone, self.mock_get_study, self.mock_lane_for_study, uploader=self.do_sync, upload_mode='upload')
			actual.run()
		calls = [call(self.database_3, self.database_3, self.root, 'output.txt')]
		self.do_sync.assert_has_calls(calls)

	def test_run_make_new_database_with_list_upload(self):
		with patch("archive_project.RunBackup.open".format(__name__), create=True) as _file:
			actual = RunBackup(self.mock_study_1, self.database_1, self.database_1, self.root, self.mock_make_bucket_ifnone, self.mock_get_study, self.mock_lane_for_study, uploader=self.do_sync, upload_mode='upload')
			actual.run()
		calls = [call(self.database_1,self.database_1,self.root, 'output.txt'),call().boto3_upload(self.mock_lane_1[0])]
		self.do_sync.assert_has_calls(calls)
		
	def test_run_database_already_exists_with_list_upload(self):
		with patch("archive_project.RunBackup.open".format(__name__), create=True) as _file:
			actual = RunBackup(self.mock_study_4, self.database_2, self.database_2, self.root, self.mock_make_bucket_ifnone, self.mock_get_study, self.mock_lane_for_study, uploader=self.do_sync, upload_mode='upload')
			actual.run()
		calls = [call(self.database_2,self.database_2,self.root, 'output.txt'),call().boto3_upload(self.mock_lane_1[0]),call().boto3_upload(self.mock_lane_3[0]),call().boto3_upload(self.mock_lane_3[1])]
		self.do_sync.assert_has_calls(calls)
		
	def test_run_database_study_is_none_with_list_as_upload(self):
		with patch("archive_project.RunBackup.open".format(__name__), create=True) as _file:
			actual = RunBackup(self.mock_study_3, self.database_3, self.database_3, self.root, self.mock_make_bucket_ifnone, self.mock_get_study, self.mock_lane_for_study, uploader=self.do_sync, upload_mode='upload')
			actual.run()
		calls=[call(self.database_3, self.database_3, self.root, 'output.txt')]
		self.do_sync.assert_has_calls(calls)
		
	def test_run_make_new_database_with_file_sync(self):
		with patch("archive_project.RunBackup.open".format(__name__), create=True) as _file:
			actual = RunBackup(self.studies_file_path_1, self.database_1, self.database_1, self.root, self.mock_make_bucket_ifnone, self.mock_get_study, self.mock_lane_for_study, uploader=self.do_sync)
			actual.run()
		calls = [call(self.database_1,self.database_1,self.root, 'output.txt'),call().s3_sync(self.mock_lane_1[0])]
		self.do_sync.assert_has_calls(calls)
		
	def test_run_database_already_exists_with_file_sync(self):
		with patch("archive_project.RunBackup.open".format(__name__), create=True) as _file:
			actual = RunBackup(self.studies_file_path_2, self.database_2, self.database_2, self.root, self.mock_make_bucket_ifnone, self.mock_get_study, self.mock_lane_for_study, uploader=self.do_sync, upload_mode='sync')
			actual.run()
		calls = [call(self.database_2, self.database_2, self.root, 'output.txt'),call().s3_sync(self.mock_lane_1[0])]
		self.do_sync.assert_has_calls(calls)
		
	def test_run_make_new_database_with_list_sync(self):
		with patch("archive_project.RunBackup.open".format(__name__), create=True) as _file:
			actual = RunBackup(self.mock_study_1, self.database_1, self.database_1, self.root, self.mock_make_bucket_ifnone, self.mock_get_study, self.mock_lane_for_study, uploader=self.do_sync)
			actual.run()
		calls = [call(self.database_1,self.database_1,self.root, 'output.txt'),call().s3_sync(self.mock_lane_1[0])]
		self.do_sync.assert_has_calls(calls)
		
	def test_run_database_already_exists_with_list_sync(self):
		with patch("archive_project.RunBackup.open".format(__name__), create=True) as _file:
			actual = RunBackup(self.mock_study_4, self.database_2, self.database_2, self.root, self.mock_make_bucket_ifnone, self.mock_get_study, self.mock_lane_for_study, uploader=self.do_sync)
			actual.run()
		calls = [call(self.database_2,self.database_2,self.root, 'output.txt'),call().s3_sync(self.mock_lane_1[0]),call().s3_sync(self.mock_lane_3[0]),call().s3_sync(self.mock_lane_3[1])]
		self.do_sync.assert_has_calls(calls)

	def test_run_with_study_as_integer(self):
		with patch("archive_project.RunBackup.open".format(__name__), create=True) as _file:
			actual = RunBackup(self.mock_study_5, self.database_2, self.database_2, self.root, self.mock_make_bucket_ifnone, self.mock_get_study, self.mock_lane_for_study, uploader=self.do_sync)
			actual.run()
		calls = [call(self.database_2, self.database_2, self.root, 'output.txt')]
		self.do_sync.assert_has_calls(calls)
		
if __name__ == '__main__':
        unittest.main()
