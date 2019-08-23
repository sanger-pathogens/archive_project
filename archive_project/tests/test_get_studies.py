import unittest
from get_studies import Get_studies

class TestGet_studies(unittest.TestCase):
	
	def setUp(self):
		self.database1 = 'prokaryotes'
		self.database2 = 'PROKARYOTES'
		self.database3 = 'fake'
		self.prok_path = '/nfs/pathnfs05/conf/prokaryotes/prokaryotes.ilm.studies'
		
	def tearDown(self):
		pass
	
	def test_make_path(self):
		self.assertEqual(Get_studies.make_path(self.database1),self.prok_path) #check correct path made
		self.assertEqual(Get_studies.make_path(self.database2),self.prok_path) #check any uppercase works
		

	def test_read_studies(self):
		self.assertIsNotNone(Get_studies.read_studies(self.database1))
		self.assertIsNotNone(Get_studies.read_studies(self.database2))
		self.assertIsNone(Get_studies.read_studies(self.database3)) #check fake database doesn't work
		with self,assertRaises(TypeError):
			Get_studies.read_studies(2)

if __name__ == '__main__':
    unittest.main()
