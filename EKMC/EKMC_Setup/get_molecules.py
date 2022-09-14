"""
get_molecules.py, Geoffrey Weal, 17/2/22

This script is able to obtain the molecules from the crystal
"""
import os
from copy import deepcopy
from ase.io import read
from SUMELF import less_than_or_equal_to_max_bondlength

def get_molecules(molecules_path):
	"""
	This method will obtain the molecules from the crystal

	Parameters
	----------
	molecules_path : str.
		This is the path to the folders where the molecules are stored. 

	Returns
	-------
	molecules : list of ase.Atoms
		This is a list of the molecules in the crystal.
	"""

	# These are the folder names.
	all_molecule_folder = 'All_Molecules'

	# Obtain the list of all the molecules in the "All Molecules" folder. 
	all_molecules_list = [file for file in os.listdir(molecules_path+'/'+all_molecule_folder) if (os.path.isfile(molecules_path+'/'+all_molecule_folder+'/'+file) and file.startswith('molecule_') and file.endswith('.xyz'))]
	all_molecules_list.sort(key=lambda x: int(x.replace('molecule_','').replace('.xyz','')))

	# This is a check to see if their are no molecules that are obviously missing.
	# Molecules may still be missing however, so check to make sure you have enough molecules
	if not [int(x.replace('molecule_','').replace('.xyz','')) for x in all_molecules_list] == list(range(1,len(all_molecules_list)+1)):
		print('Error in EKMC: You may be missing some molecules in the '+str(all_molecule_folder)+' folder.')
		print('The list of molecules in the '+str(all_molecule_folder)+' should be consecutive. This may be a sign you are missing a molecule')
		print('Molecules in '+all_molecule_folder+' folder: '+str(all_molecules_list))
		print('Check this out.')
		exit('This program will finish without beginning.')

	# Get the paths to molecules to use
	molecule_filepaths = []
	for molecule_filename in all_molecules_list:
		folder_name = all_molecule_folder
		molecule_filepaths.append(molecules_path+'/'+folder_name+'/'+molecule_filename)
	
	# Get molecules
	molecules = [read(molecule_filepath) for molecule_filepath in molecule_filepaths]

	return molecules

	# ------------------------------------------------------------------------------------------------------


