"""
Run_KMC_algorithm_in_C.py, Geoffrey Weal, 28/5/23

This script is designed to provide a C wrapper to run the KMC code in C++ from python
"""
import os, ctypes
from random import choice

class Molecule_Centre_Of_Mass_CObject(ctypes.Structure):
	_fields_ = [('mol', ctypes.c_int), ('centre_of_mass_x', ctypes.c_longdouble), ('centre_of_mass_y', ctypes.c_longdouble), ('centre_of_mass_z', ctypes.c_longdouble)]

class Bandgap_Energies_CObject(ctypes.Structure):
	_fields_ = [('mol', ctypes.c_int), ('bandgap_energy', ctypes.c_longdouble)]

class Reorganisation_Energies_CObject(ctypes.Structure):
	_fields_ = [('mol1', ctypes.c_int), ('mol2', ctypes.c_int), ('reorganisation_energy', ctypes.c_longdouble)]

class Coupling_Value_Data_CObject(ctypes.Structure):
	_fields_ = [('mol1', ctypes.c_int), ('mol2', ctypes.c_int), ('uniti', ctypes.c_int), ('unitj', ctypes.c_int), ('unitk', ctypes.c_int), ('coupling_value', ctypes.c_longdouble)]

def Run_KMC_algorithm_in_C(path_to_c_code, path_to_kMC_sim, path_to_kMC_sim_rate_constants, molecule_list_and_com, unit_cell_matrix, kinetic_model, constant_rate_data, conformationally_equivalent_data, molecule_bandgap_energy_data, dimer_reorganisation_energy_data, coupling_value_data, energetic_disorder, coupling_disorder, sim_time_limit=float('inf'), max_no_of_steps='inf', starting_molecule='any', temp_folder_path=None, write_rate_constants_to_file=False):
	"""
	This method is a C wrapper to run the kMC algorithm for an exciton moving about the molecules in a crystal in C++.

	This method was designed with advice from https://realpython.com/python-bindings-overview/

	Parameters
	----------
	path_to_c_code : str.
		This is the path to the Exciton kinetic Monte Carlo C++ shared objects file.
	path_to_kMC_sim : str
		This is the path to ...
	path_to_kMC_sim_rate_constants : str
		This is the path to ...
	molecule_list_and_com : dict. 
		This dictionary contains the centre of masses for each molecule in the unit cell crystal.
	unit_cell_matrix : list of list of doubles
		This contains the matrix elements for the unit cell matrix. 
	kinetic_model :str.
		This is the kinetic model you would like to use to simulate an exciton about the molecules within a crystal.
	constant_rate_data : tuple.
		These are the constants in the rate law that are the same for each neighbour.
	conformationally_equivalent_data : dict.
		This dictionary contains information about which molecules are conformationally equivalent to each other. 
	molecule_bandgap_energy_data : dict.
		These are all the bandgap energies of the molecules in the crystal. Bandgap energies are in eV.
	dimer_reorganisation_energy_data : dict.
		These are the reorganisation energies of the dimers in the crystal. Reorganisation energies are in eV.
	coupling_value_data : dict.
		This dictionary contains all the coupling data between molecules in the dimers in the crystal. Coupling values are in eV.
	energetic_disorder : float
		This is the disorder that is associated with the DeltaE value
	coupling_disorder : float
		This is the disorder that is associated with the V12 value
	sim_time_limit : float
		This is the simulated time limit to run the kinetic Monte Carlo simulation over. Time given in ps.
	max_no_of_steps : int
		This is the maximum number of kmc steps to run the kinetic Monte Carlo simulation over.
	temp_folder_path : str. or None
		This is the path to place files as the KMC file is running for temporary storage. This is not vital for running a simulation. If set to None, no temporary folder will be created. Dafault: None 
	write_rate_constants_to_file : bool
		This indicates if you want to write a file called "kMC_sim_rate_constants.txt" that includes all the rate constant data for an exciton moving from the exciton donor it is currently on to any of the neighbouring exciton acceptors. 
	"""

	# First, setup the C string that specifies the 
	path_to_kMC_sim_C                = ctypes.c_char_p(path_to_kMC_sim.encode())
	path_to_kMC_sim_rate_constants_C = ctypes.c_char_p(path_to_kMC_sim_rate_constants.encode())

	# Second, setup the C string that specifies the kinetic model that will be used.
	kinetic_model_C = ctypes.c_char_p(kinetic_model.lower().encode())

	# Third, get the C tuple for the list of molecules in the unit cell crystal along with it's centre of mass.
	centre_of_masses_C = (Molecule_Centre_Of_Mass_CObject * len(molecule_list_and_com))()
	for index, (molname, centre_of_mass) in enumerate(molecule_list_and_com.items()):
		centre_of_masses_C[index] = Molecule_Centre_Of_Mass_CObject(int(molname), centre_of_mass[0], centre_of_mass[1], centre_of_mass[2])
	centre_of_masses_C_size = len(centre_of_masses_C)

	# Fourth, get the C tuple for the list containing the unit cell matrix.
	unit_cell_matrix_1D = [j for sub in unit_cell_matrix for j in sub]
	unit_cell_matrix_C = (ctypes.c_longdouble * len(unit_cell_matrix_1D))(*unit_cell_matrix_1D)
	unit_cell_matrix_C_size = len(unit_cell_matrix_C)

	# Fifth, get the C long double of the Marcus rate constant constants
	constant_rate_data_1C = ctypes.c_longdouble(constant_rate_data[0])
	constant_rate_data_2C = ctypes.c_longdouble(constant_rate_data[1])

	# Sixth, get the C tuple for the bandgap energies of the molecules in the crystal.
	bandgap_energies_C = (Bandgap_Energies_CObject * len(molecule_bandgap_energy_data))()
	for index, (molname, bandgap_energy) in enumerate(molecule_bandgap_energy_data.items()):
		bandgap_energies_C[index] = Bandgap_Energies_CObject(molname, bandgap_energy)
	bandgap_energies_C_size = len(bandgap_energies_C)

	# Seventh, get the C tuple for the reorganisation energies of the dimers in the crystal.
	reorganisation_energies_C = (Reorganisation_Energies_CObject * len(dimer_reorganisation_energy_data))()
	for index, ((mol1, mol2), reorganisation_energy) in enumerate(dimer_reorganisation_energy_data.items()):
		reorganisation_energies_C[index] = Reorganisation_Energies_CObject(mol1, mol2, reorganisation_energy)
	reorganisation_energies_C_size = len(reorganisation_energies_C)

	# Eighth, get the C objects for the coupling values of the dimers in the crystal.
	coupling_value_data_list = []
	for mol1, value1 in sorted(coupling_value_data.items()):
		for mol2, value2 in sorted(value1.items()):
			for (uniti, unitj, unitk), coupling_value in sorted(value2.items()):
				coupling_value_data_list.append((mol1, mol2, uniti, unitj, unitk, coupling_value))
	coupling_value_data_C = (Coupling_Value_Data_CObject * len(coupling_value_data_list))()
	for index, (mol1, mol2, uniti, unitj, unitk, coupling_value) in enumerate(coupling_value_data_list):
		coupling_value_data_C[index] = Coupling_Value_Data_CObject(mol1, mol2, uniti, unitj, unitk, coupling_value)
	del coupling_value_data_list
	coupling_value_data_size_C = len(coupling_value_data_C)

	# Ninth, obtain the C long double for the energetic (site energy) value, and specify if it is a percentage or not.
	if isinstance(energetic_disorder,str):
		energetic_disorder_is_percent_C = ctypes.c_bool(True)
		energetic_disorder_value_C  = ctypes.c_longdouble(float(energetic_disorder.replace('%','')))
	else:
		energetic_disorder_is_percent_C = ctypes.c_bool(False)
		energetic_disorder_value_C  = ctypes.c_longdouble(float(energetic_disorder))

	# Tenth, obtain the C long double for the coupling value, and specify if it is a percentage or not.
	if isinstance(coupling_disorder,str):
		coupling_disorder_is_percent_C = ctypes.c_bool(True)
		coupling_disorder_value_C  = ctypes.c_longdouble(float(coupling_disorder.replace('%','')))
	else:
		coupling_disorder_is_percent_C = ctypes.c_bool(False)
		coupling_disorder_value_C  = ctypes.c_longdouble(float(coupling_disorder))

	# Eleventh, get the C long double for the simulation time to simulate the KMC simulation for. 
	if sim_time_limit == 'inf':
		sim_time_limit_C = ctypes.c_longdouble(-1.0)
	else:
		sim_time_limit_C = ctypes.c_longdouble(float(sim_time_limit))

	# Twelfth, specify the maximum number of steps to perform if you want to put a KMC step limit on your simulation. 
	if max_no_of_steps == 'inf':
		max_no_of_steps_C = ctypes.c_longlong(-1)
	else:
		max_no_of_steps_C = ctypes.c_longlong(max_no_of_steps)

	# Thirteenth, specify what the starting molecule in the origin nit cell for the simulation will be. 
	if starting_molecule == None:
		starting_molecule = 'any'
	if isinstance(starting_molecule,str):
		if starting_molecule.lower() == 'any':
			molecule_names = list(coupling_value_data.keys())
			starting_molecule_C = ctypes.c_int(choice(molecule_names))
		elif starting_molecule.lower() == 'lowest':
			molecule_names = names_of_lowest_bandgap_molecules_in_crystal(molecule_reorganisation_energy_data, conformationally_equivalent_data)
			starting_molecule_C = ctypes.c_int(choice(molecule_names))
		else:
			raise Exception('Error: starting_molecule needs to be either "any", "lower", or the molecule or molecules you would like as the molecule the exciton begins on.')
	else:
		starting_molecule_C = ctypes.c_int(int(starting_molecule))

	# Fourtheenth, get the C string for the directory to temprarly store KMC data to while the simulation is running if desired. 
	if temp_folder_path is None:
		temp_folder_path = '.'
	temp_folder_path_C = ctypes.c_char_p(temp_folder_path.encode())

	# Fiftheenth, determine if you want to write the rate constants for each of the KMC steps for an exciton moving from the exciton donor it is currently on to one of the neighbouring exciton acceptors. 
	write_rate_constants_to_file_C     = ctypes.c_bool(write_rate_constants_to_file[0])
	write_500_rate_constants_to_file_C = ctypes.c_bool(write_rate_constants_to_file[1])

	# Sixteenth, load the EKMC C++ shared object code for running the simulation in. 
	print('Beginning to run KMC simulation in C++')
	if not os.path.exists(path_to_c_code):
		raise Exception('There was an error when trying to load the EKMC C++ shared object file. You may have not compiled the C++ code?\nCheck to see if this file exists: '+str(path_to_c_code)+'\n\nRun the following command in the terminal to compile the EKMC C++ code and try again: \n\nEKMC compile\n')
	try:
		run_kMC_algorithm = ctypes.CDLL(path_to_c_code)	
	except Exception as exception:
		raise Exception('There was an error when trying to run the EKMC C++ shared object file. See below:\n\n'+str(exception))

	# Seventeenth, run the EKMC C++ code. 
	run_kMC_algorithm.KMC_algorithm(path_to_kMC_sim_C, path_to_kMC_sim_rate_constants_C, centre_of_masses_C, centre_of_masses_C_size, unit_cell_matrix_C, unit_cell_matrix_C_size, kinetic_model_C, constant_rate_data_1C, constant_rate_data_2C, bandgap_energies_C, bandgap_energies_C_size, reorganisation_energies_C, reorganisation_energies_C_size, coupling_value_data_C, coupling_value_data_size_C, coupling_disorder_value_C, coupling_disorder_is_percent_C, energetic_disorder_value_C, energetic_disorder_is_percent_C, sim_time_limit_C, max_no_of_steps_C, starting_molecule_C, temp_folder_path_C, write_rate_constants_to_file_C, write_500_rate_constants_to_file_C)

