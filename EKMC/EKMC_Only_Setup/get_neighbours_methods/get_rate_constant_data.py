"""
get_rate_constant_data.py, Geoffrey Weal, 23/3/22

This script is designed to obtain all the values that are used in obtaining rate constants that do not change between moving from unit cell to unit cell.
"""
from copy import deepcopy

from EKMC.EKMC_Only_Setup.calculators.get_coulomb_energy import get_coulomb_energy

from EKMC.EKMC_Only_Setup.get_neighbours_methods.get_rate_constant_methods.Marcus_parameters import get_Marcus_parameters
from EKMC.EKMC_Only_Setup.get_neighbours_methods.get_rate_constant_methods.MLJ_parameters    import get_MLJ_parameters

def get_rate_constant_data(kinetic_model, molecule1, molecule2, displacement_vector, electronic_coupling, original_kinetics_details):
	"""
	This method will obtain all the non-changing components used to obtain the the rate constants. 

	None of these values are dependent on the disorder values. 

	Parameters
	----------
	molecule1 : ase.Atoms
		This is the first molecule. This is the focus molecule, where we consider that the exciton is on this molecule. Therefore, we get rate data of an exciton coming from this molecule,
	molecule2 : ase.Atoms
		This is the second molecule. We consider this is the molecule that will be recieving the exciton from molecule1. 
	displacement_vector : numpy.array
		This is the displacement vector to move the second molecule into the unit cell you want to place it in.
	electronic_coupling : float
		This is the electron coupling between molecule 1 and molecule 2 (where molecule 2 is in the unit cell given by displacement_vector). Given in eV.
	original_kinetics_details : dict.
		This dictionary contains all the relavant information required for obtaining the rate constants.

	Returns
	-------
	rate_constant_data : tuple
		The values required for the rate constant for different molecules that are not dependent on disorder.
	"""

	# First, copy of the kinetics_details.
	kinetics_details = deepcopy(original_kinetics_details)

	# Second, pop the relative_permittivity. 
	relative_permittivity = kinetics_details.pop('relative_permittivity')
	if relative_permittivity is None:
		relative_permittivity = 1.0
	
	# Third, get the value for V12 (coupling_energy).
	if electronic_coupling is not None:
		coupling_energy = electronic_coupling
	else:
		coupling_energy = get_coulomb_energy(molecule1, molecule2, displacement_vector, relative_permittivity)

	# Fourth, get the rate constant data for the kinetic model you want to use
	if   kinetic_model.lower() == 'marcus':
		rate_constant_data = get_Marcus_parameters(molecule1, molecule2, displacement_vector, coupling_energy, **kinetics_details)
	elif kinetic_model.lower() == 'mlj':
		rate_constant_data = get_MLJ_parameters   (molecule1, molecule2, displacement_vector, coupling_energy, **kinetics_details)
	else:
		raise Exception('Error: You must set "kinetic_model" to either "Marcus" or "MLJ". Your kinetic_model is set to: '+str(kinetic_model)+'. Check this out.')

	# Fifth, return the rate constant data
	return deepcopy(rate_constant_data)

'''
def determine_if_molecules_within_max_dimer_distance(positions1, positions2, displacement, max_dimer_distance):
	"""
	This method will determine if two molecules are within max_dimer_distance of each other. 

	Parameters
	----------
	positions1 : numpy.array
		These are the positions of atoms in molecule 1.
	positions2 : numpy.array
		These are the positions of atoms in molecule 2.
	displacement : numpy.array
		This is the displacement to move molecule 2 by.
	max_dimer_distance : float.
		This is the maximum distance that atoms in two molecules can be within each other for the two molecules to be considered as a dimer pair. Given in Å. 

	Returns
	-------
	True if these two molecules are within max_dimer_distance of each other. False if not. 
	"""

	# First, determine the shortest distance between the two molecules.
	shortest_distance = float('inf')
	for pos_index1 in range(len(positions1)):
		for pos_index2 in range(len(positions2)):
			distance = round(get_distance(positions1[pos_index1],positions2[pos_index2] + displacement),4)
			# If we have found a distance that is less than max_dimer_distance, then these two molcules are a dimer.
			if (distance <= shortest_distance):
				shortest_distance = distance

	# Second, determine if the distance is less than the maximum dimer distance
	return (shortest_distance <= max_dimer_distance), shortest_distance
'''



