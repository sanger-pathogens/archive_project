from archive_project.MakeBucketIfNone import MakeBucketIfNone

def make_bucket_ifnone_factory(bucket_name):
	MB = MakeBucketIfNone(bucket_name)
	return MB.create_bucket()

	
