'''
Check_Result.py, Geoffrey Weal, 12/8/22

This program will determine 
'''
from tqdm import trange

def gather_and_format_step_data(all_sims, begin_recording_no_of_steps):
    """
    This method is designed to process the data from across all simulations performed for this system.
    """

    # First, go through all the data in all_sims and remove all steps that are less than begin_recording_no_of_steps
    for index in trange(len(all_sims)):

        # 1.1: Record a pointer to the information we want to reduce to steps greater than or equal to begin_recording_no_of_steps.
        steps_information = all_sims[index][1]

        # 1.2: Check to see that there are more steps to sample than begin_recording_no_of_steps
        if len(steps_information) <= begin_recording_no_of_steps:
            exit('Error. There are not enough steps to record. Total number of steps: '+str(len(steps_information)-1)+'; Step number to begin recording: '+str(begin_recording_no_of_steps))

        # 1.3: Remove all steps in simulations that are less than begin_recording_no_of_steps
        del all_sims[index][1][:begin_recording_no_of_steps]

    # Second, check that all the simulations have the same number of steps recorded.
    if not len(set([len(all_sim[1]) for all_sim in all_sims])) == 1:
        raise Exception('here ')

    # Third, return the reduced steps version of all_sims.
    return all_sims
