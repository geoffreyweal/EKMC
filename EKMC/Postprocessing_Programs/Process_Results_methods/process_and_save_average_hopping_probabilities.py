"""
time_average_data.py, Geoffrey Weal, 30/8/22

This script is designed to collect the time average data for simulations
"""

import os
from statistics import mean, stdev

def process_and_save_average_hopping_probabilities(data_foldername, path, all_sims_hop_probs):

    all_sims_hop_probs = get_average_hopping_probabilities(all_sims_hop_probs)
    save_average_hopping_probabilities(data_foldername, path, all_sims_hop_probs)


def get_average_hopping_probabilities(all_sims_hop_probs):
    """
    This method is designed to obtain the average hopping probability for between exciton donor and all its neighbouring exciton acceptors across all simulations performed. 

    Parameters
    ----------
    all_sims_hop_probs : list
        This is the hopping probability data between exciton donor and all its neighbouring exciton acceptors.
    """

    print('Rearranging Hopping Probability Data')

    # First, gather all the hopping probabilities across all simulation and concatenate them together. 
    all_hop_probs_across_sims = {}
    for index, sim_hop_probs in enumerate(all_sims_hop_probs):
        simname, sim_hop_probs_data = sim_hop_probs
        for exciton_donor_acceptor_info in list(sim_hop_probs_data.keys()):
            all_hop_probs_across_sims[exciton_donor_acceptor_info] = all_hop_probs_across_sims.get(exciton_donor_acceptor_info,[]) + sim_hop_probs_data[exciton_donor_acceptor_info]
            del all_sims_hop_probs[index][1][exciton_donor_acceptor_info]

    print('Obtaining Average Hopping Probability for Exciton Donor Acceptor Hops')

    # Second, obtain the average and standard deviations for all hopping probabilities across all simulation together. 
    for exciton_donor_acceptor_info in all_hop_probs_across_sims:
        mean_hopping_probability  = mean(all_hop_probs_across_sims[exciton_donor_acceptor_info])
        stdev_hopping_probability = stdev(all_hop_probs_across_sims[exciton_donor_acceptor_info])
        all_hop_probs_across_sims[exciton_donor_acceptor_info] = (mean_hopping_probability, stdev_hopping_probability)

    # Third, return all_hop_probs_across_sims
    return all_hop_probs_across_sims

def save_average_hopping_probabilities(data_foldername, path, all_sims_hop_probs):
    """
    Save the data for the average hopping probabilities into a text file. 

    Parameters
    ----------
    all_sims_hop_probs : list
        This is the hopping probability data between exciton donor and all its neighbouring exciton acceptors.
    """
    print('Save exciton hopping probability data and figures to disk.')
    path_to_place_data_in = data_foldername+'/'+path
    if path_to_place_data_in[-1] == '/':
        path_to_place_data_in = path_to_place_data_in[:-1]
    time_averaged_filename = 'Average_Hopping_Probability.txt'

    if os.path.exists(path_to_place_data_in+'/'+time_averaged_filename):
        os.remove(path_to_place_data_in+'/'+time_averaged_filename)

    with open(path_to_place_data_in+'/'+time_averaged_filename, 'w') as fileTXT:
        for exciton_donor_acceptor_info in sorted(all_sims_hop_probs.keys(), key=lambda x: (x[0], x[1], abs(x[2]), abs(x[3]), abs(x[4]), -x[2], -x[3], -x[4])):
            average_hopping_probability, stdev_hopping_probability = all_sims_hop_probs[exciton_donor_acceptor_info]
            fileTXT.write(str(exciton_donor_acceptor_info)+': '+str(average_hopping_probability)+' ['+str(average_hopping_probability)+']\n')







