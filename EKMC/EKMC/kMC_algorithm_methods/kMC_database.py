"""
kMC_database.py, Geoffrey Weal, 26/3/22

kMC_database is the object for storing molecules in various unit cells (nodes) and the rate constants between those molecules (edges).
"""
from EKMC.EKMC.kMC_algorithm_methods.on_disk_database import on_disk_database

class kMC_database:
	"""
	This class is designed to hold nodes that represent molecules in the OPV crystal. 

	This class incorporates the SQlite database to move node information to the database and off of the RAM memory when the RAM gets too full.
	"""
	def __init__(self, number_of_molecules, no_of_molecules_at_cell_points_to_store_on_RAM, no_of_V_with_disorders_to_store_in_RAM=None, store_data_in_databases=True):

		# First, determine if we want to store the data in a database.
		self.store_data_in_databases = store_data_in_databases

		# Second, set up the nodes variables for supporting rate constant from from molecules
		self.E_with_disorders = {}
		if self.store_data_in_databases:
			self.most_recently_viewed_nodes_stack = []
			self.no_of_molecules_at_cell_points_to_store_on_RAM = no_of_molecules_at_cell_points_to_store_on_RAM

		# Third, set up the variables for storing V_with_disorders values between mol1s and mol2s.
		self.V_with_disorders = {}
		if self.store_data_in_databases:
			self.most_recently_viewed_V_with_disorders_stack = []
			if no_of_V_with_disorders_to_store_in_RAM is None:
				self.no_of_V_with_disorders_to_store_in_RAM = no_of_molecules_at_cell_points_to_store_on_RAM*(no_of_molecules_at_cell_points_to_store_on_RAM+1)/2 # ** 2
			else:
				self.no_of_V_with_disorders_to_store_in_RAM = no_of_V_with_disorders_to_store_in_RAM

		# Create the database for storing data on disk
		#self.database = on_disk_database(number_of_molecules)

	def check_database(self):
		"""
		To do
		"""
		pass

	# ------------------------------------------------------------------------------------------------------------------------------------------------

	def get_E_with_disorder(self, current_molecule_description):
		"""
		This method will return the data about the current simulation, based on the keys given.

		The value of E given includes its disorder.

		Parameters
		----------
		current_molecule_description : tuple
			This is the label for the molecule in the unit cell that the exciton is on.

		Returns
		-------
		current_molecule_E_with_disorder : float
			This is the E value for the molecule that includes it's disorder for the molecule at a cell position.
		"""

		# First, obtain the disorder of the current molecule of interest
		current_molecule_E_with_disorder = self.E_with_disorders.get(current_molecule_description,None)

		# Second, return the current_molecule_E_with_disorder value.
		return current_molecule_E_with_disorder

	def add_E_with_disorder(self, current_molecule_description, current_molecule_E_with_disorder):
		"""
		This method will add the rate constant data about how the exciton will move from current_molecule_description to all other molecules in the same or other unit cells that neighbour the current molecule.

		The value of E added should include its disorder.

		Parameters
		----------
		current_molecule_description : tuple
			This is the label for the molecule in the unit cell that the exciton is on.
		current_molecule_E_with_disorder : float
			This is the E value for the molecule that includes it's disorder for the molecule at a cell position.
		""" 
		self.E_with_disorders[current_molecule_description] = current_molecule_E_with_disorder

	# ------------------------------------------------------------------------------------------------------------------------------------------------

	def get_V_with_disorder(self, molecule1_description, molecule2_description):
		"""
		This method is designed to return the V12 value of a coupled dimer, including its given disorder.

		Parameters
		----------
		molecule1_description : tuple
			This is the label for the first molecule in the unit cell that the exciton is on.
		molecule2_description : tuple
			This is the label for the second molecule in the unit cell that the exciton could move to.

		Returns
		-------
		V_with_disorder : float
			This is a coupling energy for the dimer. This includes the disorder assigned to this dimer coupling energy.
		"""

		# First, write the key to get V_with_disorder for the dimer involving (molecule1_description, molecule2_description)
		key_to_get = self.get_lower_and_higher_molecule_descriptions(molecule1_description, molecule2_description)

		# Second, obtain the coupling energy V12 with disorder for this dimer, if it has been given in the database.
		V_with_disorder = self.V_with_disorders.get(key_to_get, None)

		# Third, return V_with_disorder
		return V_with_disorder
	
	def add_V_with_disorder(self, molecule1_description, molecule2_description, V_with_disorder):
		"""
		This method is designed to add the coupling energy of a dimer to the V_with_disorders database. 

		Parameters
		----------
		molecule1_description : tuple
			This is the label for the first molecule in the unit cell that the exciton is on.
		molecule2_description : tuple
			This is the label for the second molecule in the unit cell that the exciton could move to.
		V_with_disorder : float
			This is a coupling energy for the dimer. This includes the disorder assigned to this dimer coupling energy.
		"""

		# First, get the dimer key for the dimer involving (molecule1_description, molecule2_description)
		key_to_add = self.get_lower_and_higher_molecule_descriptions(molecule1_description, molecule2_description)

		# Second, check if the key_to_add is already in self.V_with_disorders. If this is True, something weird is happening in the EKMC code.
		if key_to_add in self.V_with_disorders:
			print(self.V_with_disorders[key_to_add])
			raise Exception('Huh?')

		# Third, add the V_with_disorder for this dimer to the self.V_with_disorders dictionary (database).
		self.V_with_disorders[key_to_add] = V_with_disorder

	# ------------------------------------------------------------------------------------------------------------------------------------------------

	def get_lower_and_higher_molecule_descriptions(self, current_molecule1_description, current_molecule2_description):
		"""
		This method will convert the unit cell ijk numbers into a octadecimal integer, where 8 means a positive number and 9 a negative number.

		Parameters
		----------
		molecule1_description : tuple
			This is the label for the first molecule in the unit cell that the exciton is on.
		molecule2_description : tuple
			This is the label for the second molecule in the unit cell that the exciton could move to.

		Returns
		-------
		key_to_add : tuple
			This contains the information for the key to store information in the dictionary databases.
		"""

		# First, obtain the molecule number and the cell point for each molecule in the dimer
		molecule_no1, cell_1 = current_molecule1_description
		molecule_no2, cell_2 = current_molecule2_description

		# Second, determine the key_to_add to return, either (current_molecule1_description, current_molecule2_description) or (current_molecule2_description, current_molecule1_description)
		if molecule_no1 < molecule_no2:
			return (current_molecule1_description, current_molecule2_description)
		elif molecule_no1 == molecule_no2:
			if cell_1 < cell_2:
				return (current_molecule1_description, current_molecule2_description)
			elif cell_1 == cell_2:
				raise Exception('Same molecule for current_molecule1_description and current_molecule2_description? Weird???')
			else:
				return (current_molecule2_description, current_molecule1_description)
		else:
			return (current_molecule2_description, current_molecule1_description)

	# ------------------------------------------------------------------------------------------------------------------------------------------------




