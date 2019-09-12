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
		
	def make_s3path(self, data_path):
		#path_root = str('../../../../Documents/lustre/scratch118/infgen/pathogen/pathpipe/' + self.database + '/seq-pipelines/') ### Need to remove 
		path_root = str('/lustre/scratch118/infgen/pathogen/pathpipe/' + self.database + '/seq-pipelines/')
		s3_path = str('s3://' + self.database + '/' + data_path.replace(path_root,'') )
		if s3_path == str('s3://' + self.database + '/' + data_path):
			print(data_path, 'Data not from specified database or is invalid path')  
			return None 
		else:
			return s3_path
		
	def exclusions(self, dirs, files):
		dirs[:] = [d for d in dirs if not d.endswith('_tmp_files')]
		ext = ['.fastq.gz','.bam','.sam']
		files[:] = [f for f in files if not f.endswith(tuple(ext))]
		return dirs, files 
		
	def get_filepaths(self):
		file_paths = []
		for subdir, dirs, files in os.walk(self.path):
			print('output',self.exclusions(dirs, files))
			dirs, files = self.exclusions(dirs, files)
			for file in files:
				full_path = os.path.join(subdir, file)
				file_paths.append(full_path)
		return file_paths 
		
	def boto3_upload(self):
		session = boto3.Session()
		s3 = session.resource('s3', endpoint_url="https://cog.sanger.ac.uk")
		bucket = s3.Bucket(self.database)
		file_paths = self.get_filepaths()
		print('file_paths =',file_paths)
		failed = []
		for full_path in file_paths:
			s3_path = self.make_s3path(full_path)
			if s3_path is not None:
				print('run',s3_path)
				with open(full_path, 'rb') as data:
						bucket.put_object(Key=s3_path, Body=data)
			else: failed.append(full_path)
		return failed
		
'''
DS = do_sync('../../../../Documents/lustre/scratch118/infgen/pathogen/pathpipe/prokaryotes/seq-pipelines/','prokaryotes')
#DS = do_sync('/lustre/scratch118/infgen/pathogen/pathpipe/prokaryotes/seq-pipelines/','prokaryotes')
DS.boto3_upload()
'''

