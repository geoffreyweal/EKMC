"""
get_stepwise_diffusion_properties.py, Geoffrey Weal, 20/11/23

This script is designed to obtain the stepwise diffusion properties for the system of interest. 
"""
from tqdm import tqdm
from collections import Counter

import numpy as np
from numpy.linalg import eig

import multiprocessing as mp
from tqdm.contrib.concurrent import process_map

from EKMC.Postprocessing_Programs.Process_Results_methods.process_data_methods.get_diffusion_over_time        import convert_diffusion_coefficient
from EKMC.Postprocessing_Programs.Process_Results_methods.process_data_methods.get_diffusion_tensor_over_time import diagonalise_diffusion_tensor_at_time

displacement_components_to_measure = ((0,0), (1,1), (2,2), (0,1), (0,2), (1,2))

def get_stepwise_diffusion_properties(all_stepwise_diffusion_data, molnames_and_coms):
	"""
	This method is designed to obtain the stepwise diffusion properties for the system of interest. 

	Parameters
	----------
	all_stepwise_diffusion_data : list
		This list contains all the information about each step of each simulation. 
    molnames_and_coms : dict of numpy.array
        This dictionary contains the names of the molecules as well as their centre of masses
	"""

	# First, get the names of the molecules in the crystal to analyse
	molecule_names = sorted(molnames_and_coms.keys())

	# Second, initialise a Counter object to record the number of times the exciton was on a molecule per step.
	molecule_step_counter        = Counter({molecule_name: 0   for molecule_name in molecule_names})

	# Third, initialise the dictionaries to hold data for obtaining the average spatial-based stepwise diffusion tensor. 
	spatial_stepwise_sum_of_tensor_components_per_mol               = {molecule_name : [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]       for molecule_name in molecule_names}
	spatial_stepwise_sum_of_timestep_per_mol                        = {molecule_name : 0.0                                  for molecule_name in molecule_names}
	average_spatial_stepwise_displacement_tensor_components_per_mol = {molecule_name : [None, None, None, None, None, None] for molecule_name in molecule_names}
	average_spatial_stepwise_timestep_per_mol                       = {molecule_name : None                                 for molecule_name in molecule_names}
	average_spatial_stepwise_D_tensors_per_mol                      = {molecule_name : [None, None, None, None, None, None] for molecule_name in molecule_names}

	# Fourth, initialise the dictionaries to hold data for obtaining the average probability-based stepwise diffusion tensor. 
	prob_stepwise_sum_of_D_tensor_components_per_mol                = {molecule_name : [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]       for molecule_name in molecule_names}
	average_prob_stepwise_D_tensors_per_mol                         = {molecule_name : [None, None, None, None, None, None] for molecule_name in molecule_names}

	# Fifth, for each step in each simulation perform the following:
	for molecule_name, displacement_vector, time_step_in_fs, site_energy, apb_D_xx, apb_D_yy, apb_D_zz, apb_D_xy, apb_D_xz, apb_D_yz in tqdm(all_stepwise_diffusion_data):

		# 5.1: Convert the timestep from femtoseconds to picoseconds. 
		time_step_in_ps = time_step_in_fs / 1000

		# 5.2.1: Obtain the components of the spatial-based stepwise displacement tensor  for each molecule in the crystal for this KMC step. 
		for index, (index1, index2) in enumerate(displacement_components_to_measure):
			spatial_stepwise_sum_of_tensor_components_per_mol[molecule_name][index] += displacement_vector[index1] * displacement_vector[index2]

		# 5.2.2: Obtain the components of the spatial-based stepwise timestep for each molecule in the crystal for this KMC step. 
		spatial_stepwise_sum_of_timestep_per_mol[molecule_name] += time_step_in_ps
		
		# 5.3: Obtain the probability-based stepwise diffusion tensor for each molecule in the crystal for this KMC step. 
		for index, apb_D_component in enumerate([apb_D_xx, apb_D_yy, apb_D_zz, apb_D_xy, apb_D_xz, apb_D_yz]):
			prob_stepwise_sum_of_D_tensor_components_per_mol[molecule_name][index] += apb_D_component

		# 5.4: Increment the counter for this molecule. The counter is given by the time the exciton was on the molecule for. 
		molecule_step_counter[molecule_name] += 1

	# ==============================================================================================================================

	# Sixth, get the average for the displacement tensor and timesteps for each molecule across all the steps in all the KMC simulation.
	#          Use thees to obtain the components of the spatial-based stepwise diffusion tensor for each molecule across all the steps in all the KMC simulation.
	
	# 6.1: Obtain the average displacement tensor for each molecule across all the steps in all the KMC simulation. 
	for molecule_name, sum_of_tensor_component_for_a_molecule in spatial_stepwise_sum_of_tensor_components_per_mol.items():
		for index in range(len(sum_of_tensor_component_for_a_molecule)):
			average_displacement = sum_of_tensor_component_for_a_molecule[index] / molecule_step_counter[molecule_name]
			average_spatial_stepwise_displacement_tensor_components_per_mol[molecule_name][index] = average_displacement
	
	# 6.2: Obtain the average time step for each molecule across all the steps in all the KMC simulation. 
	for molecule_name, sum_of_time_steps_in_ps_for_a_molecule in spatial_stepwise_sum_of_timestep_per_mol.items():
		average_time_step = sum_of_time_steps_in_ps_for_a_molecule / molecule_step_counter[molecule_name]
		average_spatial_stepwise_timestep_per_mol[molecule_name] = average_time_step

	# 6.3: Obtain the spatial-based stepwise diffusion tensor for each molecule across all the steps in all the KMC simulation
	for molecule_name in average_spatial_stepwise_displacement_tensor_components_per_mol.keys(): 

		# 6.3.1: Obtain the average displacement tensor and timesteps for the molecule of interest. 
		average_spatial_stepwise_displacement_tensor_components = average_spatial_stepwise_displacement_tensor_components_per_mol[molecule_name]
		average_spatial_stepwise_timestep                       = average_spatial_stepwise_timestep_per_mol[molecule_name]

		# 6.3.2: Obtain the spatial-based stepwise diffusion tensor for the molecule of interest. 
		for index in range(len(average_spatial_stepwise_displacement_tensor_components)):
			spatial_stepwise_diffusion_tensor_component_in_A2_per_ps = (1.0/2.0) * average_spatial_stepwise_displacement_tensor_components[index] / average_spatial_stepwise_timestep
			spatial_stepwise_diffusion_tensor_component = convert_diffusion_coefficient(spatial_stepwise_diffusion_tensor_component_in_A2_per_ps)
			average_spatial_stepwise_D_tensors_per_mol[molecule_name][index] = spatial_stepwise_diffusion_tensor_component
		
	# ==============================================================================================================================

	# Seventh, obtain the probability that the exciton will be on a certain molecule during the KMC simulation. 
	total = sum(molecule_step_counter.values())
	probability_exciton_found_on_molecule = {key: value/total for key, value in molecule_step_counter.items()}

	# Eighth, obtain the overall spatial-based stepwise diffusion tensor for this crystal, and use this to obtain the eigenvalues and 
	#        eigenvectors of the spatial-based stepwise diffusion tensor, as well as the exciton diffusion coefficient using the 
	#        eigenvalues of the spatial-based stepwise diffusion tensor.
	spatial_stepwise_D_tensor = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
	for molecule_name, sum_of_spatial_stepwise_D_tensor_components in average_spatial_stepwise_D_tensors_per_mol.items():
		for index in range(len(sum_of_spatial_stepwise_D_tensor_components)):
			spatial_stepwise_D_tensor[index] += sum_of_spatial_stepwise_D_tensor_components[index] * probability_exciton_found_on_molecule[molecule_name]
	eigenvalues_of_spatial_stepwise_diffusion_tensor, eigenvectors_of_spatial_stepwise_diffusion_tensor, diffusion_coefficient_from_spatial_stepwise_diffusion_tensor = get_data_from_diagonalisation(spatial_stepwise_D_tensor)

	# Ninth, obtain the overall probability-based stepwise diffusion tensor for this crystal, and use this to obtain the eigenvalues and 
	#        eigenvectors of the probability-based stepwise diffusion tensor, as well as the exciton diffusion coefficient using the 
	#        eigenvalues of the probability-based stepwise diffusion tensor.
	prob_stepwise_D_tensor = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
	for molecule_name, sum_of_prob_stepwise_D_tensor_components_for_a_molecule in prob_stepwise_sum_of_D_tensor_components_per_mol.items():
		for index in range(len(sum_of_prob_stepwise_D_tensor_components_for_a_molecule)):
			average_prob_stepwise_D_tensors_per_mol[molecule_name][index] = sum_of_prob_stepwise_D_tensor_components_for_a_molecule[index] / molecule_step_counter[molecule_name]
			prob_stepwise_D_tensor[index] += average_prob_stepwise_D_tensors_per_mol[molecule_name][index] * probability_exciton_found_on_molecule[molecule_name]
	eigenvalues_of_prob_stepwise_diffusion_tensor, eigenvectors_of_prob_stepwise_diffusion_tensor, diffusion_coefficient_from_prob_stepwise_diffusion_tensor = get_data_from_diagonalisation(prob_stepwise_D_tensor)

	import pdb; pdb.set_trace()

	# Tenth, return stepwise diffusion properties
	return spatial_stepwise_D_tensor, eigenvalues_of_spatial_stepwise_diffusion_tensor, eigenvectors_of_spatial_stepwise_diffusion_tensor, diffusion_coefficient_from_spatial_stepwise_diffusion_tensor, prob_stepwise_D_tensor, eigenvalues_of_prob_stepwise_diffusion_tensor, eigenvectors_of_prob_stepwise_diffusion_tensor, diffusion_coefficient_from_prob_stepwise_diffusion_tensor

def get_data_from_diagonalisation(stepwise_diffusion_tensor):
	"""
	This method is designed to diagonalise the stepwise diffusion tensor to obtain the eigenvalues and eigenvector of said matrix, 
	as well as use the eigenvalues to obtain the exciton diffusion coefficient for the crystal. 

	Parameters
	----------
	stepwise_diffusion_tensor : list of 6 floats
		This list contains the component of the stepwise diffusion tensor, given as [D_xx, D_yy, D_zz, D_xy = D_yx, D_xz = D_zx, D_yz = D_zy]

	Returns
	-------
	eigenvalues_of_stepwise_diffusion_tensor : 3x1 numpy.array
		These are the eigenvalues of the stepwise diffusion tensor
	eigenvectors_of_stepwise_diffusion_tensor : 3x3 numpy.array
		These are the eigenvectors of the stepwise diffusion tensor
	diffusion_coefficient_from_stepwise_diffusion_tensor : float
		This is the diffusion coefficient as calculated using the eigenvalue of the stepwise diffusion tensor. 
	"""

	# First, create the stepwise diffusion tensor matrix
	stepwise_diffusion_tensor_row_1 = (stepwise_diffusion_tensor[0], stepwise_diffusion_tensor[3], stepwise_diffusion_tensor[4])
	stepwise_diffusion_tensor_row_2 = (stepwise_diffusion_tensor[3], stepwise_diffusion_tensor[1], stepwise_diffusion_tensor[5])
	stepwise_diffusion_tensor_row_3 = (stepwise_diffusion_tensor[4], stepwise_diffusion_tensor[5], stepwise_diffusion_tensor[2])
	stepwise_diffusion_tensor = np.array([stepwise_diffusion_tensor_row_1, stepwise_diffusion_tensor_row_2, stepwise_diffusion_tensor_row_3])

	# Second, diagonalise the stepwise diffusion tensor matrix to get the eigenvalues and eigenvectors of the stepwise diffusion tensor.
	eigenvalues_of_stepwise_diffusion_tensor, eigenvectors_of_stepwise_diffusion_tensor = diagonalise_diffusion_tensor_at_time(stepwise_diffusion_tensor)

	# THird, use the eigenvalues of the stepwise diffusion tensor to get the diffusion_coefficient
	diffusion_coefficient_from_stepwise_diffusion_tensor = (eigenvalues_of_stepwise_diffusion_tensor[0] + eigenvalues_of_stepwise_diffusion_tensor[1] + eigenvalues_of_stepwise_diffusion_tensor[2]) ** (1./2.)

	# Fourth, return data
	return eigenvalues_of_stepwise_diffusion_tensor, eigenvectors_of_stepwise_diffusion_tensor, diffusion_coefficient_from_stepwise_diffusion_tensor

