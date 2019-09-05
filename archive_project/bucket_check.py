#Check if database has bucket on s3 already, if not create one 

import boto3
s3 = boto3.resource('s3')

   
class bucket_check:
	
	def __init__(self, bucket_name):
		 self.bucket_name = bucket_name
		 
	def check_exist(self):
		#check if bucket exists 
		print(s3.Bucket(self.bucket_name).creation_date)
		if s3.Bucket(self.bucket_name).creation_date is None: 
			return False 
		else: return True 
	
	def create_bucket(self, region=None):
		"""Create an S3 bucket in a specified region if the bucket doesn't already exist

		If a region is not specified, the bucket is created in the S3 default
		region (us-east-1).

		:param bucket_name: Bucket to create
		:param region: String region to create bucket in, e.g., 'us-west-2'
		:return: True if bucket created, else False
		"""
	
		if self.check_exist() == False:
			try: 
				if region is None: 
					s3_client = boto3.client('s3')
					s3_client.create_bucket(Bucket=self.bucket_name)
					print('1')
				else: 
					s3_client = boto3.client('s3', region_name=region)
					location = {'LocationConstraint': region}
					s3_client.create_bucket(Bucket=bucket_name, CreateBucketConfiguration=location)
					print('1')
			except ClientError as e:
				logging.error(e)
				print('New bucket, {}, failed to be created'.format(self.bucket_name))
				print('1')
				return False
			print('New bucket created:', self.bucket_name)
			return True
		
		else: 
			print('1')
			return True 
print('1')
bc = bucket_check('test')
bc.create_bucket()
