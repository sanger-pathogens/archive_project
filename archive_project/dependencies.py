from archive_project.MakeBucketIfNone import MakeBucketIfNone


def make_bucket_ifnone_factory(bucket_name, output_file):
    MB = MakeBucketIfNone(bucket_name, output_file)
    return MB.create_bucket()
