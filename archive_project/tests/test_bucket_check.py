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
		with patch("boto3.resource", return_value=self.s3) as resource:
			self.s3.Bucket.return_value = self.bucket
			self.bucket.creation_date = "some date"
			BC_class = BC.bucket_check(self.bucketname)
			actual = BC_class.check_exist()
		resource.assert_called_once_with("s3", endpoint_url="https://cog.sanger.ac.uk",) #check_output called correctly 
		self.s3.Bucket.assert_called_once_with(self.bucketname)
		self.assertEqual(True,actual) #output of function as expected
			
	def test_check_of_new_bucket(self):
		with patch("boto3.resource", return_value=self.s3) as resource:
			self.s3.Bucket.return_value = self.bucket
			self.bucket.creation_date = None 
			BC_class = BC.bucket_check(self.bucketname)
			actual = BC_class.check_exist()
		resource.assert_called_once_with("s3", endpoint_url="https://cog.sanger.ac.uk",)
		self.s3.Bucket.assert_called_once_with(self.bucketname)
		self.assertEqual(False,actual)
		
	def test_create_new_bucket_noregion(self):
		with patch("archive_project.bucket_check.bucket_check.check_exist", return_value=False) as check_func:
			with patch("boto3.client", return_value=self.s3_client) as client:
				self.s3_client.create_bucket.return_value = self.bucket
				BC_class = BC.bucket_check(self.bucketname)
				actual = BC_class.create_bucket()
		client.assert_called_once_with('s3',endpoint_url="https://cog.sanger.ac.uk")
		check_func.assert_called_once_with()
		self.s3_client.create_bucket.assert_called_once_with(Bucket=self.bucketname)
		self.assertEqual(True,actual)
		
	def test_create_new_bucket_withregion(self):
		with patch("archive_project.bucket_check.bucket_check.check_exist", return_value=False) as check_func:
			with patch("boto3.client", return_value=self.s3_client) as client:
				self.s3_client.create_bucket.return_value = self.bucket
				BC_class = BC.bucket_check(self.bucketname)
				actual = BC_class.create_bucket('region')
		client.assert_called_once_with('s3', region_name='region',endpoint_url="https://cog.sanger.ac.uk")
		check_func.assert_called_once_with()
		self.s3_client.create_bucket.assert_called_once_with(Bucket=self.bucketname, CreateBucketConfiguration={'LocationConstraint': 'region'})
		self.assertEqual(True,actual)
		
	def test_try_creating_existing_bucket(self):
		with patch("archive_project.bucket_check.bucket_check.check_exist", return_value=True) as check_func:
			BC_class = BC.bucket_check(self.bucketname)
			actual = BC_class.create_bucket()
		check_func.assert_called_once_with()
		self.assertEqual(True,actual)
		
	

	
if __name__ == '__main__':
	unittest.main()
	

