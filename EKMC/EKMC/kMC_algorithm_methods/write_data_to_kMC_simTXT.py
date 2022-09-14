"""
write_data_to_kMC_simTXT.py, Geoffrey Weal, 26/3/22

This script is designed to write the information about the kinetic Monte Carlo's progress to disk,
"""

def write_data_to_kMC_simTXT(counter, current_molecule_name, current_cell_point, current_time, current_time_step, current_molecule_description_energy, sum_of_rate_constants, kMC_simTXT):
	"""
	This method is designed to write the information about a KMC step into the kMC_simTXT file. 

	Information is written to the kMC_simTXT file.

	Parameters
	----------
	counter : int
		This is the current number of KMC steps that have been performed by the KMC algorithm.
	current_molecule_name : int
		This is the name (int number) of the molecule that the exciton is on.
	current_cell_point : tuple of ints
		This is the unit cell that the exciton is in.
	current_time : float
		This is the current simulation time for this KMC simulation. Given in picoseconds.
	current_time_step : float
		This is the timestep of the currently performed KMC step. Given in femtoseconds.
	current_molecule_description_energy : float
		This is the energy level of the molecule the exciton is currently on (including the disorder). 
	sum_of_rate_constants : float
		This is the sum of all the rate constants of all the rate constants from the previous molecule the exciton was on.
	kMC_simTXT : Open
		This is the file to save the information about the process of the KMC simulation to.
	"""

	# First, obtain all the information to save to the kMC_simTXT file. 
	counter_placement = placement_counter(counter, 10)
	current_molecule_name_placement = placement_counter(current_molecule_name, 10)
	current_cell_point_placement = placement_counter(current_cell_point, 25)
	current_time_placement = placement_counter(current_time, 30+2, 30)
	current_time_step_placement = placement_counter(current_time_step, 30+2, 30)
	current_molecule_description_energy_placement = placement_counter(current_molecule_description_energy, 30+2, 30)
	sum_of_rate_constants_placement = placement_counter(sum_of_rate_constants, 30+2, 30)

	# Second, save the data from above into the kMC_simTXT file.
	kMC_simTXT.write(counter_placement+' '+current_molecule_name_placement+' '+current_cell_point_placement+' '+current_time_placement+' '+current_time_step_placement+' '+current_molecule_description_energy_placement+' '+sum_of_rate_constants_placement+' |'+'\n')

def placement_counter(input_thing, total_no_of_charaters, input_thing_max_length=1000000000):
	"""
	This method will write the input as a string that contain total_no_of_charaters characters.

	Parameters
	----------
	input_thing : input
		This is the input you would like to convert to a string.
	total_no_of_charaters : int
		This is the number of characters you would like to have in the output.
	input_thing_max_length : int
		This is the maximum number of characters to take from the input_thing string.

	Returns
	-------
	output_thing : str.
		This is the input_thing as a string of size given by total_no_of_charaters
	"""

	# First, obtain input_thing as a string.
	input_thing_string = str(input_thing)[:input_thing_max_length]

	# Second, extend the  input_thing_string string so that it contains total_no_of_charaters characters by adding spaces to the end of the string.
	output_thing = input_thing_string + ' '*(total_no_of_charaters - len(input_thing_string))

	# Third, return output_thing
	return output_thing


