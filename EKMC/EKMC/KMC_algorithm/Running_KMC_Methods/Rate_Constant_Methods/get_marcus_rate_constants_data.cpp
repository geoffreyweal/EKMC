/**
 * get_marcus_rate_constants_data.cpp, Geoffrey Weal, 30/5/23
 * 
 * This algorithm is designed to obtain the exciton hopping rate constants between molecule in a crystal in accordance to Marcus Theory. 
 */
#include <iostream>
#include <list>
#include <vector>
#include <cstdlib>
#include <cmath>
#include <unordered_map>
using namespace std;
#include "get_E_with_disorder.h"
#include "get_V_with_disorder.h"
#include "get_marcus_rate_constants_data.h"

tuple<long double, list<tuple<int,int,int,int>>, list<long double>> get_marcus_rate_constants_data(int current_molecule_name, int* current_cell_point, 
	long double M_constant, long double X_constant, long double energetic_disorder_value, bool energetic_disorder_is_percent, 
	long double coupling_disorder_value, bool coupling_disorder_is_percent, unordered_map<int, long double>* molecule_bandgap_energies, 
	unordered_map<tuple<int,int>, long double, hash_tuple_DRE>* dimer_reorganisation_energies,
	unordered_map<int, vector<tuple<int,int,int,int,long double>>>* coupling_value_data,
	Molecule_Energetic_Disorder_Database* molecule_energetic_disorder_database, Rate_Constant_Database* rate_constant_database) {
	/**
	 * This algorithm is designed to obtain the exciton hopping rate constants between molecule in a crystal in accordance to Marcus Theory. 
	 * 
	 * @param current_molecule_name This is the molecule that the exciton is currently on.
	 * @param current_cell_point This is the cell that the exciton is currently in.
	 * @param M_constant This is the M constant in the Marcus Theory Rate law. This is a constant for every dimer in this crystal.
	 * @param X_constant This is the X constant in the Marcus Theory Rate law. This is a constant for every dimer in this crystal.
	 * @param energetic_disorder_value This is the energetic (bandgap) disorder value, either given as a standard deviation (in eV), or as a percentage of a energy (bandgap) for a molecule. 
	 * @param energetic_disorder_is_percent If True, energetic_disorder_value is a percentage. If False, energetic_disorder_value is a standard deviation (in eV).
	 * @param coupling_disorder_value This is the coupling disorder value, either given as a standard deviation (in eV), or as a percentage of a coupling value for a dimer. 
	 * @param coupling_disorder_is_percent If True, coupling_disorder_value is a percentage. If False, coupling_disorder_value is a standard deviation (in eV).
	 * @param molecule_bandgap_energies This contains all the bandgap energies for each molecule in the crystal.
	 * @param dimer_reorganisation_energies This contains all the reorganisation energies for each dimer in the crystal. 
	 * @param coupling_value_data This unordered_map contains all the information about the neighbourhoods that surrounded each molecule in your crystal, including coupling values for each dimer pair.
	 * @param molecule_energetic_disorder_database This map holds all the energies (bandgap) for each molecule sampled in a KMC simulation. 
	 * @param rate_constant_database This map holds all the rate constants for each dimer sampled in a KMC simulation. 
	 * 
	 * @returns current_molecule_donor_E_with_disorder: The energy of the current molecule the exciton is on, including disorder (in eV); neighbouring_molecule_descriptions: The molecules and the absolute unit cell positions of neighbour molecules that are coupled to the current molecule; rate_constants: The exciton hopping rate constants for an exciton hopping from the current molecule to the neighbouring molecules about it that it is coupled to.
	 */

	// First, initalise the list and dictionaries to record data into
	list<tuple<int,int,int,int>> neighbouring_molecule_descriptions;
	list<long double> rate_constants;

	// Second, get the energy for this molecule that has had disorder applied to it.
	long double current_molecule_donor_E_with_disorder = get_E_with_disorder(current_molecule_name, current_cell_point, molecule_energetic_disorder_database, molecule_bandgap_energies, energetic_disorder_value, energetic_disorder_is_percent);

	// Third, obtain the relative local neighbourhood for the current molecule
	vector<tuple<int,int,int,int,long double>>* local_coupling_value_data = &(*coupling_value_data)[current_molecule_name];

	// Fourth, obtain all the rate constants and data for an exciton moving from the current molecule to another molecule that maybe in another unit cell.
	for (const auto& local_neighbourhood : (*local_coupling_value_data)){

		// 4.1: Obtain the neighbouring molecule name.
		int neighbouring_molecule_name = get<0>(local_neighbourhood);

		// 4.2: Obtain the absolute position of the potential acceptor molecule by 
		//      adding the absolute position of the donor molecule to the relative 
		//      unit cell displacement of molecule 2 to molecule 1.
		int neighbouring_cell_point[3] = {get<1>(local_neighbourhood), get<2>(local_neighbourhood), get<3>(local_neighbourhood)};
		for (int index = 0; index < 3; index++) {
			neighbouring_cell_point[index] = neighbouring_cell_point[index] + current_cell_point[index];
		}

		// 4.3: Obtain the rate constant search key for looking through the rate_constant_database.
		tuple<int,int,int,int, int,int,int,int> R_search_key = make_tuple(current_molecule_name, current_cell_point[0], current_cell_point[1], current_cell_point[2], neighbouring_molecule_name, neighbouring_cell_point[0], neighbouring_cell_point[1], neighbouring_cell_point[2]);

		// 4.4: obtain the rate constant for this dimer in the crystal.
		long double k_12;
		if (! rate_constant_database->contains(R_search_key)) {

			// 4.4.1: Obtain the energy for the neighbouring (acceptor) molecule that has had disorder applied to it.
			long double neighbouring_molecule_acceptor_E_with_disorder = get_E_with_disorder(neighbouring_molecule_name, neighbouring_cell_point, molecule_energetic_disorder_database, molecule_bandgap_energies, energetic_disorder_value, energetic_disorder_is_percent);

			// 4.4.2: Obtain the deltaE for this exciton hop with included disorders.
			long double deltaE_with_disorders = neighbouring_molecule_acceptor_E_with_disorder - current_molecule_donor_E_with_disorder;

			// 4.4.3: Obtain the coupling between current_molecule_name and neighbouring_molecule_name at relative unit cell displacement neighbouring_cell_point
			long double coupling_value = get<4>(local_neighbourhood);

			// 4.4.4: Obtain the randomly generated number to describe the energetic and coupling disorders, based on a normal distribution. 
			long double V_with_disorder = get_V_with_disorder(coupling_value, coupling_disorder_value, coupling_disorder_is_percent);

			// 4.4.5: Obtain the reorganisation energy for the exciton moving from current molecule (in the excited geometry structure) to the neighbouring molecule (in the ground geometry structure).
			long double reorganisation_energy = (*dimer_reorganisation_energies)[make_tuple(current_molecule_name,neighbouring_molecule_name)];

			// 4.4.6: Obtain the rate constant for the exciton to move from the current molecule to another molecule that maybe in another unit cell.
			long double prefix_value = pow(abs(V_with_disorder),2.0) / pow(reorganisation_energy,0.5);
			long double exp_value = pow(deltaE_with_disorders + reorganisation_energy,2.0) / reorganisation_energy;
			k_12 = prefix_value * M_constant * exp( -X_constant * exp_value );

			// 4.4.7: Add k_12 to rate_constant_database with key R_search_key
			rate_constant_database->add(R_search_key, k_12);

		} else {

			// 4.4.8: Get the k_12 from rate_constant_database for R_search_key key.
			k_12 = rate_constant_database->get(R_search_key);
		}

		// 4.5: Add the rate constant data to the storage list and dictionaries. 
		neighbouring_molecule_descriptions.push_back(make_tuple(neighbouring_molecule_name, neighbouring_cell_point[0], neighbouring_cell_point[1], neighbouring_cell_point[2]));
		rate_constants.push_back(k_12);

	}

    // Fifth, return current_molecule_donor_E_with_disorder, neighbouring_molecule_descriptions, and rate_constants.
	return make_tuple(current_molecule_donor_E_with_disorder, neighbouring_molecule_descriptions, rate_constants);

}
