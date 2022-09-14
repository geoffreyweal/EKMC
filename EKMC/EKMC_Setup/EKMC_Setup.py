"""
EKMC_Setup.py, Geoffrey Weal, 12/8/22

This script is designed to set up the files needed for runningt the excitonic kinetic Monte Carlo algorithm. 

"""
import os

from numpy import array_equal

from EKMC.EKMC_Setup.get_molecules                               import get_molecules
from SUMELF                                                      import obtain_graph
from EKMC.EKMC_Setup.add_charges_to_molecules                    import add_charges_to_molecules
from EKMC.EKMC_Setup.get_electronic_coupling_data                import get_electronic_coupling_data
from EKMC.EKMC_Setup.get_neighbours_to_molecules_in_central_cell import get_neighbours_to_molecules_in_central_cell
from SUMELF                                                      import remove_folder, make_folder

def EKMC_Setup(molecules_path, ATC_folder_path, functional_and_basis_set, kinetic_model, dimer_couplings, kinetics_details, neighbourhood_rCut=40.0, path_to_KMC_setup_data=''):
	"""
	This program is designed to simulate the movement of an exciton through a OPV crystal system.

	Parameters
	----------
	molecules_path : str.
		The path to the molecules that make up the crystal, as obtained from the ECCP program. 
	ATC_folder_path : str.
		A folder that contains all the .chg files.
	functional_and_basis_set : str.
		This is the folder name for the functional and basis set used in calculations. This name is given from the ECCP program. 
	kinetic_model : str.
		This is the type of kinetic model you would like to use.
	dimer_couplings : dict.
		This dictionary contains all the energetic information about the dimers (such as EET energies).
	kinetics_details : dict.
		This contains all the information required to obtain the rate constants (except for electronic coupling and ATC charge data)
	neighbourhood_rCut : float
		This is the maximum distance that two molecules in the dimer can be to be in the neighbourhood. 
		This variable defines how far from one molecule to determine the coulombic energy between itself and another molecule. 
		This is to include the possibility that the exciton will jump between molecules that are very far from each other based on their dipole rather than orbital overlap. Default: 40.0 A. 
	path_to_KMC_setup_data : str.
		This is the path to the ekmc file that contains all the information about the ekmc simulation for this crystal.
	"""

	# First, get the absolute path to the folders that we will be looking at.
	crystal_name    = os.path.basename(molecules_path)
	molecules_path  = os.path.abspath(molecules_path)
	ATC_folder_path = os.path.abspath(ATC_folder_path)

	# Second, get the molecules that make up the crystal, and the crystal lattice.
	molecules = get_molecules(molecules_path)
	if not all([array_equal(molecules[index].get_cell()[:], molecules[0].get_cell()[:]) for index in range(1,len(molecules))]):
		raise Exception('Error. Not all the unit cells of the molecules in your crystal are the same. Check the unit cells of your molecules out.')
	crystal_cell_lattice = molecules[0].get_cell()

	# Third, get the graphs of molecules
	molecule_graphs = [obtain_graph(molecules[index],mic=False,name='molecule_'+str(index)) for index in range(len(molecules))]

	# Fourth, add charges to molecules from chg files in ATC folder. The charges added to the molecules are the atomic transition charges. 
	add_charges_to_molecules(molecules, molecule_graphs, ATC_folder_path, functional_and_basis_set)

	# Fifth, obtain electronic coupling energies from dimers.
	electronic_coupling_data = get_electronic_coupling_data(dimer_couplings, crystal_name, functional_and_basis_set, molecules_path)

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
	all_local_neighbourhoods = get_neighbours_to_molecules_in_central_cell(kinetic_model, molecules, crystal_cell_lattice, electronic_coupling_data, non_changing_lattice_kinetics_details, neighbourhood_rCut=40.0)

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
		KMC_setup_data.write(str(all_local_neighbourhoods)+'\n')

# ==================================================================================================================================================================================================

