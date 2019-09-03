from archive_project.get_studies import get_studies
from archive_project.get_lanes import get_lanes
from archive_project.get_files import get_files 


class run_backup:

	def __init__(self, database):
		self.database = database
		
	def run(self): 
		study_find = get_studies(self.database) #Get all studies associated with this database
		studies = study_find.read_studies()
		if studies is not None:  #If there are studies then find all lanes for each study 
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
			
