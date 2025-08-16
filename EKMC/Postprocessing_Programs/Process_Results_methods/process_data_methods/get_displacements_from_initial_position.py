"""
get_displacement_vectors_from_initial_position.py, Geoffrey Weal, 16/8/22

This script is designed to obtain the displacement vectors for all the simulations over sampled time.
"""
import numpy as np
import multiprocessing as mp

from tqdm import tqdm
from tqdm.contrib.concurrent import process_map

from SUMELF import get_distance

def get_displacements_from_initial_position(displacement_vectors_from_initial_position, cpu_count=1):
    """
    This method is designed to obtain the scalar displacement of the exciton from its initial position, as well as this value squared.

    Parameters
    ----------
    displacement_vectors_from_initial_position : list of list of numpy.array
        These are the displacement vectors of the exciton from the initial_position at t = 0.0 fs to the current position at t = current time.

    Returns
    -------
    displacements_from_initial_position : list of list of floats
        This is a list of the displacements of the exciton from the initial_position at t = 0.0 fs to the current position at t = current time.
    displacements_squared_from_initial_position : list of list of floats
        This is a list of the displacement squared values of the exciton from the initial_position at t = 0.0 fs to the current position at t = current time.
    """

    # First, obtain the displacements across time for each simulation.
    displacements_from_initial_position = process_map(get_displacements_from_initial_position_for_simulation, displacement_vectors_from_initial_position, max_workers=cpu_count, unit=' KMC Sim', desc="Obtaining the exciton displacements over time", leave=False)

    # Second, obtain the displacement squared values across time for each simulation. 
    displacements_squared_from_initial_position = []
    for displacements_from_initial_position_for_simulation in displacements_from_initial_position:
        displacements_squared_from_initial_position_for_simulation = []
        for displacements_from_initial_position_for_simulation_at_time in displacements_from_initial_position_for_simulation:
            displacement_squared_values_from_initial_position_for_simulation_at_time = displacements_from_initial_position_for_simulation_at_time ** 2.0
            displacements_squared_from_initial_position_for_simulation.append(displacement_squared_values_from_initial_position_for_simulation_at_time)
        displacements_squared_from_initial_position.append(displacements_squared_from_initial_position_for_simulation)

    # Third, return displacements_from_initial_position and displacements_squared_from_initial_position
    return displacements_from_initial_position, displacements_squared_from_initial_position

zero_vector = np.array((0.,0.,0.))
def get_displacements_from_initial_position_for_simulation(displacement_vectors_from_initial_position_for_simulation):
    """
    This method is designed to obtain the scalar displacement of the exciton from its initial position for each KMC simulation. 

    Parameters
    ----------
    displacement_vectors_from_initial_position_for_simulation : list of list of numpy.array
        These are the displacement vectors of the exciton for a simulation, from the initial_position at t = 0.0 fs to the current position at t = current time.

    Returns
    -------
    displacements_from_initial_position : list of list of floats
        This is a list of the displacements of the exciton for a simulation, from the initial_position at t = 0.0 fs to the current position at t = current time.
    """

    # First, initialise the list to append the displacements from.
    displacements_from_initial_position_at_time = []

    # Second, for each displacement vector measured for the simulation at the sampled time
    for displacement_vector_from_initial_position_for_simulation_at_time in displacement_vectors_from_initial_position_for_simulation:

        # Third, get the displacement from the displacement vector
        displacement = get_distance(displacement_vector_from_initial_position_for_simulation_at_time, zero_vector)

        # Fourth, append the displacement to displacements_from_initial_position_at_time
        displacements_from_initial_position_at_time.append(displacement)

    # Fifth, return displacements_from_initial_position_at_time
    return displacements_from_initial_position_at_time





