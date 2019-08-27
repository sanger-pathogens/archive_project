import unittest
from get_studies import get_studies

class TestGet_studies(unittest.TestCase):

	def setUp(self):
		self.database1 = get_studies('prokaryotes')
		self.database2 = get_studies('PROKARYOTES')
		self.database3 = get_studies('fake')
		self.prok_path = '/nfs/pathnfs05/conf/prokaryotes/prokaryotes.ilm.studies'
	
	def tearDown(self):
		pass

	def test_make_path(self):
		self.assertEqual(self.database1.make_path(),self.prok_path) #check correct path made
		self.assertEqual(self.database2.make_path(),self.prok_path) #check any uppercase works
		

	def test_read_studies(self):
		#opening the file needs to be mocked 	
		self.assertIsNotNone(self.database1.read_studies())
		self.assertIsNotNone(self.database2.read_studies())
		self.assertIsNone(self.database3.read_studies()) #check fake database doesn't work


	def test_read_studies(self):
		#test valid file 
		

if __name__ == '__main__':
	unittest.main()

'''
def test_open_json_file(self):
    # test valid JSON
    read_data = json.dumps({'a': 1, 'b': 2, 'c': 3})
    mock_open = mock.mock_open(read_data=read_data)
    with mock.patch('__builtin__.open', mock_open):
        result = open_json_file('filename')
    self.assertEqual({'a': 1, 'b': 2, 'c': 3}, result)
    # test invalid JSON
    read_data = ''
    mock_open = mock.mock_open(read_data=read_data)
    with mock.patch("__builtin__.open", mock_open):
        with self.assertRaises(ValueError) as context:
            open_json_file('filename')
        self.assertEqual(
            'filename is not valid JSON.', str(context.exception))
    # test file does not exist
    with self.assertRaises(IOError) as context:
        open_json_file('null')
    self.assertEqual(
        'null does not exist.', str(context.exception))
'''
