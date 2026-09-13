# How To Use The EKMC Program

The EKMC program is used in two parts:

1. A **python script** sets up the simulations for a crystal and writes the slurm files needed to run them.
2. The **``ekmc`` terminal command** compiles the kMC code, submits those simulations to slurm, and processes the results.

## Part 1: Setting up your simulations

EKMC is set up by writing a python script that calls ``EKMC_Setup``. A complete working example is given in [the ``Examples`` folder](https://github.com/geoffreyweal/EKMC/tree/main/Examples/setup_EKMC_sims.py).

```python
from EKMC import EKMC_Setup

EKMC_Setup(EKMC_settings, mass_submission_information)
```

``EKMC_Setup`` takes the following arguments:

* ``EKMC_settings`` (*dict.*): The description of the crystal and the kinetics to simulate. See below.
* ``mass_submission_information`` (*dict.*): The information used to write the ``ekmc_mass_submit.sl`` slurm files. See below.
* ``setup_folder_name`` (*str.*): The name of the folder to write the initial setup files into (coupling data and so on). Default: ``None``.
* ``write_rate_constants_to_file`` (*bool.*): If ``True``, write the calculated rate constants to disk so you can inspect them. Default: ``False``.
* ``no_of_cpus_for_setup`` (*int.*): The number of cpus to use while setting up the simulations. Setting up the crystal neighbourhood is the slow part, so raise this for large crystals. Default: ``1``.

If you want to run simulations for several crystals, build a list of ``EKMC_settings`` dictionaries and call ``EKMC_Setup`` once for each:

```python
for EKMC_settings, mass_submission_information in zip(all_EKMC_settings, all_mass_submission_information):
	EKMC_Setup(EKMC_settings, mass_submission_information)
```

### The ``EKMC_settings`` dictionary

* ``folder_name`` (*str.*): The name of the folder to write this crystal's simulations into.
* ``molecules_path`` (*str.*): The path to the ECCP output folder for this crystal, which holds the molecules and their electronic data.
* ``functional_and_basis_set`` (*str.*): The functional and basis set that the DFT calculations were run with, for example ``'F_wB97XD_B_6_31plusGd_p'``. This selects which set of ECCP results to read.
* ``kinetic_model`` (*str.*): The kinetic model used to turn couplings and energies into hopping rate constants, for example ``'Marcus'``.
* ``short_range_couplings`` / ``long_range_couplings`` (*str.*): How the short-range and long-range exciton couplings are obtained.
* ``kinetics_details`` (*dict.*): The parameters the kinetic model needs, such as the classical reorganisation energy and the temperature.
* ``reorganisation_and_bandgap_energy_details`` (*dict.*): How to obtain the reorganisation energies and bandgap energies for an exciton moving between molecules.
* ``include_solvents`` (*bool.*): Whether solvent molecules take part in the simulation.
* ``overall_folder_suffix_name`` (*str.*): An optional suffix added to the folder names, useful for keeping several parameter sets side by side.

The following are read when the simulation runs:

* ``sim_time_limit`` (*float* or ``'inf'``): How long, in ps, to simulate the exciton for.
* ``max_no_of_steps`` (*int* or ``'inf'``): The maximum number of hops to simulate.
* ``starting_molecule``: Which molecule the exciton starts on. Default: ``'any'``.
* ``temp_folder_path`` (*str.*): A scratch folder for the simulation to write to.

### The ``mass_submission_information`` dictionary

These settings are written into the ``ekmc_mass_submit.sl`` files:

* ``submission_type`` (*str.*): How the simulations are submitted to slurm.
* ``no_of_simulations`` (*int.*): The number of repeat simulations to run for this crystal.
* ``no_of_sims_per_packet`` (*int.*): The number of simulations to group into a single slurm job.
* ``mem`` (*str.*): The memory to request for each job, for example ``'4GB'``.
* ``time`` (*str.*): The wall time to request, for example ``'0-08:00'``.
* ``partition`` (*str.*): The slurm partition to submit to.

## Part 2: Running and processing your simulations

Once ``EKMC_Setup`` has written the simulation folders, the ``ekmc`` command manages them.

### ``ekmc compile``

EKMC runs its kinetic Monte Carlo steps in C for speed. Compile that code once before your first run:

```bash
ekmc compile
```

### ``ekmc submit``

Submit the simulations to slurm. Run this in the folder containing your simulation folders:

```bash
ekmc submit
```

See ``ekmc submit --help`` for the options available.

### ``ekmc did_complete``

Report which simulations have finished and which have not:

```bash
ekmc did_complete
```

### ``ekmc process_results``

Once your simulations have finished, process them into exciton diffusion results:

```bash
ekmc process_results
```

### ``ekmc process_steps``

Process the per-step results of the simulations:

```bash
ekmc process_steps
```

## Output from the EKMC Program

``EKMC_Setup`` creates a folder named after ``folder_name`` for each crystal, containing the simulation folders and the ``ekmc_mass_submit.sl`` file used to submit them to slurm. After ``ekmc process_results`` has run, the exciton diffusion coefficient obtained from the simulations is written alongside them.
