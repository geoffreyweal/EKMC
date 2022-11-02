"""
get_electronic_coupling_data.py, Geoffrey Weal, 19/4/22

This script will obtain the electronic coupling energies as calculated using the eet function in Gaussian between pairs of neighbouring molecules (dimers).
"""
import os

from ase.io import read

from EKMC.EKMC_Only_Setup.get_electronic_coupling_data_methods.get_electronic_coupling_data_methods import read_dimer_data_from_All_Dimer_Information
from EKMC.EKMC_Only_Setup.get_electronic_coupling_data_methods.get_electronic_coupling_data_methods import read_dimer_data_from_Unique_Dimer_Information
from EKMC.EKMC_Only_Setup.get_electronic_coupling_data_methods.get_electronic_coupling_data_methods import get_EET_calculation_information

def get_electronic_coupling_data(short_range_couplings, crystal_name, functional_and_basis_set, molecules_path):
	"""
	This method will obtain the electronic coupling energies as calculated using the eet function in Gaussian between pairs of neighbouring molecules (dimers).

	Parameters
	----------
	short_range_couplings : dict.
		This dictionary includes the information required for obtaining dimer information.
	crystal_name : str.
		This is the name of the crystal.
	functional_and_basis_set : str.
		This is the name of the functional and basis set used in calculations to obtain EET and ATC information. 
	molecules_path : str.
		This is the path to all the molecules in the crystal.

	Returns
	------- 
	electronic_coupling_data : dict.
		This is all the energetic energy for each dimer involving each molecule from the unit cell.
	"""

	# First, if you do not want to use EET information, return an empty dictionary.
	if (short_range_couplings['model'] is None) or (short_range_couplings['model'].lower() == 'none'):
		return {}

	# Second, get the path to the dimers to obtain electronic coupling data from.
	path_to_dimer_information_file = short_range_couplings['path_to_dimer_information_file']

	# Third, get the spatial information about the molecules that make up the dimer.
	all_dimer_information     = read_dimer_data_from_All_Dimer_Information(molecules_path)

	# Fourth, determine which symmetric dimers are associated with which unique dimer that EET calculations were performed upon.
	symmetric_to_unique_dimer = read_dimer_data_from_Unique_Dimer_Information(molecules_path)

	# Fifth, get electronic coupling energies from EET calculations
	dimers_EET_information    = get_EET_calculation_information(path_to_dimer_information_file+'/Individual_EET_Data', crystal_name, functional_and_basis_set)

	# Sixth, gather all spatial and EET calculation information together
	electronic_coupling_data  = combine_dict_information(all_dimer_information, dimers_EET_information, symmetric_to_unique_dimer)

	# Seventh, return the electronic_coupling_data dictionary.
	return electronic_coupling_data

def combine_dict_information(all_dimer_information, dimers_EET_information, symmetric_to_unique_dimer):
	"""
	This method will take the all_dimer_information, dimers_EET_information, and symmetric_to_unique_dimer dictionaries, and combine them together to give all the electronic information about the dimers in the crystal.
	
	Parameters
	----------
	all_dimer_information : dict.
		This dictionary includes all the spatial information about the dimers in the crystal, with respect to the unit cell vectors.
	dimers_EET_information : dict.
		This dictionary includes all the energetic EET information about the unique dimers in the crystal.
	symmetric_to_unique_dimer : dict.
		This dictionary includes the dimers that are the same as a unique dimer, which has had it's EET recorded in the dimers_EET_information dictionary.

	Returns
	------- 
	electronic_coupling_data : dict.
		This is all the energetic energy for each dimer involving each molecule from the unit cell.
	"""

	# First, setup the electronic_coupling_data dictionary.
	electronic_coupling_data = {}

	# Second, for each dimer in the all_dimer_information dictionary.
	for dimer_no in all_dimer_information:

		# Third, obtain the molecules and the displacement vector that make up each dimer in all_dimer_information
		molecule1_no, molecule2_no, displacement_vector = all_dimer_information[dimer_no]

		# Fourth, obtain the dimer that contains the EET energy, either
		#   * For the unique dimer itself.
		#   * For non-unique dimer, where it's EET value is the same as it unique dimer counterpart.
		if dimer_no in symmetric_to_unique_dimer.keys():
			dimer_no_for_EET = symmetric_to_unique_dimer[dimer_no]
		else:
			dimer_no_for_EET = dimer_no

		# Fifth, obtain the EET coupling energy for the dimer of interest
		mol1_no, mol2_no, coupling_energy = dimers_EET_information[dimer_no_for_EET]

		# Sixth, make sure that the molecules involved in the non-unique dimer was also the same molecules in the unique dimer.
		if (dimer_no_for_EET == dimer_no) and (not ((molecule1_no == mol1_no) and (molecule2_no == mol2_no))):
			raise Exception('Huh?')

		# Eighth, record the electronic data into the electronic_coupling_data, where the key describes the relative displacement between each molecule in the system.
		electronic_coupling_data[(molecule1_no,molecule2_no,displacement_vector[0],displacement_vector[1],displacement_vector[2])] = coupling_energy #(molecule1_no, molecule2_no, displacement_vector, total_electronic_coupling_energy)

	# Ninth, return the electronic_coupling_data dictionary.
	return electronic_coupling_data



