"""
get_initial_data_for_beginning_kMC.py, Geoffrey Weal, 26/3/22

This script is designed to determine if the simulation has already finished based on the simulation time run.
"""
import os
from EKMC.EKMC.Run_EKMC_setup_files.reverse_readline import reverse_readline 

def did_finish(kMC_sim_name, sim_time_limit, max_no_of_steps):
    """
    This method will determine if the simulation has already finished based on the simulation time run.

    Parameters
    ----------
    kMC_sim_name : str.
        This is the name/path to the KMC simulation text file.
    sim_time_limit : float
        This is the maximum simulated time limit to run the kinetic Monte Carlo simulation over.
    max_no_of_steps : int
        This is the maximum number of kmc steps to run the kinetic Monte Carlo simulation over.

    Returns
    -------
    If True, the simulation has finished. If False, the simulation has not finished
    """

    # First, set the current time to 0.0 ps and the number of steps performed to 0 if the simulation has not started. 
    time = 0.0
    no_of_steps = 0

    # Second, get the last point in the KMC simulation from the kMC_sim_name file.
    if os.path.exists(kMC_sim_name):
        end_lines_to_remove = 0
        for line in reverse_readline(kMC_sim_name):
            if line.startswith('Count'):
                break
            if line.endswith('|'):
                line = line.rstrip().split()
                no_of_steps = int(line[0])
                molecule_name = int(line[1])
                cell_point = eval(line[2])
                time = float(line[3])
                break 

    # Third, determine if the simulation has either run for as long as the user wants, or has reached the maximum number of steps that the user want to perform. 
    reached_sim_time_limit  = False if (sim_time_limit  == 'inf') else (time > sim_time_limit)
    reached_max_no_of_steps = False if (max_no_of_steps == 'inf') else (no_of_steps > max_no_of_steps)

    # Third, return if the simulation finished, and the current simulation time and number of kmc steps performed. 
    return reached_sim_time_limit, reached_max_no_of_steps, time, no_of_steps