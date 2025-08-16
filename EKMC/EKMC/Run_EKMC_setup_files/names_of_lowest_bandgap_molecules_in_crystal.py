"""
names_of_lowest_bandgap_molecules_in_crystal.py, Geoffrey Weal, 2/7/23

This script will return a list of the molecule/molecules with the lowest (smallest) band gaps.
"""

def names_of_lowest_bandgap_molecules_in_crystal(molecule_bandgap_energy_data):
    """
    This method will return a list of the molecule/molecules with the lowest (smallest) band gaps.

    Parameters
    ----------
    molecule_bandgap_energy_data : dict.
        These are the bandgap energies of the unique molecules in the crystal.
    conformationally_equivalent_data : dict.
        This dictionary contains information about which molecules are conformationally equivalent to each other. 

    Returns
    -------
    molecule_names_with_lowest_bandgaps : list
        This is a list of all the molecules with the lowest band gaps in the crystal.
    """

    # First, determine the molecule(s) in the molecule_reorganisation_energy_data dictionary with the lowest band gap.
    molecule_names_with_lowest_bandgaps = []
    lowest_bandgap = float('inf')
    for molecule_name, bandgap_energy in molecule_bandgap_energy_data.items():

        # 1.1: Record the molecule if it has a bandgap that is smaller or equal to lowest_bandgap
        if bandgap_energy < lowest_bandgap:
            molecule_names_with_lowest_bandgaps = [molecule_name]
            lowest_bandgap = bandgap_energy
        elif bandgap_energy == lowest_bandgap:
            molecule_names_with_lowest_bandgaps.append(molecule_name)

    # Second, return molecule_names_with_lowest_bandgaps
    return sorted(molecule_names_with_lowest_bandgaps)
