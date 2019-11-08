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
        s3 = boto3.resource("s3", endpoint_url="https://cog.sanger.ac.uk", )
        return s3.Bucket(self.bucket_name).creation_date is not None

    def create_bucket(self, region=None):
        """Create an S3 bucket in a specified region if the bucket doesn't already exist

		If a region is not specified, the bucket is created in the S3 default
		region (us-east-1).

		:param bucket_name: Bucket to create
		:param region: String region to create bucket in, e.g., 'us-west-2'
		:return: True if bucket created, else False
		"""
        if not self.check_exist():
            try:
                s3_client = boto3.client('s3', endpoint_url="https://cog.sanger.ac.uk")
                s3_client.create_bucket(Bucket=self.bucket_name)
                message=('New bucket created: {}'.format(self.bucket_name))
            except ClientError as e:
                logging.error(e)
                message=("New bucket, {}, failed to be created".format(self.bucket_name))
        else:
            message=('{} bucket already exists'.format(self.bucket_name))
        return message