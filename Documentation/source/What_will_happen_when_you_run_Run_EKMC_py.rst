
.. _What_will_happen_when_you_run_Run_EKMC_py:

What Will Happen When You Run the ``Run_EKMC.py`` script
########################################################

Once your EKMC simulations are running in slurm, you will see a few things happen in the directory that your ``Run_EKMC.py``, ``KMC_setup_data.ekmc``, and ``ekmc_mass_submit.sl`` files are in. 

First, you will see that a number of folders will be created that all begin with the name ``Sim``. These folders hold all the simulations that you want to run. In each of these folder will be a copy of the ``Run_EKMC.py`` file, as well as a file called ``kMC_sim.txt``. This text file contains all the information about the excitonic kinetic Monte Carlo simulation as the simulation proceeded over time. The format of this file is as follows:

	* ``Count``: This is the current kinetic Monte Carlo step that has been performed. 
	* ``Molecule``: This is the molecule type that the exciton is currently on. The number is the name of the molecule, given in the ``ECCP_Information`` folder, given by the ``ECCP_Information.txt`` text file and the molecules in the ``Unique_Molecules`` folder. This molecule number is unique to the position of the molecule in the origin unit cell.
	* ``Cell Point``: This indicates which cell in the extended crystal the exciton (and therefore the molecule that contains the exciton) is located in the crystal.
	* ``Time (ps)``: This is the time when the exciton first hopped to this molecule. This time is given in picoseconds. 
	* ``Time Step (fs))``: This is the amount of time that the exciton was in the previous KMC state before jumping into this state. This is given in femtoseconds. 
	* ``Energy (eV))``: This is the energy of the molecule that the exciton is on. This is given in eV.
	* ``∑ kij (ps-1))``: This is the sum of all rate constants from the molecule that this exciton is currrently on. 
	* ``|``: This is an end of line mark to indiate this is the end of the line. This is just needed for the computer for reading in information. ]]]
