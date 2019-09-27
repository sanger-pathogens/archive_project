
#Read studies from .ilm.studies file for database 
def get_studies(studies_file_path):
	#Test if path exists
	try: 
		with open(studies_file_path) as f:
			studies = [line.rstrip('\n') for line in f] #read study names
			return studies
	except FileNotFoundError:
		print('Invalid studies file')
		return None 
