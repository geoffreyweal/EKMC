/**
 * KMC_algorithm.cpp, Geoffrey Weal, 29/5/23
 * 
 * This program is designed to run an exciton KMC simulation for an exciton in a crystal. 
 */
#include <iostream>
#include <filesystem>
#include <cstring>
#include <fstream>
#include <random>
#include <list>
#include <tuple>
#include <vector>
#include <stdexcept>
#include <unordered_map>
using namespace std;
#include "databases.h"
#include "Initialisation_Methods/convert_arrays_to_unordered_maps.h"
#include "Running_KMC_Methods/write_data_to_kMC_simTXT.h"
#include "Running_KMC_Methods/write_data_to_kMC_sim_rate_constantsTXT.h"
#include "Running_KMC_Methods/print_time_passed.h"
#include "Running_KMC_Methods/Rate_Constant_Methods/get_distance.h"
#include "Running_KMC_Methods/Rate_Constant_Methods/get_marcus_rate_constants_data.h"
#include "Running_KMC_Methods/get_probability_based_stepwise_diffusion_tensor.h"
#include "auxillary_file.h"

// Create a random number generator for simulating the time the exciton lies on a molecules in the crystal. 
random_device rd;
mt19937 gen(rd());
uniform_real_distribution<long double> random_time_value(0.0, 1.0);

extern "C" void KMC_algorithm (const char* path_to_kMC_sim, const char* path_to_kMC_sim_rate_constants, 
	const COM_CObject* centre_of_molecules_array, const int centre_of_molecules_array_size, 
	const long double* unit_cell_matrix_array, const int unit_cell_matrix_array_size, 
	const char* kinetic_model, const long double constant_rate_data_1, const long double constant_rate_data_2, 
	const Bandgap_Energies_CObject* molecule_bandgap_energies_array, const int molecule_bandgap_energies_array_array_size, 
	const Reorganisation_Energies_CObject* dimer_reorganisation_energies_array, const int dimer_reorganisation_energies_array_size, 
	const Coupling_Value_Data_CObject* coupling_value_data_array, const int coupling_value_data_array_size, 
	const long double coupling_disorder_value, const bool coupling_disorder_is_percent, const long double energetic_disorder_value, 
	const bool energetic_disorder_is_percent, const long double sim_time_limit, const long long max_no_of_steps, const int starting_molecule, 
	const char* temp_folder_path, const bool write_rate_constants_to_file, const bool write_500_rate_constants_to_file) {
	/**
	 * This method is designed to run the kMC algorithm for an exciton moving about the molecules in a crystal in C++.
	 * 
	 * @param path_to_kMC_sim_C This is the path to the kMC.txt file where KMC running data is written to. 
	 * @param molecule_centre_of_molecules This list contains the 
	 * @param kinetic_model This is the kinetic model you would like to use to simulate an exciton about the molecules within a crystal.
	 * @param molecule_reorganisation_energy_data These are the energies required to calculate reorganisation energies and band gap/diff in energy values.
	 * @param constant_rate_data_1
	 * @param constant_rate_data_2
	 * @param coupling_value_data_array This dictionary contains all the coupling values information about the neighbourhoods that surrounded each molecule in your crystal.
	 * @param coupling_value_data_array_size This is the number of values in the coupling_value_data array.
	 * @param coupling_disorder_value This is the disorder that is associated with the V12 value.
	 * @param coupling_disorder_is_percent This parameter indicates if coupling_disorder_value is a value or a percentage of V12.
	 * @param energetic_disorder_value This is the disorder that is associated with the DeltaE value/the bandgap of the molecule containing the exciton.
	 * @param energetic_disorder_is_percent This parameter indicates if energetic_disorder_value is a value or a percentage of DeltaE.
	 * @param sim_time_limit This is the simulated time limit to run the kinetic Monte Carlo simulation over. Time given in ps.
	 * @param max_no_of_steps This is the maximum number of kmc steps to run the kinetic Monte Carlo simulation over.
	 * @param starting_molecule This is the molecule that this KMC simulation will begin from in the origin unit cell.
	 * @param temp_folder_path This is the path to place files as the KMC file is running for temporary storage. 
	 * @param write_rate_constants_to_file This indicates if you want to write a file called "kMC_sim_rate_constants.txt" that includes all the rate constant data for an exciton moving from the exciton donor it is currently on to any of the neighbouring exciton acceptors. 
	 */ 

	// First, convert molecule_centre_of_molecules into a unordered_map.
	unordered_map<int, vector<long double>> centre_of_molecules = convert_to_COM_dictionary(&centre_of_molecules_array, centre_of_molecules_array_size);

	// Second, convert the unit_cell_matrix_array back into a 2D matrix
	vector<vector<long double>> unit_cell_matrix = convert_to_UCM_dictionary(&unit_cell_matrix_array, unit_cell_matrix_array_size);

	// First, convert the molecule_bandgap_energies tuple into an unordered_map
	unordered_map<int, long double> molecule_bandgap_energies = convert_to_MBE_dictionary(&molecule_bandgap_energies_array, molecule_bandgap_energies_array_array_size);

	// Second, convert the dimer_reorganisation_energies tuple into an unordered_map
	unordered_map<tuple<int,int>, long double, hash_tuple_DRE> dimer_reorganisation_energies = convert_to_DRE_dictionary(&dimer_reorganisation_energies_array, dimer_reorganisation_energies_array_size);

	// Second, turn coupling_value_data into a dictionary that indicates the coupling values for dimers involving a original unit cell molecule. 
	unordered_map<int, vector<tuple<int,int,int,int,long double>>> coupling_value_data = convert_to_ALN_dictionary(&coupling_value_data_array, coupling_value_data_array_size);

	// Third, create a database to store energetic disorder, coupling disorder, and rate constant data in.
	Molecule_Energetic_Disorder_Database molecule_energetic_disorder_database;
	Rate_Constant_Database rate_constant_database;

	// Fourth, begin from time = 0.0 fs.
	long double current_time = 0.0; // in ps
	long double delta_time = 0.0; // in fs

	// Fifth, give the current cell point, which is the origin unit cell (0, 0, 0)
	int current_molecule_name = starting_molecule;
	int current_cell_point[3] = {0, 0, 0};
	tuple<int,int,int,int> current_molecule_description;

	// Sixth, record the position of the previous molecule position
	int previous_molecule_name = starting_molecule;
	int previous_cell_point[3] = {0, 0, 0};

	// Eighth, get the hopping distance from previous to current molecule
	long double hop_distance = 0.0; // A

	// Ninth, initiate the kMC_simTXT file.
	if (filesystem::exists(path_to_kMC_sim)) { filesystem::remove(path_to_kMC_sim); };
	ofstream kMC_simTXT(path_to_kMC_sim);
	if (kMC_simTXT.is_open()) { // Check if the file can be opened successfully, and if so add titles for columns.
		kMC_simTXT << write_data_to_kMC_simTXT("Count:", "Molecule", "Cell Point", "Time (ps)", "Time Step (fs)", "Hop Distance (A)", "Energy (eV)", "\u03A3 kij (ps-1)", "D(xx)", "D(yy)", "D(zz)", "D(xy)", "D(xz)", "D(yz)") << endl; 
	} else {
		throw runtime_error(string("Error: Something is up with") + path_to_kMC_sim + "\n");
	}
	remove(path_to_kMC_sim_rate_constants);
	ofstream kMC_sim_rate_constantsTXT(path_to_kMC_sim_rate_constants);
	if (write_rate_constants_to_file) {
		if (kMC_sim_rate_constantsTXT.is_open()) { // Check if the file can be opened successfully, and if so add titles for columns.
			kMC_sim_rate_constantsTXT << string("Counter Current Molecule (current molecule cell position) [sum of all rate constants (s-1)] ; (Neighbouring Molecule and relative unit cell displacement): rate constant (s-1), ...") << endl; 
		} else {
			throw runtime_error(string("Error: Something is up with") + path_to_kMC_sim_rate_constants + "\n");
		}
	}

	//temp
	long double write_rate_constants_to_file_time;
	if (write_500_rate_constants_to_file) {
		write_rate_constants_to_file_time = 500.0;
	} else {
		write_rate_constants_to_file_time = 0.0;
	}

	// Tenth, perform the kinetic Monte Carlo algorithm. 
	std::cout << "-------------" << std::endl;
	std::cout << "Start performing the Exciton kinetic Monte Carlo algorithm."  << std::endl;
	long double current_molecule_description_energy; 
	list<tuple<int,int,int,int>> other_molecule_descriptions; list<long double> rate_constants;
	long double D_xx; long double D_yy; long double D_zz;
	long double D_xy; long double D_xz; long double D_yz;
	auto start_time = chrono::high_resolution_clock::now();

	cout << "sim_time_limit: " << to_string(sim_time_limit) << endl;
	cout << "max_no_of_steps: " << to_string(max_no_of_steps) << endl;

	for (long counter = 0; (max_no_of_steps == -1) or (counter <= max_no_of_steps); counter++) {

		//cout << "mol: " << current_molecule_name << " cell: (" << current_cell_point[0] << ", " << current_cell_point[1] << ", " << current_cell_point[2] << ")" << endl;

		// 10.1: If the current molecule in the current_cell_point has not been examined before, obtain all the 
		//      rate constants for all the surrounding molecules that the exciton can move to.
		if (strcmp(kinetic_model, "marcus") == 0) {
			tie(current_molecule_description_energy, other_molecule_descriptions, rate_constants) = get_marcus_rate_constants_data(current_molecule_name, current_cell_point, constant_rate_data_1, constant_rate_data_2, energetic_disorder_value, energetic_disorder_is_percent, coupling_disorder_value, coupling_disorder_is_percent, &molecule_bandgap_energies, &dimer_reorganisation_energies, &coupling_value_data, &molecule_energetic_disorder_database, &rate_constant_database);
		} else if (strcmp(kinetic_model, "mlj") == 0) {
			; // To do
		}

		// 10.2: Get the sum of all the rate constants between the current molecule and its neighbours that it is coupled to.
		long double sum_of_rate_constants = 0.0; // in s-1
		for (long double k1j : rate_constants) {
			sum_of_rate_constants += k1j;
		}

		//10.3: Obtain the probability based stepwise diffusion tensor for the step of interest. 
		tie(D_xx, D_yy, D_zz, D_xy, D_xz, D_yz) = get_probability_based_stepwise_diffusion_tensor(current_molecule_name, current_cell_point, &other_molecule_descriptions, &rate_constants, &unit_cell_matrix, &centre_of_molecules);

		// 10.4: Print data of the current molcule in the current cell position to disk.
		kMC_simTXT << write_data_to_kMC_simTXT(counter, current_molecule_name, current_cell_point, current_time, delta_time, hop_distance, current_molecule_description_energy, sum_of_rate_constants * pow(10.0,-12.0), D_xx, D_yy, D_zz, D_xy, D_xz, D_yz) << endl; 
		if (write_rate_constants_to_file and (current_time >= write_rate_constants_to_file_time)) {
			kMC_sim_rate_constantsTXT << write_data_to_kMC_sim_rate_constantsTXT(counter, current_molecule_name, current_cell_point, &other_molecule_descriptions, &rate_constants, sum_of_rate_constants) << endl; 
		}

		// 10.5: If you have reached the time limit, finish the kinetic Monte Carlo algorithm.
		if ((sim_time_limit != -1.0) and (current_time >= sim_time_limit)) {
			print_time_passed(counter, start_time, current_time);
			break;
		}

		// 10.6: Move the current molecule spatial details to the previous molecule spatial.
		previous_molecule_name = current_molecule_name;
		previous_cell_point[0] = current_cell_point[0];
		previous_cell_point[1] = current_cell_point[1];
		previous_cell_point[2] = current_cell_point[2];

		// 10.7: Randomly select where the exciton will move to based on the relative rate constants.
		discrete_distribution<int> next_KMC_step_distribution(rate_constants.begin(), rate_constants.end());
		int index = next_KMC_step_distribution(gen);

		//if (index == 0) {
		//cout << "index chosen: " << index << endl;
		//}

		// 10.8: Extract the current cell point as well as the molecule that the exciton is on.
		auto other_molecule_descriptions_front = other_molecule_descriptions.begin();
		advance(other_molecule_descriptions_front, index);
		current_molecule_description = *other_molecule_descriptions_front;
		current_molecule_name = get<0>(current_molecule_description);
		current_cell_point[0] = get<1>(current_molecule_description);
		current_cell_point[1] = get<2>(current_molecule_description);
		current_cell_point[2] = get<3>(current_molecule_description);

		//cout << "mol: " << current_molecule_name << " cell: (" << current_cell_point[0] << ", " << current_cell_point[1] << ", " << current_cell_point[2] << ")" << endl;

		// 10.9: Get the hopping distance from the previous molecule to the current molecule.
		hop_distance = get_distance(&centre_of_molecules[current_molecule_name], current_cell_point, &centre_of_molecules[previous_molecule_name], previous_cell_point, &unit_cell_matrix);

		// 10.10: Determine the time that has lapped, and add this to the current time
		delta_time = -log(random_time_value(gen))/sum_of_rate_constants; // in seconds
		current_time += delta_time * pow(10.0,12.0); // in ps
		delta_time *= pow(10.0,15.0); // in fs

		// 10.11: Print counter to screen to show to the user that the algorithm is performing.
		if ((counter % 500) == 0) {
			print_time_passed(counter, start_time, current_time);
			//cout << "E_database_size: " << molecule_energetic_disorder_database.size() << endl;
			//cout << "RC_database_size: " << rate_constant_database.size() << endl;
		}
	}
	kMC_simTXT.close(); kMC_sim_rate_constantsTXT.close();
	if (!write_rate_constants_to_file) {
		remove(path_to_kMC_sim_rate_constants);
	}

}
