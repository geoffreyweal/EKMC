'''
Check_Result.py, Geoffrey Weal, 12/8/22

This program will determine 
'''
import numpy as np
from tqdm import trange

from EKMC.Postprocessing_Programs.Process_Results_methods.process_data_methods.sample_data_from_ensemble_over_time     import sample_data_from_ensemble_over_time
from EKMC.Postprocessing_Programs.Process_Results_methods.process_data_methods.get_timesteps_from_ensemble             import get_timesteps_from_ensemble
from EKMC.Postprocessing_Programs.Process_Results_methods.process_data_methods.get_sample_data_from_ensemble_over_time import get_sample_data_from_ensemble_over_time
from EKMC.Postprocessing_Programs.Process_Results_methods.process_data_methods.get_displacements_from_initial_position import get_displacements_from_initial_position
from EKMC.Postprocessing_Programs.Process_Results_methods.process_data_methods.get_diffusion_over_time                 import get_diffusion_over_time
from EKMC.Postprocessing_Programs.Process_Results_methods.process_data_methods.get_diffusion_tensor_over_time          import get_diffusion_tensor_over_time
from EKMC.Postprocessing_Programs.Process_Results_methods.process_data_methods.get_average_values_over_time            import get_average_values_over_time

def process_data(all_sims, molnames_and_coms, unit_cell_matrix, end_recording_time, no_of_times_to_sample=10000, cpu_count=1):
    """
    This method is designed to process the data from across all simulations performed for this system.
    """

    # First, collect the positions of exciton for each Simulation every dt intervals
    print('Sampling '+str(no_of_times_to_sample+1)+' time points from the ensemble of simulations between 0 ps and '+str(end_recording_time)+' ps (intervals of '+str(float(end_recording_time)/no_of_times_to_sample)+' ps)')
    data_over_time_for_all_sims, times = sample_data_from_ensemble_over_time(all_sims, end_recording_time, no_of_times_to_sample=no_of_times_to_sample, cpu_count=cpu_count)

    # Second, obtain the distance from the starting point across all ensembles.
    print('Get the displacement vectors from the ensemble of simulations')
    positions_at_time, displacement_vectors_from_initial_position, energies_over_time_for_all_sims = get_sample_data_from_ensemble_over_time(data_over_time_for_all_sims, molnames_and_coms, unit_cell_matrix, cpu_count=cpu_count)
    
    # Third, delete the data_over_time_for_all_sims which contains a lot of information that is not needed anymore. 
    del data_over_time_for_all_sims

    # Fourth, obtain the displacement and displacement^2 values.
    print('Get the displacements from the ensemble of simulations')
    displacements_from_initial_position, displacements_squared_from_initial_position = get_displacements_from_initial_position(displacement_vectors_from_initial_position, cpu_count=cpu_count)

    # Fifth, get the diffusion values of the system over time.
    print('Get the Diffusion Coefficients from the ensemble of simulations')
    diffusion_over_time = get_diffusion_over_time(times, displacements_squared_from_initial_position, cpu_count=cpu_count)

    # Sixth, get the diffusion tensor of the system over time.
    print('Get the Diffusion Tensor from the ensemble of simulations')
    diffusion_tensor_over_time, eigenvalues_of_diffusion_tensor_over_time, eigenvectors_of_diffusion_tensor_over_time = get_diffusion_tensor_over_time(times, displacement_vectors_from_initial_position, cpu_count=cpu_count)

    # Seventh, get data for plotting and showing/comparing
    print('Obtaining data for comparisons and plotting.')
    average_displacements_from_initial_position_over_time, average_displacements_squared_from_initial_position_over_time, average_energies_over_time = get_average_values_over_time(displacements_from_initial_position, displacements_squared_from_initial_position, energies_over_time_for_all_sims)

    # Eighth, gather the timestep information from across all ensembles
    print('Gather the timesteps of exciton movements over time.')
    all_timesteps, time_for_all_sims = get_timesteps_from_ensemble(all_sims)

    # Ninth, return the lists of quantities across all ensembles for each sampled time.
    return times, positions_at_time, average_displacements_from_initial_position_over_time, average_displacements_squared_from_initial_position_over_time, average_energies_over_time, diffusion_over_time, diffusion_tensor_over_time, eigenvalues_of_diffusion_tensor_over_time, eigenvectors_of_diffusion_tensor_over_time, all_timesteps, time_for_all_sims
