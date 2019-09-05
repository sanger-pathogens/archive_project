import unittest
from unittest import mock
from unittest.mock import mock_open, patch, Mock 
from archive_project import bucket_check as BC

'''
class TestBucket_check(unittest.TestCase):

	def test_check_exist(self):
		
		with mock.patch('archive_project.bucket_check.s3.Bucket(self.bucket_name).creation_date',return_value=None) as cd: #?????
			BC_class = BC.check_bucket("name")
			actual = BC_class.check_exist()
		self.assertEqual(False,actual)
		
		with mock.patch('archive_project.bucket_check.s3.Bucket(self.bucket_name).creation_date',return_value='date') as cd: #?????
			BC_class = BC.check_bucket("name")
			actual = BC_class.check_exist()
		self.assertEqual(True,actual)
		
	#def test_create_bucket(self):

if __name__ == '__main__':
	unittest.main()
'''
