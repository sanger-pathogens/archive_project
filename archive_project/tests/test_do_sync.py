import unittest
from unittest import mock
from unittest.mock import mock_open, patch, Mock
from archive_project import do_sync as DS

class TestDo_sync(unittest.TestCase):

	def test_make_s3path(self):
		
		test_path = '/lustre/scratch118/infgen/pathogen/pathpipe/prokaryotes/seq-pipelines/Salmonella/enterica_subsp_enterica_serovar_Typhi_str_Ty2/TRACKING/5798/4316STDY6559668/SLX/17718553/20953_1#1'
		database = 'prokaryotes'
		s3_path = 's3://prokaryotes/Salmonella/enterica_subsp_enterica_serovar_Typhi_str_Ty2/TRACKING/5798/4316STDY6559668/SLX/17718553/20953_1#1'
		sync_class = DS.do_sync(test_path,database)
		self.assertEqual(sync_class.make_s3path(),s3_path)
		
if __name__ == '__main__':
        unittest.main()
