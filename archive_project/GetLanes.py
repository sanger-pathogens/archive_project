from subprocess import Popen, PIPE, call, check_output 

	
def get_lanes(study):
	data = check_output(["pf", "data", "-t", "study", "-i", study]).decode('ascii').splitlines()
	if len(data) == 0:
		print('Unknown study or no data associated with study', study)
		return None 
	else:
		return data 		

