import subprocess

class GetStudies:
	
	def __init__(self, database):
		 self.database = database
		 
	#Create string of path to .ilm.studies file for specific database
	def make_path(self):
		return ('/nfs/pathnfs05/conf/' + str(self.database) +'/' +str(self.database) + '.ilm.studies')

	#Read studies from .ilm.studies file for database 
	def read_studies(self):
		path = self.make_path()
		#Test if path exists
		try: 
			with open(path) as f:
				studies = [line.rstrip('\n') for line in f] #read study names
				return studies
		except FileNotFoundError:
			print('Unknown Database:', self.database)
			return None 
