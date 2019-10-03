from archive_project.dependencies import make_bucket_ifnone_factory, do_sync_factory 
from archive_project.GetLanes import get_lanes
from archive_project.GetStudies import get_studies

class RunBackup:

	def __init__(self,run_type, run_id, database, bucket_name, data_root, make_bucket_ifnone_factory=make_bucket_ifnone_factory, get_study_names=get_studies, get_lane=get_lanes, sync_2s3=do_sync_factory, output_file="failed_uploads.txt"):
		self.run_type = run_type
		self.run_id = run_id
		self.database = database
		self.bucket_name = bucket_name 
		self.data_root = data_root
		self.make_bucket_ifnone_factory = make_bucket_ifnone_factory
		self.get_study_names= get_study_names
		self.get_lane = get_lane
		self.sync_2s3 = sync_2s3
		self.output_file = output_file
			
	def run(self): 
		self.make_bucket_ifnone_factory(self.bucket_name)
		if self.run_type=='file':
			studies = self.get_study_names(self.run_id) #get all studies for a database
		elif self.run_type=='studies':
			studies = self.run_id
		else: 
			print("Invalid value for 'type'\n Value must be one of these values: file, studies")
			return None 
		if studies is not None:  #If there are studies then find all lanes for each study
			for study in studies: 
				data = self.get_lane(study)
				print(data)
				if data is not None: #Check data exists for the study 
					for path in data: #Upload files that meet criteria for each path
						self.sync_2s3(self.database, self.bucket_name, self.data_root, path, self.output_file)
						
