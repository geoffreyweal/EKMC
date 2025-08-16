"""
update_bandgap_and_reorganisation_energy_data.py, Geoffrey Weal, 24/3/23

This script is designed to update the reorganisation energy data sources for the KMC program to use. 
"""
from copy import deepcopy

def update_bandgap_and_reorganisation_energy_data(original_molecule_bandgap_energy_data, original_dimer_reorganisation_energy_data, conformationally_equivalent_data):
    """
    This method will update the reorganisation energy data sources for the KMC program to use. 

    Parameters
    ----------
    original_molecule_bandgap_energy_data : dict.
        These are the bandgap energies of the unique molecules in the crystal.
    original_dimer_reorganisation_energy_data : dict.
        These are the reorganisation energies of the unique dimers in the crystal.
    conformationally_equivalent_data : dict.
        This dictionary contains information about which molecules are conformationally equivalent to each other. 

    Returns
    -------
    molecule_reorganisation_energy_data : dict.
        These are the energies required to calculate reorganisation energies and band gap/diff in energy values.
    conformationally_equivalent_data : dict.
        This dictionary contains information about which molecules are conformationally equivalent to each other. 
    """

    # First, update molecule_bandgap_energy_data to include bandgap energies of both unique and equivalent molecules in the crystal.
    molecule_bandgap_energy_data = {}
    for equivalent_molname, unique_molname in conformationally_equivalent_data.items():
        molecule_bandgap_energy_data[equivalent_molname] = deepcopy(original_molecule_bandgap_energy_data[unique_molname])

    # Second, update dimer_reorganisation_energy_data to include reorganisation energies of both unique and equivalent molecules in the crystal.
    dimer_reorganisation_energy_data = {}
    for equivalent_molname1, unique_molname1 in conformationally_equivalent_data.items():
        for equivalent_molname2, unique_molname2 in conformationally_equivalent_data.items(): 
            dimer_reorganisation_energy_data[(equivalent_molname1, equivalent_molname2)] = deepcopy(original_dimer_reorganisation_energy_data[(unique_molname1, unique_molname2)])

    # Third, return the updated molecule_bandgap_energy_data and dimer_reorganisation_energy_data dictinaries.
    return molecule_bandgap_energy_data, dimer_reorganisation_energy_data
