"""
get_sample_data_from_ensemble_over_time.py, Geoffrey Weal, 16/8/22

This script is designed to obtain the displacement vectors and energies for all the simulations over sampled time.
"""
import numpy as np

import multiprocessing as mp
from tqdm.contrib.concurrent import process_map

def get_stepwise_information(all_sims, molnames_and_coms, unit_cell_matrix, cpu_count=1):
    """
    This method is designed to obtain the stepwise displacement vectors and energies for all the simulations over all the steps that you want to sample over.

    Parameters
    ----------
    all_sims : list
        This is the 
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
    #[get_stepwise_information_for_each_step(input_datum) for input_datum in get_inputs(all_sims, molnames_and_coms, unit_cell_matrix)]
    all_simulation_stepwise_diffusion_data = process_map(get_stepwise_information_for_each_step, get_inputs(all_sims, molnames_and_coms, unit_cell_matrix), max_workers=cpu_count, unit=' KMC Sim', total=len(all_sims))

    # Second, obtain the displacement_vectors and energies for each simulation over sampled time from data.
    all_stepwise_diffusion_data = [j for sub in all_simulation_stepwise_diffusion_data for j in sub]

    # Third, return displacement_vectors_from_initial_point
    return all_stepwise_diffusion_data

def get_inputs(all_sims, molnames_and_coms, unit_cell_matrix):
    """
    This generator is designed to give thr data for each KMC simulation in data_over_time, along with molnames_and_coms, unit_cell_matrix and initial_position

    Parameters
    ----------
    data_over_time : list
        This is the 
    molnames_and_coms : dict of numpy.array
        This dictionary contains the names of the molecules as well as their centre of masses
    unit_cell_matrix : numpy.array
        These are the lattice vectors of the unit cell.
    """
    for simulation_data in all_sims:
        yield (simulation_data, molnames_and_coms, unit_cell_matrix)

def get_stepwise_information_for_each_step(input_datum):
    """
    This method is designed to obtain the displacement vectors for a single KMC simulations across all the steps you want to sample across. 

    Parameters
    ----------
    data_over_time : list
        This is the  
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
    simulation_data, molnames_and_coms, unit_cell_matrix = input_datum

    # Second, obtain the intial molecule and cell_point for this simulation
    initial_counter, initial_molecule, initial_cell_point, initial_simulation_time, initial_time_step, initial_hop_distance, initial_energy, initial_sum_of_kij, initial_D_xx, initial_D_yy, initial_D_zz, initial_D_xy, initial_D_xz, initial_D_yz = simulation_data[1][0]

    # Third, obtain the initial position for this simulation.
    initial_position = get_position(initial_molecule, initial_cell_point, molnames_and_coms, unit_cell_matrix)

    # Fourth, initialise the list to record the diffusion data for each step. 
    stepwise_diffusion_data = []

    # Fifth, for each set of spatial data over time
    for simulation_datum in simulation_data[1][1:]:

        # 5.1: Get the information about step index-1 from step index
        final_counter, final_molecule, final_cell_point, final_simulation_time, final_time_step, final_hop_distance, final_energy, final_sum_of_kij, final_D_xx, final_D_yy, final_D_zz, final_D_xy, final_D_xz, final_D_yz = simulation_datum

        # 5.2: Get the position of the exciton at step index
        final_position = get_position(final_molecule, final_cell_point, molnames_and_coms, unit_cell_matrix)

        # 5.3: Get the displacement vector for the exciton hop for step index
        displacement_vector = final_position - initial_position

        # 5.4: Get the time step for step index
        time_step = final_time_step

        # 5.5: Record the diffusion data for step index-1
        stepwise_diffusion_data.append((initial_molecule, displacement_vector, time_step, initial_energy, initial_D_xx, initial_D_yy, initial_D_zz, initial_D_xy, initial_D_xz, initial_D_yz))

        # 5.6: Set final data to initial data.
        initial_molecule        = final_molecule
        initial_cell_point      = final_cell_point
        initial_position        = final_position
        initial_simulation_time = final_simulation_time
        initial_time_step       = final_time_step
        initial_hop_distance    = final_hop_distance
        initial_energy          = final_energy
        initial_sum_of_kij      = final_sum_of_kij
        initial_D_xx            = final_D_xx
        initial_D_yy            = final_D_yy
        initial_D_zz            = final_D_zz
        initial_D_xy            = final_D_xy
        initial_D_xz            = final_D_xz
        initial_D_yz            = final_D_yz

    # Sixth, return stepwise_diffusion_data
    return stepwise_diffusion_data

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

