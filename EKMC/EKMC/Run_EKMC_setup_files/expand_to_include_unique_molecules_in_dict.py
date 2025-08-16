"""
expand_to_include_unique_molecules_in_dict.py, Geoffrey Weal, 2/7/23

This script is designed to update the conformationally_equivalent_data to include all molecules in molecule_names.
Missing molecules in conformationally_equivalent_data.keys() are unique, and link to thrmselves.
"""

from copy import deepcopy

def expand_to_include_unique_molecules_in_dict(original_conformationally_equivalent_data, molecule_names):
    """
    This method will update the conformationally_equivalent_data to include all molecules in molecule_names.
    Missing molecules in conformationally_equivalent_data.keys() are unique, and link to thrmselves.

    Parameters
    ----------
    conformationally_equivalent_data : dict.
        This dictionary contains information about which molecules are conformationally equivalent to each other. 
    molecule_names : list of ints
        This list contains all the names of the molecules in the crystal.

    Returns
    -------
    conformationally_equivalent_data : dict.
        This dictionary contains information about which molecules are conformationally equivalent to each other. 
    """

    # First, make a copy of conformationally_equivalent_data
    conformationally_equivalent_data = deepcopy(original_conformationally_equivalent_data)

    # Second, add molecule_names that are not keys in original_conformationally_equivalent_data into 
    #         original_conformationally_equivalent_data that link to themselves.
    for molecule_name in molecule_names:
        if molecule_name not in original_conformationally_equivalent_data.keys():
            conformationally_equivalent_data[molecule_name] = molecule_name

    # Third, return the updated conformationally_equivalent_data dictionary
    return conformationally_equivalent_data