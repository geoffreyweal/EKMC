#include <tuple>
#include <iostream>
using namespace std;
#include "databases.h"

// ====================================================================================================

void Molecule_Energetic_Disorder_Database::add(tuple<int,int,int,int> E_search_key, long double molecule_energy_with_disorder) {
	/**
	 * This method is will add a disordered site energy for a molecule in a certain unit cell in the crystal. 
	 * 
	 * @param E_search_key This key describes the (molecule, unit i, unit j, unit k) position of the molecule in the crystal.
	 * @param molecule_energy_with_disorder This is the disordered site energy for this molecule in the (i,j,k) unit cell.
	 */
	/**
	cout << "E_search_key: (" << std::get<0>(E_search_key) << ", "
		 << std::get<1>(E_search_key) << ", "
		 << std::get<2>(E_search_key) << ", "
		 << std::get<3>(E_search_key) << ")  molecule_energy_with_disorder: "
		 << molecule_energy_with_disorder << std::endl;
	*/
	molecule_energetic_disorder_database.insert(make_pair(E_search_key, molecule_energy_with_disorder));
}

long double Molecule_Energetic_Disorder_Database::get(tuple <int,int,int,int> E_search_key) {
	/**
	 * This method is will return the disordered site energy for a molecule in a certain unit cell in the crystal. 
	 * 
	 * @param E_search_key This key describes the (molecule, unit i, unit j, unit k) position of the molecule in the crystal.
	 * 
	 * @returns the disordered site energy for a molecule in a certain unit cell in the crystal, given by E_search_key
	 */
	return molecule_energetic_disorder_database[E_search_key];
}

bool Molecule_Energetic_Disorder_Database::contains(tuple <int,int,int,int> E_search_key) {
	/**
	 * This method is will return if the disordered site energy for molecule in a certain unit cell has been recorded in the Molecule_Energetic_Disorder_Database database
	 * 
	 * @param E_search_key This key describes the (molecule, unit i, unit j, unit k) position of the molecule in the crystal.
	 * 
	 * @returns the disordered site energy for a molecule in a certain unit cell in the crystal, given by E_search_key
	 */
	return molecule_energetic_disorder_database.count(E_search_key);
}

int Molecule_Energetic_Disorder_Database::size() {
	/**
	 * This method will return the size of the Molecule_Energetic_Disorder_Database database
	 * 
	 * @returns The size (the number of inputs) of the Molecule_Energetic_Disorder_Database database
	 */
	return molecule_energetic_disorder_database.size();
}

void Molecule_Energetic_Disorder_Database::print() {
	/**
	 * This method will print the data in the Molecule_Energetic_Disorder_Database database
	 */
	cout << "data in molecule_energetic_disorder_database marcus: " << std::endl;
	// Print all keys and values
	for (const auto& pair : molecule_energetic_disorder_database) {
		const auto& key = pair.first;
		const auto& value = pair.second;

		std::cout << "E_search_key: (" << std::get<0>(key) << ", " << std::get<1>(key) << ", " << std::get<2>(key) << ", " << std::get<3>(key) << "); ";
		std::cout << " molecule_energetic_disorder_database: " << value << std::endl;
	}
}

// ====================================================================================================

void Rate_Constant_Database::add(tuple <int,int,int,int, int,int,int,int> R_search_key, long double dimer_rate_constant) {
	/**
	 * This method is will add the rate constant data between molecule 1 and molecule 2.
	 * 
	 * @param R_search_key This key describes the dimer between molecule 1 in its unit cell (first four ints) and molecule 2 in its unit cell (last four ints).
	 * @param dimer_rate_constant This is the rate constant for this dimer.
	 */
	rate_constant_database.insert(make_pair(R_search_key, dimer_rate_constant));
}

long double Rate_Constant_Database::get(tuple <int,int,int,int, int,int,int,int> R_search_key) {
	/**
	 * This method is will return the rate constant between molecule 1 in its unit cell (first four ints) and molecule 2 in its unit cell (last four ints).
	 * 
	 * @param R_search_key This key describes the dimer between molecule 1 in its unit cell (first four ints) and molecule 2 in its unit cell (last four ints).
	 * 
	 * @returns the rate constant for this dimer.
	 */
	return rate_constant_database[R_search_key];
}

bool Rate_Constant_Database::contains(tuple <int,int,int,int, int,int,int,int> R_search_key) {
	/**
	 * This method is will return if the rate constant data for the dimer described by R_search_key has been recorded in the Molecule_Energetic_Disorder_Database database
	 * 
	 * @param R_search_key This key describes the dimer between molecule 1 in its unit cell (first four ints) and molecule 2 in its unit cell (last four ints).
	 * 
	 * @returns if the rate constant data for this dimer exists in the Molecule_Energetic_Disorder_Database database
	 */
	return rate_constant_database.count(R_search_key);
}

int Rate_Constant_Database::size() {
	/**
	 * This method will return the size of the Rate_Constant_Database database
	 * 
	 * @returns The size (the number of inputs) of the Rate_Constant_Database database
	 */
	return rate_constant_database.size();
}

void Rate_Constant_Database::print() {
	/**
	 * This method will print the data in the Rate_Constant_Database database
	 */
	cout << "data in rate_constant_database marcus: " << std::endl;
	// Print all keys and values
	for (const auto& pair : rate_constant_database) {
		const auto& key = pair.first;
		const auto& value = pair.second;

		std::cout << "R_search_key: (" << std::get<0>(key) << ", " << std::get<1>(key) << ", " << std::get<2>(key) << ", " << std::get<3>(key) << ") (" <<std::get<4>(key) << ", " << std::get<5>(key) << ", " << std::get<6>(key) << ", " << std::get<7>(key) << "); ";
		std::cout << "rate_constant_database: " << value << std::endl;
	}
}

// ====================================================================================================

