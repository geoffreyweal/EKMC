'''
Check_Result.py, Geoffrey Weal, 12/8/22

This program will determine 
'''
import os
import numpy as np
from tqdm import tqdm
from ase.io import read
import multiprocessing as mp
from SUMELF import make_folder, remove_folder

from EKMC.Postprocessing_Programs.Process_Results_methods.split_string_by_floats                         import split_string_by_floats
from EKMC.Postprocessing_Programs.Process_Results_methods.collect_data                                   import collect_data
from EKMC.Postprocessing_Programs.Process_Results_methods.process_and_save_average_hopping_probabilities import process_and_save_average_hopping_probabilities
from EKMC.Postprocessing_Programs.Process_Results_methods.process_data                                   import process_data
from EKMC.Postprocessing_Programs.Process_Results_methods.save_data_and_plot_figures                     import save_data_and_plot_figures
from EKMC.Postprocessing_Programs.Process_Results_methods.time_average_data                              import time_average_data
from EKMC.Postprocessing_Programs.Process_Results_methods.save_time_averaged_data                        import save_time_averaged_data
from EKMC.Postprocessing_Programs.Process_Results_methods.save_to_excel_spreadsheet                      import save_to_excel_spreadsheet

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

        dirs.sort(key=lambda dirname: split_string_by_floats(dirname))
        files.sort(key=lambda filename: split_string_by_floats(filename))

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
            molnames_and_coms                 = eval(KMC_setup_data_EKMC.readline().rstrip())
            for molname in molnames_and_coms.keys():
                molnames_and_coms[molname]    = np.array(molnames_and_coms[molname])
            unit_cell_matrix                  = np.array(eval(KMC_setup_data_EKMC.readline().rstrip()))
            kinetic_model                     = KMC_setup_data_EKMC.readline().rstrip()
            kinetic_model_parameters          = eval(KMC_setup_data_EKMC.readline().rstrip())
            temperature                       = kinetic_model_parameters['temperature']
            energetic_disorder                = kinetic_model_parameters['energetic_disorder']
            coupling_disorder                 = kinetic_model_parameters['coupling_disorder']
            bandgap_energies                  = eval(KMC_setup_data_EKMC.readline().rstrip())
            reorganisation_energies           = eval(KMC_setup_data_EKMC.readline().rstrip())
            conformationally_unique_molecules = eval(KMC_setup_data_EKMC.readline().rstrip())

        # Sixth, only store the bandgap energies for the conformationally unique molecules.
        conformationally_unique_bandgap_energies = obtain_confromationally_unique_molecules_bandgap_energies(bandgap_energies, molnames_and_coms, conformationally_unique_molecules)

        # Seventh, get the path to the Run_EKMC.py to get the simulation time limit from.
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

        # Eighth, get the simulation time limit from the Run_EKMC.py
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

        # Ninth, collect a root to investigate
        roots.append((root, molnames_and_coms, unit_cell_matrix, temperature, energetic_disorder, coupling_disorder, conformationally_unique_bandgap_energies, sim_time_limit))

        # Tenth, remove items in list from dirs and files
        dirs[:]  = []
        files[:] = []

    # Eleventh, Process the data from EKMC simulations, and gather the data to save to excel spreadsheet
    #with mp.Pool(no_of_cpus) as pool:
        #data_for_excel = pool.map(collect_save_and_provide_data_from_simulation, tqdm(roots, total=len(roots), desc='Gathering data (This may take some time)', unit='sims'))
    begin_recording_time = 500
    end_recording_time = 1000
    print('Node to Geoff: I have permamentatly set begin_recording_time = '+str(begin_recording_time)+' and end_recording_time '+str(end_recording_time))
    data_for_excel = [collect_save_and_provide_data_from_simulation(root, molnames_and_coms, unit_cell_matrix, temperature, energetic_disorder, coupling_disorder, conformationally_unique_bandgap_energies, sim_time_limit, path_to_crystal_file, begin_recording_time, end_recording_time, no_of_cpus) for root, molnames_and_coms, unit_cell_matrix, temperature, energetic_disorder, coupling_disorder, conformationally_unique_bandgap_energies, sim_time_limit in roots]

    # Twelfth, save data to excel spreadsheet.
    save_to_excel_spreadsheet(data_foldername, data_for_excel)

    # Report that everything finished successfully
    #print('EKMC process_results finished successfully.')

# ============================================================================================================================================================================================================

def obtain_confromationally_unique_molecules_bandgap_energies(bandgap_energies, molnames_and_coms, conformationally_unique_molecules):

    # First, get the names of all the molecules in the crystal origin unit cell.
    molecule_names = list(molnames_and_coms.keys())

    # Second, initialise the conformationally unique bandgap energies dictionary. 
    conformationally_unique_bandgap_energies = {}

    # Third, get the bandgap energies of all the conformationally unique molecules in the crystal.
    for molname in molecule_names:

        # 3.1: If molname is not in the keys of conformationally_unique_molecules, 
        #      molname is conformationally unique, so record it.
        if molname not in conformationally_unique_molecules.keys():
            conformationally_unique_bandgap_energies[molname] = bandgap_energies[molname]

    # Fourth, return conformationally_unique_bandgap_energies
    return conformationally_unique_bandgap_energies

# ============================================================================================================================================================================================================

def create_saving_folder(data_foldername, path):
    path_to_place_data_in = data_foldername+'/'+path
    if path_to_place_data_in[-1] == '/':
        path_to_place_data_in = path_to_place_data_in[:-1]
    remove_folder(path_to_place_data_in)
    make_folder(path_to_place_data_in)
    return path_to_place_data_in

# ============================================================================================================================================================================================================

def collect_save_and_provide_data_from_simulation(root, molnames_and_coms, unit_cell_matrix, temperature, energetic_disorder, coupling_disorder, conformationally_unique_bandgap_energies, sim_time_limit, path_to_crystal_file, begin_recording_time, end_recording_time, no_of_cpus=1):

    print('=================================================================================')
    print('Gathering data for: '+str(root))

    # First, collect the data from this subdirectory.
    all_sims, all_sims_hop_probs = collect_data(root, cpu_count=no_of_cpus)

    # Second, obtain the path to save data to.
    path = root[2::]

    # Third, create folder to save data to. 
    path_to_place_data_in = create_saving_folder(data_foldername, path)

    # Ninth, obtain the average hopping probabilities for each exciton hop across all simulations. 
    process_and_save_average_hopping_probabilities(data_foldername, path, all_sims_hop_probs)

    # Tenth, process the collected data across all simulations.
    times, positions_at_time, average_displacements_from_initial_position_over_time, average_displacements_squared_from_initial_position_over_time, average_energies_over_time, diffusion_over_time, diffusion_tensor_over_time, eigenvalues_of_diffusion_tensor_over_time, eigenvectors_of_diffusion_tensor_over_time, all_timesteps, time_for_all_sims = process_data(all_sims, molnames_and_coms, unit_cell_matrix, end_recording_time, no_of_times_to_sample=10000, cpu_count=no_of_cpus)

    # Eleventh, make plots of quantites.
    save_data_and_plot_figures(path_to_place_data_in, times, positions_at_time, average_displacements_from_initial_position_over_time, average_displacements_squared_from_initial_position_over_time, average_energies_over_time, diffusion_over_time, diffusion_tensor_over_time, eigenvalues_of_diffusion_tensor_over_time, eigenvectors_of_diffusion_tensor_over_time, unit_cell_matrix, temperature, energetic_disorder, coupling_disorder, conformationally_unique_bandgap_energies, path_to_crystal_file)

    time_average_energy, time_average_energy_sd, time_average_energy_ci, time_average_diffusion, time_average_diffusion_sd, time_average_diffusion_ci, time_average_diffusion_tensor, time_average_diffusion_tensor_sd, time_average_diffusion_tensor_ci, time_average_eigenvalues_of_diffusion_tensor, time_average_eigenvalues_of_diffusion_tensor_sd, time_average_eigenvalues_of_diffusion_tensor_ci = time_average_data(times, average_energies_over_time, diffusion_over_time, diffusion_tensor_over_time, eigenvalues_of_diffusion_tensor_over_time, begin_recording_time=begin_recording_time, end_recording_time=end_recording_time)

    endtime = times[-1]

    del times
    del positions_at_time
    del average_displacements_from_initial_position_over_time
    del average_displacements_squared_from_initial_position_over_time
    del average_energies_over_time
    del diffusion_over_time
    del diffusion_tensor_over_time
    del eigenvalues_of_diffusion_tensor_over_time
    del eigenvectors_of_diffusion_tensor_over_time
    del all_timesteps
    del time_for_all_sims 

    save_time_averaged_data(path_to_place_data_in, time_average_energy, time_average_energy_sd, time_average_energy_ci, time_average_diffusion, time_average_diffusion_sd, time_average_diffusion_ci, time_average_diffusion_tensor, time_average_diffusion_tensor_sd, time_average_diffusion_tensor_ci, time_average_eigenvalues_of_diffusion_tensor, time_average_eigenvalues_of_diffusion_tensor_sd, time_average_eigenvalues_of_diffusion_tensor_ci, begin_recording_time, endtime, temperature, energetic_disorder, coupling_disorder, conformationally_unique_bandgap_energies)

    print('Finished processing the KMC results for: '+str(root))
    print('=================================================================================')

    return root, time_average_energy, time_average_energy_sd, time_average_energy_ci, time_average_diffusion, time_average_diffusion_sd, time_average_diffusion_ci, time_average_diffusion_tensor, time_average_diffusion_tensor_sd, time_average_diffusion_tensor_ci, time_average_eigenvalues_of_diffusion_tensor, time_average_eigenvalues_of_diffusion_tensor_sd, time_average_eigenvalues_of_diffusion_tensor_ci, begin_recording_time, endtime, temperature, energetic_disorder, coupling_disorder, conformationally_unique_bandgap_energies

# ============================================================================================================================================================================================================
