"""
get_neighbours_to_molecules_in_central_cell.py, Geoffrey Weal, 20/3/22

get_neighbours_to_molecules_in_central_cell is a method that will give all the neighbours 
"""
import numpy as np

from tqdm import tqdm

from SUMELF                                                                 import get_distance, get_cell_corner_points
from EKMC.EKMC_Setup.get_neighbours_methods.get_expanded_cell_corner_points import get_expanded_cell_corner_points
from EKMC.EKMC_Setup.get_neighbours_methods.rate_constant_data_methods      import rate_constant_data_for_same_molecule_in_different_cells
from EKMC.EKMC_Setup.get_neighbours_methods.rate_constant_data_methods      import rate_constant_data_for_different_molecules_in_origin_cell
from EKMC.EKMC_Setup.get_neighbours_methods.rate_constant_data_methods      import rate_constant_data_for_different_molecules_in_different_cells

def get_neighbours_to_molecules_in_central_cell(kinetic_model, molecules, crystal_cell_lattice, electronic_coupling_data, kinetics_details, neighbourhood_rCut=40.0):
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
	electronic_coupling_data : dict.
		This is all the energetic energy for each dimer involving each molecule from the unit cell.
	kinetics_details : dict.
		These are the details required for performing the kinetic Monte Carlo algorithm.
	neighbourhood_rCut : float
		This is the circumference around the COM of each molecule to add to the neighbourhood.

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
	nn = int(float(len(molecules)+1)*(float(len(molecules))/2.0))
	pbar = tqdm(total=nn,unit='task')
	all_local_neighbourhoods = {index1: {index2: [] for index2 in range(len(molecules))} for index1 in range(len(molecules))}
	for index1 in range(len(molecules)):
		molecule1 = molecules[index1]
		centre_of_mass1 = centre_of_masses[index1]
		for index2 in range(index1,len(molecules)): 
			if index1 == index2:
				# 4.1: If index1 equal index2, then get all the rate_constant_data between itself in different unit cells
				pbar.set_description('Comparing molecule '+str(index1+1)+' with itself in different cells')
				rate_constant_data_for_same_molecule_in_different_cells(kinetic_model, index1, molecule1, centre_of_mass1, kinetics_details, electronic_coupling_data, all_local_neighbourhoods, all_cell_points, displacement_vectors)
			else:
				# 4.2: If index1 not equal to index2, then get all the rate_constant_data between:
				#    * Molecule index1 and molecule index2 within the same unit cell (origin unit cell).
				#    * Molecule index1 and molecule index2 in different unit cells
				pbar.set_description('Comparing molecule '+str(index1+1)+' and molecule '+str(index2+1)+' in the same and different unit cells')
				molecule2 = molecules[index2]; centre_of_mass2 = centre_of_masses[index2]
				rate_constant_data_for_different_molecules_in_origin_cell    (kinetic_model, index1, index2, molecule1, molecule2, centre_of_mass1, centre_of_mass2, kinetics_details, electronic_coupling_data, all_local_neighbourhoods)
				rate_constant_data_for_different_molecules_in_different_cells(kinetic_model, index1, index2, molecule1, molecule2, centre_of_mass1, centre_of_mass2, kinetics_details, electronic_coupling_data, all_local_neighbourhoods, all_cell_points, displacement_vectors)
			pbar.update(1)
	pbar.close()

	# Fifth, Sort the lists in all_local_neighbourhoods. This just makes it easier for a human to see what is happening, but is not necessary for the running of this algorithm.
	for key1 in all_local_neighbourhoods.keys():
		for key2 in all_local_neighbourhoods[key1].keys():
			all_local_neighbourhoods[key1][key2].sort()

	# Sixth, return all_local_neighbourhoods
	print('-------------')
	return all_local_neighbourhoods





