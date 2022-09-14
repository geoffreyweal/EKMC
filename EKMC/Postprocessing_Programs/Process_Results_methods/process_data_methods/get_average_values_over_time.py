"""
get_average_values_over_time.py, Geoffrey Weal, 17/8/22

This script is designed to obtain the average values of quantity across the ensemble over time.
"""
import numpy as np

from tqdm import trange

def get_average_values_over_time(displacements_from_initial_position, displacements_squared_from_initial_position, energies_over_time_for_all_sims):
    """
    This method is designed to obtain the average values of quantity across the ensemble over time.

    Parameters
    ----------
    displacements_from_initial_position : list
        These are the displacements from all ensembles over all sampled time.
    displacements_squared_from_initial_position : list
        These are the displacement squared values from all ensembles over all sampled time.
    energies_over_time_for_all_sims : list
        These are the energies from all ensembles over all sampled time.

    Returns
    -------
    average_displacements_from_initial_position_over_time : list
        These are the average displacements across all ensembles over all sampled time.
    average_displacements_squared_from_initial_position_over_time : list
        These are the average displacement squared values across all ensembles over all sampled time.
    average_energies_over_time : list
        These are the average energies across all ensembles over all sampled time.
    """

    # First, swap the rows and columns of the matrices from matrix[simulation][sample time] to matrix[sample time][simulation].
    displacements_from_initial_position_reverse = swap_2D_list_rows_and_columns(displacements_from_initial_position)
    displacements_squared_from_initial_position_reverse = swap_2D_list_rows_and_columns(displacements_squared_from_initial_position)
    energies_reverse = swap_2D_list_rows_and_columns(energies_over_time_for_all_sims)

    # Second, get the average displacement, displacement squared, and energies across the ensembles over sampled time
    average_displacements_from_initial_position_over_time = [np.mean(displacements_from_initial_position_reverse_at_time) for displacements_from_initial_position_reverse_at_time in displacements_from_initial_position_reverse]
    average_displacements_squared_from_initial_position_over_time = [np.mean(displacements_squared_from_initial_position_reverse_at_time) for displacements_squared_from_initial_position_reverse_at_time in displacements_squared_from_initial_position_reverse]
    average_energies_over_time = [np.mean(energies_reverse_at_time) for energies_reverse_at_time in energies_reverse]

    # Third, return average quantity lists.
    return average_displacements_from_initial_position_over_time, average_displacements_squared_from_initial_position_over_time, average_energies_over_time

def swap_2D_list_rows_and_columns(a_2D_list):
    """
    This method is designed to swap the rows and colurms of 2D lists so that:

                matrix[simulation][sample time] --> matrix[sample time][simulation]

    Parameters
    ----------
    a_2D_list : list
        This is a 2D list with rows and columns given as matrix[simulation][sample time]

    Returns
    -------
    a_2D_list_reverse : list
        This is a 2D list with rows and columns reversed, given as matrix[sample time][simulation]
    """

    # First, initise the a_2D_list_reverse list
    a_2D_list_reverse = [[None]*len(a_2D_list) for non in a_2D_list[0]]

    #Second, create the 2D list that is the reverse of a_2D_list, where the rows and columns have been swapped.
    for ii in trange(len(a_2D_list)):
        for jj in range(len(a_2D_list[ii])):
            a_2D_list_reverse[jj][ii] = a_2D_list[ii][jj]

    # Third, return a_2D_list_reverse
    return a_2D_list_reverse

