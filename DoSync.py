import os 
from subprocess import Popen, PIPE, STDOUT
from os import path
import argparse
import pandas as pd

class DoSync:
	
	def __init__(self, database, bucket_name, data_root, output_file):
		self.database = database 
		self.bucket_name = bucket_name 
		self.data_root = data_root
		self.output_file = output_file 
		
	def runrealcmd(command):
		'''Run command in bash and wait until done to run the next one'''
		print(str(command))
		process = Popen(command, stdout=PIPE, shell=True, stderr=STDOUT, bufsize=1, close_fds=True)
		for line in iter(process.stdout.readline, b''):
			print(line.rstrip().decode('utf-8'))
		process.stdout.close()
		process.wait()
		return process.returncode
	
#sync to s3
df['return_code'] = df['path'].apply(lambda x: runrealcmd('s3cmd --verbose --no-preserve --no-check-md5 sync ' + x + ' s3://archive/ --progress')) 

