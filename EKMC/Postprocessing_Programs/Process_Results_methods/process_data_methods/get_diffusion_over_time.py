"""
get_diffusion_over_time.py, Geoffrey Weal, 16/8/22

This script is designed to obtain the diffusion coefficient of an ensemble of the same system over time.
"""
import numpy as np

import multiprocessing as mp
from tqdm.contrib.concurrent import process_map

def get_diffusion_over_time(times, displacement_squared_values_from_initial_position, cpu_count=1):
    """
    This method is designed to obtain the diffusion coefficient of an ensemble of the same system over time.

    Parameters
    ----------
    times : list/numpy.array
        These are the sample times sampled for each simulation in the ensemble.
    displacement_squared_values_from_initial_position : list of list of floats
        These are the displacement squared values of the each simulation in the ensemble over sampled time.

    Returns
    -------
    diffusion_over_time : list of floats
        This is the diffusion coefficients over time across the ensemble of simulations.
    """

    # First, the diffusion coefficients as sampled over time
    diffusion_over_time = process_map(get_diffusion_at_time, get_inputs(times, displacement_squared_values_from_initial_position), max_workers=cpu_count, unit=' sample times', total=len(times), desc="Obtaining the Diffusion Coefficient over time", leave=False)

    # Second, return diffusion_over_time
    return diffusion_over_time

def get_inputs(times, displacement_squared_values_from_initial_position):
    """
    This generator is designed to give each simulation data in all_sims, along with sim_time_limit and no_of_times_to_sample

    Parameters
    ----------
    times : list/numpy.array
        These are the sample times sampled for each simulation in the ensemble.
    displacement_squared_values_from_initial_position : list of list of floats
        These are the displacement squared values of the each simulation in the ensemble over sampled time.
    """

    for index in range(0,len(times)):
        time = times[index]
        displacement_squared_values_from_initial_position_for_sims_at_a_time = [displacement_squared_values_from_initial_position_for_a_sim[index] for displacement_squared_values_from_initial_position_for_a_sim in displacement_squared_values_from_initial_position]
        yield (time, displacement_squared_values_from_initial_position_for_sims_at_a_time)

def get_diffusion_at_time(input_data):
    """
    This method is designed to obtain the diffusion tensor at a specific sample time.

    Parameters
    ----------
    times : list/numpy.array
        These are the sample times sampled for each simulation in the ensemble.
    displacement_squared_values_from_initial_position_for_sims_at_a_time : list of list of floats
        These are the displacement squared values of the each simulation in the ensemble at a sampled time.

    Returns
    -------
    diffusion_coefficient_in_cm2_per_s : float
        This is the diffusion coefficient at the sampled time. Given in units of cm^2/s
    """

    # First, extract the data from the data list.
    time, displacement_squared_values_from_initial_position_for_sims_at_a_time = input_data

    # Second, get the average displacement squared values across all simulations in the ensemble at time.
    average_displacement_squared = np.mean(displacement_squared_values_from_initial_position_for_sims_at_a_time)

    # Third, obtain the diffusion coefficient at time. Units are A^2/ps
    diffusion_coefficient_in_A2_per_ps = average_displacement_squared/(6*time)

    # Fourth, convert the diffusion coefficient from A^2/ps to cm^2/s
    diffusion_coefficient_in_cm2_per_s = convert_diffusion_coefficient(diffusion_coefficient_in_A2_per_ps)

    # Fifth, return diffusion_coefficient_in_cm2_per_s
    return diffusion_coefficient_in_cm2_per_s

A_to_cm = (10.0 ** -10.0)/(10.0 ** -2.0)
ps_to_s = 10.0 ** -12.0
A_to_cm_squared_divide_by_ps_to_s = (A_to_cm ** 2.0) / ps_to_s
def convert_diffusion_coefficient(diffusion_coefficient_in_A2_per_ps):
    """
    This method is designed to convert the diffusion coefficient from A^2/ps to cm^2/s

    Parameters
    ----------
    diffusion_coefficient_in_A2_per_ps : float
        This is the diffusion coefficient in A^2/ps

    Returns
    -------
    diffusion_coefficient_in_cm2_per_s : float
        This is the diffusion coefficient in cm^2/s
    """

    # First, convert the diffusion coefficient from A^2/ps to cm^2/s
    diffusion_coefficient_in_cm2_per_s = diffusion_coefficient_in_A2_per_ps * A_to_cm_squared_divide_by_ps_to_s

    # Second, return diffusion_coefficient_in_cm2_per_s
    return diffusion_coefficient_in_cm2_per_s



