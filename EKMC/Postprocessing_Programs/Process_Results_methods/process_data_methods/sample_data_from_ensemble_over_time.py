"""
sample_data_from_ensemble_over_time.py, Geoffrey Weal, 16/8/22

This script is designed to obtain the data from each of the simulation over time, sampled at time intervals of dt and ending at sim_time_limit.
"""
import numpy as np

import multiprocessing as mp
from tqdm.contrib.concurrent import process_map

def sample_data_from_ensemble_over_time(all_sims, sim_time_limit, no_of_times_to_sample=10000, cpu_count=1):
    """
    This method will sample the data from each of the simulation over time, sampled at time intervals of dt and ending at sim_time_limit

    Parameters
    ----------
    all_sims : list
        This is the data obtained for all kinetic Monte Carlo simulations. 
    sim_time_limit : float
        This it the time that all kinetic Monte Carlo simulations were simulated for.
    no_of_times_to_sample : int
        This is the number of times to samples over, from 0.0 fs to sim_time_limit fs

    Returns
    -------
    time : list of floats
        These are the times that have been sampled.
    data_over_time_for_all_sims : list
        This is the data of each simulations at each time interval.
    """
    
    # First, obtain the data from the simulations as sampled over time
    if cpu_count == 1:
        data_over_time_for_all_sims = [get_data_over_time(input_data) for input_data in get_inputs(all_sims, sim_time_limit, no_of_times_to_sample)]
    else:
        data_over_time_for_all_sims = process_map(get_data_over_time, get_inputs(all_sims, sim_time_limit, no_of_times_to_sample), max_workers=cpu_count, unit=' KMC Sim', total=len(all_sims), desc="Sampling all KMC simulations over time", leave=False)

    # Second, initialise all the times to record over
    times = np.linspace(0.0, sim_time_limit, num=no_of_times_to_sample+1)

    # Third, return the sample times and data_over_time_for_all_sims
    return data_over_time_for_all_sims, times

def get_inputs(all_sims, sim_time_limit, no_of_times_to_sample):
    """
    This generator is designed to give each simulation data in all_sims, along with sim_time_limit and no_of_times_to_sample

    Parameters
    ----------
    all_sims : list
        This is the data obtained for all kinetic Monte Carlo simulations. 
    sim_time_limit : float
        This it the time that all kinetic Monte Carlo simulations were simulated for.
    no_of_times_to_sample : int
        This is the number of times to samples over, from 0.0 fs to sim_time_limit fs
    """
    for simulation_datum in all_sims:
        yield (simulation_datum, sim_time_limit, no_of_times_to_sample)

def get_data_over_time(input_datum):
    """
    This method is designed to sample a simulation over time.

    Parameters
    ----------
    simulation_datum : list
        This is the data obtained for a single kinetic Monte Carlo simulation. 
    sim_time_limit : float
        This it the time that all kinetic Monte Carlo simulations were simulated for.
    no_of_times_to_sample : int
        This is the number of times to samples over, from 0.0 fs to sim_time_limit fs

    Returns
    -------
    data_over_time_for_simulation : list
        This is the data of the current simulation at each time interval.
    """

    # First, get the input data to process the simulation over time
    simulation_datum, sim_time_limit, no_of_times_to_sample = input_datum

    # Second, note the current index to monitor.
    index = 0

    # Third, initialise all the times to record over
    times = np.linspace(0.0, sim_time_limit, num=no_of_times_to_sample+1)

    # Fourth, initialise the list to save sampled data to over time.
    data_over_time_for_simulation = []

    # Fifth, for each time to sample
    for time in times:

        # Sixth, determine the index of simulation_datum to sample.
        while True:

            # 6.1: Get the simulation time at index
            sim_time = simulation_datum[1][index][3]

            # 6.2: If the simulation time for index is creater than time, we want to sample simulation_datum at index-1.
            if sim_time > time:
                index -= 1
                break

            # 6.3: Else, increment index by 1
            index += 1

        # Seventh, Obtain the data from index position in simulation_data
        count, molecule, cell_point, sim_time, change_in_time, hopping_distance, energy, sum_of_kij, D_xx, D_yy, D_zz, D_xy, D_xz, D_yz = simulation_datum[1][index]

        # Eighth, append data to data_over_time_for_simulation
        data_over_time_for_simulation.append((molecule, cell_point, energy))

    # Ninth, return data_over_time_for_simulation
    return data_over_time_for_simulation

