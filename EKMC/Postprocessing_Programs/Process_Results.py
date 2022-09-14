'''
Check_Result.py, Geoffrey Weal, 12/8/22

This program will determine 
'''
import os
import numpy as np
import multiprocessing as mp
from tqdm import tqdm

from ase.io import read

from EKMC.Postprocessing_Programs.Process_Results_methods.collect_data               import collect_data
from EKMC.Postprocessing_Programs.Process_Results_methods.process_data               import process_data
from EKMC.Postprocessing_Programs.Process_Results_methods.save_data_and_plot_figures import save_data_and_plot_figures
from EKMC.Postprocessing_Programs.Process_Results_methods.time_average_data          import time_average_data
from EKMC.Postprocessing_Programs.Process_Results_methods.save_time_averaged_data    import save_time_averaged_data
from EKMC.Postprocessing_Programs.Process_Results_methods.save_to_excel_spreadsheet  import save_to_excel_spreadsheet

class CLICommand:
    """Will determine which exciton kinetic monte carlo jobs have run for the time you desire.
    """
    @staticmethod
    def add_arguments(parser):
        parser.add_argument('no_of_cpus', nargs='*', help='This is the number of CPUs to use to process data.')
        parser.add_argument('path_to_crystal_file', nargs='*', help='This is the crystal to add to Diffusion Diagonalisation Eigenvector Analysis.')

    @staticmethod
    def run(arguments):

        # First, print the number of cpus to use
        no_of_cpus = arguments.no_of_cpus
        if not no_of_cpus == []:
            no_of_cpus = int(no_of_cpus[0])
        else:
            no_of_cpus = 1

        # Second, print the path to the crystal file
        path_to_crystal_file = arguments.path_to_crystal_file
        if not path_to_crystal_file == []:
            path_to_crystal_file = path_to_crystal_file[0]
            try:
                read(path_to_crystal_file)
            except:
                exit('Error: Problem with input crystal file: '+str(path_to_crystal_file))
        else:
            path_to_crystal_file = None

        # Third, run the processing program.
        Run_method(path_to_crystal_file, no_of_cpus=no_of_cpus)

KMC_setup_data_filename = 'KMC_setup_data.ekmc'
data_foldername = 'EKMC_Ensemble_Data_Folder'
def Run_method(path_to_crystal_file=None, no_of_cpus=1):
    """
    This method will create a number of plots for checking the simulations performed, as well as to obtain data about your KMC simulation.
    """

    # First, get the current path.
    #current_path = os.getcwd()

    roots = []

    # First, for each subdirectory in the path
    for root, dirs, files in os.walk('.'):

        dirs.sort()
        files.sort()

        # Second, if you are searching through data_foldername, move on.
        if data_foldername in root:
            dirs[:]  = []
            files[:] = []
            continue

        # Third, check that the current subdirectory contains Sim folders.
        # These contain the kinetic Monte Carlo simulations.
        for dirname in dirs:
            if (dirname.startswith('Sim') and dirname.replace('Sim','').isdigit()):
                break
        else:
            continue

        # Fourth, check to see if KMC_setup_data_filename is in the root
        path_to_KMC_setup_data_file = root+'/'+KMC_setup_data_filename
        if not os.path.exists(path_to_KMC_setup_data_file):
            print('==============================================================================')
            print('Error: Sim folder(s) found, but no '+str(KMC_setup_data_filename)+' file found. Check this.')
            print('In: '+str(root))
            print('==============================================================================')
            dirs[:]  = []
            files[:] = []
            continue

        # Fifth, retrieve data for setting up the kinetic Monte Carlo simulation from the KMC_setup_data.ekmc file.
        with open(path_to_KMC_setup_data_file,'r') as KMC_setup_data_EKMC:
            centre_of_masses = [np.array(centre_of_mass) for centre_of_mass in eval(KMC_setup_data_EKMC.readline().rstrip())]
            unit_cell_matrix = np.array(eval(KMC_setup_data_EKMC.readline().rstrip()))
            KMC_setup_data_EKMC.readline()
            kinetic_model_parameters = eval(KMC_setup_data_EKMC.readline().rstrip())
            energetic_disorder = kinetic_model_parameters['energetic_disorder']
            temperature = kinetic_model_parameters['temperature']

        # Sixth, get the path to the Run_EKMC.py to get the simulation time limit from.
        #dirs.sort(key=lambda x: int(x.replace('Sim','')))
        for dirname in dirs+['.']:
            path_to_KMC_Run_file = root+'/'+dirname+'/Run_EKMC.py'
            if os.path.exists(path_to_KMC_Run_file):
                break
        else:
            print('==============================================================================')
            print('Error: Run_EKMC.py file could not be found. Check this.')
            print('In: '+str(root))
            print('==============================================================================')
            dirs[:]  = []
            files[:] = []
            continue

        # Seventh, get the simulation time limit from the Run_EKMC.py
        with open(path_to_KMC_Run_file) as KMC_setup_data_EKMC:
            for line in KMC_setup_data_EKMC:
                if 'sim_time_limit' in line:
                    line = line.rstrip().replace('sim_time_limit','').replace('=','')
                    sim_time_limit = eval(line)
                    break
            else:
                print('==============================================================================')
                print('Error: Could not find sim_time_limit in Run_EKMC.py. Check this.')
                print('In: '+str(path_to_KMC_Run_file))
                print('==============================================================================')
                dirs[:]  = []
                files[:] = []
                continue

        # Eighth, collect a root to investigate
        roots.append((root, centre_of_masses, unit_cell_matrix, energetic_disorder, temperature, sim_time_limit))

        # Ninth, remove items in list from dirs and files
        dirs[:]  = []
        files[:] = []

    # Tenth, Process the data from EKMC simulations, and gather the data to save to excel spreadsheet
    #with mp.Pool(no_of_cpus) as pool:
        #data_for_excel = pool.map(collect_save_and_provide_data_from_simulation, tqdm(roots, total=len(roots), desc='Gathering data (This may take some time)', unit='sims'))
    begin_recording_time = 500
    data_for_excel = [collect_save_and_provide_data_from_simulation(root, centre_of_masses, unit_cell_matrix, energetic_disorder, temperature, sim_time_limit, path_to_crystal_file, begin_recording_time, no_of_cpus) for root, centre_of_masses, unit_cell_matrix, energetic_disorder, temperature, sim_time_limit in roots]

    # Eleventh, save data to excel spreadsheet.
    save_to_excel_spreadsheet(data_foldername, data_for_excel)

def collect_save_and_provide_data_from_simulation(root, centre_of_masses, unit_cell_matrix, energetic_disorder, temperature, sim_time_limit, path_to_crystal_file, begin_recording_time, no_of_cpus=1):

    print('=================================================================================')
    print('Gathering data for: '+str(root))

    # Eighth, collect the data from this subdirectory.
    all_sims = collect_data(root, cpu_count=no_of_cpus)

    # Ninth, process the collected data across all simulations.
    times, positions_at_time, average_displacements_from_initial_position_over_time, average_displacements_squared_from_initial_position_over_time, average_energies_over_time, diffusion_over_time, diffusion_tensor_over_time, eigenvalues_of_diffusion_tensor_over_time, eigenvectors_of_diffusion_tensor_over_time, all_timesteps, time_for_all_sims = process_data(all_sims, centre_of_masses, unit_cell_matrix, sim_time_limit, no_of_times_to_sample=10000, cpu_count=no_of_cpus)

    # Tenth, make plots of quantites.
    save_data_and_plot_figures(data_foldername, root[2::], times, positions_at_time, average_displacements_from_initial_position_over_time, average_displacements_squared_from_initial_position_over_time, average_energies_over_time, diffusion_over_time, diffusion_tensor_over_time, eigenvalues_of_diffusion_tensor_over_time, eigenvectors_of_diffusion_tensor_over_time, unit_cell_matrix, energetic_disorder, temperature, path_to_crystal_file)

    time_average_energy, time_average_energy_sd, time_average_energy_ci, time_average_diffusion, time_average_diffusion_sd, time_average_diffusion_ci, time_average_diffusion_tensor, time_average_diffusion_tensor_sd, time_average_diffusion_tensor_ci, time_average_eigenvalues_of_diffusion_tensor, time_average_eigenvalues_of_diffusion_tensor_sd, time_average_eigenvalues_of_diffusion_tensor_ci = time_average_data(times, average_energies_over_time, diffusion_over_time, diffusion_tensor_over_time, eigenvalues_of_diffusion_tensor_over_time, begin_recording_time=begin_recording_time)
    datum = (root, time_average_energy, time_average_energy_sd, time_average_energy_ci, time_average_diffusion, time_average_diffusion_sd, time_average_diffusion_ci, time_average_diffusion_tensor, time_average_diffusion_tensor_sd, time_average_diffusion_tensor_ci, time_average_eigenvalues_of_diffusion_tensor, time_average_eigenvalues_of_diffusion_tensor_sd, time_average_eigenvalues_of_diffusion_tensor_ci, begin_recording_time, times, energetic_disorder, temperature)
    save_time_averaged_data(data_foldername, root[2::], time_average_energy, time_average_energy_sd, time_average_energy_ci, time_average_diffusion, time_average_diffusion_sd, time_average_diffusion_ci, time_average_diffusion_tensor, time_average_diffusion_tensor_sd, time_average_diffusion_tensor_ci, time_average_eigenvalues_of_diffusion_tensor, time_average_eigenvalues_of_diffusion_tensor_sd, time_average_eigenvalues_of_diffusion_tensor_ci, begin_recording_time, times)
    
    print('=================================================================================')

    return datum
