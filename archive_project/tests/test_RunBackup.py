import unittest
from unittest import mock
from unittest.mock import mock_open, patch, Mock, MagicMock
from archive_project import DoSync as DS
import os
from testfixtures import TempDirectory
from archive_project.RunBackup import RunBackup

class TestRunBackup(unittest.TestCase):
	
	def setUp(self):
		self.database_1 = 'database1'
		self.database_2 = 'database2'
		self.database_3 = 'database3'
		self.mock_study_1 = ['mock_study_1']
		self.mock_study_2 = ['mock_study_2']
		self.mock_study_3 = None
		self.mock_lane_1 = ['mock_lane_1']
		self.mock_lane_2 = None
		self.do_sync_factory = Mock() 
		
	def tearDown(self):
		pass 

	def mock_make_bucket_ifnone(self,database):
		if database == self.database_1:
			return True
		if database == self.database_2 or database ==self.database_3:
			return False
		
	def mock_get_study(self,database):
		if database == self.database_1:
			return self.mock_study_1
		if database == self.database_2:
			return self.mock_study_2
		if database == self.database_3:
			return self.mock_study_3
			
	def mock_lane_for_study(self,study):
		if study == self.mock_study_1[0] or study == self.mock_study_2[0]:
			return self.mock_lane_1
		if study == self.mock_study_3: #fake study (or study=None) and lanes is None
			return self.mock_lane_2
			
	def mock_sync_for_study(self,database,path):
		if study == self.mock_study_1:
			return []
		if study == self.mock_study_2 or study == self.mock_study_3:
			return [fake_failed1,fake_failed_2]
			
	def test_run_make_new_database(self):
		actual = RunBackup(self.database_1, self.mock_make_bucket_ifnone, self.mock_get_study, self.do_sync_factory, get_lane=self.mock_lane_for_study)
		actual.run()
		self.do_sync_factory.assert_called_once_with(self.database_1,self.mock_lane_1[0])
		
	def test_run_database_already_exists(self):
		actual = RunBackup(self.database_2, self.mock_make_bucket_ifnone, self.mock_get_study, self.do_sync_factory, get_lane=self.mock_lane_for_study)
		actual.run()
		self.do_sync_factory.assert_called_once_with(self.database_2,self.mock_lane_1[0])
		
	def test_run_database_study_is_none(self):
		actual = RunBackup(self.database_3, self.mock_make_bucket_ifnone, self.mock_get_study, self.do_sync_factory, get_lane=self.mock_lane_for_study)
		actual.run()
		self.do_sync_factory.assert_not_called()
		
		
if __name__ == '__main__':
        unittest.main()
        
