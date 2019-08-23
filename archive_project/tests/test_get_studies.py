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
                self.assertIsNotNone(self.database1.read_studies())
                self.assertIsNotNone(self.database2.read_studies())
                self.assertIsNone(self.database3.read_studies()) #check fake database doesn't work


if __name__ == '__main__':
    unittest.main()
