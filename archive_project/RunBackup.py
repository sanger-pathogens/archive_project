from archive_project.dependencies import make_bucket_ifnone_factory
from archive_project.GetLanes import get_lanes
from archive_project.GetStudies import get_studies
from archive_project.DoUpload import DoUpload


class RunBackup:
	'''Runs modules in correct order'''
	def __init__(self, study_names, database, bucket_name, data_root,
				 make_bucket_ifnone_factory=make_bucket_ifnone_factory,
				 get_study_names=get_studies, get_lane=get_lanes, uploader=DoUpload, output_file="output.txt",
				 upload_mode='sync'):
		self.study_names = study_names
		self.database = database
		self.bucket_name = bucket_name
		self.data_root = data_root
		self.make_bucket_ifnone_factory = make_bucket_ifnone_factory
		self.get_study_names = get_study_names
		self.get_lane = get_lane
		self.uploader = uploader
		self.output_file = output_file
		self.mode = upload_mode.lower()

	def run(self):
		'''Makes bucket if it doesnt already exist. Reads study names if type was file. Gets the lanes for
		each of the studies and uploads the files for each lane'''
		f =  open(self.output_file, "a+")
		bucket_message = self.make_bucket_ifnone_factory(self.bucket_name)
		print(bucket_message)
		f.write(bucket_message)
		studies, studies_message = self.get_study_names(self.study_names)
		f.write(studies_message)
		f.close()
		upload = self.uploader(self.database, self.bucket_name, self.data_root,self.output_file)
		for study in studies:
			lanes, lanes_message = self.get_lane(study)
			f.write(lanes_message)
			for lane in lanes:
				if self.mode == 'upload':
					upload.boto3_upload(lane)
				elif self.mode == 'sync':
					upload.s3_sync(lane)
				else:
					f = open(self.output_file, "a+")
					f.write(self.mode, ' is not a valid mode. (must be "upload" or "sync")')
					f.close()