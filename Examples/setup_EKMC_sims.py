"""
setup_EKMC_sims.py, Geoffrey Weal, 17/9/22

This script is designed to setup your excitonic kinetic Monte Carlo files for running multiple simulations.
"""
from math import pi
from copy import deepcopy
from EKMC import EKMC_Multi_Setup

h_bar = 6.582119569 * (10.0 ** -16.0) # eV s
plancks_constant = h_bar * 2.0 * pi # eVs
speed_of_light = 29979245800 # cms-1

# -----------------------------------------------------------------------------------------------
# First, give general settings.

functional_and_basis_set = 'F_wB97XD_B_6_31plusGd_p'
kinetic_model = 'Marcus'

frequency_wavenumber = 1500 # cm-1
Wang_number = plancks_constant * speed_of_light * frequency_wavenumber

temperature = 300

# -----------------------------------------------------------------------------------------------
# Second, give settings for each crystal and electronic settings.

crystal_names = ['Y6', 'EH-IDTBR', 'ITIC', 'itic-2cl-g', 'itic-2cl-y', 'ITIC-4F']

energetic_disorders = {'Y6': 56, 'IDIC': 34, 'ITIC': 53, 'itic-2cl-g': 45, 'itic-2cl-y': 45, 'ITIC-4F': 39, 'EH-IDTBR': 48}
for crystal_shortname in energetic_disorders.keys():
	energetic_disorders[crystal_shortname] = energetic_disorders[crystal_shortname] / 1000.0

coupling_disorders = list(range(0,55,5))

relative_permittivities = {'Y6': 5, 'IDIC': 4, 'ITIC': 5, 'itic-2cl-g': 4, 'itic-2cl-y': 4, 'ITIC-4F': 4, 'EH-IDTBR': 4}
huang_rhys_factors      = {'Y6': 0.294, 'IDIC': None, 'ITIC': None, 'itic-2cl-g': 0.5291, 'itic-2cl-y': 0.4798, 'ITIC-4F': 0.6591, 'EH-IDTBR': 0.5819}
reorganisation_energies = {'Y6': 0.26623, 'IDIC': None, 'ITIC': None, 'itic-2cl-g': 0.41139443, 'itic-2cl-y': 0.316988, 'ITIC-4F': 0.311641, 'EH-IDTBR': 0.38139}

# -----------------------------------------------------------------------------------------------
# Third, obtain all the settings for all the EKMC simulations you would like to perform.

all_EKMC_settings = []
for crystal_name in crystal_names:
	for coupling_disorder in coupling_disorders:

		molecules_path  = 'Electronic_Calculations_Results/ECCP_Data/ECCP_Information/'+crystal_name
		ATC_folder_path = 'Electronic_Calculations_Results/ECCP_Data/Unique_ATC_Gaussian_Jobs/'+crystal_name

		Individual_EET_folder_path = 'Electronic_Calculations_Results/ECCP_Data/Unique_EET_Gaussian_Jobs'
		dimer_couplings = {'Use_non_atc_model_for_dimers': True, 'path_to_dimer_information_file': Individual_EET_folder_path}

		kinetics_details = {}
		kinetics_details['energetic_disorder'] = energetic_disorders[crystal_name]
		coupling_disorder = str(float(coupling_disorder))+'%'
		kinetics_details['coupling_disorder'] = coupling_disorder
		kinetics_details['relative_permittivity'] = relative_permittivities[crystal_name]
		huang_rhys_factor = huang_rhys_factors[crystal_name]
		reorganisation_energy = reorganisation_energys[crystal_name]
		kinetics_details['classical_reorganisation_energy'] = reorganisation_energy - huang_rhys_factor*Wang_number
		kinetics_details['temperature'] = temperature

		neighbourhood_rCut = 40.0 # A
		sim_time_limit = 1000 # ps
		max_no_of_steps = 'inf'

		store_data_in_databases = False
		no_of_molecules_at_cell_points_to_store_on_RAM = None

		crystal_settings = {'folder_name': crystal_name+'/'+str(coupling_disorder), 'molecules_path': molecules_path, 'ATC_folder_path': ATC_folder_path, 'functional_and_basis_set': functional_and_basis_set, 'kinetic_model': kinetic_model, 'dimer_couplings': dimer_couplings, 'kinetics_details': kinetics_details, 'neighbourhood_rCut': neighbourhood_rCut, 'sim_time_limit': sim_time_limit, 'max_no_of_steps': max_no_of_steps, 'store_data_in_databases': store_data_in_databases, 'no_of_molecules_at_cell_points_to_store_on_RAM': no_of_molecules_at_cell_points_to_store_on_RAM}

		all_EKMC_settings.append(crystal_settings)

# -----------------------------------------------------------------------------------------------
# Fourth, obtaining the dictionary that will add tags to your ekmc_mass_submit.sl files

mass_submission_information = {}
mass_submission_information['ntasks_per_node'] = 1
mass_submission_information['mem'] = '4GB'
mass_submission_information['time'] = '0-08:00'
mass_submission_information['partition'] = 'parallel'
mass_submission_information['email'] = 'geoffreywealslurmnotifications@gmail.com'
mass_submission_information['python_version'] = 'python/3.8.1'

mass_submission_information['submission_type'] = 'full'
mass_submission_information['no_of_simulations'] = 2000
#mass_submission_information['no_of_packets_to_make'] = 100

all_mass_submission_information = [deepcopy(mass_submission_information)]*len(all_EKMC_settings)

# -----------------------------------------------------------------------------------------------
# Fifth, setup all your excitonic kinetic Monte Carlo simulations!

EKMC_Multi_Setup(all_EKMC_settings=all_EKMC_settings, all_mass_submission_information=all_mass_submission_information)

# -----------------------------------------------------------------------------------------------

