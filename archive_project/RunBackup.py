from archive_project.dependencies import make_bucket_ifnone_factory, get_studies_factory, do_sync_factory 
from archive_project.GetLanes import get_lanes

class RunBackup:

	def __init__(self,database, make_bucket_ifnone_factory=make_bucket_ifnone_factory, get_studies_factory=get_studies_factory, get_lane=get_lanes, do_sync_factory=do_sync_factory):
		self.database = database
		self.make_bucket_ifnone_factory = make_bucket_ifnone_factory
		self.get_studies_factory = get_studies_factory
		self.get_lane = get_lane
		self.do_sync_factory = do_sync_factory
			
	def run(self): 
		self.make_bucket_ifnone_factory(self.database)
		studies = self.get_studies_factory(self.database) #get all studies for a database
		if studies is not None:  #If there are studies then find all lanes for each study
			for study in studies: 
				print(study)
				data = self.get_lane(study)
				print(data)
				if data is not None: #Check data exists for the study 
					for path in data: #Upload files that meet criteria for each path
						self.do_sync_factory(self.database,path)
						

	
