/**
 * convert_arrays_to_unordered_maps.h, 29/5/23, Geoffrey Weal
 * 
 * This program is designed to convert the coupling_value_data array into an unordered_map to be used as a quick lookup table
 */

#ifndef CONVERT_ARRAYS_TO_UNORDERED_MAPS_H
#define CONVERT_ARRAYS_TO_UNORDERED_MAPS_H

#include <tuple>
#include <vector>
#include <unordered_map>
using namespace std;
#include "../auxillary_file.h"

struct hash_tuple_DRE {
    /**
     * This gives the lookup proceedure for the dimer_reorganisation_energies unordered map
     */
    size_t operator()(const std::tuple<int,int> &t) const {
        /**
         * This method will return the seed for a given tuple<int,int>
         * 
         * @param t This is the tuple input for the unordered_map.
         * 
         * @returns seed The position of the data in the RAM.
         */
        size_t seed = 0;
        hash<int> hasher;
        seed ^= hasher(get<0>(t)) + 0x9e3779b9 + (seed << 6) + (seed >> 2);
        seed ^= hasher(get<1>(t)) + 0x9e3779b9 + (seed << 6) + (seed >> 2);
        return seed;
    }
};

unordered_map<int, vector<long double>> convert_to_COM_dictionary(const COM_CObject** centre_of_molecules_array, const int centre_of_molecules_array_size);
vector<vector<long double>> convert_to_UCM_dictionary(const long double** unit_cell_matrix_array, const int unit_cell_matrix_array_size);
unordered_map<int, long double> convert_to_MBE_dictionary(const Bandgap_Energies_CObject** molecule_bandgap_energies_array, const int molecule_bandgap_energies_array_size);
unordered_map<tuple<int,int>, long double, hash_tuple_DRE> convert_to_DRE_dictionary(const Reorganisation_Energies_CObject** dimer_reorganisation_energies_array, const int dimer_reorganisation_energies_array_size);
unordered_map<int, vector<tuple<int,int,int,int,long double>>> convert_to_ALN_dictionary(const Coupling_Value_Data_CObject** coupling_value_data_array, const int coupling_value_data_array_size);

#endif
