from archive_project.bucket_check import bucket_check
from archive_project.get_studies import get_studies
from archive_project.get_lanes import get_lanes
from archive_project.do_sync import do_sync


class run_backup:

	def __init__(self, database):
		self.database = database
		self.failed_file = open("failed_uploads%s.txt"%self.database,"w+")
		
	def __init__(self, get_study, bucket_checker, get_lane):
		self.database = database
		self.failed_file = open("failed_uploads%s.txt"%self.database,"w+")
		
	def study(self):
		#Get list of studies for the database
		study_find = get_studies(self.database)
		return study_find.read_studies()
		
	def lanes(self,study):
		lane_find = get_lanes(study) #Find paths to the data for each lane within the study 
		data = lane_find.pf_data()
		
	def upload_study(self,study):
		self.lanes(study) #Get lanes
		if data is not None: #Check data exists for the study 
			for path in data: #Upload files that meet criteria for each path
				syncer = do_sync(path, self.database)
				failed = boto3_upload()
				for f in failed:
					self.failed_file.write("%s\n" % f) #write any that failed to file 
		else: 
			self.failed_file.write("No data associated with study %s\n"%study)
			
	def run(self): 
		find_bucket = BucketCheck(self.database) 
		find_bucket.create_bucket() #if bucket doesn't already exist for database then make one
		studies = self.study() #get all studies for a database
		#If there are studies then find all lanes for each study
		if studies is not None:   
			for study in studies: 
				self.failed_file.write("%s - files that failed to upload\n"%study)
				self.upload_study()
			self.failed_file.close()
			return True 
		else: 
			self.failed_file.write("No studies associated with database")
			self.failed_file.close()
			return None #Error message will have been printed, telling user no studies associated 
			
#change class to upper 
#dependency injection 
