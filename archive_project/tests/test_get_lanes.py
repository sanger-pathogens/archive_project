import unittest
from unittest import mock
from unittest.mock import mock_open, patch, Mock
from archive_project import get_lanes as GL


class TestGet_lanes(unittest.TestCase):

	def test_pf_data(self):
		
		#for study that exists 
		data_list = b"""/lustre/scratch118/infgen/pathogen/pathpipe/prokaryotes/seq-pipelines/viral/metagenome/TRACKING/5547/ICUVIRAL7690100/SLX/22628838/27984_4#1\n
		/lustre/scratch118/infgen/pathogen/pathpipe/prokaryotes/seq-pipelines/viral/metagenome/TRACKING/5547/ICUVIRAL7690101/SLX/22628850/27984_4#2\n 
		/lustre/scratch118/infgen/pathogen/pathpipe/prokaryotes/seq-pipelines/viral/metagenome/TRACKING/5547/ICUVIRAL7690102/SLX/22628862/27984_4#3\n
		/lustre/scratch118/infgen/pathogen/pathpipe/prokaryotes/seq-pipelines/viral/metagenome/TRACKING/5547/ICUVIRAL7690103/SLX/22628874/27984_4#4\n"""
		with mock.patch('archive_project.get_lanes.check_output', return_value=data_list) as co:
			lane_class = GL.get_lanes("study")
			actual = lane_class.pf_data()
		co.assert_called_once_with(['pf', 'data', '-t', 'study', '-i', 'study']) #check_output called correctly 
		expected = data_list.decode('ascii').splitlines() 
		self.assertEqual(expected,actual) #output of function as expected
		
		#For study that doesn't exits or had no data
		with mock.patch('archive_project.get_lanes.check_output', return_value=b'') as co:
			lane_class = GL.get_lanes("study")
			actual = lane_class.pf_data()
		self.assertEqual(None,actual) #output as expected 
		
if __name__ == '__main__':
        unittest.main()