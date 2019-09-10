#Take data path 
#Retain directory strucure below /lustre/scratch118/infgen/pathogen/pathpipe/<tracking_database>/seq-pipelines/
#Upload files if they don't already exist 
import boto3
import os
import subprocess

#/lustre/scratch118/infgen/pathogen/pathpipe/prokaryotes/seq-pipelines/Salmonella/enterica_subsp_enterica_serovar_Typhi_str_Ty2/TRACKING/5798/4316STDY6559668/SLX/17718553/20953_1#1

class do_sync: 
	
	def __init__(self, path, database):
		self.path = path
		self.database = database
		
	def make_s3path(self,path):
		path_root = str('/lustre/scratch118/infgen/pathogen/pathpipe/' + self.database + '/seq-pipelines/')
		s3_path = str('s3://' + self.database + '/' + path.replace(path_root,'') )
		return s3_path
		
	def boto3_upload(self):
		#upload to s3 using boto3
		session = boto3.Session()
		s3 = session.resource('s3', endpoint_url="https://cog.sanger.ac.uk")
		bucket = s3.Bucket(self.database)
		for subdir, dirs, files in os.walk(self.path):
			for file in files:
				full_path = os.path.join(subdir, file)
				s3_path = self.make_s3path(full_path)
				with open(full_path, 'rb') as data:
					bucket.put_object(Key=s3_path, Body=data)
		
	def aws_sync_folder(self, exclude1, exclude2, exclude3, exclude4):
		
		s3_path = self.make_s3path()
		subprocess.call(['aws', 's3', 'sync', self.path, s3_path, '--dryrun', '--exclude', exclude1,'--exclude', exclude2, '--exclude', exclude3, '--exclude', exclude4])
	
'''	
DS = do_sync('fake_path/fake1/fake2/','fake_bucket')
DS.boto3_upload()
'''
