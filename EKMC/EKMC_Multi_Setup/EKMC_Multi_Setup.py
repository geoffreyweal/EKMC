"""
EKMC_Multi_Setup.py, Geoffrey Weal, 12/8/

This program is designed to setup the exciton kMC algorithm for performing multiple repeats of the same simulation in slurm
"""
import os
from EKMC.EKMC_Setup.EKMC_Setup import EKMC_Setup
from EKMC.EKMC_Multi_Setup.Create_submitSL_slurm_Main import make_mass_submitSL_full, make_mass_submitSL_packets

exciton_filename = 'Run_EKMC.py'
mass_submit_filename = 'mass_submit.sl'

def EKMC_Multi_Setup(all_EKMC_settings, all_mass_submission_information):
	"""
	This method is designed to setup the exciton kMC algorithm for performing multiple repeats of the same simulation in slurm.

	Parameters
	----------
	all_EKMC_settings : list of dicts.
		This contains all the information about the crystals you want to simulate using this kMC program
	all_mass_submission_information : list of dicts.
		This contains all the information required for the mass_submit.sl files, for submitting jobs to slurm.
	"""

	# For each crystal in the EKMC_settings (and associated mass_submission_information).
	for EKMC_settings, mass_submission_information in zip(all_EKMC_settings, all_mass_submission_information):

		# First, get the file names and paths of data to obtain local neighbourhood data for
		if not 'folder_name' in EKMC_settings:
			folder_name = crystal_name
		elif EKMC_settings['folder_name'] is None:
			folder_name = crystal_name
		else:
			folder_name = EKMC_settings['folder_name']
		molecules_path  = EKMC_settings['molecules_path']
		crystal_name    = os.path.basename(molecules_path)
		ATC_folder_path = EKMC_settings['ATC_folder_path']

		# Second, obtain the functional and basis set settings used for this simulation
		functional_and_basis_set = EKMC_settings['functional_and_basis_set']

		# Third, obtain the kinetic model that you would like to use for performing the kinetic monte carlo algorithm.
		kinetic_model = EKMC_settings['kinetic_model']

		# Fourth, obtain information about the dimers, kinetic details, and neighbourhood cut-off from EKMC_settings
		dimer_couplings    = EKMC_settings['dimer_couplings']
		kinetics_details   = EKMC_settings['kinetics_details']
		neighbourhood_rCut = EKMC_settings['neighbourhood_rCut']

		# Fifth, begin creating Run_EKMC.py files for running the excitonic kinetic Monte Carlo algorithm.  
		print('#########################################################################')
		print('#########################################################################')
		print('#########################################################################')
		print('      Setting up: '+str(crystal_name))
		print('#########################################################################')
		print('#########################################################################')
		print('#########################################################################')

		# Sixth, get the path to store this simulation in.
		path_to_simulation = os.getcwd()+'/'+'Multi_EKMC_Simulations'+'/'+folder_name+'/'+functional_and_basis_set

		# Seventh, setup the kMC simulations and get the exciton kMC setup files for performing simulations, and put it in the path_to_simulation folder
		EKMC_Setup(molecules_path, ATC_folder_path, functional_and_basis_set, kinetic_model, dimer_couplings, kinetics_details, neighbourhood_rCut=neighbourhood_rCut, path_to_KMC_setup_data=path_to_simulation)

		# Eighth, get information for creating the Run_EKMC.py file
		sim_time_limit = EKMC_settings.get('sim_time_limit',float('inf'))
		max_no_of_steps = EKMC_settings.get('max_no_of_steps','inf')
		store_data_in_databases = EKMC_settings.get('store_data_in_databases',False)
		no_of_molecules_at_cell_points_to_store_on_RAM = EKMC_settings.get('no_of_molecules_at_cell_points_to_store_on_RAM',None)

		# Ninth, create the Run_EKMC.py for performing kMC simulatinos on the exciton
		print('-----------------------------------------------------')
		print('MAKING '+str(exciton_filename)+' FILE')
		make_Run_EKMC_file(path_to_simulation=path_to_simulation, path_to_KMC_setup_data='..', sim_time_limit=sim_time_limit, max_no_of_steps=max_no_of_steps, store_data_in_databases=store_data_in_databases, no_of_molecules_at_cell_points_to_store_on_RAM=no_of_molecules_at_cell_points_to_store_on_RAM)

		# Tenth, create the mass_submit.sl for submitting a number of repeated simulation to slurm
		print('-----------------------------------------------------')
		print('MAKING '+str(mass_submit_filename)+' FILE')
		make_mass_submit_file(path_to_simulation=path_to_simulation, crystal_name=crystal_name, functional_and_basis_set=functional_and_basis_set, mass_submission_information=mass_submission_information)
		print('-----------------------------------------------------')

	print('#########################################################################')
	print('#########################################################################')
	print('#########################################################################')

def make_Run_EKMC_file(path_to_simulation, path_to_KMC_setup_data, sim_time_limit, max_no_of_steps, store_data_in_databases, no_of_molecules_at_cell_points_to_store_on_RAM):
	"""
	This method is designed to create the Run_EKMC.py for performing the KMC simulation.

	Parameters
	----------
	path_to_simulation : str.
		This is the path to save this Run_EKMC.py file to.
	path_to_KMC_setup_data : str.
		This is the path to the ekmc file that contains all the information about the ekmc simulation for this crystal.
	sim_time_limit : float
		This is the maximum simulated time limit to run the kinetic Monte Carlo simulation over.
	max_no_of_steps : int
		This is the maximum number of kmc steps to run the kinetic Monte Carlo simulation over.
	store_data_in_databases : bool.
		To do.
	no_of_molecules_at_cell_points_to_store_on_RAM : int
		This is the maximum number of entries to maintain in the RAM memory in the graph.
	"""
	with open(path_to_simulation+'/'+exciton_filename, 'w') as EKMC_PY:
		EKMC_PY.write('"""\n')
		EKMC_PY.write('This script will allow you to perform a Exciton-based kinetic Monte-Carlo simulation on your crystal.\n')
		EKMC_PY.write('"""\n')
		EKMC_PY.write('\n')
		EKMC_PY.write('from EKMC import Run_EKMC'+'\n')
		EKMC_PY.write('\n')
		EKMC_PY.write('# First, give the path to the KMC_setup_data, which has been run previously.\n')
		EKMC_PY.write('# This file contains all the kinetic information and the electronic information around the local neighbourhood of each molecule in the crystal.\n')
		EKMC_PY.write(f'path_to_KMC_setup_data="{path_to_KMC_setup_data}"\n')
		EKMC_PY.write('\n')
		EKMC_PY.write('# Second, give the amount of time or the number of steps you would like to simulate.\n')
		EKMC_PY.write(f'sim_time_limit = {sim_time_limit}'+'\n')
		if isinstance(max_no_of_steps,str):
			max_no_of_steps = '"'+max_no_of_steps+'"'
		EKMC_PY.write(f'max_no_of_steps = {max_no_of_steps}'+'\n')
		EKMC_PY.write('\n')
		EKMC_PY.write('# Third, if you want to store data about the random energetic and coupling disorders in databases, provide the information required to use a database here.\n')
		EKMC_PY.write(f'store_data_in_databases = {store_data_in_databases}'+'\n')
		EKMC_PY.write(f'no_of_molecules_at_cell_points_to_store_on_RAM = {no_of_molecules_at_cell_points_to_store_on_RAM}'+'\n')
		EKMC_PY.write('\n')
		EKMC_PY.write('# Fourth, perform the exciton kinetic Monte Carlo simulation.\n')
		EKMC_PY.write('Run_EKMC(path_to_KMC_setup_data=path_to_KMC_setup_data, sim_time_limit=sim_time_limit, max_no_of_steps=max_no_of_steps, store_data_in_databases=store_data_in_databases, no_of_molecules_at_cell_points_to_store_on_RAM=no_of_molecules_at_cell_points_to_store_on_RAM)'+'\n')

def make_mass_submit_file(path_to_simulation, crystal_name, functional_and_basis_set, mass_submission_information):
	"""
	This method is designed to create the Run_EKMC.py for performing the KMC simulation/

	Parameters
	----------
	path_to_simulation : str.
		This is the path to save this Run_EKMC.py file to.
	crystal_name : str.
		This is the name of the crystal file.
	functional_and_basis_set : str.
		This is the names of the functional and basis set you are using. Refer to the ECCP program info.
	mass_submission_information : dict.
		This is all the information required for submitting the exciton kinetic Monte Carlo algorithm on slurm using ArrayJobs.
	"""

	# First, get all the variables for making the mass_submit.sl file with
	job_name         = crystal_name+'_'+functional_and_basis_set
	ntasks_per_node  = mass_submission_information['ntasks_per_node']
	mem              = mass_submission_information['mem']
	time             = mass_submission_information['time']
	partition        = mass_submission_information['partition']
	constraint       = mass_submission_information.get('constraint',None)
	email            = mass_submission_information.get('email', '')
	python_version   = mass_submission_information.get('python_version', 'python/3.8.1')
	project          = mass_submission_information.get('project',None)
	nodes            = mass_submission_information.get('nodes',1)

	# Second, determine the number of simulatinos you would like to perform, and make the mass_submit.sl file.
	submission_type = mass_submission_information['submission_type']
	no_of_simulations = mass_submission_information['no_of_simulations']
	if submission_type == 'full':
		make_mass_submitSL_full(path_to_simulation,job_name,project,no_of_simulations,time,nodes,ntasks_per_node,mem,None,partition,constraint,email,python_version)
	elif submission_type == 'packet':
		no_of_packets_to_make = mass_submission_information['no_of_packets_to_make']
		make_mass_submitSL_packets(path_to_simulation,job_name,project,no_of_simulations,no_of_packets_to_make,time,nodes,ntasks_per_node,mem,None,partition,constraint,email,python_version)
	else:
		print('Error in def make_mass_submit_file, in EKMC_Multi_Setup.py')
		print('Your input for the "submission_type" tag in the mass_submission_information dictionary must be either:')
		print('  * full: Perform "no_of_simulations" number of individual simulations in "no_of_simulations" submitted jobs.')
		print('  * packet: Perform "no_of_simulations" number of individual simulations in "no_of_packets_to_make" submitted jobs.')
		exit('Check this out and try this program again. This program will finish without continuing')

