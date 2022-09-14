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
    all_sims = process_map(read_EKMC_datafile, get_folder_path(root, sim_names), max_workers=cpu_count, unit=' KMC Sim', total=len(sim_names))

    # Sixth, sort the simulation data by it's simulation folder name.
    all_sims.sort(key=lambda x: int(x[0].replace('Sim','')))

    # Sixth, return the data for all the kinetic Monte Carlo simulations
    return all_sims

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
    '''
    counter = 0
    for sim_name in sim_names:
        yield (root, sim_name)
        counter += 1
        if counter == 10:
            break
    '''
    for sim_name in sim_names:
        yield (root, sim_name)

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
        for line in datafile:

            # Sixth, extract the data from the line.
            count, molecule, cell_point, sim_time, time_step, energy, sum_kij, end_of_line = line.rstrip().split()

            # Seventh, convert all the variables into ints, tuples, and floats
            count = int(count)
            molecule = int(molecule)
            cell_point = eval(cell_point)
            sim_time = float(sim_time)
            time_step = float(time_step)
            energy = float(energy) 
            sum_kij = float(sum_kij)

            # Eighth, save this data to the data list
            data.append((count, molecule, cell_point, sim_time, time_step, energy, sum_kij))

    # Ninth, sort the data by the count
    data.sort()

    # Tenth, return the data list.
    return (sim_name,data)


