"""
get_franck_condon_overlap.py, Geoffrey Weal, 23/3/22

This script is designed to obtain the frank condon overlap value efficiently and without loss of data.

Based on equation 7 in "A very general rate expression for charge hopping in semiconducting polymers", DOI: 10.1063/1.4920945
"""
from math  import exp
from numpy import prod

from collections import Counter

def get_franck_condon_overlap(huang_rhys_factor, uu, vv):
	"""
	This method calulates the Franck-Condon (overlap) integral between two vibrational states v and w with Huang-Rhys factor.

	Parameters
	----------
	huang_rhys_factor : int
		https://second.wiki/wiki/huang-rhys-faktor 
	uu : int
		This is the vibrational mode to examine in molecule 1
	vv : int
		This is the vibrational mode to examine in molecule 2
	"""
	sqrt_of_huang_rhys_factor = huang_rhys_factor ** 0.5
	franck_condon_integral_sum = 0.0
	for ii in range(0,uu+1):
		for jj in range(0,vv+1):
			# This if statement defines the Kronecker delta
			if (uu - ii) == (vv - jj):
				part1 = 1 if (jj % 2 == 0) else -1
				part2 = sqrt_of_huang_rhys_factor ** float(ii+jj)
				factorial_combination = get_factorial_component_of_franck_condon_overlap(uu,vv,ii,jj)
				sqrt_of_factorial_combination = factorial_combination ** 0.5
				ii_jj_value = part1 * part2 * sqrt_of_factorial_combination
				franck_condon_integral_sum += ii_jj_value
	franck_condon_integral = exp(-huang_rhys_factor/2.0) * franck_condon_integral_sum
	return franck_condon_integral

# ----------------------------------------------------------------------------------------------------------------------------

def get_factorial_component_of_franck_condon_overlap(uu,vv,ii,jj):
	"""
	This method is designed to give the results from the factorial component of equation 7 given in "A very general rate expression for charge hopping in semiconducting polymers", DOI: 10.1063/1.4920945

	Parameters
	----------
	uu : int
		This is the vibrational mode to examine in molecule 1
	vv : int
		This is the vibrational mode to examine in molecule 2
	ii : int
		This is the sum index value related to the vibrational mode to examine in molecule 1
	jj : int
		This is the sum index value related to the vibrational mode to examine in molecule 2

	Returns
	-------
	factorial_combination : float
		This is the value of the factorial component of equation 7
	"""

	# First, get the values in the factorials from the rCr equations
	comb_ui_num, comb_ui_dem = get_combination_list(uu,ii)
	comb_vj_num, comb_vj_dem = get_combination_list(vv,jj)

	# Get the factorials for ii and jj
	ii_factorial = get_partial_factorial(ii)
	jj_factorial = get_partial_factorial(jj)

	# Get the factorials in the numerator and denominator of equation 7
	all_nums = comb_ui_num + comb_vj_num
	all_dem = comb_ui_dem + comb_vj_dem + ii_factorial + jj_factorial

	# Some of the values in the numerator and denominator will cancel eachother out or will be factored, so just get the lists
	# of values in the numerator and denominator that need to be multiplied together. 
	unique_nums, unique_dems = get_unique_nums_and_dems(all_nums,all_dem)

	# Multiply all the values in the numerator and denominator lists together.
	import pdb; pdb.set_trace()
	numerator   = prod(unique_nums)
	denominator = prod(unique_dems)

	# Get the result from the factorial component of equation 7 
	factorial_combination = float(numerator)/float(denominator)

	return factorial_combination

def get_combination_list(uu,ii):
	"""
	This method will give the values in the factorials involved in the numerator and demoninator of the combination (nCr) equation.

	More information about the nCr equation is given in https://en.wikipedia.org/wiki/Combination

	Parameters
	----------
	uu : int
		This is the vibrational mode to examine in a molecule.
	ii : int
		This is the sum index value related to the vibrational mode to examine in a molecule.

	Returns
	-------
	numerator : list
		These are the numbers that are involved in the factorial of the numerator of the nCr equation.
	denominator : list
		These are the numbers that are involved in the factorial of the denominator of the nCr equation.
	"""
	numerator = get_partial_factorial(uu,uu-ii+1) # start with uu and end with and including uu-ii+1
	denominator = get_partial_factorial(ii)
	return numerator, denominator

def get_factorial_list(xx):
	partial_factorial = list(range(xx,0,-1))
	partial_factorial = [1] if (partial_factorial == []) else partial_factorial
	return partial_factorial

def check_the_get_partial_factorial_is_working(partial_factorial,xx,yy):
	# Check to make sure this function is working

	partial_factorial_copy = list(partial_factorial)
	if 1 in partial_factorial_copy:
		partial_factorial_copy.remove(1)
	partial_factorial_copy.sort()

	check_factorial = get_factorial_list(xx)
	for value in get_factorial_list(yy-1):
		if value in check_factorial:
			check_factorial.remove(value)
	check_factorial = [1] if (check_factorial == []) else check_factorial
	if 1 in check_factorial:
		check_factorial.remove(1)
	check_factorial.sort()

	if not partial_factorial_copy == check_factorial:
		print('partial_factorial = '+str(partial_factorial_copy))
		print('check_factorial = '+str(check_factorial))
		exit('huh')

def get_partial_factorial(xx,yy=1):
	"""
	This method will give the partial factorial from xx.(xx-1).(xx-2)...(yy+2).(yy+1).yy

	Parameters
	----------
	xx : int
		This is the top of the range
	yy : int
		This is the bottom of the range. This value IS included in the range

	Returns
	-------
	partial_factorial : list
		These are all the numbers that are involved in the partial factional from xx to yy. E.g. [xx,xx-1,xx-2,...,yy+2,yy+1,yy]
	"""
	partial_factorial = list(range(xx,yy-1,-1))
	partial_factorial = [1] if (partial_factorial == []) else partial_factorial
	check_the_get_partial_factorial_is_working(partial_factorial,xx,yy)
	return partial_factorial

def get_unique_nums_and_dems(all_nums,all_dem):
	"""
	This method is designed to give the result of the get_factorial_component_of_franck_condon_overlap method as efficiently as possible but also with no loss of information. 

	This method will give the 

	Parameters
	----------
	all_nums : list
		This is the list of all values in the numerator that will be multiplied together. 
	all_dem : list
		This is the list of all values in the denominator that will be multiplied together. 

	Returns
	-------
	unique_nums : list
		This is the list of all values in the numerator that will be multiplied together. 
	unique_dems : list
		This is the list of all values in the denominator that will be multiplied together. 
	"""
	# First, determine all the numbers in the numerator and denominator that are in common in the two lists.
	identical_items_including_duplicates = list((Counter(all_nums) & Counter(all_dem)).elements())

	# Second, remove all values from the identical_items_including_duplicates list from all_nums (and all_dem) to give unique_nums (and unique_dems).
	unique_nums = list(all_nums)
	unique_dems = list(all_dem)
	for value in identical_items_including_duplicates:
		unique_nums.remove(value)
		unique_dems.remove(value)

	# Third, if there are any numbers in the numerator that can be factored by a number from the denominator
	# factorise the numerator number and remove that denominator number from the unique_dems list
	for index_dem in range(len(unique_dems)-1,-1,-1):
		unique_dem = unique_dems[index_dem]
		for index_num in range(len(unique_nums)):
			unique_num = unique_nums[index_num]
			divide_value, modulus_value = divmod(unique_num, unique_dem)
			if modulus_value == 0.0:
				unique_nums[index_num] = divide_value
				del unique_dems[index_dem]
				break

	# Fifth, check after the factorizing routiene determine all the numbers in the numerator and denominator that are in common in the two lists.
	# and then remove all values from the identical_items_including_duplicates list from all_nums (and all_dem) to give unique_nums (and unique_dems).
	identical_items_including_duplicates = list((Counter(unique_nums) & Counter(unique_dems)).elements())
	for value in identical_items_including_duplicates:
		unique_nums.remove(value)
		unique_dems.remove(value)

	# if the unique_dems list is empty, append 1 to it so the numerator can be divided by the denominator 
	if len(unique_nums) == 0:
		unique_nums = [1]
	if len(unique_dems) == 0:
		unique_dems = [1]

	return unique_nums, unique_dems

# ----------------------------------------------------------------------------------------------------------------------------





