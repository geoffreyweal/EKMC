/**
 * print_time_passed.h, 29/5/23, Geoffrey Weal
 * 
 * This algorithm is designed to print the amount of time passed after performing a number of KMC steps.
 */
#include <chrono>
using namespace std;

void print_time_passed(long counter, chrono::time_point<chrono::high_resolution_clock> start_time, long double current_time);