"""
get_sample_data_from_ensemble_over_time.py, Geoffrey Weal, 16/8/22

This script is designed to obtain the displacement vectors and energies for all the simulations over sampled time.
"""
import numpy as np

import multiprocessing as mp
from tqdm.contrib.concurrent import process_map

def get_sample_data_from_ensemble_over_time(data_over_time, molnames_and_coms, unit_cell_matrix, cpu_count=1):
    """
    This method is designed to obtain the displacement vectors and energies for all the simulations over sampled time.

    Parameters
    ----------
    data_over_time : list
        This is the list of molecule number, cell_point, and energy of each simulation per sampled simulation time.
    molnames_and_coms : dict of numpy.array
        This dictionary contains the names of the molecules as well as their centre of masses
    unit_cell_matrix : numpy.array
        These are the lattice vectors of the unit cell.

    Returns
    -------
    displacement_vectors_from_initial_point : list
        This is a list of the displacement vectors (over sampled time) for each simulation.
    energies_over_time_for_all_sims : list
        This is a list of the energies (over sampled time) for each simulation.
    timesteps_over_time_for_all_sims : list
        This is a list of the timesteps (over sampled time) for each simulation.
    """

    # First, obtain the displacement vector for each KMC simulation.
    data = process_map(get_displacement_vector_from_initial_position, get_inputs(data_over_time, molnames_and_coms, unit_cell_matrix), max_workers=cpu_count, unit=' KMC Sim', total=len(data_over_time), desc="Sampling the KMC simulation data over time", leave=False)

    # Second, obtain the displacement_vectors and energies for each simulation over sampled time from data.
    positions_at_time = []
    displacement_vectors_from_initial_point = []
    energies_over_time_for_all_sims = []
    for position_at_time, displacement_vectors_from_initial_point_for_a_sim, energies_over_time_for_a_sim in data:
        positions_at_time.append(position_at_time)
        displacement_vectors_from_initial_point.append(displacement_vectors_from_initial_point_for_a_sim)
        energies_over_time_for_all_sims.append(energies_over_time_for_a_sim)

    # Third, return displacement_vectors_from_initial_point
    return positions_at_time, displacement_vectors_from_initial_point, energies_over_time_for_all_sims

def get_inputs(data_over_time, molnames_and_coms, unit_cell_matrix):
    """
    This generator is designed to give thr data for each KMC simulation in data_over_time, along with molnames_and_coms, unit_cell_matrix and initial_position

    Parameters
    ----------
    data_over_time : list
        This is the data obtained for all kinetic Monte Carlo simulations.
    molnames_and_coms : dict of numpy.array
        This dictionary contains the names of the molecules as well as their centre of masses
    unit_cell_matrix : numpy.array
        These are the lattice vectors of the unit cell.
    """
    for datum_at_time in data_over_time:
        yield (datum_at_time, molnames_and_coms, unit_cell_matrix)

def get_displacement_vector_from_initial_position(input_datum):
    """
    This method is designed to obtain the displacement vectors for a single KMC simulations over sampled time.

    Parameters
    ----------
    data_over_time : list
        This is the data obtained for all kinetic Monte Carlo simulations at a single sampled time.
    molnames_and_coms : dict of numpy.array
        This dictionary contains the names of the molecules as well as their centre of masses
    unit_cell_matrix : numpy.array
        These are the lattice vectors of the unit cell.

    Returns
    -------
    displacement_vectors_from_initial_point_for_a_sim : list
        These are the displacement vectors from the initial position at time 0.0 fs to the position of the exciton at the sampled time.
    """

    # First, obtain the data from input_datum
    data_over_time, molnames_and_coms, unit_cell_matrix = input_datum

    # Second, obtain the intial molecule and cell_point for this simulation
    initial_molecule, initial_cell_point, initial_energy = data_over_time[0]

    # Third, obtain the initial position for this simulation.
    initial_position = get_position(initial_molecule, initial_cell_point, molnames_and_coms, unit_cell_matrix)

    # Second, initialise the list to record the displacement vectors from initial_point across time. 
    positions_at_time = []
    displacement_vectors_from_initial_point_for_a_sim = []
    energies_over_time_for_a_sim = []
    timesteps_over_time_for_a_sim = []

    # Third, for each set of spatial data over time
    for molname, cell_point, energy in data_over_time:

        # Fourth, obtain the position of the exciton in the crystal.
        position_at_time = get_position(molname, cell_point, molnames_and_coms, unit_cell_matrix)
        positions_at_time.append(position_at_time)

        # Fifth, get the displacement vector for disp(t=current time) - disp(t=0.0 fs)
        displacement_vector = position_at_time - initial_position

        # Sixth, append this displacement_vector to displacement_vectors_from_initial_point_at_time
        displacement_vectors_from_initial_point_for_a_sim.append(displacement_vector)

        # Seventh, collect the energy values of the exciton in the system at this sample time
        energies_over_time_for_a_sim.append(energy)

    # Seventh, return displacement_vectors_from_initial_point_for_a_sim
    return positions_at_time, displacement_vectors_from_initial_point_for_a_sim, energies_over_time_for_a_sim

def get_position(molname, cell_point, molnames_and_coms, unit_cell_matrix):
    """
    This method is designed to get the position of the exciton given the cell point of the exciton and the molecule the exciton is on.

    Parameters
    ----------
    molname : int
        This is the name of the molecule that the exciton is currently on.
    cell_point : tuple
        This described the ijk values of the cell the exciton is currently in.
    molnames_and_coms : list of numpy.array
        This is the centre of mass for each molecule in the crystal unit cell.
    unit_cell_matrix : numpy.array
        These are the lattice vectors of the unit cell.

    Returns
    -------
    position : numpy.array
        This is the position of the exciton on molecule in the cell described by the ijk values of cell_point
    """

    # First, get the position of the exciton.
    # Note: Because of how unit cell works in ASE, need to perform
    #       np.matmul(cell_point,unit_cell_matrix) or np.matmul(unit_cell_matrix.T,cell_point)
    position = np.matmul(cell_point,unit_cell_matrix) + molnames_and_coms[molname]

    # Second, return the position of the exciton in the cell.
    return position

