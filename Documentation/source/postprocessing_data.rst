
.. _postprocessing_data:

Post-processing programs that are available in the EKMC program
###############################################################

There are a few programs that you can run after you have run your EKMC simulation in slurm. These are:

	* ``EKMC did_complete``: Check if simulations have completed successfully or not.
	* ``EKMC process_results``: This will process all the data from all your repeatde simulations collectively to give results across each simulation, as well as average value results. 

These programs are described in more detail below.


``EKMC did_complete``: Check that your EKMC simulations have all completed successfully
***************************************************************************************

You can check if all your EKMC simulations have finished successfully by typing ``EKMC did_complete`` into the terminal. ``EKMC`` will go through all the folders and look through all the ``kMC_sim.txt`` in each of your ``Sim`` folders. If the ``kMC_sim.txt`` file shows that the simulation has run to at least the simulation time as given by the ``sim_time_limit`` variable in the ``Run_EKMC.py`` file, then it will be marked as complete. Otherwise, the simulation will be marked as not complete. 

To do this program, move into the folder that contains your jobs and run ``EKMC did_complete`` in the terminal: 

.. code-block:: bash

	cd path/to/EKMC_simulation/jobs
	EKMC did_complete


``EKMC process_results``: Processing the results of all your repeated simulations collectively
**********************************************************************************************

Once all your repeated simulations have finished, you can use ``EKMC process_results`` to process all these simulations together for results. 

The information that is obtained from ``EKMC process_results`` are:

	* here

To run this program. Move into the directory that contains all the subdirectory of EKMC simulations you want to process and type ``EKMC process_results`` into the terminal:

.. code-block:: bash

	cd path/to/EKMC_simulation/jobs
	EKMC process_results



