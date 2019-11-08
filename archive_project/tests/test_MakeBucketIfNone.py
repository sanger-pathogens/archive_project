import unittest
from unittest import mock
from unittest.mock import mock_open, patch, Mock, MagicMock, call
from archive_project import MakeBucketIfNone as BC
import boto3
from botocore.exceptions import ClientError


class TestMakeBucketIfNone(unittest.TestCase):

    def setUp(self):
        self.bucket_name = 'bucket_name'
        self.bucket = MagicMock()
        self.s3 = MagicMock()
        self.s3_client = MagicMock()
        with patch("archive_project.MakeBucketIfNone.open".format(__name__), create=True) as _file1:
            self.BC_class = BC.MakeBucketIfNone(self.bucket_name)

    def tearDown(self):
        pass

    def test_check_existing_bucket(self):
        with patch("boto3.resource", return_value=self.s3) as resource:
            self.s3.Bucket.return_value = self.bucket
            self.bucket.creation_date = "some date"
            actual = self.BC_class.check_exist()
        resource.assert_called_once_with("s3", endpoint_url="https://cog.sanger.ac.uk", )
        self.s3.Bucket.assert_called_once_with(self.bucket_name)
        self.assertEqual(True, actual)

    def test_check_of_new_bucket(self):
        with patch("boto3.resource", return_value=self.s3) as resource:
            self.s3.Bucket.return_value = self.bucket
            self.bucket.creation_date = None
            actual = self.BC_class.check_exist()
        resource.assert_called_once_with("s3", endpoint_url="https://cog.sanger.ac.uk", )
        self.s3.Bucket.assert_called_once_with(self.bucket_name)
        self.assertEqual(False, actual)

    def test_create_new_bucket(self):
        with patch("archive_project.MakeBucketIfNone.MakeBucketIfNone.check_exist", return_value=False) as check_func:
            with patch("boto3.client", return_value=self.s3_client) as client:
                self.s3_client.create_bucket.return_value = self.bucket
                actual = self.BC_class.create_bucket()
        client.assert_called_once_with('s3', endpoint_url="https://cog.sanger.ac.uk")
        check_func.assert_called_once_with()
        self.s3_client.create_bucket.assert_called_once_with(Bucket=self.bucket_name)
        self.assertEqual(('New bucket created: {}\n'.format(self.bucket_name)),actual)

    def test_try_creating_existing_bucket(self):
        with patch("archive_project.MakeBucketIfNone.MakeBucketIfNone.check_exist", return_value=True) as check_func:
            actual = self.BC_class.create_bucket()
        check_func.assert_called_once_with()
        self.assertEqual(('{} bucket already exists\n'.format(self.bucket_name)),actual)

    def test_try_creating_get_error(self):
        with patch("archive_project.MakeBucketIfNone.MakeBucketIfNone.check_exist", return_value=False) as check_func:
            with patch("boto3.client", side_effect=ClientError({'Error': {'Code': 'ResourceInUseException'}},
                                                               'create_stream')) as client:
                self.s3_client.create_bucket.return_value = self.bucket
                actual = self.BC_class.create_bucket()
        client.assert_called_once_with('s3', endpoint_url="https://cog.sanger.ac.uk")
        check_func.assert_called_once_with()
        self.assertEqual(("New bucket, {}, failed to be created\n".format(self.bucket_name)),actual)

if __name__ == '__main__':
    unittest.main()
