# The Exciton Kinetic Monte Carlo (EKMC) Program

Authors: Dr. Geoffrey Weal<sup>\*,†</sup>, Dr. Chayanit Wechwithayakhlung<sup>†</sup>, Dr. Josh Sutton<sup>\*</sup>, Dr. Daniel Packwood<sup>†</sup>, Dr. Paul Hume<sup>\*</sup>, Prof. Justin Hodgkiss<sup>\*</sup>

<sup>\*</sup> Victoria University of Wellington, Wellington, New Zealand; The MacDiarmid Institute for Advanced Materials and Nanotechnology, Wellington, New Zealand. 

<sup>†</sup> Institute for Integrated Cell-Material Sciences (iCeMS), Kyoto University, Kyoto, Japan.

Group pages: https://people.wgtn.ac.nz/paul.hume/grants, https://www.packwood.icems.kyoto-u.ac.jp/, https://people.wgtn.ac.nz/justin.hodgkiss/grants


## What is the Exciton Kinetic Monte Carlo (EKMC) Program

The Exciton Kinetic Monte Carlo (EKMC) program simulates the movement of an exciton through a molecular crystal using the kinetic Monte Carlo (kMC) method, and from those simulations obtains the exciton diffusion coefficient.

EKMC takes the electronic data that the [ECCP program](https://geoffreyweal.github.io/ECCP) obtains from DFT calculations — excited-state energies, reorganisation energies, and exciton (EET) couplings — and uses them to build the rate constants for an exciton hopping between neighbouring molecules in the crystal. It then:

1. Builds the local neighbourhood of each molecule in the crystal, including neighbours across periodic cell boundaries.
2. Calculates the hopping rate constant between each pair of neighbouring molecules, using the chosen kinetic model (for example, Marcus theory).
3. Runs repeated kMC simulations of an exciton hopping through the crystal.
4. Processes the resulting trajectories into an exciton diffusion coefficient.

EKMC is designed to run many repeat simulations in parallel on a slurm cluster.

!!! note

	If you want the exciton diffusion coefficient without simulating individual trajectories, see the [SORE program](https://geoffreyweal.github.io/SORE), which answers the same question analytically using a sum-over-rates equation.

## Installation

It is recommended to read the installation page before using the EKMC program. See [Installation: Setting Up EKMC and Pre-Requisites Packages](Installation.md) for more information.

## Guide To Using EKMC

The EKMC program is one in a series of programs that are designed to be used in the workflow shown below. After you have installed EKMC, see [How To Use The EKMC Program](Using_The_EKMC_Program.md) to learn about how to use this program.

## The Grand Scheme

The EKMC program is used as part of a grand scheme for calculating the excited-state electronic properties of molecules in a crystal. This includes simulations of exciton and charge diffusion through crystal structures, in particular for organic molecules (but not limited to them). This scheme is shown below, along with where the EKMC program is used in this scheme. 

<img alt="Schematic of Grand Scheme" src="Shared_Images/Grand_Scheme/Grand_Scheme.png?raw=true#only-light" />
<img alt="Schematic of Grand Scheme" src="Shared_Images/Grand_Scheme/Grand_Scheme_Dark.png?raw=true#only-dark" />

## Websites and Github Repositories for All Associated Programs

### Instructional Websites

* ACSD: https://geoffreyweal.github.io/ACSD
* ReCrystals: https://geoffreyweal.github.io/ReCrystals
* RSGC: https://geoffreyweal.github.io/RSGC
* ReJig: https://geoffreyweal.github.io/ReJig
* ECCP: https://geoffreyweal.github.io/ECCP
* EKMC: https://geoffreyweal.github.io/EKMC
* SORE: https://geoffreyweal.github.io/SORE
* SUMELF: https://geoffreyweal.github.io/SUMELF

### Github Repositories

* ACSD: https://github.com/geoffreyweal/ACSD
* ReCrystals: https://github.com/geoffreyweal/ReCrystals
* RSGC: https://github.com/geoffreyweal/RSGC
* ReJig: https://github.com/geoffreyweal/ReJig
* ECCP: https://github.com/geoffreyweal/ECCP
* EKMC: https://github.com/geoffreyweal/EKMC
* SORE: https://github.com/geoffreyweal/SORE
* SUMELF: https://github.com/geoffreyweal/SUMELF
