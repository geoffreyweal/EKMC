/**
 * get_stepwise_diffusion_tensor.cpp, 16/11/23, Geoffrey Weal
 * 
 * This algorithm is designed to obtain the stepwise diffusion tensor components from the rate constants and hopping displacement vectors. 
 */
#include <cmath>
#include <list>
#include <tuple>
#include <vector>
#include <unordered_map>
#include <stdexcept>
using namespace std;

tuple<long double,long double,long double,long double,long double,long double> get_probability_based_stepwise_diffusion_tensor(int current_molecule_name, int* current_cell_point, list<tuple<int,int,int,int>> *other_molecule_descriptions, list<long double> *rate_constants, vector<vector<long double>> *unit_cell_matrix, unordered_map<int, vector<long double>> *centre_of_molecules) {
	/**
	 * This algorithm is designed to obtain the stepwise diffusion tensor components from the rate constants and hopping displacement vectors. 
	 * 
	 * @param current_molecule_name This is the name of the molecule.
	 * @param current_cell_point This is the relative unit cell that the molecule can be found in.
	 * @param other_molecule_descriptions This is the descriptions of the molecules neighbouring (current_molecule_name, current_cell_point).
	 * @param rate_constants These are the rate constants between (current_molecule_name, current_cell_point) and the nrighbouring molecules in other_molecule_descriptions.
	 */

	// First, initiate all the components of the diffusion tensor.
	long double D_xx = 0.0; long double D_yy = 0.0; long double D_zz = 0.0; long double D_xy = 0.0; long double D_xz = 0.0; long double D_yz = 0.0;

	// Second, obtain the centre of mass/molecule for the molecule the exciton is currently on. 
	vector<long double> centre_of_current_molecule = (*centre_of_molecules)[current_molecule_name];

	// Third, initise the name and unit cell components that will be used to hold each of the neighbouring molecules details (neighbouring the molecule the exciton is currently on).
	int neighbouring_molecule_name; int neighbouring_unit_cell_i; int neighbouring_unit_cell_j; int neighbouring_unit_cell_k; long double rate_constant; 

	// Fourth, check that other_molecule_descriptions and rate_constants are the same size/length.
	if (other_molecule_descriptions->size() != rate_constants->size()) {
		throw std::invalid_argument("Error in def get_probability_based_stepwise_diffusion_tensor: other_molecule_descriptions is not the same size as rate_constants. other_molecule_descriptions->size() = "+to_string(other_molecule_descriptions->size())+"; rate_constants->size()"+to_string(rate_constants->size()));
	}

	// Fifth, initialise the pointer to the start of each of the neighbouring molecules lists (other_molecule_descriptions and rate_constants).
	auto other_molecule_descriptions_front = other_molecule_descriptions->begin();
	auto rate_constants_front = rate_constants->begin();

	// Sixth, obtain the components of the probability-based stepwise diffusion tensor. 
	for (int index = 0; index < other_molecule_descriptions->size(); index++) {

		// 6.1: Obtain the neighbouring molecule name and unit cell details.
		tie(neighbouring_molecule_name, neighbouring_unit_cell_i, neighbouring_unit_cell_j, neighbouring_unit_cell_k) = *other_molecule_descriptions_front;

		// 6.2: Obtain the rate constant for the exciton hop from the current molecule to this neighbouring molecule. 
		rate_constant = *rate_constants_front;

		// 6.3: Get the centre of mass/molecule for this neighbouring molecule. 
		vector<long double> centre_of_neighbouring_molecule = (*centre_of_molecules)[neighbouring_molecule_name];

		// 6.4: Detemine the distance between the two cells that the previous and current molecules are in
		long double cell_x_point_diff = neighbouring_unit_cell_i - current_cell_point[0];
		long double cell_y_point_diff = neighbouring_unit_cell_j - current_cell_point[1];
		long double cell_z_point_diff = neighbouring_unit_cell_k - current_cell_point[2];

		// 6.5: Get the displacements of the excitons hop in the x, y, and z directions.
		//std::cout << unit_cell_matrix[0][0] << " " << unit_cell_matrix[0][1] << " "<< unit_cell_matrix[0][2] << " " << std::endl;
		//std::cout << unit_cell_matrix[1][0] << " " << unit_cell_matrix[1][1] << " "<< unit_cell_matrix[1][2] << " " << std::endl;
		//std::cout << unit_cell_matrix[2][0] << " " << unit_cell_matrix[2][1] << " "<< unit_cell_matrix[2][2] << " " << std::endl;
		long double hop_x_displacement = (centre_of_neighbouring_molecule[0] - centre_of_current_molecule[0]) + (*unit_cell_matrix)[0][0]*cell_x_point_diff + (*unit_cell_matrix)[0][1]*cell_y_point_diff + (*unit_cell_matrix)[0][2]*cell_z_point_diff;
		long double hop_y_displacement = (centre_of_neighbouring_molecule[1] - centre_of_current_molecule[1]) + (*unit_cell_matrix)[1][0]*cell_x_point_diff + (*unit_cell_matrix)[1][1]*cell_y_point_diff + (*unit_cell_matrix)[1][2]*cell_z_point_diff;
		long double hop_z_displacement = (centre_of_neighbouring_molecule[2] - centre_of_current_molecule[2]) + (*unit_cell_matrix)[2][0]*cell_x_point_diff + (*unit_cell_matrix)[2][1]*cell_y_point_diff + (*unit_cell_matrix)[2][2]*cell_z_point_diff;

		// 6.6: Add the probability-based stepwise diffusion tensor components that are contributed from this exciton hopping step to the overall probability-based stepwise diffusion tensor. 
		D_xx += rate_constant * hop_x_displacement * hop_x_displacement;
		D_yy += rate_constant * hop_y_displacement * hop_y_displacement;
		D_zz += rate_constant * hop_z_displacement * hop_z_displacement;
		D_xy += rate_constant * hop_x_displacement * hop_y_displacement;
		D_xz += rate_constant * hop_x_displacement * hop_z_displacement;
		D_yz += rate_constant * hop_y_displacement * hop_z_displacement;

		// 6.7: Increment the pointer for the list to the next variable in the lists. 
		if (index + 1 < other_molecule_descriptions->size()) {
			std::advance(other_molecule_descriptions_front, 1);
			std::advance(rate_constants_front, 1);
		}
	}

	// Seventh, obtain the constant to multiply each component in the overall probability-based stepwise diffusion tensor. 
	//          1/2 for the diffusion tensor, and pow(10.0,-16.0) to convert A^2 to cm^2.
	long double diffusion_tensor_constant = (1.0/2.0) * pow(10.0,-16.0);

	// Eighth, multiply diffusion_tensor_constant to each component in the overall probability-based stepwise diffusion tensor. 
	D_xx *= diffusion_tensor_constant;
	D_yy *= diffusion_tensor_constant;
	D_zz *= diffusion_tensor_constant;
	D_xy *= diffusion_tensor_constant;
	D_xz *= diffusion_tensor_constant;
	D_yz *= diffusion_tensor_constant;
	
	// Ninth, return overall probability-based stepwise diffusion tensor. 
	return make_tuple(D_xx, D_yy, D_zz, D_xy, D_xz, D_yz);

}