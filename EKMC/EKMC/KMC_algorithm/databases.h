
#ifndef DATABASES_H
#define DATABASES_H

#include <tuple>
#include <unordered_map>
using namespace std;

struct hash_tuple_energy {
    size_t operator()(const std::tuple<int,int,int,int> &t) const {
        size_t seed = 0;
        hash<int> hasher;
        seed ^= hasher(get<0>(t)) + 0x9e3779b9 + (seed << 6) + (seed >> 2);
        seed ^= hasher(get<1>(t)) + 0x9e3779b9 + (seed << 6) + (seed >> 2);
        seed ^= hasher(get<2>(t)) + 0x9e3779b9 + (seed << 6) + (seed >> 2);
        seed ^= hasher(get<3>(t)) + 0x9e3779b9 + (seed << 6) + (seed >> 2);
        return seed;
    }
};

struct hash_tuple_coupling {
    size_t operator()(const std::tuple<int,int,int,int, int,int,int,int> &t) const {
        size_t seed = 0;
        hash<int> hasher;
        seed ^= hasher(get<0>(t)) + 0x9e3779b9 + (seed << 6) + (seed >> 2);
        seed ^= hasher(get<1>(t)) + 0x9e3779b9 + (seed << 6) + (seed >> 2);
        seed ^= hasher(get<2>(t)) + 0x9e3779b9 + (seed << 6) + (seed >> 2);
        seed ^= hasher(get<3>(t)) + 0x9e3779b9 + (seed << 6) + (seed >> 2);
        seed ^= hasher(get<4>(t)) + 0x9e3779b9 + (seed << 6) + (seed >> 2);
        seed ^= hasher(get<5>(t)) + 0x9e3779b9 + (seed << 6) + (seed >> 2);
        seed ^= hasher(get<6>(t)) + 0x9e3779b9 + (seed << 6) + (seed >> 2);
        seed ^= hasher(get<7>(t)) + 0x9e3779b9 + (seed << 6) + (seed >> 2);
        return seed;
    }
};

class Molecule_Energetic_Disorder_Database {
	public:
		bool contains(tuple <int,int,int,int> E_search_key);
		void add(tuple <int,int,int,int> E_search_key, long double molecule_energy_with_disorder);
		long double get(tuple <int,int,int,int> E_search_key);
		void print();
		int size();
	private:
		unordered_map<tuple <int,int,int,int>, long double, hash_tuple_energy> molecule_energetic_disorder_database;
};

class Rate_Constant_Database {
	public:
		bool contains(tuple <int,int,int,int, int,int,int,int> R_search_key);
		void add(tuple <int,int,int,int, int,int,int,int> R_search_key, long double rate_constant_database);
		long double get(tuple <int,int,int,int, int,int,int,int> R_search_key);
		void print();
		int size();
	private:
		unordered_map<tuple <int,int,int,int, int,int,int,int>, long double, hash_tuple_coupling> rate_constant_database;
};

#endif


