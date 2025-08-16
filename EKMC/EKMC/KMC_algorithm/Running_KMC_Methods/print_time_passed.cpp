/**
 * print_time_passed.cpp, 29/5/23, Geoffrey Weal
 * 
 * This algorithm is designed to print the amount of time passed after performing a number of KMC steps.
 */
#include <iostream>
#include <iomanip>
#include <chrono>
#include <cmath>
#include "print_time_passed.h"
using namespace std;

void print_time_passed(long no_of_KMC_steps_performed, chrono::time_point<chrono::high_resolution_clock> start_time, long double current_time) {
	/**
	 * This algorithm is designed to print the amount of time passed after performing a number of KMC steps.
	 * 
	 * @param no_of_KMC_steps_performed This is the number of KMC steps that have been performed
	 * @param start_time This is the time when the KMC program begun.
	 * @param current_time Thisis the current time simulated (in ns).
	 */

	auto end_time = chrono::high_resolution_clock::now();
	long double duration = chrono::duration_cast<chrono::microseconds>(end_time - start_time).count() / 1000000.0;

	int hours = (duration / 3600.0);
	int minutes = fmod(duration, 3600.0) / 60.0;
	long double seconds = fmod(duration, 60.0);

	cout << "Count: " << no_of_KMC_steps_performed
		<< "\tTime Simulated: " << current_time << " ns"
		<< "\tTime Passed (HH:MM:SS): "
		<< setfill('0') << setw(2) << hours << ":"
		<< setfill('0') << setw(2) << minutes << ":"
		<< setfill('0') << setw(2) << seconds << endl;

}