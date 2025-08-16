'''
Check_Result.py, Geoffrey Weal, 12/8/22

This program will determine 
'''
import os

from tqdm.contrib.concurrent import process_map

def collect_data(root, cpu_count=1):
    """
    This method is designed to gather all the kinetic Monte Carlo data for all the kinetic Monte Carlo simulations performed.

    Parameters
    ----------
    root : str
        This is the path to the folders that contain kinetic Monte Carlo simulations.

    Returns
    -------
    all_sims : list
        This is all the data from all the kinetic Monte Carlo simulations performed. 
    """

    print('Collecting the various KMC simulation data from disk.')

    # First, obtain the names of the folders that contain each of the kinetic Monte Carlo simulations.
    sim_names = [dirname for dirname in os.listdir(root) if (os.path.isdir(root+'/'+dirname) and dirname.startswith('Sim') and dirname.replace('Sim','').isdigit())]

    # Second, collect all the data from all the  kinetic Monte Carlo simulations
    all_sims = []

    # Third, obtain all the names of the simulation folders
    sim_names.sort(key=lambda x: int(x.replace('Sim','')))

    # Fourth, obtain the number of cpus that are available for use.
    print('Number of CPUs that will be used: '+str(cpu_count))

    # Fifth, obtain the data from all the kinetic Monte Carlo simulations.
    all_sims = process_map(read_EKMC_datafile, get_folder_path(root, sim_names), max_workers=cpu_count, unit=' KMC Sim', total=len(sim_names), desc="Obtaining the data from all the kinetic Monte Carlo simulations", leave=False)

    # Sixth, sort the simulation data by it's simulation folder name.
    all_sims.sort(key=lambda x: int(x[0].replace('Sim','')))

    # Seventh, obtain the data from all the kinetic Monte Carlo simulations.
    #all_sims_hop_probs = [read_EKMC_rate_constant_datafile(input_data) for input_data in get_folder_path_rate_constants(root, all_sims)]
    all_sims_hop_probs = process_map(read_EKMC_rate_constant_datafile, get_folder_path_rate_constants(root, all_sims), max_workers=cpu_count, unit=' KMC Sim Probs', total=len(sim_names), desc="Obtaining the rate constant data from all the kinetic Monte Carlo simulations (if this data has been written to disk)", leave=False)

    # Eighth, return the data for all the kinetic Monte Carlo simulations
    return all_sims, all_sims_hop_probs

def get_folder_path(root, sim_names):
    """
    This is a generator designed to generator all the path to all the KMC simulations in root. 

    Parameters
    ----------
    root : str.
        This is the path to the folders that contain kinetic Monte Carlo simulations.
    sim_name : str.
        This is the name of the simulation folder that contains the information about the kinetic Monte Carlo simulation.
    """
    for sim_name in sim_names:
        yield (root, sim_name)

def get_folder_path_rate_constants(root, all_sims):
    """
    This is a generator designed to generator all the path to all the KMC simulations in root. 

    Parameters
    ----------
    root : str.
        This is the path to the folders that contain kinetic Monte Carlo simulations.
    sim_name : str.
        This is the name of the simulation folder that contains the information about the kinetic Monte Carlo simulation.
    """
    for a_sim in all_sims:
        sim_name, sim_data = a_sim
        yield (root, sim_name, sim_data)

EKMC_data_filename = 'kMC_sim.txt'
def read_EKMC_datafile(input_data):
    """
    This method is designed to read the data from the kinetic Monte Carlo simulation files, called EKMC_data_filename

    Parameters
    ----------
    root : str.
        This is the path to the overall folder that contains all the kinetic Monte Carlo simulations for a particular system.
    sim_name : str.
        This is the name of the simulation that was performed, and is the name of the folder that it's kinetic Monte Carlo simulation is held in.

    Attributes
    ----------
    EKMC_data_filename :str.
        This is the name of the data files that contain the kinetic Monte Carlo simulation data.

    Returns
    -------
    data : list
        This is the list of the movement of the exciton about the molecules of the crystal over time. 
    """

    # First, separate the input_data into the root and the sim_name variables.
    root, sim_name = input_data

    # Second, initalise the data list to record the data about this kinetic Monte Carlo simulation. 
    data = []

    # Third, open the EKMC_data_filename file.
    with open(root+'/'+sim_name+'/'+EKMC_data_filename, 'r') as datafile:

        # Fourth, ignore the first line, which is the top of the table
        datafile.readline()

        # Fifth, for each line in the datafile:
        #counter = 0
        for line in datafile:

            # Sixth, extract the data from the line.
            count, molecule, cell_point, sim_time, time_step, hopping_distance, energy, sum_kij, end_of_line1, D_xx, D_yy, D_zz, D_xy, D_xz, D_yz, end_of_line2 = line.rstrip().split()

            # Seventh, convert all the variables into ints, tuples, and floats
            count            = int(count)
            molecule         = int(molecule)
            cell_point       = eval(cell_point)
            sim_time         = float(sim_time)
            time_step        = float(time_step)
            hopping_distance = float(hopping_distance) 
            energy           = float(energy) 
            sum_kij          = float(sum_kij)
            D_xx             = float(D_xx)
            D_yy             = float(D_yy)
            D_zz             = float(D_zz)
            D_xy             = float(D_xy)
            D_xz             = float(D_xz)
            D_yz             = float(D_yz)

            # Eighth, save this data to the data list
            data.append((count, molecule, cell_point, sim_time, time_step, hopping_distance, energy, sum_kij, D_xx, D_yy, D_zz, D_xy, D_xz, D_yz))

            #if counter > 10:
            #    break
            #counter += 1

    # Ninth, sort the data by the count
    data.sort()

    # Tenth, return the data list.
    return (sim_name, data)

import re
EKMC_rate_constant_data_filename = 'kMC_sim_rate_constants.txt'
def read_EKMC_rate_constant_datafile(input_data):
    """
    This method is designed to read the rate constant data from the kinetic Monte Carlo simulation files, called EKMC_rate_constant_data_filename

    The rate constant data given is for an exciton on an exciton donor to all the neighbouring exciton acceptor. 

    Parameters
    ----------
    root : str.
        This is the path to the overall folder that contains all the kinetic Monte Carlo simulations for a particular system.
    sim_name : str.
        This is the name of the simulation that was performed, and is the name of the folder that it's kinetic Monte Carlo simulation is held in.

    Attributes
    ----------
    EKMC_rate_constant_data_filename :str.
        This is the name of the data files that contain the kinetic Monte Carlo simulation data.

    Returns
    -------
    data : list
        This is the list of the movement of the exciton about the molecules of the crystal over time. 
    """

    # First, separate the input_data into the root and the sim_name variables.
    root, sim_name, sim_data = input_data

    # Second, initalise the data list to record the data about this kinetic Monte Carlo simulation. 
    hop_probability_data = {}

    # Third, get the path to the EKMC_rate_constant_data_filename
    path_to_EKMC_rate_constant_data_filename = root+'/'+sim_name+'/'+EKMC_rate_constant_data_filename

    # Fourth, check to see if the EKMC_rate_constant_data_filename file exists. 
    if os.path.exists(path_to_EKMC_rate_constant_data_filename):

        # Fifth, open the EKMC_data_filename file.
        with open(path_to_EKMC_rate_constant_data_filename, 'r') as datafile:

            # Sixth, ignore the first line, which is the top of the table
            datafile.readline()

            # Seventh, for each line in the datafile:
            for line, sim_datum in zip(datafile, sim_data):

                counter_KMC_sim = sim_datum[0]
                simulation_time = sim_datum[3]

                if simulation_time < 500.0: 
                    continue

                # 7.1: Split string into exciton donor informtion and the corresponding exciton acceptor rate constants. 
                exciton_donor_info, exciton_acceptor_rate_constants = line.rstrip().split('-->')

                # 7.2: Get the molecule name for the exciton donor that the exciton is current on.
                counter_KMC_sim_prob, exciton_donor_info = exciton_donor_info.split(':')
                counter_KMC_sim_prob = int(counter_KMC_sim_prob)
                if not counter_KMC_sim == counter_KMC_sim_prob:
                    raise Exception('Error')

                # 7.2: Get the molecule name for the exciton donor that the exciton is current on.
                exciton_donor_name = int(exciton_donor_info.split()[0])

                # 7.3: Get the unit cell position for the exciton donor that the exciton is currently on. 
                exciton_donor_unit_cell_position = eval(re.findall(r'\(.*?\)', exciton_donor_info)[0])

                # 7.4: Get the unit cell position for the exciton donor that the exciton is currently on. 
                sum_of_k_ijs = float(re.findall(r'\[.*?\]', exciton_donor_info)[0].replace('[','').replace(']','')) # s-1

                #hop_probability_data.setdefault(exciton_donor_name,{})

                # 7.5: Get the rate constant data for the neighbouring exciton acceptors.
                for exciton_acceptor_rate_constant_data in exciton_acceptor_rate_constants.split('/'):

                    # 7.5.1: split the data into info and rate constant data.
                    exciton_acceptor_info, exciton_acceptor_rate_constant = exciton_acceptor_rate_constant_data.split(':')

                    # 7.5.2: Get the molecule name for the exciton acceptor that the exciton could hop to.
                    exciton_acceptor_name = int(exciton_acceptor_info.split()[0])

                    # 7.5.3: Get the unit cell position for the exciton acceptor that the exciton could hop to.
                    exciton_acceptor_unit_cell_position = eval(re.findall(r'\(.*?\)', exciton_acceptor_info)[0])

                    # 7.5.4: Get the rate constant data for an exciton moving from the exciton donor the exciton is currently 
                    #        on, to the neighbouring exciton acceptor. 
                    exciton_acceptor_hop_probability = float(exciton_acceptor_rate_constant)/sum_of_k_ijs

                    relative_exciton_acceptor_unit_cell_position_i = exciton_acceptor_unit_cell_position[0] - exciton_donor_unit_cell_position[0]
                    relative_exciton_acceptor_unit_cell_position_j = exciton_acceptor_unit_cell_position[1] - exciton_donor_unit_cell_position[1]
                    relative_exciton_acceptor_unit_cell_position_k = exciton_acceptor_unit_cell_position[2] - exciton_donor_unit_cell_position[2]

                    exciton_donor_acceptor_info = (exciton_donor_name, exciton_acceptor_name, relative_exciton_acceptor_unit_cell_position_i, relative_exciton_acceptor_unit_cell_position_j, relative_exciton_acceptor_unit_cell_position_k)

                    #hop_probability_data[exciton_donor_name].setdefault(exciton_acceptor_info, []).append(exciton_acceptor_hop_probability)
                    if not exciton_donor_acceptor_info in hop_probability_data:
                        hop_probability_data[exciton_donor_acceptor_info] = []
                    hop_probability_data.setdefault(exciton_donor_acceptor_info,[]).append(exciton_acceptor_hop_probability)

    # Come back here
    #for exciton_donor_name in hop_probability_data.keys():
    #    for exciton_acceptor_info in hop_probability_data[exciton_donor_name].keys():
    #        all_hopping_probabilities = hop_probability_data[exciton_donor_name][exciton_acceptor_info]
    #        hop_probability_data[exciton_donor_name][exciton_acceptor_info] = sum(all_hopping_probabilities) / float(len(all_hopping_probabilities))

    # Eighth, return the hop_probability_data containing hopping probability averages.
    return (sim_name, hop_probability_data)





