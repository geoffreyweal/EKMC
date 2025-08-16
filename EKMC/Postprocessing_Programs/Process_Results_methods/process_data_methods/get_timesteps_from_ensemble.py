"""
get_timesteps_from_ensemble.py, Geoffrey Weal, 17/8/22

This script is designed to gather the timesteps obtained over time for all simulations.
"""
import numpy as np
from tqdm import tqdm

def get_timesteps_from_ensemble(all_sims):
    """
    This method is designed to obtain the timesteps for all the simulations over all time.

    Parameters
    ----------
    all_sims : list
        This is the data obtained for all kinetic Monte Carlo simulations. 

    Returns
    -------
    timesteps_for_all_sims : list
        This is a list of all the timesteps for each simulation.
    time_for_all_sims : list
        This is a list of all the times for each movement for each simulation.
    """

    # Currently not using this, just return None.
    return None, None

    '''

    # First, initialise the lists to record the timesteps and times of each exciton movement for each simulation.
    time_for_all_sims      = []
    timesteps_for_all_sims = []

    # Second, for each simulation
    for a_sim in tqdm(all_sims, unit='sims'):

        # Third, intialise the lists to record the timesteps and times of each exciton movement for a simulation.
        time_for_a_sim      = []
        timesteps_for_a_sim = []

        # Fourth, for each movement in the simulation.
        for count, molecule, cell_point, sim_time, change_in_time, energy, sum_of_kij in a_sim[1]:

            # Fifth, append the simulation time and the timestep to the previous lists
            time_for_a_sim.append(sim_time)
            timesteps_for_a_sim.append(change_in_time)

        # Sixth, append the times and timesteps for the current simulation to the overall lists
        time_for_all_sims.append(time_for_a_sim)
        timesteps_for_all_sims.append(timesteps_for_a_sim)

    # Seventh, return timesteps_for_all_sims and time_for_all_sims
    return timesteps_for_all_sims, time_for_all_sims

    '''



