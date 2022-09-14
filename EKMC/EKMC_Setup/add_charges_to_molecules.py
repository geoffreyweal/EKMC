"""
add_charges_to_molecules.py, Geoffrey Weal, 20/3/22

This script will assign charges to the atoms in each molecule.
"""
import os
from numpy import array

from EKMC.EKMC_Setup.add_charges_to_molecules_methods.invariance_method import assigned_ATCs_to_molecules_invariance_method

def add_charges_to_molecules(molecules, molecule_graphs, ATC_folder_path, functional_and_basis_set, max_disparity=None):
	"""
	This method is designed to assign charges to each atom in the molecules in your crystal based on DFT calculations.

	The charges of your molecules are given in the .chg files given in your ATC_folder_path folder

	This method is able to determine the symmetries in a crystal and determine which molecules are symmetrically the same. This means you only have to determine the charges of molecules that are not symmetric in the crystal.

	This method will apply the correct charges to the correct atoms in the symmetrically equivalent molecules.

	Parameters
	----------
	molecules : list of ase.Atoms
		This is a list of all the molecules in your crystal.
	molecule_graphs : list of networkx.Graph
		This is the list of the undirected graph representations of each molecule.
	ATC_folder_path : str.
		This is the folder that contains all the chg files to obtain the charges of atoms in each molecule.
	functional_and_basis_set : str.
		This is the folder of information for the given functional and basis set that you would like to use. 
	max_disparity : float
		This is the maximum disparity between two dimers to be considered invariant. 
	"""

	# First, get how the molecule indices are assigned to the ATC. Also get ATC ase objects.
	all_atomic_transition_charges = [read_chg_file(ATC_folder_path+'/'+CHG_filename+'/'+functional_and_basis_set+'/output.chg') for CHG_filename in os.listdir(ATC_folder_path) if (os.path.isdir(ATC_folder_path+'/'+CHG_filename) and CHG_filename.startswith('molecule_'))]
	molecule_to_atc, ATC_ase_objects = assigned_ATCs_to_molecules_invariance_method(all_atomic_transition_charges, molecules, molecule_graphs)
	
	# Second, apply the charges from the ATC to the appropriate molecule.
	for ATC_index, mol_index, ATC_idx in molecule_to_atc:
		ATC_charges = ATC_ase_objects[ATC_index].get_initial_charges()
		non_hydrogen_ATC_reordered_charges = [ATC_charges[index] for index in ATC_idx]
		molecules[mol_index].set_initial_charges(non_hydrogen_ATC_reordered_charges)

# ------------------------------------------------------------------------------------------------------------------------

def read_chg_file(CHG_filename):
	"""
	This method will read in the chg files 

	Parameters
	----------
	CHG_filename : str
		This is the name of the chg file to be read

	Returns
	-------
	atc_data : tuple of tuples
		This is an object that contains the charges of all atoms in your molecule, given as (symbol, position, charge) for each atom.
	"""

	# First, initialise the ATC data list.
	atc_data = []

	# Second, read the ATC charge data from the .chg file.
	with open(CHG_filename,'r') as CHGfile:
		for line in CHGfile:
			symbol, xx, yy, zz, atc = line.rstrip().split()
			xx = float(xx); yy = float(yy); zz = float(zz)
			position = array([xx, yy, zz])
			atc = float(atc)
			atc /= (2.0 ** 0.5) # This is to manually correct an issue. See the Multiwfn 3.8 dev manual, Section 4.A.9, page 960.
			atc_data.append((symbol, position, atc))

	# Third, return the ATC data list
	return tuple(atc_data)

# ------------------------------------------------------------------------------------------------------------------------
