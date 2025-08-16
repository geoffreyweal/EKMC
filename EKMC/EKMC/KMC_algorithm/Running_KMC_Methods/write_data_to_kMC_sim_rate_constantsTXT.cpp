/**
 * write_data_to_kMC_sim_rate_constantsTXT.cpp, 31/10/23, Geoffrey Weal
 * 
 * This algorithm is designed to write the information about a rate constants between the exciton donor that the exciton is current on to all the neighbouring exciton acceptors the exciton could jump to for each KMC step.
 * 
 * Information is written to the kMC_sim_probTXT file.
 */
#include <sstream>
#include <string>
#include <list>
#include <tuple>
#include "write_data_to_kMC_sim_rate_constantsTXT.h"
#include "Auxiliary_Methods/auxillary_methods.h"
using namespace std;

string write_data_to_kMC_sim_rate_constantsTXT(long counter, int current_molecule_name, int *current_cell_point, list<tuple<int,int,int,int>> *other_molecule_descriptions, list<long double> *rate_constants, long double sum_of_rate_constants) {
	/**
	 * This method is designed to write the information about the probability for an exciton to jump from the exciton donor to any of its neighbours during a KMC step.
	 * 
	 * Information is written to the kMC_sim_probTXT file.
	 * 
	 * @param counter This is the current number of KMC steps that have been performed by the KMC algorithm.
	 * @param current_molecule_name This is the name (as a int number) of the molecule the exciton is on.
	 * @param current_cell_point This is the unit cell the exciton lies in, relative to the initial origin starting point unit cell.
	 * @param other_molecule_descriptions These are all the details of the neighbouring molecules surrounding the exciton donor that the exciton is currently on.
	 * @param rate_constants These are all the rate constants for all the neighbouring molecules given in other_molecule_descriptions
	 * @param sum_of_rate_constants This is the sum of rate constants for the exciton to jump from current_molecule_name, current_cell_point to a neighbouring molecule. 
	 * 
	 * @return toString a string that can be written to the kMC.txt simulations storage file containing the information about the probabilities. 
	 */

	// First, check that other_molecule_descriptions and rate_constants are the same length (size).
	if (other_molecule_descriptions->size() != rate_constants->size()) {
		throw runtime_error(string("Error: other_molecule_descriptions and rate_constants are not the same size: other_molecule_descriptions.size() = ") + to_string(other_molecule_descriptions->size()) + string(", rate_constants.size() = ") + to_string(rate_constants->size()) + "\n");
	}

	// Second, print the details about the exciton donor that the exciton is current on.
	string toString = to_string(counter)+": "+to_string(current_molecule_name)+" ("+to_string(current_cell_point[0])+", "+to_string(current_cell_point[1])+", "+to_string(current_cell_point[2])+") ";

	// Third, add the sum_of_rate_constants to the information given.
	toString += "["+to_string_long_double(sum_of_rate_constants)+"] --> ";

	// Fourth, initialise all the components needed for printing probabilities data to file. 
    auto it1 = other_molecule_descriptions->begin();
    auto it1_end = other_molecule_descriptions->end();
    auto it2 = rate_constants->begin();
    int index = 0;
    int total_length = other_molecule_descriptions->size();
    tuple<int,int,int,int> other_molecule_description;

	// Fifth, print all the data about the probabilities for an exciton to move from the exciton donor to any of the neighbouring exciton acceptors. 
    while (it1 != it1_end) {

    	// 5.1: Get the details about neighbouring exciton acceptor.
    	other_molecule_description = (*it1); 
		toString += to_string(get<0>(other_molecule_description))+" ("+to_string(get<1>(other_molecule_description))+", "+to_string(get<2>(other_molecule_description))+", "+to_string(get<3>(other_molecule_description))+"): ";
		
		// 5.2: Get the rate constant for the corresponding neighbouring exciton acceptor.
		toString += to_string_long_double(*it2);

		// 5.3: Print separator 
		if (index < total_length - 1) {
			toString += "/ ";
		}

		// 5.4: Move on to next neighbouring exciton acceptor in the other_molecule_descriptions and rate_constants lists. 
		it1++; it2++; index++;

	}

	// Sixth, return the data from above into the kMC_simTXT file.
	return toString;
}

