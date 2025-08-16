/**
 * get_distance.cpp, Geoffrey Weal, 30/10/23
 * 
 * This algorithm is designed to obtain the hopping distance for an exciton moving from the centre-of-mass of the exciton donor to centre-of-mass of the acceptor donor.
 */
#include <cmath>
#include <vector>
#include <iostream>
using namespace std;

long double get_distance(vector<long double> *current_molecule_com, int* current_cell_point, vector<long double> *previous_molecule_com, int* previous_cell_point, vector<vector<long double>> *unit_cell_matrix) {
	/**
	 * This method is designed to obtain the hopping distance for an exciton moving from the centre-of-mass of the exciton donor to centre-of-mass of the acceptor donor.
	 * 
	 * @param current_molecule_com This is the centre of mass for the current molecule (A).
	 * @param current_cell_point This is the lattice cell position the current molecule is in.
	 * @param previous_molecule_com This is the centre of mass for the previous molecule (A).
	 * @param previous_cell_point This is the lattice cell position the previous molecule is in.
	 * @param unit_cell_matrix This is the lattice matrix of the unit cell for this crystal.
	 * 
	 * @returns The hopping distance for an exciton moving from the centre-of-mass of the exciton donor to centre-of-mass of the acceptor donor (A).
	 */

	// First, detemine the distance between the two cells that the previous and current molecules are in
	long double cell_x_point_diff = current_cell_point[0] - previous_cell_point[0];
	long double cell_y_point_diff = current_cell_point[1] - previous_cell_point[1];
	long double cell_z_point_diff = current_cell_point[2] - previous_cell_point[2];

	// Second, get the displacements of the excitons hop in the x, y, and z directions.
	//std::cout << unit_cell_matrix[0][0] << " " << unit_cell_matrix[0][1] << " "<< unit_cell_matrix[0][2] << " " << std::endl;
	//std::cout << unit_cell_matrix[1][0] << " " << unit_cell_matrix[1][1] << " "<< unit_cell_matrix[1][2] << " " << std::endl;
	//std::cout << unit_cell_matrix[2][0] << " " << unit_cell_matrix[2][1] << " "<< unit_cell_matrix[2][2] << " " << std::endl;
	long double hop_x_displacement = ((*current_molecule_com)[0] - (*previous_molecule_com)[0]) + (*unit_cell_matrix)[0][0]*cell_x_point_diff + (*unit_cell_matrix)[0][1]*cell_y_point_diff + (*unit_cell_matrix)[0][2]*cell_z_point_diff;
	long double hop_y_displacement = ((*current_molecule_com)[1] - (*previous_molecule_com)[1]) + (*unit_cell_matrix)[1][0]*cell_x_point_diff + (*unit_cell_matrix)[1][1]*cell_y_point_diff + (*unit_cell_matrix)[1][2]*cell_z_point_diff;
	long double hop_z_displacement = ((*current_molecule_com)[2] - (*previous_molecule_com)[2]) + (*unit_cell_matrix)[2][0]*cell_x_point_diff + (*unit_cell_matrix)[2][1]*cell_y_point_diff + (*unit_cell_matrix)[2][2]*cell_z_point_diff;

	// Third, get the hop_distance by doing Pythagoras on hop_x_displacement, hop_y_displacement, and hop_z_displacement.
	long double hop_distance = sqrt(pow(hop_x_displacement, 2) + pow(hop_y_displacement, 2) + pow(hop_z_displacement, 2));

	// Fourth, return hop_distance
	return hop_distance;
}

