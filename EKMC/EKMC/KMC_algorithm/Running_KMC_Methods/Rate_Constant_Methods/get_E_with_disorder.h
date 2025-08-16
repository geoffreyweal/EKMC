/**
 * get_E_with_disorder.h, Geoffrey Weal, 30/5/23
 * 
 * This algorithm is designed to obtain the energy (bandgap) of a molecule with disorder, and store the result in an energetic disorder database (molecule_energetic_disorder_database).
 */
using namespace std;
#include "get_marcus_rate_constants_data.h"
#include "../../auxillary_file.h"
#include "../../databases.h"

long double get_E_with_disorder(int molecule_name, int* cell_point, Molecule_Energetic_Disorder_Database* molecule_energetic_disorder_database, 
    unordered_map<int, long double>* molecule_bandgap_energies, long double energetic_disorder_value, bool energetic_disorder_is_percent);