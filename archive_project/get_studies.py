import subprocess

class get_studies:
	
	def __init__(self, database):
		 self.database = database.lower()
		 
	#Create string of path to .ilm.studies file for specific database
	def make_path(self):
		return ('/nfs/pathnfs05/conf/' + str(self.database) +'/' +str(self.database) + '.ilm.studies')

	#Read studies from .ilm.studies file for database 
	def read_studies(self):
		path = self.make_path()
		#Test if path exists
		try: 
			f = open(path)
		except FileNotFoundError:
			print('Unknown Database')
			return None 
		
		studies = [line.rstrip('\n') for line in f]
		return studies
			
		
db = input("Database:")
get_stud = get_studies(db)
studies = get_stud.read_studies()
print(studies)
