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
		
	def make_s3path(self):
		path_root = str('/lustre/scratch118/infgen/pathogen/pathpipe/' + self.database + '/seq-pipelines/')
		s3_path = str('s3://' + self.database + '/' + self.path.replace(path_root,'') )
		return s3_path
		
	def sync_folder(self, exclude1, exclude2, exclude3, exclude4):
		
		s3_path = make_s3path()
	
		subprocess.call(['aws', 's3', 'sync', self.path, s3_path, '--dryrun', '--exclude', exclude1,'--exclude', exclude2, '--exclude', exclude3, '--exclude', exclude4])
		
'''		
ds = do_sync('../test', 'test')
ds.sync_folder('*.fastq.gz','*.bam','*_tmp_files/','*.sam')
'''

'''
#filter the files and upload to s3 using command similar to rsync 

class get_files: 

        def __init__(self, data_path):
                self.data_path = data_path
				
        def rsync_folder(self, exclude1, exclude2, exclude3, exclude4):
				
				
				str(self.data_path + '_temp')
				url = 'abcdc.com'
				print(url.replace('.com',''))
				
				
				s3_path = #create path for where to upload s3 data to 

                boto-rsync --glob " " -n /local/path/ s3://bucketname/remote/path/
'''	

'''
directory = input('Directory to archive:')
cf = get_files(directory.strip("'"))
cf.rsync_folder('*.fastq.gz','*.bam','*_tmp_files/','*.sam')

#think about destination of tmp folder for it so be synced with correct hierarcy 


def upload_files(path):
    session = boto3.Session(
        aws_access_key_id='YOUR_AWS_ACCESS_KEY_ID',
        aws_secret_access_key='YOUR_AWS_SECRET_ACCESS_KEY_ID',
        region_name='YOUR_ACCOUNT_REGION'
    )
    s3 = session.resource('s3')
    bucket = s3.Bucket('YOUR_BUCKET_NAME')

    for subdir, dirs, files in os.walk(path):
        for file in files:
            full_path = os.path.join(subdir, file)
            file_mime = mimetypes.guess_type(file)[0] or 'binary/octet-stream'
            with open(full_path, 'rb') as data:
                bucket.put_object(Key=full_path[len(path)+1:], Body=data, ContentType=file_mime)

if __name__ == "__main__":
    upload_files('/path/to/your/folder')
'''
