/**
 * convert_arrays_to_unordered_maps.cpp, 29/5/23, Geoffrey Weal
 * 
 * This program is designed to convert the coupling_value_data array into an unordered_map to be used as a quick lookup table
 */
#include <iostream>
#include <iomanip>
#include <tuple>
#include <vector>
#include <unordered_map>
#include "convert_arrays_to_unordered_maps.h"
using namespace std;

unordered_map<int, vector<long double>> convert_to_COM_dictionary(const COM_CObject** centre_of_molecules_array, const int centre_of_molecules_array_size) {
	/**
	 * This method is designed to convert the centre_of_molecules_array array into an unordered_map to be used as a quick lookup table.
	 * The inputs for this may be the centre of molecule or centre of mass for the molecules in the unit cell. 
	 * 
	 * @param centre_of_molecules_array This list contains all the molecules in the crystal, along with their centre of mass/molecule. 
	 * @param centre_of_molecules_array_size This is the number of values in the centre_of_molecules_array array.
	 * 
	 * @returns molecule_bandgap_energies an unordered_map that provides the bandgap energy for each molecule in your crystal.
	 */

	// First, initialise the unordered_map. 
	unordered_map<int, vector<long double>> centre_of_molecules; 
	centre_of_molecules.reserve(centre_of_molecules_array_size);

	// Second, go through the array of Coupling_Value_Data_CObjects, take the data, and place it in the unordered_map. 
	for (int i = 0; i < centre_of_molecules_array_size; i++) {

		// 2.1: collect all the data from molecule_bandgap_energies_array[i]
		int mol = (*centre_of_molecules_array)[i].mol;
		//vector<long double> centre_of_molecules = {(*centre_of_molecules_array)[i].centre_of_mass_x, (*centre_of_molecules_array)[i].centre_of_mass_y, (*centre_of_molecules_array)[i].centre_of_mass_z};

		// 2.2: Store the centre of molecule/mass in centre_of_molecules for molname
		centre_of_molecules[mol] = {(*centre_of_molecules_array)[i].centre_of_mass_x, (*centre_of_molecules_array)[i].centre_of_mass_y, (*centre_of_molecules_array)[i].centre_of_mass_z}; // Attaching vecor directly
	}

	// Third, return centre_of_molecules as an unordered map.
	return centre_of_molecules;
}

vector<vector<long double>> convert_to_UCM_dictionary(const long double** unit_cell_matrix_array, const int unit_cell_matrix_array_size) {
	/**
	 * This method is designed to convert the unit cell matrix that is current in a 1D array into a 2D array. 
	 * 
	 * @param unit_cell_matrix_array This list contains the unit cell matrix as [xx, xy, xz, yx, yy, yz, zx, zy, zz]
	 * @param unit_cell_matrix_array_size This is the number of values in the unit_cell_matrix_array array.
	 * 
	 * @returns molecule_bandgap_energies an unordered_map that provides the bandgap energy for each molecule in your crystal.
	 */

	// First, initialise and create the 2D unit cell matrix. 
	vector<vector<long double>> unit_cell_matrix
	{ 
		{(*unit_cell_matrix_array)[0], (*unit_cell_matrix_array)[3], (*unit_cell_matrix_array)[6]}, 
		{(*unit_cell_matrix_array)[1], (*unit_cell_matrix_array)[4], (*unit_cell_matrix_array)[7]}, 
		{(*unit_cell_matrix_array)[2], (*unit_cell_matrix_array)[5], (*unit_cell_matrix_array)[8]} 
	}; 

	// Second, return centre_of_molecules as an unordered map.
	return unit_cell_matrix;
}

unordered_map<int, long double> convert_to_MBE_dictionary(const Bandgap_Energies_CObject** molecule_bandgap_energies_array, const int molecule_bandgap_energies_array_size) {
	/**
	 * This method is designed to convert the molecule_bandgap_energies array into an unordered_map to be used as a quick lookup table
	 * 
	 * @param molecule_bandgap_energies_array This dictionary contains all the coupling values information about the neighbourhoods that surrounded each molecule in your crystal.
	 * @param molecule_bandgap_energies_array_size This is the number of values in the coupling_value_data array.
	 * 
	 * @returns molecule_bandgap_energies an unordered_map that provides the bandgap energy for each molecule in your crystal.
	 */

	// First, initialise the unordered_map. 
	unordered_map<int, long double> molecule_bandgap_energies;
	molecule_bandgap_energies.reserve(molecule_bandgap_energies_array_size);

	// Second, go through the array of Coupling_Value_Data_CObjects, take the data, and place it in the unordered_map. 
	for (int i = 0; i < molecule_bandgap_energies_array_size; i++) {

		// 2.1: collect all the data from molecule_bandgap_energies_array[i]
		int mol = (*molecule_bandgap_energies_array)[i].mol;
		long double bandgap_energy = (*molecule_bandgap_energies_array)[i].bandgap_energy;

		// 2.2: Store the bandgap energy in molecule_bandgap_energies for molname
		molecule_bandgap_energies[mol] = bandgap_energy;
	}

	// Third, return molecule_bandgap_energies as an unordered map.
	return molecule_bandgap_energies;
}

unordered_map<tuple<int,int>, long double, hash_tuple_DRE> convert_to_DRE_dictionary(const Reorganisation_Energies_CObject** dimer_reorganisation_energies_array, const int dimer_reorganisation_energies_array_size) {
	/**
	 * This method is designed to convert the dimer_reorganisation_energies array into an unordered_map to be used as a quick lookup table
	 * 
	 * @param dimer_reorganisation_energies_array This dictionary contains all the coupling values information about the neighbourhoods that surrounded each molecule in your crystal.
	 * @param dimer_reorganisation_energies_array_size This is the number of values in the coupling_value_data array.
	 * 
	 * @returns dimer_reorganisation_energies an unordered_map that gives the reorganisation energy for dimers in your crystal.
	 */

	// First, initialise the unordered_map. 
	unordered_map<tuple<int,int>, long double, hash_tuple_DRE> dimer_reorganisation_energies;
	dimer_reorganisation_energies.reserve(dimer_reorganisation_energies_array_size);

	// Second, go through the array of Coupling_Value_Data_CObjects, take the data, and place it in the unordered_map. 
	for (int i = 0; i < dimer_reorganisation_energies_array_size; i++) {

		// 2.1: collect all the data from dimer_reorganisation_energies_array[i]
		int mol1 = (*dimer_reorganisation_energies_array)[i].mol1;
		int mol2 = (*dimer_reorganisation_energies_array)[i].mol2;
		long double reorganisation_energy = (*dimer_reorganisation_energies_array)[i].reorganisation_energy;

		// 2.2: Create the key for the unordered map, which is the dimer
		tuple <int,int> dimer_name = make_tuple(mol1, mol2);

		// 2.3: Store the coupling value in coupling_value_data for coupling_value_data_key
		dimer_reorganisation_energies[dimer_name] = reorganisation_energy;
	}

	// Third, return dimer_reorganisation_energies as an unordered unordered_map.
	return dimer_reorganisation_energies;
}

unordered_map<int, vector<tuple<int,int,int,int,long double>>> convert_to_ALN_dictionary(const Coupling_Value_Data_CObject** coupling_value_data_array, const int coupling_value_data_array_size) {
	/**
	 * This method is designed to convert the coupling_value_data array into an unordered_map to be used as a quick lookup table
	 * 
	 * @param coupling_value_data_array This dictionary contains all the coupling values information about the neighbourhoods that surrounded each molecule in your crystal.
	 * @param coupling_value_data_array_size This is the number of values in the coupling_value_data array.
	 * 
	 * @returns coupling_value_data an unordered_map that gives the coupling value between a molecule in the origin unit cell and another molecule displaced from the origin unit cell by (i,j,k) unit cell lengths
	 */

	// First, initialise the unordered_map. 
	unordered_map<int, vector<tuple<int,int,int,int,long double>>> coupling_value_data;
	coupling_value_data.reserve(coupling_value_data_array_size);

	// Second, go through the array of Coupling_Value_Data_CObjects, take the data, and place it in the unordered_map. 
	for (int i = 0; i < coupling_value_data_array_size; i++) {

		// 2.1: collect all the data from coupling_value_data_C[i]
		int mol1  = (*coupling_value_data_array)[i].mol1;
		int mol2  = (*coupling_value_data_array)[i].mol2;
		int uniti = (*coupling_value_data_array)[i].uniti;
		int unitj = (*coupling_value_data_array)[i].unitj;
		int unitk = (*coupling_value_data_array)[i].unitk;
		long double coupling_value = (*coupling_value_data_array)[i].coupling_value;

		// 2.2: Create the value for the unordered_map that contains all the coupling data. 
		tuple <int,int,int,int,long double> coupling_value_data_value = make_tuple(mol2, uniti, unitj, unitk, coupling_value);

		// 2.3: Store the coupling value in coupling_value_data for coupling_value_data_key
		coupling_value_data[mol1].push_back(coupling_value_data_value);
	}

	// return coupling_value_data as an unordered unordered_map.
	return coupling_value_data;
}

