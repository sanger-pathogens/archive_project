import boto3
import os

class DoSync: 
	'''Uploads files in data_path to s3 as long as they don't fall in the
	exclusions criteria'''
	def __init__(self, database, bucket_name, data_root, output_file):
		self.database = database
		self.bucket_name = bucket_name 
		self.data_root = data_root
		self.failed_file = open(output_file,"w+")  
		
	def make_s3path(self, data_path):
		'''Generates the path for the data to be uploaded to on s3 by excluding the root the 
		user specifies they want removed and adds s3:://<bucket name> to the beggining'''
		s3_path = str('s3://' + self.bucket_name + '/' + data_path.replace(self.data_root,'') )
		if s3_path == str('s3://' + self.bucket_name + '/' + data_path):
			print(data_path, 'Data not from specified database or is invalid path')  
			return None 
		else:
			return s3_path
		
	def exclusions(self, dirs, files):
		'''Removes the data that doesn't need backed up'''
		dirs[:] = [d for d in dirs if not d.endswith('_tmp_files')]
		ext = ['.fastq.gz','.bam','.sam']
		files[:] = [f for f in files if not f.endswith(tuple(ext))]
		return dirs, files 
		
	def get_filepaths(self,data_path):
		'''Walks the directory for a given lane and returns all of the paths
		to files within it apart from those eliminated by exclusions'''
		file_paths = []
		for subdir, dirs, files in os.walk(data_path):
			print('output',self.exclusions(dirs, files))
			dirs, files = self.exclusions(dirs, files)
			for file in files:
				full_path = os.path.join(subdir, file)
				file_paths.append(full_path)
		return file_paths 
		
	def boto3_upload(self,dir_path):
		'''This does the work. Takes directory path. Uses get_filepaths to get all 
		filepaths in directory and exclude ones that meet criteria. For each of those 
		files create an s3 path for it to be stored at. Then upload each file to their 
		s3 path. If file fails write it to output file that user specifies.'''
		session = boto3.Session()
		s3 = session.resource('s3', endpoint_url="https://cog.sanger.ac.uk")
		bucket = s3.Bucket(self.bucket_name)
		file_paths = self.get_filepaths(dir_path)
		failed = []
		for full_path in file_paths:
			s3_path = self.make_s3path(full_path)
			if s3_path is not None:
				with open(full_path, 'rb') as data:
						bucket.put_object(Key=full_path.replace(self.data_root,'') , Body=data)
			else: 
				failed.append(full_path)
				self.failed_file.write("%s\n" % full_path) 
		self.failed_file.close()
		return failed


