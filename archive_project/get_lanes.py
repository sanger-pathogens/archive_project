from subprocess import Popen, PIPE, call, check_output 

class get_lanes: 
	
	def __init__(self, study):
		self.study = study.strip("'")
	
	def pf_data(self):

		data = check_output(["pf", "data", "-t", "study", "-i", self.study])
		return data
	'''
	def pf_data(self):
		data = check_output(["pf", "data", "-t", "study", "-i", self.study])
		data = data.decode('ascii').splitlines()
		if len(data) == 0:
			print('Unknown study or no data associated with study')
			return None 
		else:
			print(data)
			return data 		
	'''
'''

gl = get_lanes(study)
data = gl.pf_data()
'''
