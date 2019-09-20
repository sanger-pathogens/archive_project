from archive_project.MakeBucketIfNone import MakeBucketIfNone
from archive_project.GetStudies import GetStudies
from archive_project.DoSync import DoSync


def make_bucket_ifnone_factory(database):
	MB = MakeBucketIfNone(database)
	return MB.create_bucket()
	
def get_studies_factory(database):
	GS = GetStudies(database)
	return GS.read_studies()
	
def do_sync_factory(database,path):
	dS = DoSync(database)
	return DS.boto3_upload(path)
	
	

