"""
get_initial_data_for_beginning_kMC.py, Geoffrey Weal, 26/3/22

This script is designed to obtain the initial data from disk needs to begin the KMC algorithm run.
"""
from EKMC.EKMC.kMC_algorithm_methods.reverse_readline import reverse_readline 

def get_initial_data_for_beginning_kMC(kMC_sim_name, store_data_in_databases):
	"""
	This method will look through kMC_sim_name to see where to continue from.

	Parameters
	----------
	kMC_sim_name : str.
		This is the name/path to the KMC simulation text file.
	store_data_in_databases : bool.
		If True, this data is stored to disk, if False, this data will not be on disk. You will not be able to continue this KMC run.

	Returns
	-------
	can_resume_kmc_run : bool.
		If True, it is possible continue to run your KMC simulation from it's last simulated point. If False, the simulation can not be resumed.
	count : int.
		This is the number of KMC steps that have been performed currently by this EKMC program.
	molecule_name : str.
		This is the name of the molecule that the exciton is currently on
	cell_point : tuple
		This is the unit cell that the exciton is currently in.
	time : float
		This is the current simulation time that the KMC algorithm has simulated. 
	"""

	# First, if data is not being stored in the database, move on.
	if not store_data_in_databases:
		return False, None, None, None, None

	# Second, check to see if this file exists. If not, move on
	if not os.path.exists(kMC_sim_name):
		return False, None, None, None, None

	# Third, get the last point in the KMC simulation from the kMC_sim_name file.
	end_lines_to_remove = 0
	for line in reverse_readline(kMC_sim_name):
		if line.endswith('|'):
			line = line.rstrip().split()
			count = int(line[0])
			molecule_name = int(line[1])
			cell_point = eval(line[2])
			time = float(line[3])
			break 
		if line.startswith('Count'):
			return False, None, None, None, None

	# Fourth, return variables.
	return True, count, molecule_name, cell_point, time