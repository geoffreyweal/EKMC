/**
 * write_data_to_kMC_sim_rate_constantsTXT.cpp, 31/10/23, Geoffrey Weal
 * 
 * This algorithm is designed to write the information about a rate constants between the exciton donor that the exciton is current on to all the neighbouring exciton acceptors the exciton could jump to for each KMC step.
 * 
 * Information is written to the kMC_sim_probTXT file.
 */
#include <string>
#include <list>
using namespace std;

string write_data_to_kMC_sim_rate_constantsTXT(long counter, int current_molecule_name, int *current_cell_point, list<tuple<int,int,int,int>> *other_molecule_descriptions, list<long double> *rate_constants, long double sum_of_rate_constants); 