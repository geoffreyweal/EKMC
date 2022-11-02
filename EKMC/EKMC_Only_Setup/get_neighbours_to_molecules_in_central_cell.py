"""
get_neighbours_to_molecules_in_central_cell.py, Geoffrey Weal, 20/3/22

get_neighbours_to_molecules_in_central_cell is a method that will give all the neighbours 
"""
import numpy as np

from tqdm import tqdm
from tqdm.contrib.concurrent import process_map

from EKMC.EKMC_Only_Setup.get_neighbours_methods.get_expanded_cell_corner_points import get_expanded_cell_corner_points
from EKMC.EKMC_Only_Setup.get_neighbours_methods.rate_constant_data_methods      import rate_constant_data_for_same_molecule_in_different_cells
from EKMC.EKMC_Only_Setup.get_neighbours_methods.rate_constant_data_methods      import rate_constant_data_for_different_molecules_in_origin_cell
from EKMC.EKMC_Only_Setup.get_neighbours_methods.rate_constant_data_methods      import rate_constant_data_for_different_molecules_in_different_cells

def get_neighbours_to_molecules_in_central_cell(kinetic_model, molecules, crystal_cell_lattice, short_range_coupling_data, long_range_coupling_data, kinetics_details, neighbourhood_rCut=40.0, no_of_cpus_for_setup=1):
	"""
	This method will determine how molecules in the crystral neighbour each other over an extended lattice.

	This method will also gather other information, such as distances, orbital overlaps, coulomb energies, etc.

	Parameters
	----------
	kinetic_model : str.
		This is the kinetic model the user would like to use in their kinetic Monte Carlo algorithm upon the crystal.
	molecules : list of ase.Atoms
		This is a list of all the molecules in your crystal
	crystal_cell_lattice : ase.Cell
		This is the unit cell matrix
	short_range_coupling_data : dict.
		This is all the short range coupling energy for each dimer involving each molecule from the unit cell.
	long_range_coupling_data : dict.
		This is all the long range coupling data.
	kinetics_details : dict.
		These are the details required for performing the kinetic Monte Carlo algorithm.
	neighbourhood_rCut : float
		This is the circumference around the COM of each molecule to add to the neighbourhood.
	no_of_cpus_for_setup : int.
		This is the number of cpus used to setup the EKMC simulations.
		
	Returns
	------- 
	all_local_neighbourhoods : dict.
		This dictionary contains all the information about the neighbourhoods that surrounded each molecule in your crystal.
	"""

	# First, print that the rates will be obtained from the energy data.
	print('-------------')
	print(('Getting rate constant values between molecules in surrounding unit cells.').upper())

	# Second, get all unit cells that are within the neighbourhood_rCut of the origin unit cell.
	cell_points, surrounding_cell_points = get_expanded_cell_corner_points(crystal_cell_lattice, neighbourhood_rCut)
	all_cell_points = cell_points + surrounding_cell_points
	displacement_vectors = [np.matmul(np.array(cell_point),crystal_cell_lattice) for cell_point in all_cell_points]

	# Third, get the centre of masses of each molecule. This will represent that molecules position in the unit cell.
	centre_of_masses = [molecule.get_center_of_mass() for molecule in molecules]

	# Fourth, determine all the molecules that are within neighbourhood_rCut of each molecule in the central unit cell.
	# Also, get the rate constant values for each molecule that do not change with disorder. 
	if no_of_cpus_for_setup == 1:
		print('Obtaining rate constant information between molecules via a single CPU')
		all_local_neighbourhoods = get_rate_constant_information_for_single_cpu(molecules, centre_of_masses, kinetic_model, kinetics_details, short_range_coupling_data, all_cell_points, displacement_vectors)
	else:
		print('Obtaining rate constant information between molecules via multiple CPUs')
		all_local_neighbourhoods = get_rate_constant_information_for_multi_cpu (molecules, centre_of_masses, kinetic_model, kinetics_details, short_range_coupling_data, all_cell_points, displacement_vectors, no_of_cpus_for_setup)

	'''
	# Fifth, sort the dict in all_local_neighbourhoods. This just makes it easier for a human to see what is happening, but is not necessary for the running of this algorithm.
	for key1 in list(all_local_neighbourhoods.keys()):
		for key2 in list(all_local_neighbourhoods[key1].keys()):
			rate_constant_data_for_all_cell_points = all_local_neighbourhoods[key1][key2]
			rate_constant_data_for_all_cell_points = [(cell_point, rate_constant_data) for cell_point, rate_constant_data in rate_constant_data_for_all_cell_points.items()]
			rate_constant_data_for_all_cell_points.sort(key=lambda cell_point: [order_number(x) for x in cell_point])
			all_local_neighbourhoods[key1][key2] = {cell_point: rate_constant_data for cell_point, rate_constant_data in rate_constant_data_for_all_cell_points}
	'''

	# Sixth, return all_local_neighbourhoods
	print('-------------')
	return all_local_neighbourhoods
	
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def get_rate_constant_information_for_single_cpu(molecules, centre_of_masses, kinetic_model, kinetics_details, short_range_coupling_data, all_cell_points, displacement_vectors):
	"""
	This method will cycle through the molecules in the crystal and obtain the kinetic information needed to obtain rate constants for a EKMC simulation.

	Parameters
	----------
	molecules : list of ase.Atoms
		This is the list of molecules in the crystal to cycle through.
	centre_of_masses : list of numpy.arrays
		These are the centre of masses for each of the molecules in the crystal (given in the molecules list).
	"""

	# First, get the number of pairs of molecules that will be cycled through.
	nn = int(float(len(molecules)+1)*(float(len(molecules))/2.0))

	# Second, set up the progress bar
	pbar = tqdm(total=nn,unit='task')

	# Third, set up the all_local_neighbourhoods dictionary.
	all_local_neighbourhoods = {}

	# Fourth, Obtain all the kinetic information needed to obtain rate constants between molecule in a crystal for a EKMC simulation.
	for molecule_coupling_information in get_list_of_couplings_to_calculate_rate_constants_for(molecules, centre_of_masses):

		# 4.1: indicate to the progress bar what is being done
		if len(molecule_coupling_information) == 3:
			index1, _, _ = molecule_coupling_information
			pbar.set_description('Comparing molecule '+str(index1+1)+' with itself in different cells')
		elif len(molecule_coupling_information) == 6:
			index1, _, _, index2, _, _ = molecule_coupling_information
			pbar.set_description('Comparing molecule '+str(index1+1)+' and molecule '+str(index2+1)+' in the same and different unit cells')
		else:
			raise Exception('Huh?')

		# 4.2: Obtain the rate constant information data between molecule 1 and molecule 2 across various unit cells
		data_dump = get_rate_constant_information_single_process((molecule_coupling_information, kinetic_model, kinetics_details, short_range_coupling_data, all_cell_points, displacement_vectors))

		# 4.3: Store the data in all_local_neighbourhoods.
		for index1, index2, cell_point, rate_constant_data in data_dump:
			if does_entry_exist_in_all_local_neighbourhoods_dictionary(all_local_neighbourhoods, index1, index2, cell_point):
				raise Exception('Error: Found find (index1, index2, cell_point) = '+str(index1, index2, cell_point)+' in all_local_neighbourhoods already. Maybe two entries for the same molecule pair and relative cell_point. This should not happen. Check this.')
			all_local_neighbourhoods.setdefault(index1,{}).setdefault(index2,{})[cell_point] = rate_constant_data

		# 4.4: update the progress bar.
		pbar.update(1)

	# Fifth, close the progress bar. 
	pbar.close()

	# Sixth, return the all_local_neighbourhoods dictionary
	return all_local_neighbourhoods

def get_rate_constant_information_for_multi_cpu(molecules, centre_of_masses, kinetic_model, kinetics_details, short_range_coupling_data, all_cell_points, displacement_vectors, no_of_cpus_for_setup):
	"""
	This method will cycle through the molecules in the crystal and obtain the kinetic information needed to obtain rate constants for a EKMC simulation.

	Parameters
	----------
	molecules : list of ase.Atoms
		This is the list of molecules in the crystal to cycle through.
	centre_of_masses : list of numpy.arrays
		These are the centre of masses for each of the molecules in the crystal (given in the molecules list).
	"""

	# First, get the number of pairs of molecules that will be cycled through.
	nn = int(float(len(molecules)+1)*(float(len(molecules))/2.0))

	# Second, set up a generator to provide the input values
	def input_values(molecules, centre_of_masses, kinetic_model, kinetics_details, short_range_coupling_data, all_cell_points, displacement_vectors):
		for molecule_coupling_information in get_list_of_couplings_to_calculate_rate_constants_for(molecules, centre_of_masses):
			yield (molecule_coupling_information, kinetic_model, kinetics_details, short_range_coupling_data, all_cell_points, displacement_vectors)

	
	'''
	# from https://rednafi.github.io/reflections/running-tqdm-with-python-multiprocessing.html
    with mp.Pool(processes=no_of_cpus_for_setup) as pool:
        results = tqdm(
            pool.imap_unordered(get_rate_constant_information_single_process, inputs, chunksize=1, input_values(molecules, centre_of_masses, kinetic_model, kinetics_details, short_range_coupling_data, all_cell_points, displacement_vectors)),
            total=nn, unit='task',
        )  # 'total' is redundant here but can be useful
        # when the size of the iterable is unobvious
    '''

    # Third, perform the get_rate_constant_information_single_process method with multiprocessing.
	main_data_dump = process_map(get_rate_constant_information_single_process, input_values(molecules, centre_of_masses, kinetic_model, kinetics_details, short_range_coupling_data, all_cell_points, displacement_vectors), max_workers=no_of_cpus_for_setup, total=nn, unit='task')

	# Fourth, sort the lists in all_local_neighbourhoods and remove any entries that are empty. This just makes it easier for a human to see what is happening, but is not necessary for the running of this algorithm.
	all_local_neighbourhoods = {}
	for mol1_mol2_data_dump in main_data_dump:
		for index1, index2, cell_point, rate_constant_data in mol1_mol2_data_dump:
			if does_entry_exist_in_all_local_neighbourhoods_dictionary(all_local_neighbourhoods, index1, index2, cell_point):
				raise Exception('Error: Found find (index1, index2, cell_point) = '+str(index1, index2, cell_point)+' in all_local_neighbourhoods already. Maybe two entries for the same molecule pair and relative cell_point. This should not happen. Check this.')
			all_local_neighbourhoods.setdefault(index1,{}).setdefault(index2,{})[cell_point] = rate_constant_data

	# Fifth, return the all_local_neighbourhoods dictionary
	return all_local_neighbourhoods

# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def get_rate_constant_information_single_process(input_data):
	"""
	This method will gather rate constant information for each pair of molecule in the crystal.

	Parameters
	----------
	molecule_coupling_information : list of ase.Atoms
		This is the list of molecules in the crystal to cycle through.	
	"""

	molecule_coupling_information, kinetic_model, kinetics_details, short_range_coupling_data, all_cell_points, displacement_vectors = input_data

	if len(molecule_coupling_information) == 3:
		# 4.1: If index1 equal index2, then get all the rate_constant_data between itself in different unit cells
		index1, molecule1, centre_of_mass1 = molecule_coupling_information
		all_local_neighbourhoods_subset = rate_constant_data_for_same_molecule_in_different_cells(kinetic_model, index1, molecule1, centre_of_mass1, kinetics_details, short_range_coupling_data, {}, all_cell_points, displacement_vectors)
		return all_local_neighbourhoods_subset

	elif len(molecule_coupling_information) == 6:
		# 4.2: If index1 not equal to index2, then get all the rate_constant_data between:
		#    * Molecule index1 and molecule index2 within the same unit cell (origin unit cell).
		#    * Molecule index1 and molecule index2 in different unit cells
		index1, molecule1, centre_of_mass1, index2, molecule2, centre_of_mass2 = molecule_coupling_information
		all_local_neighbourhoods_subset_1 = rate_constant_data_for_different_molecules_in_origin_cell    (kinetic_model, index1, index2, molecule1, molecule2, centre_of_mass1, centre_of_mass2, kinetics_details, short_range_coupling_data, {})
		all_local_neighbourhoods_subset_2 = rate_constant_data_for_different_molecules_in_different_cells(kinetic_model, index1, index2, molecule1, molecule2, centre_of_mass1, centre_of_mass2, kinetics_details, short_range_coupling_data, {}, all_cell_points, displacement_vectors)
		return all_local_neighbourhoods_subset_1 + all_local_neighbourhoods_subset_2

	else:
		raise Exception('Huh?')

def get_list_of_couplings_to_calculate_rate_constants_for(molecules, centre_of_masses):
	"""
	This generator will provide information for looping through a list of molecules.

	Parameters
	----------
	molecules : list of ase.Atoms
		This is the list of molecules in the crystal to cycle through.
	centre_of_masses : list of numpy.arrays
		These are the centre of masses for each of the molecules in the crystal (given in the molecules list).
	"""

	# First, for index1 molecule in molecules 
	for index1 in range(len(molecules)):

		# Second, gather information about molecule index1
		molecule1 = molecules[index1]
		centre_of_mass1 = centre_of_masses[index1]

		# Third, for index2 molecule in molecules
		for index2 in range(index1,len(molecules)): 

			if index1 == index2:

				# Fourth, if index1 is the same as index2, return info about index1.
				yield (index1, molecule1, centre_of_mass1)

			else:

				# Fifth, if index1 is no the same as index2, return info about index1 and index2.
				molecule2 = molecules[index2]
				centre_of_mass2 = centre_of_masses[index2]
				yield (index1, molecule1, centre_of_mass1, index2, molecule2, centre_of_mass2)

# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def does_entry_exist_in_all_local_neighbourhoods_dictionary(all_local_neighbourhoods, index1, index2, cell_point):
	"""
	This method is designed to determine if their exists an entry in the all_local_neighbourhoods dictionary.

	Parameters
	----------
	all_local_neighbourhoods : dict
		This is the information about the rate constant data between all molecules in the crystal.
	index1 : int
		This is the index of the first molecule in the crystal.
	index2 : int
		This is the index of the second molecule in the crystal.
	cell_point : tuple of three ints
		This is the relative difference in unit cell between first molecule and second molecule. 

	Returns
	------- 
	True if there exists an entry for all_local_neighbourhoods[index1][index2][cell_point], otherwise will return False. 
	"""

	# First, is there an index1 entry in all_local_neighbourhoods
	if not (index1 in all_local_neighbourhoods.keys()):
		return False

	# Second, is there an index2 entry in all_local_neighbourhoods[index1]
	if not (index2 in all_local_neighbourhoods[index1].keys()):
		return False

	# Third, is there an cell_point entry in all_local_neighbourhoods[index1][index2]
	if not (cell_point in all_local_neighbourhoods[index1][index2].keys()):
		return False

	# Fourth, if here, there exists an entry for all_local_neighbourhoods[index1][index2][cell_point], return True
	return True

# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------




