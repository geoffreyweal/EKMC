/**
 * get_V_with_disorder.h, Geoffrey Weal, 30/5/23
 * 
 * This algorithm is designed to obtain the coupling value of a dimer with disorder. 
 */
#include <vector>
using namespace std;

long double get_distance(vector<long double> *current_molecule_com, int* current_cell_point, vector<long double> *previous_molecule_com, int* previous_cell_point, vector<vector<long double>> *unit_cell_matrix);
