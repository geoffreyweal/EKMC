"""
EKMC_Multi_Setup.py, Geoffrey Weal, 12/8/

This program is designed to setup the exciton kMC algorithm for performing multiple repeats of the same simulation in slurm
"""
import os, math
from EKMC.EKMC.Run_EKMC_setup_files.get_EKMC_version import get_EKMC_version
from EKMC.EKMC_Setup.EKMC_Only_Setup.EKMC_Only_Setup import EKMC_Only_Setup
from EKMC.EKMC_Setup.Create_submitSL_slurm_Main      import make_mass_submitSL_full, make_mass_submitSL_packets

exciton_filename = 'Run_EKMC.py'
mass_submit_filename = 'mass_submit.sl'

def EKMC_Setup(EKMC_settings, mass_submission_information, setup_folder_name=None, write_rate_constants_to_file=False, no_of_cpus_for_setup=1):
	"""
	This method is designed to setup the exciton kMC algorithm for performing multiple repeats of the same simulation in slurm.

	Parameters
	----------
	EKMC_settings : dict.
		This contains the information about the crystal you want to simulate using this kMC program
	mass_submission_information : list of dicts.
		This contains the information required for the mass_submit.sl files, for submitting jobs to slurm.
	setup_folder_name : str.
		This is the name of the folder to write initial setup files to. These files include coupling, ...
	write_rate_constants_to_file : bool
		This indicates if you want to write a file called "kMC_sim_rate_constants.txt" that includes all the rate constant data for an exciton moving from the exciton donor it is currently on to any of the neighbouring exciton acceptors. 
	no_of_cpus_for_setup : int.
		This is the number of cpus used to setup the EKMC simulations.
	"""

	# First, get the file names and paths of data to obtain local neighbourhood data for
	folder_name       = EKMC_settings['folder_name']
	setup_folder_name = None if (setup_folder_name is None) else str(setup_folder_name)
	molecules_path    = EKMC_settings['molecules_path']
	crystal_name      = os.path.basename(molecules_path)
	if 'temp_folder_path' in EKMC_settings:
		if isinstance(EKMC_settings['temp_folder_path'],str):
			temp_folder_path = EKMC_settings['temp_folder_path']
			if temp_folder_path.endswith('/'):
				temp_folder_path = temp_folder_path[:-1]
		elif EKMC_settings['temp_folder_path'] is None:
			temp_folder_path = None
		else:
			raise Exception('Error: Make sure your input for "temp_folder_path" in your EKMC_settings dictionary is a string or None')
	else:
		temp_folder_path = None

	# Second, obtain the functional and basis set settings used for this simulation
	functional_and_basis_set = EKMC_settings['functional_and_basis_set']

	# Third, obtain the kinetic model that you would like to use for performing the kinetic monte carlo algorithm.
	kinetic_model = EKMC_settings['kinetic_model']

	# Fourth, obtain information about the short-range and long-range couplings from EKMC_settings
	short_range_couplings = EKMC_settings['short_range_couplings']
	long_range_couplings  = EKMC_settings['long_range_couplings']

	# Fifth, obtain information about rCut for short-range and long-range coupling models. 
	short_range_rCut          = EKMC_settings['short_range_rCut']
	long_range_rCut           = EKMC_settings.get('long_range_rCut',None)
	rCut_mol_dist_description = EKMC_settings['rCut_mol_dist_description']

	# Sixth, obtain information for obtaining reorganisation energies and bandgap energies 
	# for an excton moving from one molecule to another in the crystal.
	reorganisation_and_bandgap_energy_details = EKMC_settings['reorganisation_and_bandgap_energy_details']

	# Seventh, obtain information about the kinetic details and neighbourhood cut-off from EKMC_settings
	kinetics_details = EKMC_settings['kinetics_details']

	# Eighth, determine if you want to include solvents in your EKMC runs.
	include_solvents = EKMC_settings['include_solvents']

	# Ninth, begin creating Run_EKMC.py files for running the excitonic kinetic Monte Carlo algorithm.  
	dash_number = 80
	print('-'*dash_number)
	print('-'*dash_number)
	title = ' RUNNING EXCITON KMC SIMULATION '
	space_no = math.floor((dash_number - len(title))/2.0)
	print(' '*space_no+str(title)+' '*space_no)
	version_no = get_EKMC_version()
	version_string = 'Version '+str(version_no)
	space_no = math.floor((dash_number - len(version_string))/2.0)
	print(' '*space_no+str(version_string)+' '*space_no)
	print()
	title = ' Setting up: '+str(crystal_name)+' '
	space_no = math.floor((dash_number - len(title))/2.0)
	print(' '*space_no+str(title)+' '*space_no)
	print('-'*dash_number)
	print('-'*dash_number)

	# Tenth, get the path to store this simulation in, as well as the path to save initial setup files to.
	EKMC_Simulations_name = 'EKMC_Simulations'
	if ('overall_folder_suffix_name' in EKMC_settings):
		overall_folder_suffix_name = EKMC_settings['overall_folder_suffix_name']
		if not (overall_folder_suffix_name == '' or overall_folder_suffix_name is None):
			EKMC_Simulations_name += '_'+str(overall_folder_suffix_name)
	path_to_EKMC_simulations         = os.getcwd()+'/'+EKMC_Simulations_name+'/'+folder_name+'/'+functional_and_basis_set
	path_to_initial_EKMC_setup_files = os.getcwd()+'/'+EKMC_Simulations_name+'_initial_setup_data'+'/'+setup_folder_name+'/'+functional_and_basis_set if (setup_folder_name is not None) else None

	# Eleventh, setup the kMC simulations and get the exciton kMC setup files for performing simulations, and put it in the path_to_EKMC_simulations folder
	EKMC_Only_Setup(molecules_path, functional_and_basis_set, kinetic_model, short_range_couplings, long_range_couplings, short_range_rCut, long_range_rCut, rCut_mol_dist_description, reorganisation_and_bandgap_energy_details, kinetics_details, include_solvents=include_solvents, path_to_EKMC_simulations=path_to_EKMC_simulations, path_to_initial_EKMC_setup_files=path_to_initial_EKMC_setup_files, no_of_cpus_for_setup=no_of_cpus_for_setup)

	# Twelfth, get information for creating the Run_EKMC.py file
	sim_time_limit                                 = EKMC_settings.get('sim_time_limit','inf')
	max_no_of_steps                                = EKMC_settings.get('max_no_of_steps','inf')
	starting_molecule                              = EKMC_settings.get('starting_molecule','any')

	# Thirteenth, create the Run_EKMC.py for performing kMC simulations on the exciton
	print('-----------------------------------------------------')
	print('MAKING '+str(exciton_filename)+' FILE')
	make_Run_EKMC_file(path_to_EKMC_simulations=path_to_EKMC_simulations, path_to_KMC_setup_data='..', sim_time_limit=sim_time_limit, max_no_of_steps=max_no_of_steps, write_rate_constants_to_file=write_rate_constants_to_file, starting_molecule=starting_molecule)

	# Fourteenth, create the mass_submit.sl for submitting a number of repeated simulation to slurm
	print('-----------------------------------------------------')
	print('MAKING '+str(mass_submit_filename)+' FILE')
	make_mass_submit_file(path_to_EKMC_simulations=path_to_EKMC_simulations, temp_folder_path=temp_folder_path, crystal_name=crystal_name, functional_and_basis_set=functional_and_basis_set, mass_submission_information=mass_submission_information)
	print('-----------------------------------------------------')

	print('-'*dash_number)
	print('-'*dash_number)
	print('-'*dash_number)

def make_Run_EKMC_file(path_to_EKMC_simulations, path_to_KMC_setup_data, sim_time_limit, max_no_of_steps, write_rate_constants_to_file, starting_molecule):
	"""
	This method is designed to create the Run_EKMC.py for performing the KMC simulation.

	Parameters
	----------
	path_to_EKMC_simulations : str.
		This is the path to save this Run_EKMC.py file to.
	path_to_KMC_setup_data : str.
		This is the path to the ekmc file that contains all the information about the ekmc simulation for this crystal.
	sim_time_limit : float
		This is the maximum simulated time limit to run the kinetic Monte Carlo simulation over.
	max_no_of_steps : int
		This is the maximum number of kmc steps to run the kinetic Monte Carlo simulation over.
	starting_molecule : int or str.
		This is the molecule to start the KMC simulations from. If starting_molecule = 'any', then any molecule will be selected to start the KMC simulation from. Default: 'any'. 
	"""
	with open(path_to_EKMC_simulations+'/'+exciton_filename, 'w') as EKMC_PY:
		EKMC_PY.write('"""\n')
		EKMC_PY.write('This script will allow you to perform a Exciton-based kinetic Monte-Carlo simulation on your crystal.\n')
		EKMC_PY.write('"""\n')
		EKMC_PY.write('\n')
		EKMC_PY.write('import sys\n')
		EKMC_PY.write('try:\n')
		EKMC_PY.write('\tfrom EKMC.EKMC.Run_EKMC import Run_EKMC\n')
		EKMC_PY.write('except:\n')
		EKMC_PY.write('\tfrom EKMC import Run_EKMC'+'\n')
		EKMC_PY.write('\n')
		EKMC_PY.write('# First, give the path to the KMC_setup_data, which has been run previously.\n')
		EKMC_PY.write('# This file contains all the kinetic information and the electronic information around the local neighbourhood of each molecule in the crystal.\n')
		EKMC_PY.write(f'path_to_KMC_setup_data = "{path_to_KMC_setup_data}"\n')
		EKMC_PY.write('temp_folder_path = (None if (len(sys.argv) == 1) else str(sys.argv[1]))\n')
		EKMC_PY.write('\n')
		EKMC_PY.write('# Second, give the amount of time or the number of steps you would like to simulate.\n')
		if isinstance(sim_time_limit,str):
			EKMC_PY.write(f'sim_time_limit = "inf"\n')
		else:
			EKMC_PY.write(f'sim_time_limit = {sim_time_limit}'+' # ps\n')
		if isinstance(max_no_of_steps,str):
			max_no_of_steps = '"'+max_no_of_steps+'"'
		EKMC_PY.write(f'max_no_of_steps = {max_no_of_steps}'+'\n')
		EKMC_PY.write('\n')
		EKMC_PY.write('# Third, indicate if you want the exciton to begin on a particular molecule or one of a set of molecules.\n')
		if isinstance(starting_molecule,str):
			starting_molecule = '"'+starting_molecule+'"'
		EKMC_PY.write(f'starting_molecule = {starting_molecule}'+'\n')
		EKMC_PY.write('\n')
		EKMC_PY.write('# Fourth, indicate if you want to record the rate constants for the exciton donor the exciton is on to all the neighbouring exception acceptors for each KMC step.\n')
		EKMC_PY.write(f'write_rate_constants_to_file = {write_rate_constants_to_file}'+'\n')
		EKMC_PY.write('\n')
		EKMC_PY.write('# Fifth, perform the exciton kinetic Monte Carlo simulation.\n')
		EKMC_PY.write('Run_EKMC(path_to_KMC_setup_data=path_to_KMC_setup_data, temp_folder_path=temp_folder_path, sim_time_limit=sim_time_limit, max_no_of_steps=max_no_of_steps, write_rate_constants_to_file=write_rate_constants_to_file, starting_molecule=starting_molecule)'+'\n')

def make_mass_submit_file(path_to_EKMC_simulations, temp_folder_path, crystal_name, functional_and_basis_set, mass_submission_information):
	"""
	This method is designed to create the Run_EKMC.py for performing the KMC simulation/

	Parameters
	----------
	path_to_EKMC_simulations : str.
		This is the path to save this Run_EKMC.py file to.
	temp_folder_path : str. or None
		This is the path to place files as the KMC file is running for temporary storage. This is not vital for running a simulation. If set to None, no temporary folder will be created. Dafault: None 
	crystal_name : str.
		This is the name of the crystal file.
	functional_and_basis_set : str.
		This is the names of the functional and basis set you are using. Refer to the ECCP program info.
	mass_submission_information : dict.
		This is all the information required for submitting the exciton kinetic Monte Carlo algorithm on slurm using ArrayJobs.
	"""

	# First, get all the variables for making the mass_submit.sl file with
	job_name         = crystal_name+'_'+functional_and_basis_set
	cpus_per_task    = mass_submission_information.get('cpus_per_task',1)
	mem              = mass_submission_information['mem']
	time             = mass_submission_information['time']
	partition        = mass_submission_information['partition']
	constraint       = mass_submission_information.get('constraint',None)
	email            = mass_submission_information.get('email', '')
	python_version   = mass_submission_information.get('python_version', 'Python/3.9.5')
	gcc_version      = mass_submission_information.get('gcc_version', None) # 'GCC/10.3.0')
	gcccore_version  = mass_submission_information.get('gcccore_version', 'GCCcore/10.3.0')
	binutils_version = mass_submission_information.get('binutils_version', None)
	project          = mass_submission_information.get('project',None)
	nodes            = mass_submission_information.get('nodes',1)

	# Second, determine the number of simulatinos you would like to perform, and make the mass_submit.sl file.
	submission_type = mass_submission_information['submission_type']
	no_of_simulations = mass_submission_information['no_of_simulations']
	if submission_type == 'full':
		make_mass_submitSL_full(path_to_EKMC_simulations,temp_folder_path,job_name,project,no_of_simulations,time,cpus_per_task,mem,None,partition,constraint,email,python_version,gcc_version,gcccore_version,binutils_version)
	elif submission_type == 'packet':
		no_of_sims_per_packet = mass_submission_information['no_of_sims_per_packet']
		make_mass_submitSL_packets(path_to_EKMC_simulations,temp_folder_path,job_name,project,no_of_simulations,no_of_sims_per_packet,time,cpus_per_task,mem,None,partition,constraint,email,python_version,gcc_version,gcccore_version,binutils_version)
	else:
		print('Error in def make_mass_submit_file, in EKMC_Multi_Setup.py')
		print('Your input for the "submission_type" tag in the mass_submission_information dictionary must be either:')
		print('  * full: Perform "no_of_simulations" number of individual simulations in "no_of_simulations" submitted jobs.')
		print('  * packet: Perform "no_of_simulations" number of individual simulations in "no_of_sims_per_packet" submitted jobs.')
		exit('Check this out and try this program again. This program will finish without continuing')

