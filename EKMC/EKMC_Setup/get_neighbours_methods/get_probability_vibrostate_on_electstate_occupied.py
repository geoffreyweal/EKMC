"""
get_probability_vibrostate_on_electstate_occupied.py, Geoffrey Weal, 23/3/22

This script is designed to give the probabilities of being populated in each vibrational state, based on boltzmann statistics.
"""

from math import exp

# Constants
kB = 8.617333262145 * (10.0 ** -5.0) # eV K-1

def get_probability_vibrostate_on_electstate_occupied(uu_max,WW,temperature):
	"""
	This method is designed to obtain the probabilities of being populated in each vibrational state, based on boltzmann statistics.

	Parameters
	----------
	uu_max : int
		This is the highest vibrational mode that is examined in the molecule.
	WW : float
		This is the wang value without the hbar value. explain this better. Given in eV.
	temperature : float
		This is the temperature of the crystal. Given in K. 

	Returns
	-------
	probs : list of floats
		These are the probabilities of a molecule being in the ith vibrational state.
	"""
	probs = [exp(-(uu*WW)/(kB*temperature)) for uu in range(0,uu_max+1,1)]
	sum_of_probs = sum(probs)
	probs = [prob/sum_of_probs for prob in probs]
	return probs