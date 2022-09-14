"""
get_initial_data_for_beginning_kMC.py, Geoffrey Weal, 26/3/22

This script is designed to determine if the simulation has already finished based on the simulation time run.
"""
import os
from EKMC.EKMC.kMC_algorithm_methods.reverse_readline import reverse_readline 

def did_finish(kMC_sim_name, sim_time_limit):
    """
    This method will determine if the simulation has already finished based on the simulation time run.

    Parameters
    ----------
    kMC_sim_name : str.
        This is the name/path to the KMC simulation text file.
    sim_time_limit : float
        This is the simulated time limit to run the kinetic Monte Carlo simulation over.

    Returns
    -------
    If True, the simulation has finished. If False, the simulation has not finished
    """

    # First, set the current tiem to 0.0 ps if the simulation has not befin
    time = 0.0

    # Second, get the last point in the KMC simulation from the kMC_sim_name file.
    if os.path.exists(kMC_sim_name):
        end_lines_to_remove = 0
        for line in reverse_readline(kMC_sim_name):
            if line.startswith('Count'):
                return False, None, None, None, None
            if line.endswith('|'):
                line = line.rstrip().split()
                count = int(line[0])
                molecule_name = int(line[1])
                cell_point = eval(line[2])
                time = float(line[3])
                break 

    # Third, return if the simulation finished, and the current simulation time.
    return (time > sim_time_limit), time