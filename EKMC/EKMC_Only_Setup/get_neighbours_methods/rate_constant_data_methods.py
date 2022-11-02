"""
rate_constant_data_methods.py, Geoffrey Weal, 12/8/22

This script contains methods for obtaining rate constant data for same or different molecules in same or different unit cells.
"""

from copy import deepcopy
import numpy as np
from EKMC.EKMC_Only_Setup.get_neighbours_methods.get_rate_constant_data import get_rate_constant_data

def rate_constant_data_for_same_molecule_in_different_cells(kinetic_model, index, molecule, centre_of_mass, kinetics_details, electronic_coupling_data, all_local_neighbourhoods, all_cell_points, displacement_vectors):
	"""
	This method is designed to obtain the rate constant for two of the same molecule that are in different unit cells.

	Note that this method will make updates to the all_local_neighbourhoods dictionary.

	Parameters
	----------
	kinetic_model : str.
		This is the kinetic model that you would like to use for running the kinetic Monte Carlo algorithm.
	index : int
		This is the position of the molecule in the molecules list.
	molecule : ase.Atoms
		This is the molecule
	centre_of_mass : numpy.array
		This is the xyz position of the molecule's centre of mass
	kinetics_details : dict
		This holds all the kinetic details of variables given by the user.
	electronic_coupling_data : dict.
		This is all the energetic energy for each dimer involving each molecule from the unit cell.
	all_local_neighbourhoods : dict.
		This is the dictionary that holds all the rate constant data for molecule one and molecule two around displacement points.
	all_cell_points : list of tuples
		This is the list of all cell points to displace the "2nd" molecule by.
	displacement_vectors : list of numpy.array
		This is the list of all displacement_vectors to displace the "2nd" molecule by, which correspond to the displacement cell points in all_cell_points.
	"""

	# Set up list
	all_local_neighbourhoods_subset = []

	# Get the neighbourhoods of other unit cell surrounding the central unit cell.
	for cell_point, displacement_vector in zip(all_cell_points, displacement_vectors):
		#minus_cell_point = tuple(-uc for uc in cell_point)
		# Get inputs for getting rate constant data
		# Note that the distance and electronic_coupling for mol1 -> mol2+cell_point are the same as for mol2 -> mol1-cell_point
		electronic_coupling = electronic_coupling_data.get((index+1, index+1, *cell_point), None)
		# We calculate the rate_constant_data1 and rate_constant_data2 as the kinetics_details for molecule 1 and molecule 2 may be different (for the process mol1 -> mol2 compared to the process mol2 -> mol1)
		# If mol 1 and mol2 have same attributes in kinetics_details, probably rate_constant_data1 == rate_constant_data2
		# Focusing on mol1 -> mol2+cell_point. 
		rate_constant_data1 = get_rate_constant_data(kinetic_model, molecule, molecule, displacement_vector, electronic_coupling, kinetics_details)
		# Only add if the coupling energy is non-zero
		if not (rate_constant_data1[0] == 0.0):
			all_local_neighbourhoods_subset.append((index, index, deepcopy(cell_point), rate_constant_data1))

	# Return rate constant information
	return all_local_neighbourhoods_subset

# ============================================================================================================================================================================================

zero_point = (0,0,0)
zero_point_np = np.array((0.,0.,0.))
def rate_constant_data_for_different_molecules_in_origin_cell(kinetic_model, index1, index2, molecule1, molecule2, centre_of_mass1, centre_of_mass2, kinetics_details, electronic_coupling_data, all_local_neighbourhoods):
	"""
	This method is designed to obtain the rate constant for two different molecule that are in the same unit cell (being the origin cell).

	Note that this method will make updates to the all_local_neighbourhoods dictionary.

	Parameters
	----------
	kinetic_model : str.
		This is the kinetic model that you would like to use for running the kinetic Monte Carlo algorithm.
	index1 : int
		This is the position of molecule 1 in the molecules list.
	index2 : int
		This is the position of molecule 2 in the molecules list.
	molecule1 : ase.Atoms
		This is molecule 1.
	molecule2 : ase.Atoms 
		This is molecule 2.
	centre_of_mass1 : numpy.array
		This is the xyz position of molecule 1's centre of mass.
	centre_of_mass2 : numpy.array
		This is the xyz position of molecule 2's centre of mass.
	kinetics_details : dict
		This holds all the kinetic details of variables given by the user.
	electronic_coupling_data : dict.
		This is all the energetic energy for each dimer involving each molecule from the unit cell.
	all_local_neighbourhoods : dict.
		This is the dictionary that holds all the rate constant data for molecule one and molecule two around displacement points.
	"""

	# First, get the neighbourhoods within the central unit cell
	# Note that the distance and electronic_coupling for mol1 -> mol2 are the same as for mol2 -> mol1
	electronic_coupling = electronic_coupling_data.get((index1+1, index2+1, *zero_point), None)

	# Second, we calculate the rate_constant_data1 and rate_constant_data2 as the kinetics_details for molecule 1 and molecule 2 may be different (for the process mol1 -> mol2 compared to the process mol2 -> mol1)
	# If mol1 and mol2 have same attributes in kinetics_details, probably rate_constant_data1 == rate_constant_data2

	# 2.1: Set up list
	all_local_neighbourhoods_subset = []

	# 2.1: Focusing on mol1 -> mol2
	rate_constant_data1 = get_rate_constant_data(kinetic_model, molecule1, molecule2, zero_point_np, electronic_coupling, kinetics_details)
	# Only add if the coupling energy is non-zero
	if not (rate_constant_data1[0] == 0.0):
		all_local_neighbourhoods_subset.append((index1, index2, deepcopy(zero_point), rate_constant_data1))
	
	# 2.2: Focusing on mol2 -> mol1, note: -zero_point_np == zero_point_np
	rate_constant_data2 = get_rate_constant_data(kinetic_model, molecule2, molecule1, zero_point_np, electronic_coupling, kinetics_details)
	# Only add if the coupling energy is non-zero
	if not (rate_constant_data2[0] == 0.0):
		all_local_neighbourhoods_subset.append((index2, index1, deepcopy(zero_point), rate_constant_data2))

	# Third, return all_local_neighbourhoods_subset list
	return all_local_neighbourhoods_subset

# ============================================================================================================================================================================================

def rate_constant_data_for_different_molecules_in_different_cells(kinetic_model, index1, index2, molecule1, molecule2, centre_of_mass1, centre_of_mass2, kinetics_details, electronic_coupling_data, all_local_neighbourhoods, all_cell_points, displacement_vectors):
	"""
	This method is designed to obtain the rate constant for two different molecule that are in the same unit cell (being the origin cell).

	Note that this method will make updates to the all_local_neighbourhoods dictionary.

	Parameters
	----------
	kinetic_model : str.
		This is the kinetic model that you would like to use for running the kinetic Monte Carlo algorithm.
	index1 : int
		This is the position of molecule 1 in the molecules list.
	index2 : int
		This is the position of molecule 2 in the molecules list.
	molecule1 : ase.Atoms
		This is molecule 1.
	molecule2 : ase.Atoms 
		This is molecule 2.
	centre_of_mass1 : numpy.array
		This is the xyz position of molecule 1's centre of mass.
	centre_of_mass2 : numpy.array
		This is the xyz position of molecule 2's centre of mass.
	kinetics_details : dict
		This holds all the kinetic details of variables given by the user.
	electronic_coupling_data : dict.
		This is all the energetic energy for each dimer involving each molecule from the unit cell.
	all_local_neighbourhoods : dict.
		This is the dictionary that holds all the rate constant data for molecule one and molecule two around displacement points.
	all_cell_points : list of tuples
		This is the list of all cell points to displace the "2nd" molecule by.
	displacement_vectors : list of numpy.array
		This is the list of all displacement_vectors to displace the "2nd" molecule by, which correspond to the displacement cell points in all_cell_points.
	"""

	# Prelim Step: Set up list
	all_local_neighbourhoods_subset = []

	# First, get the neighbourhoods of other unit cell surrounding the central unit cell.
	for cell_point, displacement_vector in zip(all_cell_points, displacement_vectors):

		# Second, Check that this cell point and it's minus have not already been recorded in all_local_neighbourhoods
		minus_cell_point = tuple(-uc for uc in cell_point)
		'''
		if any([(cell_point == neighbourhood_cell_point) for neighbourhood_cell_point in all_local_neighbourhoods[index1][index2].keys()]):
			raise Exception('huh?')
		if any([(minus_cell_point == neighbourhood_cell_point) for neighbourhood_cell_point in all_local_neighbourhoods[index2][index1].keys()]):
			raise Exception('huh?')

		# Third, Check that this cell point and it's minus have not already been recorded in all_local_neighbourhoods_subset
		if any([(cell_point == neighbourhood_cell_point) for _, _, neighbourhood_cell_point, _ in all_local_neighbourhoods_subset]):
			raise Exception('huh?')
		if any([(minus_cell_point == neighbourhood_cell_point) for _, _, neighbourhood_cell_point, _ in all_local_neighbourhoods_subset]):
			raise Exception('huh?')
		'''

		# Fourth, get inputs for getting rate constant data. 
		# Note that the distance and electronic_coupling for mol1 -> mol2 are the same as for mol2 -> mol1
		electronic_coupling = electronic_coupling_data.get((index1+1, index2+1, *cell_point), None)

		# Fifth, we calculate the rate_constant_data1 and rate_constant_data2 as the kinetics_details for molecule 1 and molecule 2 may be different (for the process mol1 -> mol2 compared to the process mol2 -> mol1)
		# If mol 1 and mol2 have same attributes in kinetics_details, probably rate_constant_data1 == rate_constant_data2

		# 5.1: Focusing on mol1 -> mol2+cell_point. 
		rate_constant_data1 = get_rate_constant_data(kinetic_model, molecule1, molecule2,  displacement_vector, electronic_coupling, kinetics_details)
		# Only add if the coupling energy is non-zero
		if not (rate_constant_data1[0] == 0.0):
			all_local_neighbourhoods_subset.append((index1, index2, deepcopy(cell_point), rate_constant_data1))
			#all_local_neighbourhoods[index1][index2].append((deepcopy(cell_point), rate_constant_data1))

		# 5.2: Focusing on mol2 -> mol1-cell_point
		rate_constant_data2 = get_rate_constant_data(kinetic_model, molecule2, molecule1, -displacement_vector, electronic_coupling, kinetics_details)
		# Only add if the coupling energy is non-zero
		if not (rate_constant_data2[0] == 0.0):
			all_local_neighbourhoods_subset.append((index2, index1, deepcopy(minus_cell_point), rate_constant_data2))
			#all_local_neighbourhoods[index2][index1].append((deepcopy(minus_cell_point), rate_constant_data2))

	# Sixth, return all_local_neighbourhoods_subset list
	return all_local_neighbourhoods_subset

# ============================================================================================================================================================================================





