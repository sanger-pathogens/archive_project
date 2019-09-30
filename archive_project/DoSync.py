#Take data path 
#Retain directory strucure below /lustre/scratch118/infgen/pathogen/pathpipe/<tracking_database>/seq-pipelines/
#Upload files if they don't already exist 
import boto3
import os
import subprocess


class DoSync: 
	
	def __init__(self, database, bucket_name, data_root):
		self.database = database
		self.bucket_name = bucket_name 
		self.data_root = data_root
		self.failed_file = open("failed_uploads_%s.txt"%self.database,"w+") #File for database to write any failed uploads to 
		
	def make_s3path(self, data_path):
		s3_path = str('s3://' + self.bucket_name + '/' + data_path.replace(self.data_root,'') )
		if s3_path == str('s3://' + self.bucket_name + '/' + data_path):
			print(data_path, 'Data not from specified database or is invalid path')  
			return None 
		else:
			return s3_path
		
	def exclusions(self, dirs, files):
		dirs[:] = [d for d in dirs if not d.endswith('_tmp_files')]
		ext = ['.fastq.gz','.bam','.sam']
		files[:] = [f for f in files if not f.endswith(tuple(ext))]
		return dirs, files 
		
	def get_filepaths(self,data_path):
		file_paths = []
		for subdir, dirs, files in os.walk(data_path):
			print('output',self.exclusions(dirs, files))
			dirs, files = self.exclusions(dirs, files)
			for file in files:
				full_path = os.path.join(subdir, file)
				file_paths.append(full_path)
		return file_paths 
		
	def boto3_upload(self,data_path):
		session = boto3.Session()
		s3 = session.resource('s3', endpoint_url="https://cog.sanger.ac.uk")
		bucket = s3.Bucket(self.bucket_name)
		file_paths = self.get_filepaths(data_path)
		failed = []
		for full_path in file_paths:
			s3_path = self.make_s3path(full_path)
			if s3_path is not None:
				with open(full_path, 'rb') as data:
						bucket.put_object(Key=s3_path, Body=data)
			else: 
				failed.append(full_path)
				self.failed_file.write("%s\n" % full_path) #write any that failed to file 
		self.failed_file.close()
		return failed


