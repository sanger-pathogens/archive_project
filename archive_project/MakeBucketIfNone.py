import boto3
from botocore.exceptions import ClientError
import logging 


class MakeBucketIfNone:
	'''Checks if a bucket with the name that user has specified already exists and if not creates one'''
	def __init__(self, bucket_name):
		self.bucket_name = bucket_name
		
	def list_buckets(self):
		'''Not used. Generates a list of the current buckets'''
		# Create an S3 client
		s3 = boto3.client('s3',endpoint_url="https://cog.sanger.ac.uk")
		# Call S3 to list current buckets
		response = s3.list_buckets()
		# Get a list of all bucket names from the response
		buckets = [bucket['Name'] for bucket in response['Buckets']]
		for bucket in buckets:
				print(bucket)
				
	def check_exist(self):
		'''Checks the creation date of the bucket, if None then bucket doesn't exist 
		and return false. Return True if bucket does exist'''
		s3 = boto3.resource("s3", endpoint_url="https://cog.sanger.ac.uk",)
		if s3.Bucket(self.bucket_name).creation_date is None: 
			return False #Bucket has never been created 
		else:
			return True #Bucket already exists
	
	def create_bucket(self, region=None):
		"""Create an S3 bucket in a specified region if the bucket doesn't already exist

		If a region is not specified, the bucket is created in the S3 default
		region (us-east-1).

		:param bucket_name: Bucket to create
		:param region: String region to create bucket in, e.g., 'us-west-2'
		:return: True if bucket created, else False
		"""
		if self.check_exist() == False: #Bucket doesn't exist, create one 
			try: 
				if region is None: 
					s3_client = boto3.client('s3',endpoint_url="https://cog.sanger.ac.uk")
					s3_client.create_bucket(Bucket=self.bucket_name)
				else: 
					s3_client = boto3.client('s3', region_name=region,endpoint_url="https://cog.sanger.ac.uk")
					location = {'LocationConstraint': region}
					s3_client.create_bucket(Bucket=self.bucket_name, CreateBucketConfiguration=location)
			except ClientError as e:
				logging.error(e)
				print('New bucket, {}, failed to be created'.format(self.bucket_name))
				return False
			print('New bucket created:', self.bucket_name)
			return True
		
		else: 
			print('{} bucket already exists'.format(self.bucket_name))
			return True 


