import subprocess

#create temp rsync of data folder only containing required stuff, delete once archived 

class get_files: 

        def __init__(self, data_path):
                self.data_path = data_path

        def rsync_folder(self, exclude1, exclude2):
                new_path = str(self.data_path + '_temp')
                subprocess.call(['mkdir', new_path])
                subprocess.call(['rsync', '-avz', '--exclude', exclude1,'--exclude',exclude2, self.data_path, new_path])
                #NEED SOME WAY OF FINDING THE INTERMEDIATE FILES
		
'''		
directory = input('Directory to archive:')
cf = get_files(directory.strip("'"))
cf.rsync_folder('*.fastq.gz','*.bam')
'''
