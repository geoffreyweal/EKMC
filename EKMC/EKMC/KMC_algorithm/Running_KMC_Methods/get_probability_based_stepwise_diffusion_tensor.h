/**
 * get_stepwise_diffusion_tensor.h, 16/11/23, Geoffrey Weal
 * 
 * This algorithm is designed to obtain the stepwise diffusion tensor components from the rate constants and hopping displacement vectors. 
 */
#include <list>
#include <tuple>
#include <vector>
#include <unordered_map>
using namespace std;

tuple<long double,long double,long double,long double,long double,long double> get_probability_based_stepwise_diffusion_tensor(int current_molecule_name, int* current_cell_point, list<tuple<int,int,int,int>> *other_molecule_descriptions, list<long double> *rate_constants, vector<vector<long double>> *unit_cell_matrix, unordered_map<int, vector<long double>> *centre_of_molecules);

