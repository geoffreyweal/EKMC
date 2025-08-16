'''
Check_Result.py, Geoffrey Weal, 12/8/22

This program will determine 
'''
import numpy as np
from tqdm import trange

from EKMC.Postprocessing_Programs.Process_Results_of_Steps_methods.process_data_methods.gather_and_format_step_data       import gather_and_format_step_data
from EKMC.Postprocessing_Programs.Process_Results_of_Steps_methods.process_data_methods.get_stepwise_information          import get_stepwise_information
from EKMC.Postprocessing_Programs.Process_Results_of_Steps_methods.process_data_methods.get_stepwise_diffusion_properties import get_stepwise_diffusion_properties
'''
from EKMC.Postprocessing_Programs.Process_Results_methods.process_data_methods.get_sample_data_from_ensemble_over_time import get_sample_data_from_ensemble_over_time
from EKMC.Postprocessing_Programs.Process_Results_methods.process_data_methods.get_displacements_from_initial_position import get_displacements_from_initial_position
from EKMC.Postprocessing_Programs.Process_Results_methods.process_data_methods.get_diffusion_over_time                 import get_diffusion_over_time
from EKMC.Postprocessing_Programs.Process_Results_methods.process_data_methods.get_diffusion_tensor_over_time          import get_diffusion_tensor_over_time
from EKMC.Postprocessing_Programs.Process_Results_methods.process_data_methods.get_average_values_over_time            import get_average_values_over_time
'''

def process_data(all_sims, molnames_and_coms, unit_cell_matrix, begin_recording_no_of_steps, cpu_count=1):
    """
    This method is designed to process the data from across all simulations performed for this system.
    """

    # First, collect the data from all_sims that you want to record, and format it.
    print('Sampling simulation steps from step '+str(begin_recording_no_of_steps)+' onwards')
    all_sims = gather_and_format_step_data(all_sims, begin_recording_no_of_steps-1)

    # Second, 
    print('Get the data for all the individual steps across the ensemble of simulations')
    all_stepwise_diffusion_data = get_stepwise_information(all_sims, molnames_and_coms, unit_cell_matrix, cpu_count=cpu_count)

    print('Get the displacements from the ensemble of simulations')
    spatial_stepwise_D_tensor, eigenvalues_of_spatial_stepwise_diffusion_tensor, eigenvectors_of_spatial_stepwise_diffusion_tensor, diffusion_coefficient_from_spatial_stepwise_diffusion_tensor, prob_stepwise_D_tensor, eigenvalues_of_prob_stepwise_diffusion_tensor, eigenvectors_of_prob_stepwise_diffusion_tensor, diffusion_coefficient_from_prob_stepwise_diffusion_tensor = get_stepwise_diffusion_properties(all_stepwise_diffusion_data, molnames_and_coms)


    import pdb; pdb.set_trace()



    # Eighth, return the lists of quantities across all ensembles for each sampled time.
    return spatial_stepwise_D_tensor, eigenvalues_of_spatial_stepwise_diffusion_tensor, eigenvectors_of_spatial_stepwise_diffusion_tensor, diffusion_coefficient_from_spatial_stepwise_diffusion_tensor, prob_stepwise_D_tensor, eigenvalues_of_prob_stepwise_diffusion_tensor, eigenvectors_of_prob_stepwise_diffusion_tensor, diffusion_coefficient_from_prob_stepwise_diffusion_tensor