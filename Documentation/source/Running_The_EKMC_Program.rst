
.. _Running_The_EKMC_Program:

How To Run The Exciton kinetic Monte Carlo (EKMC) Program
##########################################################

Once you have setup your EKMC files by running the ``setup_EKMC_sims.py`` script, we are now ready to run the EKMC simulations. 

.. _What_will_setup_EKMC_sims_py_do:

What will ``setup_EKMC_sims.py`` do
-----------------------------------

The ``setup_EKMC_sims.py`` script will create a (number of) new folder(s) based on your input for ``crystal_settings['folder_name']`` in this script. In this folder will include a folder based on your name for ``crystal_settings['functional_and_basis_set']`` in the ``setup_EKMC_sims.py`` script, which includes three general files. 

	* ``Run_EKMC.py``: This is the file that will be run for each simulation. See :ref:`Run_EKMC_py_example` for more information about this file.
	* ``KMC_setup_data.ekmc``: This is a text file that contains all the information required for running excitonic kinetic Monte Carlo simulations, such as components of the excitonic hopping rates from molecule to molecule in the crystal, the molecule energy and couping energy disorders, and other useful parameters. This file should not be changed. 
	* ``ekmc_mass_submit_X.sl``: This is the submission scripts for submitting numerous repeated EKMC simulations to slurm. If you are wanting to run more than 1000 simulations, there will be multiple ``ekmc_mass_submit_X.sl`` files where ``X`` is a given interger. This is because for most computer cluster systems, slurm will only submit up to 1000 jobs in a single ArrayJob. 

During this setup, the ``EKMC`` program will access the molecule xyz files in the ``All_Molecules`` folder (in the ``ECCP_Information`` folder). The name given to each molecule in the ``EKMC`` simulation is the same as given in the molecules filename. For example, ``molecule_2.xyz`` is given the name ``2`` in the ``EKMC`` simulation. 

The ``EKMC`` program will also read in information about the dimers for which EET calculations has been performed on from the ``Unique_Dimer_Information.txt`` and ``All_Dimer_Information.txt`` files (if you have selected ``dimer_couplings['Use_non_atc_model_for_dimers'] = True`` in your ``setup_EKMC_sims.py`` file). It will read in the neighbouring dimers that were discovered by the ``ECCP`` program, and link the equivalent dimers with the unique dimers so that equivalent dimers are assigned with the appropriate coupling energy values. 

.. _Run_EKMC_py_example:

Example of a ``Run_EKMC.py`` file
---------------------------------

An example of a ``Run_EKMC.py`` script is shown below. 

.. code-block:: python

	"""
	This script will allow you to perform a Exciton-based kinetic Monte-Carlo simulation on your crystal.
	"""

	from EKMC import Run_EKMC

	# First, give the path to the KMC_setup_data, which has been run previously.
	# This file contains all the kinetic information and the electronic information around the local neighbourhood of each molecule in the crystal.
	path_to_KMC_setup_data=".."

	# Second, give the amount of time or the number of steps you would like to simulate.
	sim_time_limit = 1000
	max_no_of_steps = "inf"

	# Third, if you want to store data about the random energetic and coupling disorders in databases, provide the information required to use a database here.
	store_data_in_databases = False
	no_of_molecules_at_cell_points_to_store_on_RAM = None

	# Fourth, perform the exciton kinetic Monte Carlo simulation.
	Run_EKMC(path_to_KMC_setup_data=path_to_KMC_setup_data, sim_time_limit=sim_time_limit, max_no_of_steps=max_no_of_steps, store_data_in_databases=store_data_in_databases, no_of_molecules_at_cell_points_to_store_on_RAM=no_of_molecules_at_cell_points_to_store_on_RAM)

This file should not be modified. If you want to change this file, you should make the changes you need to in your ``setup_EKMC_sims.py`` script and re-run it.

There are two exceptions for this. There are two variables in the  ``Run_EKMC.py`` file that you can change without necessarily having to re-run the ``setup_EKMC_sims.py`` script if you do not want to. These are the ``sim_time_limit`` and ``max_no_of_steps`` variables. 

How to submit EKMC simulations to slurm and the ``EKMC mass_submit`` command
----------------------------------------------------------------------------

To submit EKMC simulations to slurm, you want to submit your ``ekmc_mass_submit_X.sl`` files to slurm. For example:

.. code-block:: bash

	sbatch ekmc_mass_submit_X.sl

You can do this for each ``ekmc_mass_submit_X.sl`` file. 

**An easier way to submit your EKMC simulations to slurm** is to run the ``EKMC mass_submit`` command. This program is designed to submit all the ``ekmc_mass_submit_X.sl`` files to slurm. This command is able to submit many EKMC simulation jobs within various subdirectories from where the ``EKMC mass_submit`` command is run from in the terminal.

To use this command, first move into the overall folder that contains all the EKMC simulations you would like to run.

.. code-block:: bash

	cd the_path_to_the_folder_that_contains_all_the_EKMC_jobs_you_would_like_to_submit_to_slurm

Once you are in the folder that contains all the EKMC jobs you would like to submit to slurm, type the ``EKMC mass_submit`` command into the terminal and run it:

.. code-block:: bash

	EKMC mass_submit

This program may take a bit of time to start, but it will at some point show in the terminal what it is doing. 

This program will submit ``ekmc_mass_submit_X.sl`` files files to slurm as long as it can see that no simulations have previously been run. 


















