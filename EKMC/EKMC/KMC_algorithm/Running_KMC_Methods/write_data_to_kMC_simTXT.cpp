/**
 * write_data_to_kMC_simTXT.cpp, 29/5/23, Geoffrey Weal
 * 
 * This algorithm is designed to write the information about a KMC step into the kMC_simTXT file. 
 */
#include <string>
#include "write_data_to_kMC_simTXT.h"
#include "Auxiliary_Methods/auxillary_methods.h"
using namespace std;

string write_data_to_kMC_simTXT(string counter, string current_molecule_name, string current_cell_point, string current_time, string current_time_step, string hop_distance, string current_molecule_description_energy, string sum_of_rate_constants, string D_xx, string D_yy, string D_zz, string D_xy, string D_xz, string D_yz) {
	/**
	 * This method is designed to write the information about a KMC step into the kMC_simTXT file. 
	 * 
	 * Information is written to the kMC_simTXT file.
	 * 
	 * @param counter This is the current number of KMC steps that have been performed by the KMC algorithm.
	 * @param current_molecule_name This is the name (as a int number) of the molecule the exciton is on.
	 * @param current_cell_point This is the unit cell the exciton lies in, relative to the initial origin starting point unit cell.
	 * @param current_time This is the curent simulation time of the KMC simulation.
	 * @param current_time_step This is the amount of time that the exciton was on molecule current_molecule_name in unit cell current_cell_point.
	 * @param current_molecule_description_energy This is the energy of the molcule the exciton is on.
	 * @param sum_of_rate_constants This is the sum of rate constants for the exciton to jump from current_molecule_name, current_cell_point to a neighbouring molecule. 
	 * 
	 * @return toString a string that can be written to the kMC.txt simulations storage file.
	 */

	// First, obtain all the information to save to the kMC_simTXT file. 
	string counter_placement = placement_counter(counter, 10);
	string current_molecule_name_placement = placement_counter(current_molecule_name, 10);
	string current_cell_point_placement = placement_counter(current_cell_point, 25);
	string current_time_placement = placement_counter(current_time, 30+2, 30);
	string current_time_step_placement = placement_counter(current_time_step, 30+2, 30);
	string hop_distance_placement = placement_counter(hop_distance, 30+2, 30);
	string current_molecule_description_energy_placement = placement_counter(current_molecule_description_energy, 30+2, 30);
	string sum_of_rate_constants_placement = placement_counter(sum_of_rate_constants, 30+2, 30);

	string D_xx_placement = placement_counter(D_xx, 30+2, 30);
	string D_yy_placement = placement_counter(D_yy, 30+2, 30);
	string D_zz_placement = placement_counter(D_zz, 30+2, 30);
	string D_xy_placement = placement_counter(D_xy, 30+2, 30);
	string D_xz_placement = placement_counter(D_xz, 30+2, 30);
	string D_yz_placement = placement_counter(D_yz, 30+2, 30);

	// Second, return the data from above into the kMC_simTXT file.
	return counter_placement+" "+current_molecule_name_placement+" "+current_cell_point_placement+" "+current_time_placement+" "+current_time_step_placement+" "+hop_distance_placement+" "+current_molecule_description_energy_placement+" "+sum_of_rate_constants_placement+" | "+D_xx_placement+" "+D_yy_placement+" "+D_zz_placement+" "+D_xy_placement+" "+D_xz_placement+" "+D_yz_placement+" |";

}

string write_data_to_kMC_simTXT(long counter, int current_molecule_name, int *current_cell_point, long double current_time, long double current_time_step, long double hop_distance, long double current_molecule_description_energy, long double sum_of_rate_constants, long double D_xx, long double D_yy, long double D_zz, long double D_xy, long double D_xz, long double D_yz) {
	/**
	 * This method is designed to write the information about a KMC step into the kMC_simTXT file. 
	 * 
	 * Information is written to the kMC_simTXT file.
	 * 
	 * @param counter This is the current number of KMC steps that have been performed by the KMC algorithm.
	 * @param current_molecule_name This is the name (as a int number) of the molecule the exciton is on.
	 * @param current_cell_point This is the unit cell the exciton lies in, relative to the initial origin starting point unit cell.
	 * @param current_time This is the curent simulation time of the KMC simulation.
	 * @param current_time_step This is the amount of time that the exciton was on molecule current_molecule_name in unit cell current_cell_point.
	 * @param current_molecule_description_energy This is the energy of the molcule the exciton is on.
	 * @param sum_of_rate_constants This is the sum of rate constants for the exciton to jump from current_molecule_name, current_cell_point to a neighbouring molecule. 
	 * 
	 * @return toString a string that can be written to the kMC.txt simulations storage file.
	 */

	// First, obtain all the information to save to the kMC_simTXT file. 
	string counter_placement = placement_counter(to_string(counter), 10);
	string current_molecule_name_placement = placement_counter(to_string(current_molecule_name), 10);
	string current_cell_point_placement = placement_counter("("+to_string(current_cell_point[0])+","+to_string(current_cell_point[1])+","+to_string(current_cell_point[2])+")", 25);
	string current_time_placement = placement_counter(to_string_long_double(current_time), 30+2, 30);
	string current_time_step_placement = placement_counter(to_string_long_double(current_time_step), 30+2, 30);
	string hop_distance_placement = placement_counter(to_string_long_double(hop_distance), 30+2, 30);
	string current_molecule_description_energy_placement = placement_counter((current_molecule_description_energy > 0.0) ? "+"+to_string_long_double(current_molecule_description_energy) : to_string_long_double(current_molecule_description_energy), 30+2, 30);
	string sum_of_rate_constants_placement = placement_counter(to_string_long_double(sum_of_rate_constants), 30+2, 30);

	string D_xx_placement = placement_counter(to_string_long_double(D_xx), 30+2, 30);
	string D_yy_placement = placement_counter(to_string_long_double(D_yy), 30+2, 30);
	string D_zz_placement = placement_counter(to_string_long_double(D_zz), 30+2, 30);
	string D_xy_placement = placement_counter(to_string_long_double(D_xy), 30+2, 30);
	string D_xz_placement = placement_counter(to_string_long_double(D_xz), 30+2, 30);
	string D_yz_placement = placement_counter(to_string_long_double(D_yz), 30+2, 30);

	// Second, return the data from above into the kMC_simTXT file.
	return counter_placement+" "+current_molecule_name_placement+" "+current_cell_point_placement+" "+current_time_placement+" "+current_time_step_placement+" "+hop_distance_placement+" "+current_molecule_description_energy_placement+" "+sum_of_rate_constants_placement+" | "+D_xx_placement+" "+D_yy_placement+" "+D_zz_placement+" "+D_xy_placement+" "+D_xz_placement+" "+D_yz_placement+" |";
}








