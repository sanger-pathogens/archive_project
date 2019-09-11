from archive_project.bucket_check import bucket_check
from archive_project.get_studies import get_studies
from archive_project.get_lanes import get_lanes
from archive_project.get_files import get_files 


class run_backup:

	def __init__(self, database):
		self.database = database
	
		
	def run(self): 
		
		#Find if bucket already exists on s3 for this database. If not create one 
		find_bucket = bucket_check(self.database) 
		find_bucket.create_bucket()
		
		#Get all studies associated with this database
		study_find = get_studies(self.database)
		studies = study_find.read_studies()
		
		#If there are studies then find all lanes for each study
		if studies is not None:   
			for study in studies: 
				lane_find = get_lanes(study) #Find paths to the data for each lane within the study 
				data = lane_find.pf_data()
				if data is not None: #Check data exists for the study 
					for path in data: #NOT FINISHED 
						print('up to path') 
						#file_find = get_files(path) 
						#output rsync folder and then put into function to backup 
		else: 
			return None #Error message will have been printed, telling user no studies associated 
			
