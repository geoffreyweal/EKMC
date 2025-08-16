"""
check_molecule_consistancy_across_datasets.py, Geoffrey Weal, 2/7/23

This script is designed to check that the  molecule_bandgap_energy_data, dimer_reorganisation_energy_data, coupling_value_data and conformationally_equivalent_data
dictionaries do not include any molecules that do not exist in the crystal (not in molecule_names) and make the input data inconsistent.
"""

from itertools import product

def check_molecule_consistancy_across_datasets(molecule_names, molecule_bandgap_energy_data, dimer_reorganisation_energy_data, coupling_value_data, conformationally_equivalent_data):
    """
    This method will update the reorganisation energy data sources for the KMC program to use. 

    Parameters
    ----------
    molecule_names : list of ints
        This list contains all the names of the molecules in the crystal.
    molecule_bandgap_energy_data : dict.
        These are the bandgap energies of the unique molecules in the crystal.
    dimer_reorganisation_energy_data : dict.
        These are the reorganisation energies of the unique dimers in the crystal.
    coupling_value_data : dict.
        This dictionary contains all the information about the coupling between neighbours in the crystal. This contains both unique and equivalent molecules in (lower mol name number, higher mol name number) format.
    conformationally_equivalent_data : dict.
        This dictionary contains information about which molecules are conformationally equivalent to each other. 

    Returns
    -------
    molecule_reorganisation_energy_data : dict.
        These are the energies required to calculate reorganisation energies and band gap/diff in energy values.
    conformationally_equivalent_data : dict.
        This dictionary contains information about which molecules are conformationally equivalent to each other. 
    """

    # ===============================================================================================================================================
    # CHECKING  MOLECULES IN coupling_value_data DICTIONARY.

    # First, check that coupling_value_data dont contain any molecules it should have in the crystal
    errors = []
    for mol1, value in coupling_value_data.items():
        if (mol1 not in molecule_names) and (mol1 not in errors):
            errors.append(mol1)
        for mol2 in value.keys():
            if (mol2 not in molecule_names) and (mol2 not in errors):
                errors.append(mol2)
    if len(errors) > 0:
        toString  = 'Error: Some molecules given in the coupling_value_data dict. are not given in the molecule_names list.'+'\n'
        toString += 'The coupling_value_data dictionary should contains all the unique and equivalent molecules in the crystal.'+'\n'
        toString += 'Check this out.'+'\n'
        toString += 'All molecules in crystal (given by molecule_names): '+str(molecule_names)+'\n'
        toString += 'Molecule in coupling_value_data that are not in molecule_names: '+str(sorted(errors))+'\n'
        raise Exception(toString)

    # ===============================================================================================================================================
    # CHECKING MOLECULES IN conformationally_equivalent_data DICTIONARY.

    # Second, check if are any molecules in equivalent_molecules (conformationally_equivalent_data.keys()) that are not found in molecule_names
    equivalent_errors = []
    for equivalent_molname in conformationally_equivalent_data.keys():
        if (equivalent_molname not in molecule_names) and (equivalent_molname not in equivalent_errors):
            equivalent_errors.append(equivalent_molname)
    unique_errors = []
    for unique_molname in conformationally_equivalent_data.values():
        if (unique_molname not in molecule_names) and (unique_molname not in unique_errors):
            unique_errors.append(unique_molname)
    if len(equivalent_errors+unique_errors) > 0:
        toString  = 'Error: Some molecules given in the conformationally_equivalent_data dict. are not in the molecule_names list.'+'\n'
        toString += 'Check this out.'+'\n'
        toString += 'All molecules in crystal (given by molecule_names): '+str(molecule_names)+'\n'
        if len(equivalent_errors) > 0:
            toString += 'Equivalent molecules in conformationally_equivalent_data that are not in molecule_names (conformationally_equivalent_data.keys()): '+str(sorted(equivalent_errors))+'\n'
        if len(unique_errors) > 0:
            toString += 'Unique molecules in conformationally_equivalent_data that are not in molecule_names (conformationally_equivalent_data.values()): '+str(sorted(unique_errors))+'\n'
        raise Exception(toString)

    # ===============================================================================================================================================
    # CHECKING UNIQUE MOLECULES IN molecule_bandgap_energy_data AND dimer_reorganisation_energy_data DICTIONARIES.

    # Third, obtain all the equivalent and unique molecules from the molecule_names and conformationally_equivalent_data datasets
    equivalent_molecules = sorted(conformationally_equivalent_data.keys())
    unique_molecules = sorted(set(molecule_names) - set(equivalent_molecules))

    # Fourth, check that the all the unique molecules are found in molecule_bandgap_energy_data. 
    if not (sorted(molecule_bandgap_energy_data.keys()) == unique_molecules):
        toString  = 'Error: Not all the unique molecules in the crystal have bandgap assigned to them.'+'\n'
        toString += 'Check this.'+'\n'
        toString += 'molecules in molecule_bandgap_energy_data = '+str(sorted(molecule_bandgap_energy_data.keys()))+'\n'
        toString += 'unique molecules = '+str(unique_molecules)+'\n'
        raise Exception(toString)

    # Fifth, check that the all the unique molecules are found in dimer_reorganisation_energy_data. 
    all_expected_unique_dimers = sorted([(mol1, mol2) for (mol1, mol2) in product(unique_molecules, unique_molecules)])
    if not (sorted(dimer_reorganisation_energy_data.keys()) == all_expected_unique_dimers):
        toString  = 'Error: Not all the unique dimers in the crystal have reorganisation energies assigned to them.'+'\n'
        toString += 'Check this.'+'\n'
        toString += 'dimers in dimer_reorganisation_energy_data = '+str(sorted(dimer_reorganisation_energy_data.keys()))+'\n'
        toString += 'unique dimers = '+str(all_expected_unique_dimers)+'\n'
        raise Exception(toString)

    # ===============================================================================================================================================

 