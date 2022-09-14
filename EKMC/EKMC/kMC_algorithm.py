"""
kMC_algorithm.py, Geoffrey Weal, 26/3/22

kMC_algorithm is designed to perform a kinetic Monte Carlo simulation of the movement of the exciton about the molecules in a crystal.
"""
import os

from time import time
from datetime import timedelta
from itertools import count
from math import exp, log
from numpy.random import normal, uniform
from random import choice, choices

from EKMC.EKMC.kMC_algorithm_methods.did_finish                         import did_finish
from EKMC.EKMC.kMC_algorithm_methods.kMC_database                       import kMC_database
from EKMC.EKMC.kMC_algorithm_methods.get_initial_data_for_beginning_kMC import get_initial_data_for_beginning_kMC
from EKMC.EKMC.kMC_algorithm_methods.write_data_to_kMC_simTXT           import write_data_to_kMC_simTXT

def run_kMC_algorithm(kinetic_model, all_local_neighbourhoods, coupling_disorder, energetic_disorder, sim_time_limit=float('inf'), max_no_of_steps='inf', store_data_in_databases=False, no_of_molecules_at_cell_points_to_store_on_RAM=None):
	"""
	This method is designed to run the kMC algorithm for an exciton moving about the molecules in a crystal.

	Parameters
	----------
	kinetic_model :str.
		This is the kinetic model you would like to use to simulate an exciton about the molecules within a crystal.
	all_local_neighbourhoods : dict.
		This dictionary contains all the information about the neighbourhoods that surrounded each molecule in your crystal.
	coupling_disorder : float
		This is the disorder that is associated with the V12 value
	energetic_disorder : float
		This is the disorder that is associated with the DeltaE value
	sim_time_limit : float
		This is the simulated time limit to run the kinetic Monte Carlo simulation over. Time given in ps.
	max_no_of_steps : int
		This is the maximum number of kmc steps to run the kinetic Monte Carlo simulation over.
	store_data_in_databases : bool.
		This tag indicates if you want to store random energy and coupling disorders in a database.
	no_of_molecules_at_cell_points_to_store_on_RAM : int
		This is the maximum number of entries to maintain in the RAM memory before moving data to the database.
	"""

	# First, check that the simulation has finished.
	kMC_sim_name = 'kMC_sim.txt'
	did_simulation_finish, time_simulated = did_finish(kMC_sim_name, sim_time_limit)
	if did_simulation_finish:
		print('This simulation has already reached '+str(sim_time_limit)+' ps.')
		print('Time simulated: '+str(time_simulated)+' ps.')
		print('Will finish the Exciton kinetic Monte Carlo algorithm without doing anything.')
		print('------------------------------------------------')
		return

	# Second, make sure that the kinetic model you would like to use is available in this program.
	if   kinetic_model.lower() == 'marcus':
		from EKMC.EKMC.kMC_algorithm_methods.get_rate_constant_methods.get_Marcus_rate_constants_data import get_Marcus_rate_constants_data as get_rate_constants_data
	elif kinetic_model.lower() == 'mlj':
		from EKMC.EKMC.kMC_algorithm_methods.get_rate_constant_methods.get_MLJ_rate_constants_data    import get_MLJ_rate_constants_data    as get_rate_constants_data
	else:
		raise Exception('Error: You must set "kinetic_model" to either "Marcus" or "MLJ". Your kinetic_model is set to: '+str(kinetic_model)+'. Check this out.')

	# Third, get the number of molecules in the crystal unit cell. This is just the len of all_local_neighbourhoods
	number_of_molecules = len(all_local_neighbourhoods)

	# Fourth, we load the database to be used for a kinetic Monte Carlo simulation.
	database = kMC_database(number_of_molecules=number_of_molecules, no_of_molecules_at_cell_points_to_store_on_RAM=no_of_molecules_at_cell_points_to_store_on_RAM, store_data_in_databases=store_data_in_databases)

	# Fifth, make sure the databasehas been saving to has no issues.
	database.check_database()

	# Sixth, get the initial data for starting or resuming this kmc algorithm
	other_kMC_data_name = 'other_kMC_data.txt'
	resume_kmc_simulation, initial_count, current_molecule_name, current_cell_point, current_time = get_initial_data_for_beginning_kMC(kMC_sim_name, store_data_in_databases)

	# Seventh, if this is a new kmc simulation, initiate the new kmc simulation.
	if not resume_kmc_simulation:

		# 7.1: Randomly select a starting point in the (0,0,0) central unit cell to initiate the exciton upon.
		molecule_names = list(all_local_neighbourhoods.keys())
		current_molecule_name = choice(molecule_names)
		current_cell_point = (0,0,0)

		# 7.2: Begin from time = 0.0 s
		initial_count = 0
		current_time = 0.0 # s
		delta_time = 0.0

		# 7.3: Initiate the kMC_simTXT file.
		if os.path.exists(kMC_sim_name):
			os.remove(kMC_sim_name)
		with open(kMC_sim_name,'w') as kMC_simTXT:
			write_data_to_kMC_simTXT('Count:', 'Molecule', 'Cell Point', 'Time (ps)', 'Time Step (fs)', 'Energy (eV)', '∑ kij (ps-1)', kMC_simTXT)

	# Eighth, get the current_molecule_description, which contains current_molecule_name and current_cell_point
	current_molecule_description = (current_molecule_name, current_cell_point)
	current_molecule_E_with_disorder = database.get_E_with_disorder(current_molecule_description)
	if current_molecule_E_with_disorder is None:
		current_molecule_E_with_disorder = normal(0.0,energetic_disorder) # Set energy of molecule to 0.0 eV, and get random normal distributed number around 0.0 eV with width of energetic_disorder (given in eV)
		database.add_E_with_disorder(current_molecule_description, current_molecule_E_with_disorder)

	# Ninth, get the count function for the for loop for the kmc algorithm
	if max_no_of_steps == 'inf':
		kmc_counter_func = count(initial_count+1)
	else:
		kmc_counter_func = range(initial_count+1,max_no_of_steps+1,1)

	# Tenth, perform the kinetic Monte Carlo algorithm. 
	print('-------------')
	print('Start performing the Exciton kinetic Monte Carlo algorithm from Count: '+str(initial_count+1))
	start_time = time()
	for counter in kmc_counter_func:

		# 10.1: If the current molecule in the current_cell_point has not been examined before, obtain all the 
		#      rate constants for all the surrounding molecules that the exciton can move to.
		current_molecule_description_energy, other_molecule_descriptions, rate_constants = get_rate_constants_data(current_molecule_description, all_local_neighbourhoods, energetic_disorder, coupling_disorder, database)

		# 10.2 Print data of the current molcule in the current cell position to disk
		with open(kMC_sim_name,'a') as kMC_simTXT:
			sum_of_rate_constants = sum(rate_constants) * (10.0 ** -12.0) # in ps-1
			current_molecule_description_energy_str = ('+' if current_molecule_description_energy >= 0 else '') + str(current_molecule_description_energy)
			write_data_to_kMC_simTXT(counter-1, current_molecule_name, str(current_cell_point).replace(' ',''), current_time, f'{float(delta_time):.20f}', current_molecule_description_energy_str, sum_of_rate_constants, kMC_simTXT)

		# 10.3: If you have reached the time limit, finish the kinetic Monte Carlo algorithm.
		if current_time >= sim_time_limit:
			break

		# 10.4: Randomly select where the exciton will move to based on the relative rate constants.
		index = choices(range(len(other_molecule_descriptions)), weights=rate_constants, k = 1)[0]
		current_molecule_description = other_molecule_descriptions[index]
		path_taken_rate_constant = sum(rate_constants) # rate_constants[index]

		# 10.5: Extract the current cell point as well as the molecule that the exciton is on.
		current_molecule_name, current_cell_point = current_molecule_description

		# 10.6: Determine the time that has lapped, and add this to the current time
		delta_time = -log(uniform())/path_taken_rate_constant
		delta_time *= (10.0 ** 12.0) # in ps
		current_time += delta_time   # in ps
		delta_time *= (10.0 ** 3.0)  # in fs

		#import pdb; pdb.set_trace()

		# 10.7: Print counter to screen to show to the user that the algorithm is performing.
		if counter%100 == 0:
			print('Count: '+str(counter)+'\tTime Passed (HH:MM:SS): '+str(timedelta(seconds=time()-start_time)))

	# Eleventh, finish off with an ending message.
	print('Finished the Exciton kinetic Monte Carlo algorithm.')
	print('-------------')



