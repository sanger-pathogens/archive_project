import unittest
from moto import mock_s3
from unittest import mock
from unittest.mock import mock_open, patch, Mock, MagicMock,call
from archive_project import bucket_check as BC
import boto3


class TestBucket_check(unittest.TestCase):
	
	def setUp(self):
		self.bucketname = 'bucket_name'
		self.bucket = MagicMock()
		self.s3 = MagicMock()
		self.s3_client = MagicMock()
		
	def tearDown(self):
		pass 
		
	def test_check_existing_bucket(self):
		s3, bucket = self.mock_variables(s3=True, bucket=True)
		with patch("boto3.resource", return_value=s3) as resource:
			s3.Bucket.return_value = bucket
			bucket.creation_date = "some date"
			BC_class = BC.bucket_check(self.bucketname)
			actual = BC_class.check_exist()
		resource.assert_called_once_with("s3", endpoint_url="https://cog.sanger.ac.uk",) #check_output called correctly 
		s3.Bucket.assert_called_once_with(self.bucketname)
		self.assertEqual(True,actual) #output of function as expected
			
	def test_check_of_new_bucket(self):
		s3, bucket = self.mock_variables(s3=True, bucket=True)
		with patch("boto3.resource", return_value=s3) as resource:
			s3.Bucket.return_value = bucket
			bucket.creation_date = None 
			BC_class = BC.bucket_check(self.bucketname)
			actual = BC_class.check_exist()
		resource.assert_called_once_with("s3", endpoint_url="https://cog.sanger.ac.uk",)
		s3.Bucket.assert_called_once_with(self.bucketname)
		self.assertEqual(False,actual)
		
	def test_create_new_bucket_noregion(self):
		bucket, s3_client = self.mock_variables(bucket=True,s3_client=True)
		with patch("archive_project.bucket_check.bucket_check.check_exist", return_value=False) as check_func:
			with patch("boto3.client", return_value=s3_client) as client:
				s3_client.create_bucket.return_value = bucket
				BC_class = BC.bucket_check(self.bucketname)
				actual = BC_class.create_bucket()
		client.assert_called_once_with('s3',endpoint_url="https://cog.sanger.ac.uk")
		s3_client.create_bucket.assert_called_once_with(Bucket=self.bucketname)
		self.assertEqual(True,actual)
		
	def test_create_new_bucket_withregion(self):
		bucket, s3_client = self.mock_variables(bucket=True,s3_client=True)
		with patch("archive_project.bucket_check.bucket_check.check_exist", return_value=False) as check_func:
			with patch("boto3.client", return_value=s3_client) as client:
				s3_client.create_bucket.return_value = bucket
				BC_class = BC.bucket_check(self.bucketname)
				actual = BC_class.create_bucket('region')
		client.assert_called_once_with('s3', region_name='region',endpoint_url="https://cog.sanger.ac.uk")
		s3_client.create_bucket.assert_called_once_with(Bucket=self.bucketname, CreateBucketConfiguration={'LocationConstraint': 'region'})
		self.assertEqual(True,actual)
		
	def test_try_creating_existing_bucket(self):
		with patch("archive_project.bucket_check.bucket_check.check_exist", return_value=True) as check_func:
			BC_class = BC.bucket_check(self.bucketname)
			actual = BC_class.create_bucket()
		self.assertEqual(True,actual)
		
	

	
if __name__ == '__main__':
	unittest.main()
	

