/**
 * auxillary_file.h, Geoffrey Weal, 30/5/23
 * 
 * This script contains various structs used for KMC simulations. 
 */
#ifndef AUXILLARY_FILE_H
#define AUXILLARY_FILE_H

#include <tuple>
#include <cmath>
using namespace std;

struct COM_CObject { 
	/**
	 * This contains the information required to obtain the centre of mass/molecule for a molecule
	 * 
	 * @param mol This is the name of the molecule.
	 * @param centre_of_mass This is the centre of mass/molecule of the molecule.
	 */
	int mol;
	long double centre_of_mass_x;
	long double centre_of_mass_y;
	long double centre_of_mass_z;
};

struct Bandgap_Energies_CObject { 
	/**
	 * This contains the information required to obtain the reorganisation energy for a molecule
	 * 
	 * @param mol This is the name of the molecule.
	 * @param bandgap_energy This is the bandgap energy of the molecule.
	 */
	int mol;
	long double bandgap_energy;
};

struct Reorganisation_Energies_CObject { 
	/**
	 * This contains the information required to obtain the reorganisation energy for a molecule
	 * 
	 * @param mol1 This is the name of the first molecule.
	 * @param mol2 This is the name of the second molecule.
	 * @param reorganisation_energy This is the reorganisation energy for a exciton jumping from molecule 1 to molecule 2. 
	 */
	int mol1;
	int mol2;
	long double reorganisation_energy;
};

struct Coupling_Value_Data_CObject { 
	/**
	 * This contains the coupling values for molecules in a dimer.
	 * 
	 * @param mol1 The name of the first molecule in the dimer (which is located in the origin unit cell).
	 * @param mol2 The name of the second molecule in the dimer (which is located in the (uniti, unitj, unitk) unit cell).
	 * @param uniti This is the position of the second molecule, shifted by i * length of unit cell in i direction
	 * @param unitj This is the position of the second molecule, shifted by j * length of unit cell in j direction
	 * @param unitk This is the position of the second molecule, shifted by k * length of unit cell in k direction
	 */
	int mol1;
	int mol2;
	int uniti;
	int unitj;
	int unitk;
	long double coupling_value;
};

#endif
