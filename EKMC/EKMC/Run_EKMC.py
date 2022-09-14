"""
Run_EKMC.py, Geoffrey Weal, 12/8/22

This method is designed to extract all the data needed for running the kinetic Monte Carlo algorithm for exciton moving about the molecules of a crystal.
"""

from EKMC.EKMC.kMC_algorithm import run_kMC_algorithm

KMC_setup_data_filename = 'KMC_setup_data.ekmc'
def Run_EKMC(path_to_KMC_setup_data, sim_time_limit=float('inf'), max_no_of_steps='inf', store_data_in_databases=False, no_of_molecules_at_cell_points_to_store_on_RAM=None):
	"""
	This program is designed to simulate the movement of an exciton through a OPV crystal system.

	Parameters
	----------
	path_to_KMC_setup_data : str.
		This is te path to the ekmc file that contains information about your kinetic Monte Carlo simulation.
	sim_time_limit : float
		This is the maximum simulated time limit to run the kinetic Monte Carlo simulation over.
	max_no_of_steps : int
		This is the maximum number of kmc steps to run the kinetic Monte Carlo simulation over.
	store_data_in_databases : bool.
		This tag indicates if you want to store random energy and coupling disorders in a database.
	no_of_molecules_at_cell_points_to_store_on_RAM : int
		This is the maximum number of entries to maintain in the RAM memory in the graph.
	"""

	# First, this is needed to prevent multiprocessing.Process from doing weird stuff
	if not (__name__ == 'EKMC.EKMC.Run_EKMC'):
		return

	# Second, retrieve data for setting up the kinetic Monte Carlo simulation from the KMC_setup_data.ekmc file.
	with open(path_to_KMC_setup_data+'/'+KMC_setup_data_filename) as KMC_setup_data_EKMC:
		centre_of_masses = eval(KMC_setup_data_EKMC.readline().rstrip())
		unit_cell_matrix = eval(KMC_setup_data_EKMC.readline().rstrip())
		kinetic_model    = str(KMC_setup_data_EKMC.readline().rstrip())
		kinetics_details = eval(KMC_setup_data_EKMC.readline().rstrip())
		all_local_neighbourhoods = eval(KMC_setup_data_EKMC.readline().rstrip())
	
	# Third, get the given coupling and energetic disorders. 
	coupling_disorder = kinetics_details['coupling_disorder']
	energetic_disorder = kinetics_details['energetic_disorder']

	# Fourth, run the exciton kinetic Monte Carlo Simulation.
	print('------------------------------------------------')
	print('------------------------------------------------')
	print('-------- RUNNING EXCITON KMC SIMULATION --------')
	print('------------------------------------------------')
	print('------------------------------------------------')
	run_kMC_algorithm(kinetic_model, all_local_neighbourhoods, coupling_disorder, energetic_disorder, sim_time_limit=sim_time_limit, max_no_of_steps=max_no_of_steps, no_of_molecules_at_cell_points_to_store_on_RAM=no_of_molecules_at_cell_points_to_store_on_RAM, store_data_in_databases=store_data_in_databases)
