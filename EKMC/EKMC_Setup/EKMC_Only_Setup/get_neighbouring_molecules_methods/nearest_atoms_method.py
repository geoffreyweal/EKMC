"""
general_methods.py, Geoffrey Weal, 17/2/22

This script includes methods for obtaining neighbours by looking for molecules with non-hydrogen atoms within the vicinity of each other.
"""
import sys
from tqdm import tqdm
import multiprocessing as mp

from SUMELF import get_distance, make_folder, remove_folder
from ECCP.ECCP.get_neighbouring_molecules_methods.Neighbourhood_Generator           import Neighbourhood_Generator
from ECCP.ECCP.get_neighbouring_molecules_methods.Neighbourhood_Generator_Multi_CPU import Neighbourhood_Generator_Multi_CPU

def get_neighbours_nearest_atoms_method(molecules, molecule_graphs, max_distance, include_hydrogens_in_neighbour_analysis=False, no_of_cpus=1):
	"""
	This method will obtain the molecules in the neighbourhood of molecules in the origin unit cell. 

	Parameters
	----------
	molecules : list of ase.Atoms objects.
		These are all the individual molecules identified in the crystal that you want to determine neighbours for.
	molecule_graphs : list of networkx.graph
		This is a list of all the networkx graphs that describe the bonding system for each molecule. 
	max_distance : float.
		This is the maximum distance that atoms in two molecules can be within each other for the two molecules to be considered neighbouring. Given in Å. 
	include_hydrogens_in_neighbour_analysis: bool. 
		This tag indicates if you want to include hydrogens when accessing neighbours between molecules. Default: False
	no_of_cpus : int.
		This is the number of cpus available to use on this program. In most cases this should just be set to 1 cpu, however for very large system you may want to implement multiple cpus.

	Returns
	-------
	neighbourhood_molecules_info : list
		This is a list of all the molecules that neighbour each other within the vicinity given by max_distance.
	"""

	# First, use either the single or multi-cpu method for obtaining neighbouring molecules.
	if no_of_cpus == 1:
		neighbourhood_molecules_info = obtain_neighbours_with_single_cpu(molecules, molecule_graphs, max_distance)
	else:
		neighbourhood_molecules_info = obtain_neighbours_with_multi_cpu (molecules, molecule_graphs, max_distance, no_of_cpus)

	# Second, return the list of the information of neighbouring molecules in this crystal
	return neighbourhood_molecules_info

# ===============================================================================================================
# ===============================================================================================================
# ===============================================================================================================

def obtain_neighbours_with_multi_cpu(molecules, molecule_graphs, max_distance, no_of_cpus=1):
	"""
	This method will obtain the molecules in the neighbourhood of molecules in the origin unit cell. 

	Parameters
	----------
	molecules : list of ase.Atoms objects.
		These are all the individual molecules identified in the crystal that you want to determine neighbours for.
	molecule_graphs : list of networkx.graph
		This is a list of all the networkx graphs that describe the bonding system for each molecule. 
	max_distance : float.
		This is the maximum distance that atoms in two molecules can be within each other for the two molecules to be considered neighbouring. Given in Å. 
	no_of_cpus : int.
		This is the number of cpus available to use on this program. In most cases this should just be set to 1 cpu, however for very large system you may want to implement multiple cpus.

	Returns
	-------
	neighbourhood_molecules_info : list
		This is a list of all the molecules that neighbour each other within the vicinity given by max_distance.
	"""

	# First, create the manager to save lists to
	with mp.Manager() as manager: 

		# Second, create the list to collect information on the neighbouring molecules in the crystal. 
		neighbourhood_molecules_info = manager.list()

		# Third, run the multiprocessing jobs.
		pool = mp.Pool(no_of_cpus)
		no_of_neighbourhood_sets = int((len(molecules) * (len(molecules) + 1)) / 2)
		print('Obtaining neighbourhoods between molecules (Please wait until after 100%, as the process will still be running.)', file=sys.stderr)
		pool.map_async(obtain_neighbours_method_for_multi_cpu, tqdm(get_inputs(molecules, molecule_graphs, max_distance, neighbourhood_molecules_info), total=no_of_neighbourhood_sets, desc='Obtaining neighbouring pairs of molecules', unit='calc'))
		pool.close()
		pool.join()

		# Fourth, save the list from a multiprocessing Manager list to a regular list
		neighbourhood_molecules_info = list(neighbourhood_molecules_info)

	# Fifth, return neighbourhood_molecules_info
	return neighbourhood_molecules_info

def get_inputs(molecules, molecule_graphs, max_distance, neighbourhood_molecules_info):
	"""
	This method a generator designed to obtain the inputs for obtaining neighbours with multiple CPUs.

	Parameters
	----------
	molecules : list of ase.Atoms objects.
		These are all the individual molecules identified in the crystal that you want to determine neighbours for.
	molecule_graphs : list of networkx.graph
		This is a list of all the networkx graphs that describe the bonding system for each molecule. 
	max_distance : float.
		This is the maximum distance that atoms in two molecules can be within each other for the two molecules to be considered neighbouring. Given in Å. 
	neighbourhood_molecules_info : list
		This is a list of all the molecules that neighbour each other within the vicinity given by max_distance.
	"""

	# First, get the first molecule/monomer. 
	for index1 in range(len(molecules)): 
		molecule1 = molecules[index1]
		molecule_graph1 = molecule_graphs[index1]

		# Second, get the second molecule/monomer. This could be the same molecule as index1, but will be displaced to a different position.
		for index2 in range(index1,len(molecules)): 
			molecule2 = molecules[index2]
			molecule_graph2 = molecule_graphs[index2]

			# Third, yield the inputs
			yield (index1, index2, molecule1, molecule2, molecule_graph1, molecule_graph2, max_distance, neighbourhood_molecules_info)

def obtain_neighbours_method_for_multi_cpu(input_variables):
	"""
	This method will obtain neighbourhood information between molecules in the crystal based on the distances the closest atoms in each molecule. 

	Parameters
	----------
	molecules : list of ase.Atoms objects.
		These are all the individual molecules identified in the crystal that you want to determine neighbours for.
	molecule_graphs : list of networkx.graph
		This is a list of all the networkx graphs that describe the bonding system for each molecule. 
	max_distance : float.
		This is the maximum distance that atoms in two molecules can be within each other for the two molecules to be considered neighbouring. Given in Å. 
	no_of_cpus : int.
		This is the number of cpus available to use on this program. In most cases this should just be set to 1 cpu, however for very large system you may want to implement multiple cpus.
	neighbourhood_molecules_info : list
		This is a list of all the molecules that neighbour each other within the vicinity given by max_distance.
	"""

	# First, obtain the variables for processing from the input_variables list.
	index1, index2, molecule1, molecule2, molecule_graph1, molecule_graph2, max_distance, neighbourhood_molecules_info = input_variables

	# Second, create the neighbourhood generator that will create all the neighbouring pairs between molecules that could exist in the crystal.
	neighbourhood_generator_object = Neighbourhood_Generator_Multi_CPU(index1, index2, molecule1, molecule2, molecule_graph1, molecule_graph2, molecule1.get_cell())
	neighbourhood_generator = neighbourhood_generator_object.generator()

	# Third, identify neighbours based on if there are any atoms in each molecule that are within max_distance distance of each other
	for index1, index2, positions1, positions2, displacement, unit_cell_displacement in neighbourhood_generator:
		
		# 3.1: If any atom between each molecule is within max_distance, you have a neighbouring pair. 
		are_molecules_within_max_neighbour_distance, shortest_distance = determine_if_molecules_within_max_distance(positions1, positions2, displacement, max_distance)
		if are_molecules_within_max_neighbour_distance:
			neighbourhood_molecules_info.append((index1, index2, unit_cell_displacement, displacement, shortest_distance))

		# 3.2: Send the result of if the neighbouring pair was accepted or not back to the generator
		end_of_for_loop_check = neighbourhood_generator.send(are_molecules_within_max_neighbour_distance)
		if not (end_of_for_loop_check == 'Go to for loop'):
			raise Exception('Communication error of Neighbourhood_Generator_Multi_CPU generator with for loop.')
			
# ===============================================================================================================
# ===============================================================================================================
# ===============================================================================================================

def obtain_neighbours_with_single_cpu(molecules, molecule_graphs, max_distance):
	"""
	This method will obtain neighbouring pairs of molecules in the crystal based on the distances the closest atoms in each molecule. 

	Parameters
	----------
	molecules : list of ase.Atoms objects.
		These are all the individual molecules identified in the crystal that you want to determine neighbours for.
	molecule_graphs : list of networkx.graph
		This is a list of all the networkx graphs that describe the bonding system for each molecule. 
	max_distance : float.
		This is the maximum distance that atoms in two molecules can be within each other for the two molecules to be considered neighbouring. Given in Å. 

	Returns
	-------
	neighbourhood_molecules_info : list
		This is a list of all the molecules that neighbour each other within the vicinity given by max_distance.
	"""

	# First, create the neighbourhood generator that will create all the neighbouring pairs that could exist in the crystal.
	neighbourhood_generator_object = Neighbourhood_Generator(molecules, molecule_graphs, molecules[0].get_cell())
	neighbourhood_generator = neighbourhood_generator_object.generator()

	# Second, identify neighbouring pairs of molecules based on if there are any atoms in each molecule that are within max_distance distance of each other
	neighbourhood_molecules_info = []
	for index1, index2, positions1, positions2, displacement, unit_cell_displacement in neighbourhood_generator:
		
		# 2.1: If any atom between each molecule is within max_distance, you have a neighbouring pair of molecules. 
		are_molecules_within_max_neighbour_distance, shortest_distance = determine_if_molecules_within_max_distance(positions1, positions2, displacement, max_distance)
		if are_molecules_within_max_neighbour_distance:
			neighbourhood_molecules_info.append((index1, index2, unit_cell_displacement, displacement, shortest_distance))

		# 2.2: Send the result of if the neighbouring pair of molecules was accepted or not back to the generator
		end_of_for_loop_check = neighbourhood_generator.send(are_molecules_within_max_neighbour_distance)
		if not (end_of_for_loop_check == 'Go to for loop'):
			raise Exception('Communication error of Neighbourhood_Generator generator with for loop.')

	# Third, return the list of neighbouring pairs of molecules.
	return neighbourhood_molecules_info

# ===============================================================================================================
# ===============================================================================================================
# ===============================================================================================================

def determine_if_molecules_within_max_distance(positions1, positions2, displacement, max_distance):
	"""
	This method will determine if two molecules are within max_distance of each other. 

	Parameters
	----------
	positions1 : numpy.array
		These are the positions of atoms in molecule 1.
	positions2 : numpy.array
		These are the positions of atoms in molecule 2.
	displacement : numpy.array
		This is the displacement to move molecule 2 by.
	max_distance : float.
		This is the maximum distance that atoms in two molecules can be within each other for the two molecules to be considered neighbouring. Given in Å. 

	Returns
	-------
	True if these two molecules are within max_distance of each other. False if not. 
	"""

	# First, determine the shortest distance between the two molecules.
	shortest_distance = float('inf')
	for pos_index1 in range(len(positions1)):
		for pos_index2 in range(len(positions2)):
			distance = round(get_distance(positions1[pos_index1], positions2[pos_index2] + displacement), 4)
			# If we have found a distance that is less than max_distance, then these two molcules are a neighbouring pair.
			if (distance <= shortest_distance):
				shortest_distance = distance

	# Second, determine if the distance is less than the maximum distance
	return (shortest_distance <= max_distance), shortest_distance			

# ===============================================================================================================
# ===============================================================================================================
# ===============================================================================================================




