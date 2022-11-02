
import os

from time import time
from datetime import timedelta
from itertools import count
from math import exp, log
from numpy.random import normal, uniform
from random import choice, choices

def get_Marcus_rate_constants_data(current_molecule_description, all_local_neighbourhoods, energetic_disorder, coupling_disorder, graph):
	current_molecule_deltaE_disorder, neighbouring_molecule_descriptions, rate_constants = get_rate_constants_to_connecting_molecules(current_molecule_description, all_local_neighbourhoods, energetic_disorder, coupling_disorder, graph)
	return current_molecule_deltaE_disorder, neighbouring_molecule_descriptions, rate_constants

def get_rate_constants_to_connecting_molecules(current_molecule_description, all_local_neighbourhoods, energetic_disorder, coupling_disorder_variable, graph):
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
	coupling_disorder_variable : float
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

	# First, get the molecule current name and current cell point from the current_molecule_description tuple
	current_molecule_name, current_cell_point = current_molecule_description

	# Second, initalise the list and dictionaries to record data into
	neighbouring_molecule_descriptions = []
	rate_constants = []
	edges_details = {}

	# Third, get the energy for this molecule that has had disorder applied to it.
	current_molecule_E_with_disorder = graph.get_E_with_disorder(current_molecule_description)
	if current_molecule_E_with_disorder is None:
		current_molecule_E_with_disorder = normal(0.0,energetic_disorder) # Set energy of molecule to 0.0 eV, and get random normal distributed number around 0.0 eV with width of energetic_disorder (given in eV)
		graph.add_E_with_disorder(current_molecule_description, current_molecule_E_with_disorder)

	# Fourth, obtain the relative local neighbourhood for the current molecule
	local_neighbourhoods = all_local_neighbourhoods[current_molecule_name]

	# Fifth, obtain all the rate constants and data for an exciton moving from the current molecule to another molecule that maybe in another unit cell.
	for neighbouring_molecule_name in local_neighbourhoods.keys():
		for relative_cell_point, (coupling_energy, M_constant, X_constant, Y_constant, Z_constant) in local_neighbourhoods[neighbouring_molecule_name].items():

			# 5.1: Get the exist cell_point for the other molecule from current_cell_point + relative_cell_point
			neighbouring_cell_point = tuple(a+b for a, b in zip(current_cell_point, relative_cell_point))
			neighbouring_molecule_description = (neighbouring_molecule_name, neighbouring_cell_point)

			# 5.2.1: Get the E value based on disorder for this other molecule.
			other_molecule_E_with_disorder = graph.get_E_with_disorder(neighbouring_molecule_description)
			if other_molecule_E_with_disorder is None:
				other_molecule_E_with_disorder = normal(0.0,energetic_disorder) # Set energy of molecule to 0.0 eV, and get random normal distributed number around 0.0 eV with width of energetic_disorder (given in eV)
				graph.add_E_with_disorder(neighbouring_molecule_description, other_molecule_E_with_disorder)

			# 5.2.2: Obtain the randomly generated number to describe the energetic and coupling disorders, based on a normal distribution. 
			V_with_disorder = graph.get_V_with_disorder(current_molecule_description, neighbouring_molecule_description)
			if V_with_disorder is None:

				# 5.2.2.1: if the coupling_disorder is a string and ends with %, take the coupling_disorder as the percentage of the dimers coupling energy
				if isinstance(coupling_disorder_variable,str) and coupling_disorder_variable.endswith('%'):
					coupling_disorder_percentage = float(coupling_disorder_variable.replace('%',''))
					coupling_disorder = abs(coupling_energy * (coupling_disorder_percentage/100.0))
				else:
					coupling_disorder = coupling_disorder_variable
				
				# 5.2.2.2: Obtain the coupling disorder for the disorder energy. coupling_energy and coupling_disorder given in eV. 
				V_with_disorder = normal(coupling_energy, coupling_disorder)

				# 5.2.2.3: Add this V_with_disorder to the KMC crystal database graph 
				graph.add_V_with_disorder(current_molecule_description, neighbouring_molecule_description, V_with_disorder)

			# 5.3: get the difference in energy between the two molecules.
			deltaE_with_disorders = (other_molecule_E_with_disorder - current_molecule_E_with_disorder)

			# 5.4: Obtain the rate constant for the exciton to move from the current molecule to another molecule that maybe in another unit cell.
			k_12 = (V_with_disorder**2.0)*M_constant*exp(-((deltaE_with_disorders**2.0)*X_constant + deltaE_with_disorders*Y_constant + Z_constant))

			# 5.5: Add the rate constant data to the storage list and dictionaries. 
			neighbouring_molecule_descriptions.append(neighbouring_molecule_description)
			rate_constants.append(k_12)
			
	# Sixth, return current_molecule_E_with_disorder, neighbouring_molecule_descriptions, and rate_constants
	return current_molecule_E_with_disorder, neighbouring_molecule_descriptions, rate_constants



