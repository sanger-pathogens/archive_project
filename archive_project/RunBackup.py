from archive_project.dependencies import make_bucket_ifnone_factory
from archive_project.GetLanes import get_lanes
from archive_project.GetStudies import get_studies
from archive_project.DoUpload import DoUpload

class RunBackup:
	'''Runs modules in correct order'''
	def __init__(self,run_type, run_id, database, bucket_name, data_root, make_bucket_ifnone_factory=make_bucket_ifnone_factory, 
		get_study_names=get_studies, get_lane=get_lanes, sync_2s3=DoUpload, output_file="failed_uploads.txt"):
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
		'''Makes bucket if it doesnt already exist. Reads study names if type was file. Gets the lanes for 
		each of the studies and uploads the files for each lane'''
		self.make_bucket_ifnone_factory(self.bucket_name)
		if self.run_type=='file':
			studies = self.get_study_names(self.run_id) 
		elif self.run_type=='studies':
			studies = self.run_id
		else: 
			print("Invalid value for 'type'\n Value must be one of these values: file, studies")
			return None 
		if studies is not None:  
			syncer = self.sync_2s3(self.database, self.bucket_name, self.data_root, self.output_file)
			for study in studies: 
				data = self.get_lane(study)
				if data is not None:  
					for path in data:
						syncer.boto3_upload(path)

#Need sync option 
