import os
import boto3
from archive_project.RunCommand import runrealcmd

class DoUpload:

	'''Uploads files in data_path to s3 as long as they don't fall in the
	exclusions criteria'''
	def __init__(self, database, bucket_name, data_root, output_file):
		self.database = database
		self.bucket_name = bucket_name 
		self.data_root = data_root
		self.output_file = output_file

	def make_s3path(self, data_path):
		'''Generates the path for the data to be uploaded to on s3 by excluding the root the 
		user specifies they want removed and adds s3:://<bucket name> to the beggining'''
		s3_path = str('s3://' + self.bucket_name + '/' + data_path.replace(self.data_root,'') )
		test = str('s3://' + self.bucket_name + '/' + data_path)
		if not s3_path.endswith('/'):
			s3_path = s3_path + '/'
			test = str('s3://' + self.bucket_name + '/' + data_path + '/')
		if s3_path == test:
			print(data_path, 'Data not from specified database or is invalid path\n')
			return None 
		else:
			return s3_path
		
	def exclusions(self, dirs, files):
		'''Removes the data that doesn't need backed up'''
		dirs[:] = [d for d in dirs if not d.endswith('_tmp_files')]
		ext = ['.fastq.gz','.bam','.sam','.bam.bai']
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
		failed_file = open(self.output_file, "a+")
		session = boto3.Session()
		s3 = session.resource('s3', endpoint_url="https://cog.sanger.ac.uk")
		bucket = s3.Bucket(self.bucket_name)
		file_paths = self.get_filepaths(dir_path)
		failed = []
		for full_path in file_paths:
			s3_path = self.make_s3path(full_path)
			if s3_path is not None:
				try: 
					with open(full_path, 'rb') as data:
							bucket.put_object(Key=full_path.replace(self.data_root,'') , Body=data)
				except: 
					failed.append(full_path)
					failed_file.write("%s\nfile doesn't exist or failed to be uploaded \n" % full_path)
			else: 
				failed.append(full_path)
				failed_file.write("%s\nS3 path failed to be created\n" % full_path)
		failed_file.close()
		return failed
		
	def s3_sync(self,dir_path, command_runner = runrealcmd):
		'''use s3cmd sync, so files already uploaded aren't re-uploaded waisting comp time'''
		s3_path = self.make_s3path(dir_path)
		if s3_path is not None:
			command_runner('s3cmd --verbose --no-preserve --exclude="*/*.fastq.gz" --exclude="*/*.bam" --exclude="*/*.sam" --exclude="*/*.bam.bai" --no-check-md5 sync ' + str(dir_path) + ' ' + str(s3_path))
