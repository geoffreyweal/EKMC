"""
invariance_method.py, Geoffrey Weal, 23/2/22

This script is designed to use the procrustes analysis to determine if dimers are rotationally, translationally, and reflectively invarient.
"""
import numpy as np
from tqdm import trange, tqdm

from copy import deepcopy

from itertools import product

from ase import Atoms
from ase.visualize import view

from scipy.linalg import orthogonal_procrustes
from scipy.spatial import procrustes

from SUMELF import obtain_graph

from EKMC.EKMC_Setup.add_charges_to_molecules_methods.methods_for_invariance_method.isomorphvf2_GRW import GraphMatcher
from SUMELF import remove_hydrogens, get_distance

def assigned_ATCs_to_molecules_invariance_method(atomic_transition_charges, molecules, molecule_graphs, max_disparity=None):
	"""
	This method uses the procrustes analysis to determine if a ATC are rotationally, translationally, and reflectively invarient to a molecule.

	From using the procrustes analysis, this method will determine which ATCs and molecules are equivalent

	This analysis will ignore hydrogen atoms. 

	The procrustes analysis use is from scipy. See the website below for more information: 
		* https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.procrustes.html

	Parameters
	----------
	atomic_transition_charges : list
		A list of elements and positions of atcs.
	molecules : list of ase.Atoms
		This is the list of molecules that are in the crystal
	molecule_graphs : list of networkx.Graph
		This is the list of the undirected graph representations of each molecule
	max_disparity : float
		This is the maximum disparity between a ATC and molecule to be considered invariant. 

	Returns
	-------
	symmetric_ATCs : list
		A list of the indices of equivalent ATCs in the ATCs list. 
	"""

	# First, set max_disparity to a default value if it is given initially as None. 
	if max_disparity is None:
		max_disparity = 0.1

	##################################################################################################
	# Convert ATC lists into objects that can be used in this method

	print('-------------')
	print(('Determining equivalent ATCs using invarience method').upper())
	ATC_ase_objects = []
	ATC_graphs = []
	for atomic_transition_charge in atomic_transition_charges:
		ATC_symbols, ATC_positions, ATC_charges = get_atom_data_from_ATC(atomic_transition_charge)
		ATC_ase_object = Atoms(symbols=ATC_symbols,positions=ATC_positions,charges=ATC_charges)
		ATC_ase_objects.append(ATC_ase_object)
		ATC_graph = obtain_graph(ATC_ase_object)
		ATC_graphs.append(ATC_graph)

	# Obtain all molecules without hydrogen
	non_hydrogen_ATCs = [] # for debugging
	non_hydrogen_ATCs_elements  = []
	non_hydrogen_ATCs_positions = []
	non_hydrogen_ATC_graphs     = []

	for index in range(len(ATC_ase_objects)):
		non_hydrogen_ATC, non_hydrogen_ATC_graph = remove_hydrogens(ATC_ase_objects[index], graph=ATC_graphs[index])
		non_hydrogen_ATCs.append(non_hydrogen_ATC)
		non_hydrogen_ATCs_elements.append(non_hydrogen_ATC.get_chemical_symbols())
		non_hydrogen_ATCs_positions.append(non_hydrogen_ATC.get_positions())
		non_hydrogen_ATC_graphs.append(non_hydrogen_ATC_graph)

	##################################################################################################
	# Convert molecule ase objects into objects that can be used in this method

	print('-------------')
	print(('Determining equivalent ATCs using invarience method').upper())
	# Obtain all molecules without hydrogen
	non_hydrogen_molecules = [] # for debugging
	non_hydrogen_molecules_elements  = []
	non_hydrogen_molecules_positions = []
	non_hydrogen_molecules_graphs    = []
	for index in range(len(molecules)):
		non_hydrogen_molecule, non_hydrogen_molecule_graph = remove_hydrogens(molecules[index], graph=molecule_graphs[index])
		non_hydrogen_molecules.append(non_hydrogen_molecule)
		non_hydrogen_molecules_elements.append(non_hydrogen_molecule.get_chemical_symbols())
		non_hydrogen_molecules_positions.append(non_hydrogen_molecule.get_positions())
		non_hydrogen_molecules_graphs.append(non_hydrogen_molecule_graph)

	##################################################################################################
	# Determine how the indices of molecules can be interchanged to give the same molecule

	equivalent_molecule_to_ATC_indices = {}
	print('Examining equivalent atoms between the '+str(len(non_hydrogen_molecules_graphs))+' molecules and the '+str(len(non_hydrogen_ATC_graphs))+'ATCs identified. This can take a while with large and complex molecules.')
	nn = len(non_hydrogen_molecules_graphs)*len(non_hydrogen_ATC_graphs)
	pbar = tqdm(total=nn,unit='task')
	for mol_index, ATC_index in product(range(len(non_hydrogen_molecules_graphs)),range(len(non_hydrogen_ATC_graphs))):
		pbar.set_description('Comparing molecule '+str(mol_index+1)+' and ATC '+str(ATC_index+1))
		molecule_graph = non_hydrogen_molecules_graphs[mol_index]
		ATC_graph = non_hydrogen_ATC_graphs[ATC_index]
		GM = GraphMatcher(molecule_graph, ATC_graph)
		all_unique_matches = GM.get_all_unique_isomorphic_graphs()
		equivalent_molecule_to_ATC_indices[(mol_index,ATC_index)] = all_unique_matches
		pbar.update(1)
	pbar.close()

	##################################################################################################
	# Now compare the ATCs and molecules and match the ATCs and their indices to molecules and their indices.
	# Will use rotational, translational, and reflective symmetry to determine this.
	# The ATC positions should be exactly the same as their molecule counterparts, 
	# so keep comparisons very tight.

	print('Comparing translational, rotational, and reflective invarience between ATCs. '+str(len(atomic_transition_charges))+' ATCs to be examined. This can take a while with large and complex ATCs.')
	nn = len(atomic_transition_charges)*len(molecules)
	pbar = tqdm(total=nn,unit='task')
	molecule_to_atc = []
	for mol_index in range(len(molecules)):
		# get the position data for the molecule.
		non_hydrogen_molecule_elements = non_hydrogen_molecules_elements[mol_index]
		non_hydrogen_molecule_positions = non_hydrogen_molecules_positions[mol_index]
		non_hydrogen_molecule_graph = non_hydrogen_molecules_graphs[mol_index]

		for ATC_index in range(len(atomic_transition_charges)):
			# get the position data for the ATC.
			non_hydrogen_ATC_elements  = non_hydrogen_ATCs_elements[ATC_index]
			non_hydrogen_ATC_positions = non_hydrogen_ATCs_positions[ATC_index]
			non_hydrogen_ATC_graph     = non_hydrogen_ATC_graphs[ATC_index]

			# write description
			pbar.set_description('Comparing ATC '+str(ATC_index+1)+' and molecule '+str(mol_index+1))

			# Get all the indices that are equivalent to eachother in each molecule in each dimer. 
			emATC_indices_molecule = equivalent_molecule_to_ATC_indices[(mol_index,ATC_index)]

			# In this for loop, go though all the realistic ways that the atoms in the molecule 
			# can be permuted to give the ATC.
			for comparison1 in emATC_indices_molecule:
				non_hydrogen_ATC_idx = get_permutated_indices_list(comparison1)
				non_hydrogen_ATC_reordered_elements = [non_hydrogen_ATC_elements[index] for index in non_hydrogen_ATC_idx]
				non_hydrogen_ATC_reordered_positions = deepcopy(non_hydrogen_ATC_positions)[non_hydrogen_ATC_idx, :]
				is_varient, R_matrix, mean_mol, mean_ATC = are_molecule_and_ATC_variant(non_hydrogen_molecule_elements, non_hydrogen_ATC_reordered_elements, non_hydrogen_molecule_positions, non_hydrogen_ATC_reordered_positions, max_disparity)
				if is_varient: 
					ATC_ase_object = ATC_ase_objects[ATC_index]
					associated_molecule = molecules[mol_index]
					ATC_idx = assign_hydrogens_to_ATC_idx(ATC_ase_object, associated_molecule, non_hydrogen_ATC_idx, R_matrix, mean_mol, mean_ATC)
					molecule_to_atc.append((ATC_index, mol_index, ATC_idx))
					break
			pbar.update(1)
	pbar.close()

	# Check to make sure that each molecule has been assigned to a ATC.
	molecules_that_have_been_assigned_an_ATC_to = [mol_index for ATC_index, mol_index, ATC_idx in molecule_to_atc]
	if not sorted(molecules_that_have_been_assigned_an_ATC_to) == list(range(len(molecules))):
		print('Error in def assigned_ATCs_to_molecules_invariance_method, in invariance_method.py')
		print('Not all molecules have been assign an ATC')
		unassigned_molecules = list(set(range(len(molecules))) | set(molecules_that_have_been_assigned_an_ATC_to))
		print('Molecules that have not been assigned: '+str(unassigned_molecules))
		print('Molecules that have been assigned: '+str(molecules_that_have_been_assigned_an_ATC_to))
		view(molecules)
		view(ATC_ase_objects)
		import pdb; pdb.set_trace()
		exit('This program with finished without completing.')

	# hopefully all ATC's have been matched with the appropriate molecule.
	return molecule_to_atc, ATC_ase_objects

##############################################################################################################

def get_atom_data_from_ATC(atomic_transition_charge):
	symbols = []
	positions = []
	charges = []
	for symbol, position, atc in atomic_transition_charge:
		symbols.append(symbol)
		positions.append(position)
		charges.append(atc)
	positions = np.array(positions)
	return symbols, positions, charges

##############################################################################################################

def get_permutated_indices_list(comparison): 
	"""
	This method will provide the permutation list of how to reorder the atoms indices in a molecule from a dictionary that tell this program how the indices of one molecule translate into another equivalent molecule. 

	Parameters
	----------
	comparison : dict.
		A dictionary that contains how the indices of one molecule translate into another identical molecule. 

	Returns
	-------
	idx : list
		The permutation list that tells the program how to reorder atoms in a list.

	"""
	permutation1 = [ATC_index for mol_index, ATC_index in sorted(comparison.items())]
	return np.array(permutation1)

##############################################################################################################

def are_molecule_and_ATC_variant(mol_elements, ATC_elements, mol_distances, ATC_distances, max_distance_disparity): 
	"""
	This method will check that the elements in the ATC and the molecule are translationally, rotationally, and reflectively varient
	
	Parameters
	----------
	ATC_elements : list
		A list of the elements of atoms in the ATC
	mol_elements : list
		A list of the elements of atoms in the molecule
	ATC_distances : np.array
		A numpy array of the positions of atoms in the ATC
	mol_distances : np.array
		A numpy array of the positions of atoms in the molecule
	max_distance_disparity: float
		This is the maximum that any two "could be equivalent" atoms can be between dimer 1 and dimer 2 for dimers 1 and 2 to be considered variant

	Returns
	-------
	idx : list
		The permutation list that tells the program how to reorder atoms in a list.

	"""
	#If the order of atoms are not the same, something actually may have gone wrong, so check this out
	if not (mol_elements == ATC_elements):
		print('Error in invarient_method.py')
		print('The list of elements for mol_elements and ATC_elements are not the same. ')
		print('However, they should be the same as the networkx graph nodes have been given information about the element for each atom.')
		print('Therefore, this should have been picked up by GraphMatcher object.')
		print('Check this out')
		import pdb; pdb.set_trace()
		exit('This program will finish without completing.')

	# determine if the dimer are varient given the particular ordering of atoms in dimers 1 and 2.
	positions_are_variant, R_matrix, mean_mol, mean_ATC = determine_if_positions_are_variant(mol_distances, ATC_distances, max_distance_disparity=max_distance_disparity)

	return positions_are_variant, R_matrix, mean_mol, mean_ATC

def determine_if_positions_are_variant(data1, data2, max_distance_disparity=1.0):
	"""
	This method will determine if two dimers/molecules are translationally, rotationally, and reflectively variant.

	This method have been modified from the _procrustes.py from scipy, see below: https://github.com/scipy/scipy/blob/v1.8.0/scipy/spatial/_procrustes.py#L15-L130

	Parameters
	----------
	data1 : numpy.array
		A array of positions from dimer1/molecule1
	data1 : numpy.array
		A array of positions from dimer2/molecule2
	max_distance_disparity: float
		This is the maximum that any two "could be equivalent" atoms can be between dimer 1 and dimer 2 for dimers 1 and 2 to be considered variant

	Returns
	-------
	True if the two dimers are translationally, rotationally, and reflectively variant. False if not. 

	"""
	mtx1 = np.array(data1, dtype=np.double, copy=True)
	mtx2 = np.array(data2, dtype=np.double, copy=True)

	if mtx1.ndim != 2 or mtx2.ndim != 2:
		raise ValueError("Input matrices must be two-dimensional")
	if mtx1.shape != mtx2.shape:
		raise ValueError("Input matrices must be of same shape")
	if mtx1.size == 0:
		raise ValueError("Input matrices must be >0 rows and >0 cols")

	# translate all the data to the origin
	mean_mtx1 = np.mean(mtx1, 0)
	mean_mtx2 = np.mean(mtx2, 0)
	mtx1 -= mean_mtx1
	mtx2 -= mean_mtx2

	'''
	# We dont require scaling variance in our analysis, so ignored this part of the scipy code. 
	norm1 = np.linalg.norm(mtx1)
	norm2 = np.linalg.norm(mtx2)

	if norm1 == 0 or norm2 == 0:
	    raise ValueError("Input matrices must contain >1 unique points")

	# change scaling of data (in rows) such that trace(mtx*mtx') = 1
	mtx1 /= norm1
	mtx2 /= norm2
	'''

	# transform mtx2 to minimize disparity. This method also takes into account reflective variance
	R_matrix, ss = orthogonal_procrustes(mtx1, mtx2)

	# Obtain the rotated version of data2
	mtx2_rotated = np.dot(mtx2, R_matrix.T) ##* ss
	#mtx2_rotated = np.matmul(R_matrix,mtx2.T).T 

	# get the difference between atom positions between each dimer
	difference_in_atom_positions = np.linalg.norm(mtx1 - mtx2_rotated, axis=1)

	# True if the two dimers are translationally, rotationally, and reflectively variant. False if not. 
	are_varient = all([(distance < max_distance_disparity) for distance in difference_in_atom_positions])

	return are_varient, R_matrix, mean_mtx1, mean_mtx2

##############################################################################################################

def assign_hydrogens_to_ATC_idx(ATC_ase_object, molecule, non_hydrogen_ATC_idx, R_matrix, mean_mol, mean_ATC):
	"""
	This method will match the charge in the ATC file to the right atom in the molecule. 

	Parameters
	----------
	ATC_ase_object : ase.Atoms
		This is the ase object that represents the ATC. This inlcudes the charges
	molecule : ase.Atoms
		This is the molecule that you want to assign charges from the ATC to.
	R_matrix : numpy.array
		This is the rotation matrix which will rotate the ATC_ase_object onto the molecule. Relectivity has been included in this matrix if needed.
	mean_mol : numpy.array
		This is the translational vector to move the molecule to the origin
	mean_ATC : numpy.array
		This is the translational vector to move the ATC object to the origin

	Returns
	-------
	molecule_charges_from_ATC : list
		This is a list of the charges from the ATC to assign to the molecule.
	"""

	# get the positons from the molecule and ATC ase objects
	ATC_positions = ATC_ase_object.get_positions()
	mol_positions = molecule.get_positions()

	# get the elements from the molecule and ATC ase objects
	ATC_symbols = ATC_ase_object.get_chemical_symbols()
	mol_symbols = molecule.get_chemical_symbols()

	# Get the ATC_idx with hydrogens included with None extries
	ATC_idx = []
	add_index_value = 0
	mol_index = 0
	non_hydrogen_ATC_idx_index = 0
	for ATC_index in range(len(ATC_symbols)):
		ATC_symbol = ATC_symbols[ATC_index]
		# if H in ATC_symbol, add None to ATC_idx and move on
		if ATC_symbol == 'H':
			ATC_idx.append(None)
			continue
		while mol_index < len(mol_symbols):
			mol_symbol = mol_symbols[mol_index] 
			mol_index += 1
			# if H in mol_symbol, add 1 to add_index_value. 
			# Keep doing this till you find the next non-hydrogen in mol_symbols.
			if mol_symbol == 'H':
				add_index_value += 1
			else:
				break
		index_value = non_hydrogen_ATC_idx[non_hydrogen_ATC_idx_index]
		non_hydrogen_ATC_idx_index += 1
		ATC_idx.append(index_value+add_index_value)

	# ---------------------------------------------------------------
	# Check
	'''
	non_hydrogen_ATC = remove_hydrogens(ATC_ase_object)
	non_hydrogen_ATC_elements.append(non_hydrogen_ATC.get_chemical_symbols())
	non_hydrogen_ATC_positions.append(non_hydrogen_ATC.get_positions())

	non_hydrogen_molecule = remove_hydrogens(molecule)
	non_hydrogen_molecule_elements.append(non_hydrogen_molecule.get_chemical_symbols())
	non_hydrogen_molecule_positions.append(non_hydrogen_molecule.get_positions())

	# get the difference between atom positions between each dimer
	difference_in_atom_positions = np.linalg.norm(mtx1 - mtx2_rotated, axis=1)

	# True if the two dimers are translationally, rotationally, and reflectively variant. False if not. 
	are_varient = all([(distance < max_distance_disparity) for distance in difference_in_atom_positions])
	'''
	# ---------------------------------------------------------------

	# move the ATC object on top of the molecule object.
	ATC_positions_moved_on_top_of_mol = np.dot(ATC_positions - mean_ATC, R_matrix.T) + mean_mol

	hydrogen_indices_in_ATC = [index for index in range(len(ATC_ase_object)) if (ATC_symbols[index] == 'H')]
	hydrogen_indices_in_mol = [index for index in range(len(molecule))       if (mol_symbols[index] == 'H')]

	ATC_to_mol_hydrogens_comparisons = []
	for ATC_index in hydrogen_indices_in_ATC:
		ATC_position = ATC_positions_moved_on_top_of_mol[ATC_index]
		for mol_index in hydrogen_indices_in_mol:
			mol_position = mol_positions[mol_index]
			distance = get_distance(ATC_position,mol_position)
			ATC_to_mol_hydrogens_comparison_datum = (ATC_index,mol_index,distance)
			ATC_to_mol_hydrogens_comparisons.append(ATC_to_mol_hydrogens_comparison_datum)

	ATC_to_mol_hydrogens_comparisons.sort(key=lambda x:x[2])

	hydrogen_indices_that_have_been_assigned_in_ATC = []
	hydrogen_indices_that_have_been_assigned_in_mol = []

	ATC_to_mol_relation = {}
	for ATC_index, mol_index, distance in ATC_to_mol_hydrogens_comparisons:
		if ATC_index in hydrogen_indices_that_have_been_assigned_in_ATC:
			continue
		if mol_index in hydrogen_indices_that_have_been_assigned_in_mol:
			continue
		ATC_to_mol_relation[ATC_index] = mol_index
		hydrogen_indices_that_have_been_assigned_in_ATC.append(ATC_index)
		hydrogen_indices_that_have_been_assigned_in_mol.append(mol_index)

	if (not sorted(hydrogen_indices_in_ATC) == sorted(ATC_to_mol_relation.keys())) or (not sorted(hydrogen_indices_in_mol) == sorted(ATC_to_mol_relation.values())):
		print('Error in def assign_hydrogens_to_ATC_idx, in invariance_method.py')
		print('Not all the hydrogens in the ATC have been assigned to hydrogens in the associated molecule,')
		print('or a hydrogen in the ATC has been assigned to multiple hydrogen in the associated molecule')
		print()
		print('Hydrogen indices in the ATC: '+str(hydrogen_indices_in_ATC))
		print()
		print('Hydrogen indices in the associated molecule: '+str(hydrogen_indices_in_ATC))
		print()
		print('How the algorithm has associated the ATC hydrogens to the molecules hydrogens: ')
		print(sorted(ATC_to_mol_relation.items()))
		import pdb; pdb.set_trace()
		exit('This program with finished without completing.')

	for ATC_index, mol_index in ATC_to_mol_relation.items():
		if ATC_idx[ATC_index] is None:
			ATC_idx[ATC_index] = mol_index
		else:
			print('Error in def assign_hydrogens_to_ATC_idx, in invariance_method.py')
			print('Tried to assign a hydrogen index from the molecule to a non-hydrogen ATC index')
			print(sorted(ATC_to_mol_relation.items()))
			print('issue with index '+str(ATC_index)+' in ATC_idx')
			print('ATC_idx['+str(ATC_index)+'] = '+str(ATC_idx[ATC_index]))
			import pdb; pdb.set_trace()
			exit('This program with finished without completing.')

	if any([(ATC_idx[ATC_index] is None) for ATC_index in ATC_idx]):
		print('Error in def assign_hydrogens_to_ATC_idx, in invariance_method.py')
		print('One or more of the hydrogen indices in ATC_idx have not be assigned')
		print()
		print('ATC_to_mol_relation: ')
		print(sorted(ATC_to_mol_relation.items()))
		print()
		print('Hydrogen indices in ATC_idx that have not been assigned: '+str([ATC_index for ATC_index in ATC_idx if (ATC_idx[ATC_index] is None)]))
		import pdb; pdb.set_trace()
		exit('This program with finished without completing.')

	return ATC_idx

##############################################################################################################





