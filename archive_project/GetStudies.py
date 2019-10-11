def get_studies(studies_file_path):
	'''If type file given, read file and return studies. If file not found raise error.'''
	try: 
		with open(studies_file_path) as f:
			studies = [line.rstrip('\n') for line in f] 
			return studies
	except FileNotFoundError:
		print('Invalid studies file')
		return None 
