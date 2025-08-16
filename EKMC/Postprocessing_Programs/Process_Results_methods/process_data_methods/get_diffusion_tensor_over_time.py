"""
get_diffusion_over_time.py, Geoffrey Weal, 16/8/22

This script is designed to obtain the diffusion coefficient of an ensemble of the same system over time.
"""
import numpy as np
from numpy.linalg import eig

import multiprocessing as mp
from tqdm.contrib.concurrent import process_map

from EKMC.Postprocessing_Programs.Process_Results_methods.process_data_methods.get_diffusion_over_time import convert_diffusion_coefficient

def get_diffusion_tensor_over_time(times, displacement_vectors_from_initial_position, cpu_count=1):
    """
    This method is designed to obtain the diffusion coefficient of an ensemble of the same system over time.

    Parameters
    ----------
    times : list/numpy.array
        These are the sample times sampled for each simulation in the ensemble.
    displacement_vectors_from_initial_position : list of list of floats
        These are the displacement vectors of the each simulation in the ensemble over sampled time.

    Returns
    -------
    diffusion_over_time : list of floats
        This is the diffusion coefficients over time across the ensemble of simulations.
    """
    
    # First, obtain the data from the simulations as sampled over time
    diffusion_tensor_over_time = process_map(get_diffusion_tensor_at_time, get_inputs(times, displacement_vectors_from_initial_position), max_workers=cpu_count, unit=' sample times', total=len(times), desc="Obtaining the Diffusion Tensor over time", leave=False)

    # Second, diagonalise the diffusion tensor over time
    diagonalised_diffusion_tensor_over_time = process_map(diagonalise_diffusion_tensor_at_time, diffusion_tensor_over_time, max_workers=cpu_count, unit=' sample times', total=len(times), desc="Diagonalising the Diffusion Tensor over time", leave=False)

    # Third, separate the diagonalised_diffusion_tensor_over_time into two lists, one that holds eigenvalues and one that holds eigenvectors
    eigenvalues_of_diffusion_tensor_over_time  = [eigenvalues  for eigenvalues, eigenvectors in diagonalised_diffusion_tensor_over_time]
    eigenvectors_of_diffusion_tensor_over_time = [eigenvectors for eigenvalues, eigenvectors in diagonalised_diffusion_tensor_over_time]

    # Fourth, return diffusion_tensor_over_time
    return diffusion_tensor_over_time, eigenvalues_of_diffusion_tensor_over_time, eigenvectors_of_diffusion_tensor_over_time

def get_inputs(times, displacement_vectors_from_initial_position):
    """
    This generator is designed to give each simulation data in all_sims, along with sim_time_limit and no_of_times_to_sample

    Parameters
    ----------
    times : list/numpy.array
        These are the sample times sampled for each simulation in the ensemble.
    displacement_vectors_from_initial_position : list of list of floats
        These are the displacement vectors of the each simulation in the ensemble over sampled time.
    """

    for index in range(0,len(times)):
        time = times[index]
        XYZ_distance_values_from_initial_position_for_sims_at_a_time = [displacement_vectors_from_initial_position_for_a_sim[index] for displacement_vectors_from_initial_position_for_a_sim in displacement_vectors_from_initial_position]
        yield (time, XYZ_distance_values_from_initial_position_for_sims_at_a_time)

def get_diffusion_tensor_at_time(input_data):
    """
    This method is designed to obtain the diffusion tensor at a specific sample time.

    Parameters
    ----------
    times : list/numpy.array
        These are the sample times sampled for each simulation in the ensemble.
    XYZ_distance_values_from_initial_position_for_sims_at_a_time : list of list of floats
        These are the displacement vectors of the each simulation in the ensemble at a sampled time.

    Returns
    -------
    diffusion_tensor : np.array
        This is the diffusion tensor at the sampled time.
    """

    # First, extract the data from the data list.
    time, XYZ_distance_values_from_initial_position_for_sims_at_a_time = input_data

    # Second, obtain the displacement in each direction.
    X_displacement_values_from_initial_position_for_sims_at_a_time = [x_disp for x_disp, y_disp, z_disp in XYZ_distance_values_from_initial_position_for_sims_at_a_time]
    Y_displacement_values_from_initial_position_for_sims_at_a_time = [y_disp for x_disp, y_disp, z_disp in XYZ_distance_values_from_initial_position_for_sims_at_a_time]
    Z_displacement_values_from_initial_position_for_sims_at_a_time = [z_disp for x_disp, y_disp, z_disp in XYZ_distance_values_from_initial_position_for_sims_at_a_time]

    # Third, obtain the diffusion coefficient for each component in the diffusion tensor
    diffusion_XX_at_time = get_2D_diffusion_coefficient(X_displacement_values_from_initial_position_for_sims_at_a_time, X_displacement_values_from_initial_position_for_sims_at_a_time, time)
    diffusion_XY_at_time = get_2D_diffusion_coefficient(X_displacement_values_from_initial_position_for_sims_at_a_time, Y_displacement_values_from_initial_position_for_sims_at_a_time, time)
    diffusion_XZ_at_time = get_2D_diffusion_coefficient(X_displacement_values_from_initial_position_for_sims_at_a_time, Z_displacement_values_from_initial_position_for_sims_at_a_time, time)
    
    diffusion_YX_at_time = get_2D_diffusion_coefficient(Y_displacement_values_from_initial_position_for_sims_at_a_time, X_displacement_values_from_initial_position_for_sims_at_a_time, time)
    diffusion_YY_at_time = get_2D_diffusion_coefficient(Y_displacement_values_from_initial_position_for_sims_at_a_time, Y_displacement_values_from_initial_position_for_sims_at_a_time, time)
    diffusion_YZ_at_time = get_2D_diffusion_coefficient(Y_displacement_values_from_initial_position_for_sims_at_a_time, Z_displacement_values_from_initial_position_for_sims_at_a_time, time)
    
    diffusion_ZX_at_time = get_2D_diffusion_coefficient(Z_displacement_values_from_initial_position_for_sims_at_a_time, X_displacement_values_from_initial_position_for_sims_at_a_time, time)
    diffusion_ZY_at_time = get_2D_diffusion_coefficient(Z_displacement_values_from_initial_position_for_sims_at_a_time, Y_displacement_values_from_initial_position_for_sims_at_a_time, time)
    diffusion_ZZ_at_time = get_2D_diffusion_coefficient(Z_displacement_values_from_initial_position_for_sims_at_a_time, Z_displacement_values_from_initial_position_for_sims_at_a_time, time)

    # Fourth, obtain the diffusion tensor at time.
    diffusion_tensor = np.array([[diffusion_XX_at_time, diffusion_XY_at_time, diffusion_XZ_at_time], [diffusion_YX_at_time, diffusion_YY_at_time, diffusion_YZ_at_time], [diffusion_ZX_at_time, diffusion_ZY_at_time, diffusion_ZZ_at_time]])

    # Fifth, return diffusion_tensor
    return diffusion_tensor

def get_2D_diffusion_coefficient(dimension_displacement_1, dimension_displacement_2, time):
    """
    This method is designed to obtain the 2D diffsion coefficient, used to obtain the components of the diffusion tensor.

    Parameters
    ----------
    dimension_displacement_1 : list of floats
        This is the displacement in one dimension across the whole ensemble of KMC simulations at time.
    dimension_displacement_2 : list of floats
        This is another set of displacements in one dimension across the whole ensemble of KMC simulations at time. Can be the same or different dimension as dimension_displacement_1
    time : float
        This is the time that dimension_displacement_1 and dimension_displacement_2 were sampled at.
    """

    # First, obtain the squared displacement across dimension_displacement_1 and dimension_displacement_2
    average_disp_squared_12 = np.mean([(disps_1 * disps_2) for disps_1, disps_2 in zip(dimension_displacement_1, dimension_displacement_2)])

    # Second, obtain the diffusion_coefficient across dimension 1 and 2
    diffusion_coefficient_12_in_A2_per_ps = average_disp_squared_12/(2*time)

    # Fourth, convert the diffusion coefficient from A^2/ps to cm^2/s
    diffusion_coefficient_12_in_cm2_per_s = convert_diffusion_coefficient(diffusion_coefficient_12_in_A2_per_ps)

    # Fifth, return diffusion_coefficient_in_cm2_per_s
    return diffusion_coefficient_12_in_cm2_per_s

def diagonalise_diffusion_tensor_at_time(diffusion_tensor_at_time):
    """
    This method is designed to diagonalise the diffusion tensors at each sampled time.

    Parameters
    ----------
    diffusion_tensor_at_time : numpy.array
        This is the diffusion tensor at the sampled time.

    Returns
    -------

    """

    # First, calculate the eigenvalues and eigenvectors of the diffusion tensor at the recorded sampled time.
    try:
        eigenvalues, eigenvectors = eig(diffusion_tensor_at_time)
    except:
        return np.array((np.nan, np.nan, np.nan)), np.array((np.nan, np.nan, np.nan))

    # Second, order the eigenvalues and associated eigenvector from the highest to lowest eigenvalue.
    idx = eigenvalues.argsort()[::-1]   
    eigenvalues  = eigenvalues[idx]
    eigenvectors = eigenvectors[:,idx]

    # Third, return eigenvalues and eigenvectors
    return eigenvalues, eigenvectors


















