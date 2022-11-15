"""
EKMC_Only_Setup.py, Geoffrey Weal, 12/8/22

This script is designed to set up the files needed for runningt the excitonic kinetic Monte Carlo algorithm. 

"""
import os

from numpy import array_equal

from EKMC.EKMC_Only_Setup.get_molecules                               import get_molecules
from SUMELF                                                           import obtain_graph
from EKMC.EKMC_Only_Setup.add_zero_charges_to_molecules               import add_zero_charges_to_molecules
from EKMC.EKMC_Only_Setup.add_charges_to_molecules                    import add_charges_to_molecules
from EKMC.EKMC_Only_Setup.get_electronic_coupling_data                import get_electronic_coupling_data
from EKMC.EKMC_Only_Setup.get_neighbours_to_molecules_in_central_cell import get_neighbours_to_molecules_in_central_cell
from SUMELF                                                           import remove_folder, make_folder

def EKMC_Only_Setup(molecules_path, functional_and_basis_set, kinetic_model, short_range_couplings, long_range_couplings, kinetics_details, neighbourhood_rCut=40.0, path_to_KMC_setup_data='', no_of_cpus_for_setup=1):
	"""
	This program is designed to simulate the movement of an exciton through a OPV crystal system.

	Parameters
	----------
	molecules_path : str.
		The path to the molecules that make up the crystal, as obtained from the ECCP program. 
	functional_and_basis_set : str.
		This is the folder name for the functional and basis set used in calculations. This name is given from the ECCP program. 
	kinetic_model : str.
		This is the type of kinetic model you would like to use.
	short_range_couplings : dict. 
		This describes the coupling between molecules in the crystal at distances less than and including neighbourhood_rCut. This dictionary includes the model ('model': None if you dont want to include short range coupling) and the files which will be used to obtain the coupling energies.
	long_range_couplings : dict.
		This describes the coupling between molecules in the crystal at distances greater than neighbourhood_rCut. This dictionary includes the model ('model': None if you dont want to include long range coupling) and the files which will be used to obtain the coupling energies.
	kinetics_details : dict.
		This contains all the information required to obtain the rate constants (except for electronic coupling and ATC charge data)
	neighbourhood_rCut : float
		This is the maximum distance that two molecules in the dimer can be to be in the neighbourhood. 
		This variable defines how far from one molecule to determine the coulombic energy between itself and another molecule. 
		This is to include the possibility that the exciton will jump between molecules that are very far from each other based on their dipole rather than orbital overlap. Default: 40.0 A. 
	path_to_KMC_setup_data : str.
		This is the path to the ekmc file that contains all the information about the ekmc simulation for this crystal.
	no_of_cpus_for_setup : int.
		This is the number of cpus used to setup the EKMC simulations.
	"""

	# First, get the absolute path to the folders that we will be looking at.
	crystal_name    = os.path.basename(molecules_path)
	molecules_path  = os.path.abspath(molecules_path)

	# Second, get the molecules that make up the crystal, and the crystal lattice.
	molecules = get_molecules(molecules_path)
	if not all([array_equal(molecules[index].get_cell()[:], molecules[0].get_cell()[:]) for index in range(1,len(molecules))]):
		raise Exception('Error. Not all the unit cells of the molecules in your crystal are the same. Check the unit cells of your molecules out.')
	crystal_cell_lattice = molecules[0].get_cell()

	# Third, get the graphs of molecules
	molecule_graphs = [obtain_graph(molecules[index],mic=False,name='molecule_'+str(index)) for index in range(len(molecules))]

	# Fourth, obtain the coupling data for short range coupling.
	# Obtain electronic coupling energies from dimers.
	if (short_range_couplings['model'] is None) or (short_range_couplings['model'].lower() == 'none'):
		short_range_coupling_data = {}
	elif short_range_couplings['model'] == 'EET':
		short_range_coupling_data = get_electronic_coupling_data(short_range_couplings, crystal_name, functional_and_basis_set, molecules_path)
	else:
		raise Exception('Short Range Model?')

	# Fifth, obtain the coupling data for long range coupling.
	# Add charges to molecules from chg files in ATC folder. The charges added to the molecules are the atomic transition charges. 
	if (long_range_couplings['model'] is None) or (long_range_couplings['model'].lower() == 'none'):
		add_zero_charges_to_molecules(molecules, molecule_graphs)
	elif long_range_couplings['model'] == 'ATC':
		ATC_folder_path = long_range_couplings['path_to_ATC_folder']
		add_charges_to_molecules(molecules, molecule_graphs, ATC_folder_path, functional_and_basis_set)
	else:
		raise Exception('Long Range Model?')
	long_range_coupling_data = {'model': long_range_couplings['model']}

	# Sixth, Get the names of the neighbourhood dictionary keys to obtain.
	names = ['relative_permittivity']
	if   kinetic_model.lower() == 'marcus':
		names += ['classical_reorganisation_energy','temperature']
	elif kinetic_model.lower() == 'mlj':
		names += ['huang_rhys_factor','uu_max','vv_max','WW','classical_reorganisation_energy','temperature']
	else:
		raise Exception('Error: kinetic_model must be either "Marcus" or "MLJ". kinetic_model = '+str(kinetic_model))

	# Seventh, get the neighbourhood dictionary between molecules within a neighbourhood_rCut range.
	non_changing_lattice_kinetics_details = {}
	for name in names:
		non_changing_lattice_kinetics_details[name] = kinetics_details[name]
	all_local_neighbourhoods = get_neighbours_to_molecules_in_central_cell(kinetic_model, molecules, crystal_cell_lattice, short_range_coupling_data, long_range_coupling_data, non_changing_lattice_kinetics_details, neighbourhood_rCut=40.0, no_of_cpus_for_setup=no_of_cpus_for_setup)

	# Eighth, add disorder values to the non_changing_lattice_kinetics_details dictionary.
	names = ['coupling_disorder', 'energetic_disorder']
	for name in names:
		non_changing_lattice_kinetics_details[name] = kinetics_details[name]

	# Ninth, save this data to disk
	save_KMC_data_to_disk(path_to_KMC_setup_data, molecules, crystal_cell_lattice, kinetic_model, non_changing_lattice_kinetics_details, all_local_neighbourhoods)

# ==================================================================================================================================================================================================

def save_KMC_data_to_disk(path_to_KMC_setup_data, molecules, crystal_cell_lattice, kinetic_model, kinetics_details, all_local_neighbourhoods):
	"""
	This method is designed to save the data required to simulate the exciton kmc simulation, including the electronic details of the local behaviour of each molecule in the crystal.

	Parameters
	----------
	path_to_KMC_setup_data : str.
		This is the path to the ekmc file that contains all the information about the ekmc simulation for this crystal.
	molecules : list of ase.Atoms
		This is the list of molecules in the crystal
	crystal_cell_lattice : ase.Cell
		This contain information about the unit cell.
	kinetic_model : str.
		This is the type of kinetic model you would like to use.
	kinetics_details : dict.
		This contains all the information required to obtain the rate constants (except for electronic coupling and ATC charge data)
	all_local_neighbourhoods : dict.
		This dictionary contains all the information about the neighbourhoods that surrounded each molecule in your crystal.
	"""

	# First, make the folder to place the KMC_setup_data.ekmc file in 
	#remove_folder(path_to_KMC_setup_data)
	make_folder(path_to_KMC_setup_data)

	# Second, create the KMC_setup_data.ekmc file.
	path_to_file = path_to_KMC_setup_data+'/'+f'KMC_setup_data.ekmc'
	with open(path_to_file,'w') as KMC_setup_data:
		KMC_setup_data.write(str([tuple(molecule.get_center_of_mass()) for molecule in molecules])+'\n')
		KMC_setup_data.write(str(tuple([tuple(xx) for xx in crystal_cell_lattice[:]]))+'\n')
		KMC_setup_data.write(str(kinetic_model)+'\n')
		KMC_setup_data.write(str(kinetics_details)+'\n')
		KMC_setup_data.write(save_all_local_neighbourhoods_data(all_local_neighbourhoods)+'\n')

def save_all_local_neighbourhoods_data(all_local_neighbourhoods):
	"""
	This method is designed to order the printing of all_local_neighbourhoods
	"""

	# First, create a list to place data into
	to_string = []

	for mol1 in sorted(all_local_neighbourhoods.keys()):

		to_string_mol1_data = []

		for mol2 in sorted(all_local_neighbourhoods[mol1].keys()):

			to_string_mol1_mol2_data = []

			for cell_point, rate_constant_data in sorted(all_local_neighbourhoods[mol1][mol2].items(), key=lambda cpd: tuple([order_number(cp) for cp in cpd[0]])):
				to_string_mol1_mol2_data.append(str(cell_point)+': '+str(rate_constant_data))

			to_string_mol1_mol2_data = '{' + ', '.join(to_string_mol1_mol2_data) + '}'

			to_string_mol1_data.append(str(mol2)+': '+str(to_string_mol1_mol2_data))

		to_string_mol1_data = '{' + ', '.join(to_string_mol1_data) + '}'

		to_string.append(str(mol1)+': '+str(to_string_mol1_data))

	to_string = '{' + ', '.join(to_string) + '}'

	return to_string

def order_number(value):
	if value == 0:
		return value
	elif value < 0:
		return abs(value)*2
	elif value > 0:
		return abs(value)*2 - 1

# ==================================================================================================================================================================================================



