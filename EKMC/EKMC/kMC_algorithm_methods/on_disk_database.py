"""
on_disk_database.py, Geoffrey Weal, 26/3/22

on_disk_database is a object that will interact with a database 
"""
import os

from EKMC.EKMC.kMC_algorithm_methods.convert_between_bases import convert_between_bases

class on_disk_database:
	"""
	This class is designed allow the kMC_graph to interact with the database.

	Parameters
	----------
	number_of_molecules : int.
		This is the number of molecules in the crystal.
	database_name : str.
		This is the name of the database
	"""
	def __init__(self, number_of_molecules, database_name='graph.db', db_type='sqlite3'):
		# First, set the name of the database
		self.number_of_molecules = number_of_molecules
		self.database_name = database_name
		self.db_type = db_type

		if self.db_type == 'sqlite3':
			from sqlite3 import connect
		elif self.db_type == 'postgresql':
			from psycopg2 import connect
		self.connect = connect

		# Second, if the database does not exist, create the database and setup the table for each molecule and for V12.
		if not os.path.exists(self.database_name):
			with self.get_connection() as database:
				cursor = database.cursor()
				for molecule_no in range(self.number_of_molecules):
					self.make_molecule_table(cursor, molecule_no)
				for molecule_no1 in range(self.number_of_molecules):
					for molecule_no2 in range(molecule_no1,self.number_of_molecules): 
						self.make_V_disorder_table(cursor, molecule_no1, molecule_no2)
				database.commit()

	def get_connection(self):
		if self.db_type == 'sqlite3':
			connection = self.connect(self.database_name)
		elif self.db_type == 'postgresql':
			import pdb; pdb.set_trace()
			connection = self.connect(database=self.database_name)
		return connection

	def make_molecule_table(self, cursor, molecule_no):
		"""
		This method initialises the table for a molecule in the crystal
		"""
		# If the database does not exist, create the database and setup the table.
		cursor.execute(""" CREATE TABLE m"""+str(molecule_no)+""" (
					cell_id integer PRIMARY KEY,
					molecule_deltaE_disorder text,
					other_molecule_descriptions text,
					rate_constants text
					) WITHOUT ROWID""")

	def make_V_disorder_table(self, cursor, molecule_no1, molecule_no2):
		"""
		This method initialises the table for a molecule in the crystal
		"""
		# If the database does not exist, create the database and setup the table.
		cursor.execute(""" CREATE TABLE V"""+str(molecule_no1)+str(molecule_no2)+"""_disorders (
					m1_m2_cells_id integer PRIMARY KEY,
					V_disorder text
					) WITHOUT ROWID""")

# ------------------------------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------------------------

	def get_from_database(self, current_molecule_description):
		"""
		This method will obtain the data for the current node (current_molecule_description) from the database.
		
		Parameters
		----------
		current_molecule_description : tuple
			This is the label for the molecule in the unit cell that the exciton is on.

		Returns
		-------
		molecule_deltaE_disorder : float
			This is the disorder given to the value of E given to this current molecule in the OPV crystal. 
		other_molecule_descriptions : list
			This is a list of all the labels of the other molecules that the exciton could move to from the current molecule in the OPV crystal.
		rate_constants : list
			This is a list of all the rate_constants for the other molecules for the exciton to move to from the current molecule in the OPV crystal.
		"""
		# First, get the data from the database
		database_data = self._get_from_database(current_molecule_description)

		# Second, if this data is not in the database, it will return None
		if database_data is None:
			return None

		# if the database does contain the data, return this data.
		molecule_deltaE_disorder, other_molecule_descriptions, rate_constants = database_data
		return (eval(molecule_deltaE_disorder), eval(other_molecule_descriptions), eval(rate_constants))

	def _get_from_database(self, current_molecule_description):
		"""
		This method will obtain the data for the current node (current_molecule_description) from the database.

		This method will obtain the raw data, while the get_from_database method refine this data so it is usable.

		Parameters
		----------
		current_molecule_description : tuple
			This is the label for the molecule in the unit cell that the exciton is on.

		Returns
		-------
		database_data : tuple
			This includes all the data that was obtain about the current node (current_molecule_description) from the database
		"""
		molecule_no, cell_id = self.convert_mol_descr_into_cell_id(current_molecule_description)
		with self.get_connection() as database:
			cursor = database.cursor()
			cursor.execute("SELECT molecule_deltaE_disorder, other_molecule_descriptions, rate_constants FROM m"+str(molecule_no)+" WHERE cell_id = ?", [cell_id])
			database_data = cursor.fetchone()
			database.commit()
		return database_data

# ------------------------------------------------------------------------------------------------------------------------------------------------

	def add_to_database(self, current_molecule_description, molecule_deltaE_disorder=None, other_molecule_descriptions=None, rate_constants=None):
		"""
		This method will add data to a node in the database.

		Parameters
		----------
		current_molecule_description : tuple
			This is the label for the molecule in the unit cell that the exciton is on.
		molecule_deltaE_disorder : float
			This is the disorder given to the value of E given to this current molecule in the OPV crystal. 
		other_molecule_descriptions : list
			This is a list of all the labels of the other molecules that the exciton could move to from the current molecule in the OPV crystal.
		rate_constants : list
			This is a list of all the rate_constants for the other molecules for the exciton to move to from the current molecule in the OPV crystal.
		"""
		molecule_no, cell_id = self.convert_mol_descr_into_cell_id(current_molecule_description)
		with self.get_connection() as database:
			cursor = database.cursor()
			cursor.execute("INSERT INTO m"+str(molecule_no)+" (cell_id, molecule_deltaE_disorder, other_molecule_descriptions, rate_constants) VALUES (?, ?, ?, ?)", (cell_id, str(molecule_deltaE_disorder), str(other_molecule_descriptions), str(rate_constants)))
			database.commit()

	def update_database(self, current_molecule_description, database_data, molecule_deltaE_disorder=None, other_molecule_descriptions=None, rate_constants=None):
		"""
		This method will update data to a node in the database.

		Parameters
		----------
		current_molecule_description : tuple
			This is the label for the molecule in the unit cell that the exciton is on.
		molecule_deltaE_disorder : float
			This is the disorder given to the value of E given to this current molecule in the OPV crystal. 
		other_molecule_descriptions : list
			This is a list of all the labels of the other molecules that the exciton could move to from the current molecule in the OPV crystal.
		rate_constants : list
			This is a list of all the rate_constants for the other molecules for the exciton to move to from the current molecule in the OPV crystal.
		"""
		molecule_deltaE_disorder_in_database, other_molecule_descriptions_in_database, rate_constants_in_database = database_data
		# Determine which inputs to update. If notmal variable is set to None, keep the original database variable in the database.
		if molecule_deltaE_disorder is None:
			molecule_deltaE_disorder = molecule_deltaE_disorder_in_database
		if other_molecule_descriptions is None:
			other_molecule_descriptions = other_molecule_descriptions_in_database
		if rate_constants is None:
			rate_constants = rate_constants_in_database
		# Update the database
		molecule_no, cell_id = self.convert_mol_descr_into_cell_id(current_molecule_description)
		with self.get_connection() as database:
			cursor = database.cursor()
			cursor.execute("""UPDATE m"""+str(molecule_no)+""" SET 
				molecule_deltaE_disorder = ?,
				other_molecule_descriptions = ?, 
				rate_constants = ?
				WHERE cell_id = ?
				""", (str(molecule_deltaE_disorder), str(other_molecule_descriptions), str(rate_constants), cell_id))
			database.commit()

# ------------------------------------------------------------------------------------------------------------------------------------------------

	def convert_mol_descr_into_cell_id(self, current_molecule_description):
		"""
		This method will convert the unit cell ijk numbers into a octadecimal integer, where 8 means a positive number and 9 a negative number.
		"""
		molecule_no, (uc_i, uc_j, uc_k) = current_molecule_description
		uc_i_sign_number = 8 if uc_i >= 0 else 9 # positive numbers are 8, negative numbers are 9.
		uc_i_base_8 = convert_between_bases(abs(uc_i), 10, 8)
		uc_j_sign_number = 8 if uc_j >= 0 else 9 # positive numbers are 8, negative numbers are 9.
		uc_j_base_8 = convert_between_bases(abs(uc_j), 10, 8)
		uc_k_sign_number = 8 if uc_k >= 0 else 9 # positive numbers are 8, negative numbers are 9.
		uc_k_base_8 = convert_between_bases(abs(uc_k), 10, 8)
		cell_id = int(str(uc_i_sign_number)+str(uc_i_base_8)+str(uc_j_sign_number)+str(uc_j_base_8)+str(uc_k_sign_number)+str(uc_k_base_8))
		return molecule_no, cell_id

# ------------------------------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------------------------

	def get_V_disorder_from_database(self, current_molecule1_description, current_molecule2_description):
		"""
		This method will obtain the data for the current node (m1_m2_cells) from the database.
		
		Parameters
		----------
		m1_m2_cells : tuple
			This is the label for the molecule in the unit cell that the exciton is on.

		Returns
		-------
		molecule_deltaE_disorder : float
			This is the disorder given to the value of E given to this current molecule in the OPV crystal. 
		other_molecule_descriptions : list
			This is a list of all the labels of the other molecules that the exciton could move to from the current molecule in the OPV crystal.
		rate_constants : list
			This is a list of all the rate_constants for the other molecules for the exciton to move to from the current molecule in the OPV crystal.
		"""
		# First, get the data from the database
		V_disorder = self._get_V_disorder_from_database(current_molecule1_description, current_molecule2_description)

		# Second, if this data is not in the database, it will return None
		if V_disorder is None:
			return None

		V_disorder = float(V_disorder[0])

		# if the database does contain the data, return this data.
		return V_disorder

	def _get_V_disorder_from_database(self, current_molecule1_description, current_molecule2_description):
		"""
		This method will obtain the data for the current node (m1_m2_cells) from the database.

		This method will obtain the raw data, while the get_from_database method refine this data so it is usable.

		Parameters
		----------
		m1_m2_cells : tuple
			This is the label for the molecule in the unit cell that the exciton is on.

		Returns
		-------
		database_data : tuple
			This includes all the data that was obtain about the current node (m1_m2_cells) from the database
		"""
		molecule_no1, molecule_no2, m1_m2_cells_id = self.convert_double_mol_descr_into_cell_id(current_molecule1_description, current_molecule2_description)
		with self.get_connection() as database:
			cursor = database.cursor()
			cursor.execute("SELECT V_disorder FROM V"+str(molecule_no1)+str(molecule_no2)+"_disorders WHERE m1_m2_cells_id = ?", [m1_m2_cells_id])
			database_data = cursor.fetchone()
			database.commit()
		return database_data

# ------------------------------------------------------------------------------------------------------------------------------------------------

	def add_V_disorder_to_database(self, current_molecule1_description, current_molecule2_description, V_disorder):
		"""
		This method will add data to a node in the database.

		Parameters
		----------
		current_molecule_description : tuple
			This is the label for the molecule in the unit cell that the exciton is on.
		molecule_deltaE_disorder : float
			This is the disorder given to the value of E given to this current molecule in the OPV crystal. 
		other_molecule_descriptions : list
			This is a list of all the labels of the other molecules that the exciton could move to from the current molecule in the OPV crystal.
		rate_constants : list
			This is a list of all the rate_constants for the other molecules for the exciton to move to from the current molecule in the OPV crystal.
		"""
		molecule_no1, molecule_no2, m1_m2_cells_id = self.convert_double_mol_descr_into_cell_id(current_molecule1_description, current_molecule2_description)
		with self.get_connection() as database:
			cursor = database.cursor()
			cursor.execute("INSERT INTO V"+str(molecule_no1)+str(molecule_no2)+"_disorders (m1_m2_cells_id, V_disorder) VALUES (?, ?)", (m1_m2_cells_id, str(V_disorder)))
			database.commit()

# ------------------------------------------------------------------------------------------------------------------------------------------------

	def convert_double_mol_descr_into_cell_id(self, current_molecule1_description, current_molecule2_description):
		"""
		This method will convert the unit cell ijk numbers into a octadecimal integer, where 8 means a positive number and 9 a negative number.
		"""
		molecule_no1, cell_id_1 = self.convert_mol_descr_into_cell_id(current_molecule1_description)
		molecule_no2, cell_id_2 = self.convert_mol_descr_into_cell_id(current_molecule2_description)

		if molecule_no1 <= molecule_no2:
			m1_m2_cells_id = int(str(cell_id_1)+str(cell_id_2))
			return molecule_no1, molecule_no2, m1_m2_cells_id
		else:
			m1_m2_cells_id = int(str(cell_id_2)+str(cell_id_1))
			return molecule_no2, molecule_no1, m1_m2_cells_id

# ------------------------------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------------------------



