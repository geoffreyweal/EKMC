/**
 * write_data_to_kMC_simTXT.h, 29/5/23, Geoffrey Weal
 * 
 * This algorithm is designed to write the information about a KMC step into the kMC_simTXT file. 
 */
#include <string>
using namespace std;

string placement_counter(string input_toString, int total_no_of_charaters, int input_toString_max_length);
string write_data_to_kMC_simTXT(string counter, string current_molecule_name, string current_cell_point, string current_time, string current_time_step, string hop_distance, string current_molecule_description_energy, string sum_of_rate_constants, string D_xx, string D_yy, string D_zz, string D_xy, string D_xz, string D_yz);
string write_data_to_kMC_simTXT(long counter, int current_molecule_name, int *current_cell_point, long double current_time, long double current_time_step, long double hop_distance, long double current_molecule_description_energy, long double sum_of_rate_constants, long double D_xx, long double D_yy, long double D_zz, long double D_xy, long double D_xz, long double D_yz);

