from archive_project.MakeBucketIfNone import MakeBucketIfNone
from archive_project.DoSync import DoSync


def make_bucket_ifnone_factory(bucket_name):
	MB = MakeBucketIfNone(bucket_name)
	return MB.create_bucket()

def do_sync_factory(database, bucket_name, root, path, output_file):
	DS = DoSync(database, bucket_name, root, output_file)
	return DS.boto3_upload(path)
	
