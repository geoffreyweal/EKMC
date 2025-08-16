/**
 * get_V_with_disorder.cpp, Geoffrey Weal, 30/5/23
 * 
 * This algorithm is designed to obtain the coupling value of a dimer with disorder.
 */
#include <random>
using namespace std;

// Create a random number generator
random_device rd_coupling_disorder;
mt19937 generator_cd(rd_coupling_disorder());

long double get_V_with_disorder(long double coupling_value, long double coupling_disorder_value, bool coupling_disorder_is_percent) {
	/**
	 * This method is designed to obtain the coupling value of a dimer with disorder.
	 * 
	 * @param coupling_value This is the coupling values between the current (donor) molecule and the neighbouring (acceptor) molecule. This value does not contain disorder. 
	 * @param coupling_disorder_value This is the coupling disorder value, either given as a standard deviation (in eV), or as a percentage of a coupling value for a dimer. 
	 * @param coupling_disorder_is_percent If True, coupling_disorder_value is a percentage. If False, coupling_disorder_value is a standard deviation (in eV).
	 * 
	 * @returns The coupling value of the dimer with disorder (in eV). 
	 */

	// Second, get the coupling disorder standard deviation.
	long double coupling_disorder_sd;
	if (coupling_disorder_is_percent) {
		coupling_disorder_sd = abs(coupling_value * (coupling_disorder_value/100.0));
	} else {
		coupling_disorder_sd = coupling_disorder_value;
	}

	// Third, obtain the molecule's bandgap energy with associated disorder. 
	normal_distribution<long double> distribution(coupling_value, coupling_disorder_sd);
	long double dimer_coupling_with_disorder = distribution(generator_cd);

	// Fourth, return dimer_coupling_with_disorder
	return dimer_coupling_with_disorder;
}