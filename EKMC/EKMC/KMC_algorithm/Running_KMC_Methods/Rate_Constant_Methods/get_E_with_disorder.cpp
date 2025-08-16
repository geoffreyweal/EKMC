/**
 * get_E_with_disorder.cpp, Geoffrey Weal, 30/5/23
 * 
 * This algorithm is designed to obtain the energy (bandgap) of a molecule with disorder, and store the result in an energetic disorder database (molecule_energetic_disorder_database).
 */
#include <iostream>
#include <random>
using namespace std;
#include "get_E_with_disorder.h"
#include "../../databases.h"

// Create a random number generator
random_device rd_energy_disorder;
mt19937 generator_ed(rd_energy_disorder());

long double get_E_with_disorder(int molecule_name, int* cell_point, Molecule_Energetic_Disorder_Database* molecule_energetic_disorder_database, 
	unordered_map<int, long double>* molecule_bandgap_energies, long double energetic_disorder_value, bool energetic_disorder_is_percent) {
	/**
	 * This method is designed to obtain the energy (bandgap) of a molecule with disorder, and store the result in an energetic disorder database (molecule_energetic_disorder_database).
	 * 
	 * @param molecule_name This is the molecule of interest.
	 * @param cell_point This is the unit cell that the molecule of interest is in. 
	 * @param molecule_energetic_disorder_database This map holds all the energies (bandgap) for each molecule sampled in a KMC simulation. 
	 * @param molecule_bandgap_energies This contains all the bandgap energies for each molecule in the crystal.
	 * @param energetic_disorder_value This is the energetic (bandgap) disorder value, either given as a standard deviation (in eV), or as a percentage of a energy (bandgap) for a molecule. 
	 * @param energetic_disorder_is_percent If True, energetic_disorder_value is a percentage. If False, energetic_disorder_value is a standard deviation (in eV).
	 * 
	 * @returns The energy (bandgap) of the molecule of interest with disorder included (in eV). 
	 */

	// First, obtain the search key (molecule_name, unit cell disp i, unit cell disp j, unit cell disp k) that will have an energy (with disorder) ssigned to it.
	tuple <int,int,int,int> E_search_key = {molecule_name, cell_point[0], cell_point[1], cell_point[2]};

	// Second, determine if you already have this entry in molecule_energetic_disorder_database, if not get it.
	long double molecule_bandgap_energy_with_disorder;
	if (! molecule_energetic_disorder_database->contains(E_search_key)) {

		// 2.1: Obtain the bandgap energy for molecule_name 
		long double bandgap_energy = (*molecule_bandgap_energies)[molecule_name];

		// 2.2: Get the coupling disorder standard deviation.
		long double energetic_disorder_sd;
		if (energetic_disorder_is_percent) {
			energetic_disorder_sd = abs(bandgap_energy * (energetic_disorder_value/100.0));
		} else {
			energetic_disorder_sd = energetic_disorder_value;
		}

		// 2.3: Obtain the molecule's bandgap energy with associated disorder. 
		normal_distribution<long double> bandgap_distribution(bandgap_energy, energetic_disorder_sd);
		molecule_bandgap_energy_with_disorder = bandgap_distribution(generator_ed);

		// 2.4: Add band_gap_with_disorder to molecule_energetic_disorder_database with key E_search_key
		molecule_energetic_disorder_database->add(E_search_key, molecule_bandgap_energy_with_disorder);

	} else {
		
		// 2.5: Get the molecule_bandgap_energy_with_disorder from molecule_energetic_disorder_database
		molecule_bandgap_energy_with_disorder = molecule_energetic_disorder_database->get(E_search_key);
	}

	// Third, return molecule_bandgap_energy_with_disorder
	return molecule_bandgap_energy_with_disorder;
}

