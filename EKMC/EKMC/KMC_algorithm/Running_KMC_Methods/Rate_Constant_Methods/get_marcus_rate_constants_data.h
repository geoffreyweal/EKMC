/**
 * get_marcus_rate_constants_data.cpp, Geoffrey Weal, 30/5/23
 * 
 * This algorithm is designed to obtain the exciton hopping rate constants between molecule in a crystal in accordance to Marcus Theory. 
 */
#include <list>
#include <vector>
#include <unordered_map>
using namespace std;
#include "../../databases.h"
#include "../../Initialisation_Methods/convert_arrays_to_unordered_maps.h"

tuple<long double, list<tuple<int,int,int,int>>, list<long double>> get_marcus_rate_constants_data(int current_molecule_name, int* current_cell_point, 
    long double M_constant, long double X_constant, long double energetic_disorder_value, bool energetic_disorder_is_percent, 
    long double coupling_disorder_value, bool coupling_disorder_is_percent, unordered_map<int, long double>* molecule_bandgap_energies, 
    unordered_map<tuple<int,int>, long double, hash_tuple_DRE>* dimer_reorganisation_energies,
    unordered_map<int, vector<tuple<int,int,int,int,long double>>>* coupling_value_data,
    Molecule_Energetic_Disorder_Database* molecule_energetic_disorder_database, Rate_Constant_Database* rate_constant_database);