import boto3
from botocore.exceptions import ClientError
import logging 


class MakeBucketIfNone:
	'''Checks if a bucket with the name that user has specified already exists and if not creates one'''
	def __init__(self, bucket_name):
		self.bucket_name = bucket_name
				
	def check_exist(self):
		'''Checks the creation date of the bucket, if None then bucket doesn't exist 
		and return false. Return True if bucket does exist'''
		s3 = boto3.resource("s3", endpoint_url="https://cog.sanger.ac.uk",)
		if s3.Bucket(self.bucket_name).creation_date is None: 
			return False 
		else:
			return True 
	
	def create_bucket(self, region=None):
		"""Create an S3 bucket in a specified region if the bucket doesn't already exist

		If a region is not specified, the bucket is created in the S3 default
		region (us-east-1).

		:param bucket_name: Bucket to create
		:param region: String region to create bucket in, e.g., 'us-west-2'
		:return: True if bucket created, else False
		"""
		if self.check_exist() == False:
			print(self.bucket_name)
			try: 
				s3_client = boto3.client('s3',endpoint_url="https://cog.sanger.ac.uk")
				s3_client.create_bucket(Bucket=self.bucket_name)
			except ClientError as e:
				logging.error(e)
				print('New bucket, {}, failed to be created'.format(self.bucket_name))
				return False
			print('New bucket created:', self.bucket_name)
			return True
		
		else: 
			print('{} bucket already exists'.format(self.bucket_name))
			return True 


