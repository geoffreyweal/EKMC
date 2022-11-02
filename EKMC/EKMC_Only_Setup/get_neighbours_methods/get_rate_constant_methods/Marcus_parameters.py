"""
get_rate_constant_data.py, Geoffrey Weal, 23/3/22

This script is designed to obtain all the values that are used in obtaining rate constants that do not change between moving from unit cell to unit cell.
"""

from math import exp, pi

# Constants
kB = 8.617333262145 * (10.0 ** -5.0) # eV K-1
h_bar = 6.582119569 * (10.0 ** -16.0) # eV s

def get_Marcus_parameters(molecule1, molecule2, displacement_vector, coupling_energy, classical_reorganisation_energy, temperature):
	"""
	This method is deigned to give the rate constant parameters for excitonic movements between molecules, based on Marcus Theory.

	Parameters
	----------
	molecule1 : ase.Atoms
		This is the first molecule.
	molecule2 : ase.Atoms
		This is the second molecule. 
	displacement_vector : numpy.array
		This is the displacement vector to move the second molecule into the unit cell you want to place it in.
	coupling_energy : float
		This is the electron coupling energy between molecule 1 and molecule 2 (where molecule 2 is in the unit cell given by displacement_vector). Given in eV.
	classical_reorganisation_energy : float
		This is the classical component of the amount of energy that is required for the molecule in the excited state to change geometry from the ground state geometry to the excited state geometry. Given in eV.
	temperature : float
		This is the temperature of the crystal. Given in K. 

	Returns
	-------
	The values required for the rate constant for different molecules that are not dependent on disorder.
	"""

	# First, get the M constant.
	M_constant = get_M_constant(coupling_energy,classical_reorganisation_energy,temperature)

	# Second, get the X constant.
	X_constant = get_X_constant(classical_reorganisation_energy,temperature)

	# Third, get the X constant.
	Y_constant = get_Y_constant(temperature)

	# Fourth, get the X constant.
	Z_constant = get_Z_constant(classical_reorganisation_energy,temperature)

	# Fifth, return the various rate constant parameters for this excitonic step.
	return (coupling_energy, M_constant, X_constant, Y_constant, Z_constant)

def get_M_constant(coupling_energy, classical_reorganisation_energy, temperature):
	"""
	This method is used to obtain the M constant

	Parameters
	----------
	coupling_energy : float
		This is the total coupling energy of the dimer, given as V12. This value is given in eV.
	classical_reorganisation_energy : float
		This is the classical component of the amount of energy that is required for the molecule in the excited state to change geometry from the ground state geometry to the excited state geometry. Given in eV.
	temperature : float
		This is the temperature of the crystal. Given in K. 

	Returns
	-------
	constant_M : float
		The M constant.
	"""
	constant_M = (1/h_bar) * ((pi/(classical_reorganisation_energy*kB*temperature))**0.5)
	return constant_M

def get_X_constant(classical_reorganisation_energy, temperature):
	"""
	This method is used to obtain the X constant

	Parameters
	----------
	classical_reorganisation_energy : float
		This is the classical component of the amount of energy that is required for the molecule in the excited state to change geometry from the ground state geometry to the excited state geometry. Given in eV.
	temperature : float
		This is the temperature of the crystal. Given in K. 

	Returns
	-------
	X_constant : float
		The X constant.
	"""
	X_constant = 1/(4.0*classical_reorganisation_energy*kB*temperature)
	return X_constant

def get_Y_constant(temperature):
	"""
	This method is used to obtain the Y constant

	Parameters
	----------
	temperature : float
		This is the temperature of the crystal. Given in K. 

	Returns
	-------
	Y_constant : float
		The Y constant.
	"""
	Y_constant = 1.0/(2.0*kB*temperature)
	return Y_constant

def get_Z_constant(classical_reorganisation_energy, temperature):
	"""
	This method is used to obtain the Z constant.

	Parameters
	----------
	classical_reorganisation_energy : float
		This is the classical component of the amount of energy that is required for the molecule in the excited state to change geometry from the ground state geometry to the excited state geometry. Given in eV.
	temperature : float
		This is the temperature of the crystal. Given in K. 

	Returns
	-------
	Z_constant : float
		The Z constant.
	"""
	Z_constant = classical_reorganisation_energy/(4.0*kB*temperature)
	return Z_constant
