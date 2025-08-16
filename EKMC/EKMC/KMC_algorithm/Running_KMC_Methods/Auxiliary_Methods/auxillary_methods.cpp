/**
 * write_data_to_kMC_simTXT.cpp, 29/5/23, Geoffrey Weal
 * 
 * This method contains methods used by write_data_to_kMC_simTXT.cpp and write_data_to_kMC_sim_rate_constantsTXT.cpp
 */
#include <iomanip>
#include <string>
using namespace std;

string placement_counter(string input_toString, int total_no_of_charaters, int input_toString_max_length=1000000000) {
	/**
	 * This method will create an output toString that has a desired number of characters is it.
	 * 
	 * If input_toString is greater than total_no_of_charaters, the later characters will be remove from input_toString so it only contains total_no_of_charaters.
	 * If input_toString is less than total_no_of_charaters, white spaces will be added to the end of input_toString so that it is total_no_of_charaters characters long.
	 * 
	 * @param input_toString This is the input string we would like to make sure has the desired length
	 * @param total_no_of_charaters This is the number of characters you would like to have in the output.
	 * @param input_thing_max_length This is the maximum number of characters to take from the input_thing string.
	 */

	// First, obtain input_thing as a string.
	if (input_toString.size() > input_toString_max_length) {
		input_toString.resize(input_toString_max_length);
	}

	// Second, extend the  input_thing_string string so that it contains total_no_of_charaters characters by adding spaces to the end of the string.
	string output_toString = input_toString + string(total_no_of_charaters - input_toString.size(), ' ');

	// Third, return output_toString
	return output_toString;

}

string to_string_long_double(long double value) {
    std::ostringstream oss;
    oss << std::fixed << std::setprecision(14) << value;
    return oss.str();
}