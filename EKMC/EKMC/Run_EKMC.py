"""
Run_EKMC.py, Geoffrey Weal, 12/8/22

This method is designed to extract all the data needed for running the kinetic Monte Carlo algorithm for exciton moving about the molecules of a crystal.
"""

import os, shutil, math
from random import choice
from EKMC.EKMC.Run_EKMC_setup_files.get_EKMC_version                              import get_EKMC_version
from EKMC.EKMC.Run_EKMC_setup_files.did_finish                                    import did_finish
from EKMC.EKMC.Run_EKMC_setup_files.check_molecule_consistancy_across_datasets    import check_molecule_consistancy_across_datasets
from EKMC.EKMC.Run_EKMC_setup_files.expand_to_include_unique_molecules_in_dict    import expand_to_include_unique_molecules_in_dict
from EKMC.EKMC.Run_EKMC_setup_files.update_bandgap_and_reorganisation_energy_data import update_bandgap_and_reorganisation_energy_data
from EKMC.EKMC.Run_EKMC_setup_files.names_of_lowest_bandgap_molecules_in_crystal  import names_of_lowest_bandgap_molecules_in_crystal
from EKMC.EKMC.KMC_algorithm.Run_KMC_algorithm_in_C                               import Run_KMC_algorithm_in_C

KMC_setup_data_filename = 'KMC_setup_data.ekmc'
def Run_EKMC(path_to_KMC_setup_data, temp_folder_path=None, sim_time_limit='inf', max_no_of_steps='inf', write_rate_constants_to_file=False, starting_molecule='any'):
	"""
	This program is designed to simulate the movement of an exciton through a OPV crystal system.

	Parameters
	----------
	path_to_KMC_setup_data : str.
		This is te path to the ekmc file that contains information about your kinetic Monte Carlo simulation.
	temp_folder_path : str. or None
		This is the path to place files as the KMC file is running for temporary storage. This is not vital for running a simulation. If set to None, no temporary folder will be created. Dafault: None 
	sim_time_limit : float
		This is the maximum simulated time limit to run the kinetic Monte Carlo simulation over.
	max_no_of_steps : int
		This is the maximum number of kmc steps to run the kinetic Monte Carlo simulation over.
	write_rate_constants_to_file : bool
		This indicates if you want to write a file called "kMC_sim_rate_constants.txt" that includes all the rate constant data for an exciton moving from the exciton donor it is currently on to any of the neighbouring exciton acceptors. 
	starting_molecule : "any", "lowest", int, list of ints
		This is the molecule in the (0,0,0) cell that you want the exciton to begin the KMC simulation on. If you set this to "any", the exciton will randomly be placed on any molecule in the unit cell. "lowest" means you will place the crystal on the lowest energy molecules.
	"""

	# First, this is needed to prevent multiprocessing.Process from doing weird stuff
	if not (__name__ == 'EKMC.EKMC.Run_EKMC'):
		return

	# Second, retrieve data for setting up the kinetic Monte Carlo simulation from the KMC_setup_data.ekmc file.
	with open(path_to_KMC_setup_data+'/'+KMC_setup_data_filename) as KMC_setup_data_EKMC:
		molecule_list_and_com            = eval(KMC_setup_data_EKMC.readline().replace('S','.0').rstrip()) # remove any solvent tags, will include them here for running EKMC simulation.
		molecule_list_and_com            = {str(int(name))+'S' if isinstance(name,float) else str(name): centre_of_mass for name, centre_of_mass in molecule_list_and_com.items()}
		solvent_list                     = [int(name.replace('S','')) for name in molecule_list_and_com.keys() if name.endswith('S')]
		unit_cell_matrix                 = eval(KMC_setup_data_EKMC.readline().rstrip())
		kinetic_model                    =  str(KMC_setup_data_EKMC.readline().rstrip())
		kinetics_details                 = eval(KMC_setup_data_EKMC.readline().rstrip())
		molecule_bandgap_energy_data     = eval(KMC_setup_data_EKMC.readline().rstrip())
		dimer_reorganisation_energy_data = eval(KMC_setup_data_EKMC.readline().rstrip())
		conformationally_equivalent_data = eval(KMC_setup_data_EKMC.readline().rstrip())
		constant_rate_data               = eval(KMC_setup_data_EKMC.readline().rstrip())
		coupling_value_data              = eval(KMC_setup_data_EKMC.readline().rstrip())

	# Third, obtain all the names of the molecules in the crystal, as reported in 'KMC_setup_data.ekmc'
	molecule_names = sorted([int(str(molname).replace('S','')) for molname in molecule_list_and_com.keys()])
	
	# Fourth, get the given coupling and energetic disorders. 
	coupling_disorder = kinetics_details['coupling_disorder']
	energetic_disorder = kinetics_details['energetic_disorder']

	# Fifth, run the exciton kinetic Monte Carlo Simulation.
	print('------------------------------------------------')
	print('------------------------------------------------')
	print('-------- RUNNING EXCITON KMC SIMULATION --------')
	version_no = get_EKMC_version()
	version_string = 'Version '+str(version_no)
	space_no = math.floor((50 - len(version_string))/2.0)
	print(' '*space_no+str(version_string))
	print('------------------------------------------------')
	print('------------------------------------------------')

	# Sixth, check that the simulation has finished.
	kMC_sim_name      = 'kMC_sim.txt'
	kMC_sim_rate_constants_name = 'kMC_sim_rate_constants.txt'
	reached_sim_time_limit, reached_max_no_of_steps, time_simulated, no_of_steps_simulated = did_finish(kMC_sim_name, sim_time_limit, max_no_of_steps)
	if reached_sim_time_limit or reached_max_no_of_steps:
		finished_report = []
		if reached_sim_time_limit:
			finished_report.append(str(sim_time_limit)+' ps')
		if reached_max_no_of_steps:
			finished_report.append(str(max_no_of_steps)+' kmc steps')
		print('This simulation has already reached '+' and '.join(finished_report)+'.')
		print('Time simulated: '+str(time_simulated)+' ps')
		print('Number of steps simulated: '+str(no_of_steps_simulated))
		print('Will finish the Exciton kinetic Monte Carlo algorithm without doing anything.')
		print('------------------------------------------------')
		return

	# Seventh, if you want to save data to a temp file during the KMC run, do this here
	if temp_folder_path is not None:

		# 7.1: Check that this temp folder path does not currently exist yet
		if os.path.exists(temp_folder_path):
			raise Exception('Error: The temp folder you are trying to create has already been created ('+str(temp_folder_path)+'). Check this out')

		# 7.2: Create the temp folder
		print('Making a temp folder to store data in: '+str(temp_folder_path))
		os.makedirs(temp_folder_path)

		# 7.3: Copy the kMC_sim file into this temp folder if there is a current kMC_sim file.
		if kMC_sim_name in os.listdir('.'):
			shutil.copy(kMC_sim_name, temp_folder_path+'/'+kMC_sim_name)
		if kMC_sim_rate_constants_name in os.listdir('.'):
			shutil.copy(kMC_sim_rate_constants_name, temp_folder_path+'/'+kMC_sim_rate_constants_name)

	else:
		temp_folder_path = '.'

	# Eighth, get the path to the kMC_sim file.
	path_to_kMC_sim                = temp_folder_path+'/'+kMC_sim_name
	path_to_kMC_sim_rate_constants = temp_folder_path+'/'+kMC_sim_rate_constants_name

	# Ninth, check that the molecules in the 'KMC_setup_data.ekmc' file are consistent between molecule_bandgap_energy_data, dimer_reorganisation_energy_data, coupling_value_data, and conformationally_equivalent_data dictionaries.
	check_molecule_consistancy_across_datasets(molecule_names, molecule_bandgap_energy_data, dimer_reorganisation_energy_data, coupling_value_data, conformationally_equivalent_data)

	# Tenth, update conformationally_equivalent_data to include unique molecules that link to themselves.
	conformationally_equivalent_data = expand_to_include_unique_molecules_in_dict(conformationally_equivalent_data, molecule_names)

	# Eleventh, add conformationally unique molecule data to molecule_bandgap_energy_data and dimer_reorganisation_energy_data.
	molecule_bandgap_energy_data, dimer_reorganisation_energy_data = update_bandgap_and_reorganisation_energy_data(molecule_bandgap_energy_data, dimer_reorganisation_energy_data, conformationally_equivalent_data)

	# Twelfth, determine what the starting molecule will be where the exciton begins from in the origin unit cell. 
	if starting_molecule == None:
		starting_molecule = 'any'
	if   isinstance(starting_molecule,str):
		if starting_molecule.lower() == 'any':
			current_molecule_name = choice(molecule_names)
		elif starting_molecule.lower() == 'lowest':
			molecule_names_of_lowest_bandgap_molecules = names_of_lowest_bandgap_molecules_in_crystal(molecule_bandgap_energy_data)
			current_molecule_name = choice(molecule_names_of_lowest_bandgap_molecules)
		else:
			raise Exception('Error: starting_molecule needs to be either "any", "lower", or the molecule or molecules you would like as the molecule the exciton begins on.')
	elif isinstance(starting_molecule,list):
		current_molecule_name = int(choice(starting_molecule))
	else:
		current_molecule_name = int(starting_molecule)

	# Thirteenth, give the current cell point, which is the origin unit cell (0, 0, 0)
	# and get the current_molecule_description, which contains current_molecule_name and current_cell_point
	current_cell_point = (0, 0, 0)
	current_molecule_description = (current_molecule_name, current_cell_point)

	if write_rate_constants_to_file == False:
		write_rate_constants_to_file = (False, False)

	# Fourteenth, run the KMC algorithm in C++
	path_to_c_code = os.path.dirname(os.path.realpath(__file__)) + "/KMC_algorithm/KMC_algorithm.so"
	Run_KMC_algorithm_in_C(path_to_c_code, path_to_kMC_sim, path_to_kMC_sim_rate_constants, molecule_list_and_com, unit_cell_matrix, kinetic_model, constant_rate_data, conformationally_equivalent_data, molecule_bandgap_energy_data, dimer_reorganisation_energy_data, coupling_value_data, energetic_disorder, coupling_disorder, sim_time_limit, max_no_of_steps, starting_molecule, temp_folder_path, write_rate_constants_to_file)

	# Fiftheenth, if you had a temp folder, copy the relavant files from the temp folder to the current folder and remove the temp folder.
	if not (temp_folder_path == '.'):
		shutil.move(temp_folder_path+'/'+kMC_sim_name,'./'+kMC_sim_name)
		if write_rate_constants_to_file[0]:
			shutil.move(temp_folder_path+'/'+kMC_sim_rate_constants_name,'./'+kMC_sim_rate_constants_name)
		shutil.rmtree(temp_folder_path)

	# Sixtheenth, finish off with an ending message.
	print('Finished the Exciton kinetic Monte Carlo algorithm.')
	print('-------------')


