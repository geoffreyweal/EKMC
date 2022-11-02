
import os

from time import time
from datetime import timedelta
from itertools import count
from math import exp, log
from numpy.random import normal, uniform
from random import choice, choices

def get_MLJ_rate_constants_data(current_molecule_description, all_local_neighbourhoods, energetic_disorder, coupling_disorder, graph):
	current_molecule_deltaE_disorder, neighbouring_molecule_descriptions, rate_constants = get_rate_constants_to_connecting_molecules(current_molecule_description, all_local_neighbourhoods, energetic_disorder, coupling_disorder, graph)
	return current_molecule_deltaE_disorder, neighbouring_molecule_descriptions, rate_constants

def get_rate_constants_to_connecting_molecules(current_molecule_description, all_local_neighbourhoods, energetic_disorder, coupling_disorder, graph):
	"""
	This method is designed to gather the rate constants between the current molecule in the current cell point and every other neighbouring molecule in surrounding unit cells within the rCut_neighbourhood radius. 

	Parameters
	----------
	current_molecule_name : int
		This is the molecule that the exciton is currently on.
	current_cell_point : tuple
		This is the cell that the exciton is currently in.
	all_local_neighbourhoods : dict.
		This dictionary contains all the information about the neighbourhoods that surrounded each molecule in your crystal.
	energetic_disorder : float
		This value indicates the disorder given in the delta E value.
	coupling_disorder : float
		This value indicates the disorder given in the V (coupling) value.
	graph : kMC_graph
		This graph holds all the information about the molecules in the various positions in the crystal.

	Returns
	-------
	other_molecule_descriptions : list
		This is the name and the cell_point that the the exciton can move to from the current molecule.
	other_molecule_deltaE_disorders : list
		These are the deltaE values for the other molecules that are kinetically attached to the current molecule. 
	rate_constants : list
		These are the rate constants for the exciton to move from the current molecule to another molecule that maybe in another unit cell.
	edges_details : dict.
		These are other edge details for the possible routes for the exciton to move from the current molecule to another molecule that maybe in another unit cell.
	"""

	raise Exception('Check coding before using MLJ code')

	# Get the molecule current name and current cell point from the current_molecule_description tuple
	current_molecule_name, current_cell_point = current_molecule_description

	# First, initalise the list and dictionaries to record data into
	neighbouring_molecule_descriptions = []
	rate_constants = []
	edges_details = {}

	# Second, get the energy for this molecule that has had disorder applied to it.
	current_molecule_deltaE_disorder = graph.get_E_disorder(current_molecule_description)
	if current_molecule_deltaE_disorder is None:
		current_molecule_deltaE_disorder = normal(0.0,energetic_disorder)
		graph.add_E_disorder(current_molecule_description, current_molecule_deltaE_disorder)

	# Third, obtain the relative local neighbourhood for the current molecule
	local_neighbourhoods = all_local_neighbourhoods[current_molecule_name]

	# Fourth, obtain all the rate constants and data for an exciton moving from the current molecule to another molecule that maybe in another unit cell.
	for neighbouring_molecule_name in local_neighbourhoods.keys():
		for relative_cell_point, (M_constant, X_constant, non_changing_across_lattice_data_for_uv_inputs) in local_neighbourhoods[neighbouring_molecule_name].items():
			# 4.1: Get the exist cell_point for the other molecule from current_cell_point + relative_cell_point
			neighbouring_cell_point = tuple(a+b for a, b in zip(current_cell_point, relative_cell_point))
			neighbouring_molecule_description = (neighbouring_molecule_name, neighbouring_cell_point)

			# 4.2.1: Get the E value based on disorder for this other molecule.
			other_molecule_deltaE_disorder = graph.get_E_disorder(neighbouring_molecule_description)
			if other_molecule_deltaE_disorder is None:
				other_molecule_deltaE_disorder = normal(0.0,energetic_disorder)
				graph.add_E_disorder(neighbouring_molecule_description, other_molecule_deltaE_disorder)

			# 4.2.2: Obtain the randomly generated number to describe the energetic and coupling disorders, based on a normal distribution. 
			V_disorder = graph.get_V_disorder(current_molecule_description, neighbouring_molecule_description)
			if V_disorder is None:
				V_disorder = normal(1.0,coupling_disorder)
				graph.add_V_disorder(current_molecule_description, neighbouring_molecule_description, V_disorder)

			# 4.3: get the difference in energy between the two molecules.
			deltaE = (other_molecule_deltaE_disorder - current_molecule_deltaE_disorder)

			# 4.3: Obtain the value outside of the sum of the Fermi's Golden Rule equation.
			X_constant_deltaE_squared = X_constant*(deltaE**2.0)

			# 4.4: Obtain the value inside the sum of the Fermi's Golden Rule equation.
			total_of_sum = 0.0
			for (uu,vv), (N_constant,Y_constant,Z_constant) in non_changing_across_lattice_data_for_uv_inputs.items():
				total_of_sum += N_constant*exp(-(X_constant_deltaE_squared + deltaE*Y_constant + Z_constant))

			# 4.5: Obtain the rate constant for the exciton to move from the current molecule to another molecule that maybe in another unit cell.
			k_12 = (V_disorder**2.0)*M_constant*total_of_sum

			# 4.6: Add the rate constant data to the storage list and dictionaries. 
			neighbouring_molecule_descriptions.append(neighbouring_molecule_description)
			rate_constants.append(k_12)
			
	return current_molecule_deltaE_disorder, neighbouring_molecule_descriptions, rate_constants