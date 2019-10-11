import unittest
from unittest.mock import Mock, call
from archive_project.RunBackup import RunBackup

class TestRunBackup(unittest.TestCase):
	
	def setUp(self):
		self.database_1 = 'database1'
		self.database_2 = 'database2'
		self.database_3 = 'database3'
		self.mock_study_1 = ['mock_study_1']
		self.mock_study_2 = ['mock_study_2']
		self.mock_study_3 = None 
		self.mock_study_4 = ['mock_study_1','mock_study_3','mock_study_5']
		self.mock_lane_1 = ['mock_lane_1']
		self.mock_lane_2 = None
		self.mock_lane_3 = ['mock_lane_2.1','mock_lane_2.2']
		self.do_sync = Mock() 
		self.studies_file_path_1 = '/nfs/pathnfs05/conf/database1/database1.ilm.studies'
		self.studies_file_path_2 = '/nfs/pathnfs05/conf/database2/database2.ilm.studies'
		self.studies_file_path_3 = '/nfs/pathnfs05/conf/database3/database3.ilm.studies'
		self.root = '/lustre/scratch118/infgen/pathogen/pathpipe/prokaryotes/seq-pipelines/'
		self.type1 = 'file' 
		self.type2 = 'studies'
		self.output_file = "failed_uploads.txt"
		
	def tearDown(self):
		pass 

	def mock_make_bucket_ifnone(self,database):
		if database == self.database_1:
			return True
		if database == self.database_2 or database ==self.database_3:
			return False
		
	def mock_get_study(self,studies_file_path):
		if studies_file_path == self.studies_file_path_1:
			return self.mock_study_1
		if studies_file_path == self.studies_file_path_2:
			return self.mock_study_2
		if studies_file_path == self.studies_file_path_3:
			return self.mock_study_3
			
	def mock_lane_for_study(self,study):
		if study == self.mock_study_1[0] or study == self.mock_study_2[0]:
			return self.mock_lane_1
		if study == self.mock_study_3: 
			return self.mock_lane_2
		if study == self.mock_study_4[2]:
			return self.mock_lane_3
			
	def mock_sync_for_study(self,database,path):
		if study == self.mock_study_1:
			return []
		if study == self.mock_study_2 or study == self.mock_study_3:
			return [fake_failed1,fake_failed_2]
			
	def test_run_make_new_database_withfile(self):
		actual = RunBackup(self.type1, self.studies_file_path_1, self.database_1, self.database_1, self.root, self.mock_make_bucket_ifnone, self.mock_get_study, self.mock_lane_for_study, self.do_sync)
		actual.run()
		calls = [call(self.database_1,self.database_1,self.root, self.output_file),call().boto3_upload(self.mock_lane_1[0])]
		self.do_sync.assert_has_calls(calls)
		
	def test_run_database_already_exists_withfile(self):
		actual = RunBackup(self.type1, self.studies_file_path_2, self.database_2, self.database_2, self.root, self.mock_make_bucket_ifnone, self.mock_get_study, self.mock_lane_for_study, self.do_sync)
		actual.run()
		calls = [call(self.database_2, self.database_2, self.root, self.output_file),call().boto3_upload(self.mock_lane_1[0])]
		self.do_sync.assert_has_calls(calls)
		
	def test_run_database_study_is_nonewith_file(self):
		actual = RunBackup(self.type1, self.studies_file_path_3, self.database_3, self.database_3, self.root, self.mock_make_bucket_ifnone, self.mock_get_study, self.mock_lane_for_study, self.do_sync)
		actual.run()
		self.do_sync.assert_not_called()
		
	def test_run_make_new_database_withlist(self):
		actual = RunBackup(self.type2, self.mock_study_1, self.database_1, self.database_1, self.root, self.mock_make_bucket_ifnone, self.mock_get_study, self.mock_lane_for_study, self.do_sync)
		actual.run()
		calls = [call(self.database_1,self.database_1,self.root,self.output_file),call().boto3_upload(self.mock_lane_1[0])]
		self.do_sync.assert_has_calls(calls)
		
	def test_run_database_already_exists_withlist(self):
		actual = RunBackup(self.type2, self.mock_study_4, self.database_2, self.database_2, self.root, self.mock_make_bucket_ifnone, self.mock_get_study, self.mock_lane_for_study, self.do_sync)
		actual.run()
		calls = [call(self.database_2,self.database_2,self.root,self.output_file),call().boto3_upload(self.mock_lane_1[0]),call().boto3_upload(self.mock_lane_3[0]),call().boto3_upload(self.mock_lane_3[1])]
		self.do_sync.assert_has_calls(calls)
		
	def test_run_database_study_is_none_withlist(self):
		actual = RunBackup(self.type2,self.mock_study_3, self.database_3, self.database_3, self.root, self.mock_make_bucket_ifnone, self.mock_get_study, self.mock_lane_for_study, self.do_sync)
		actual.run()
		self.do_sync.assert_not_called()
		
		
if __name__ == '__main__':
        unittest.main()
        

