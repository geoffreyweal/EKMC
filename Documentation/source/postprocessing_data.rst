
.. _postprocessing_data:

Post-processing programs that are available in the Electronic Crystal Calculation Prep program
##############################################################################################

There are a few programs that you can run after you have submitted atomic transition charge (ATC), reorganisation energy (RE), electronic energy transfer (EET), eigendata, and intermolecular charge transfer (ICT) calculations to slurm. These are:

	* ``ECCP did_complete``: Check if jobs have completed successfully or not.
	* ``ECCP mass_submit_multiwfn``: For submitting Multiwfn jobs once your ATC gaussian jobs have finished. 
	* ``ECCP reset_RE_calc``: For resuming reorganisatino calculations if they did not completed in the allotted time.
	* ``ECCP process_RE``: For obtaining results from the reorganisation energy calculations.
	* ``ECCP process_EET``: For obtaining result from the electronic energy transfer calculations.
	* ``ECCP process_ICT``: For obtaining result from the intermolecular charge transfer calculations.
	* ``ECCP process_Eigendata``: For solely obtaining matrix files from Eigendata jobs. 
	* ``ECCP tidy``: For removing unnecessary files that are not needed anymore and take up a lot of hard disk space. 

These programs are described in more detail below.


``ECCP did_complete``: Checking which jobs have completed successfully
**********************************************************************

You can check which gaussian jobs have finished successfully and which jobs have not finished successfully by typing ``ECCP did_complete`` into the terminal. ``ECCP`` will go through all the folders and will look for ``output.log`` files. It will then look through these files for key words that indicate the job has completed successfully, whether that be ATC, RE, EET, or Eigendata (ICT) calculations. To do this, move into the folder that contains your jobs and  run ``ECCP did_complete`` in the terminal: 

.. code-block:: bash

	cd path/to/gaussian/jobs
	ECCP did_complete


``ECCP mass_submit_multiwfn``: Submitting MultiWFN ATC jobs manually
********************************************************************

When running ATC jobs, the ``ECCP`` program will first run Gaussian on the ``input.gjf`` file (containing the molecules you want to obtain ATC results for). Once this calculation has finished, it will then run the MultiWFN program on the ``.wfn`` file that is created by Gaussian automatically. However, if an issue arises that stops MultiWFN from running, it is still possible to run MultiWFN on slurm by submitting the associated ``submit_multiwfn.sl`` file to slurm: 

.. code-block:: bash

	cd path/to/atc/submit_multiwfn/file
	sbatch submit_multiwfn.sl

This will run the MultiWFN program as long as the ``.wfn`` file exists for that job. 

You can also mass submit all these file by typing ``ECCP mass_submit_multiwfn`` in to the terminal. 

.. code-block:: bash

	cd path/to/ATC/jobs
	ECCP mass_submit_multiwfn

This will search within the subdirectories for ``submit_multiwfn.sl`` files, which it will then submit to slurm. 


``ECCP reset_RE_calc``: Resetting unfinished reorganisation energy calculation for resubmission to slurm
*********************************************************************************************************

Geometry optimisations are performed when obtaining reorganisation energies for molecules. Due to the size of molecules often calculated, these can often take a while to perform. Furthermore, optimisations are performed in the ground state as well as the first excited state. These excited state geometry optimisations can take a very long time to finish. In some cases, you may run out of time on slurm when performing optimisations. Therefore, you may want to resume the Gaussian optimisation from the last optimisation step. ``ECCP reset_RE_calc`` will update the gjf files with those of the last geometry optimisation and allow you to continue the optimisation if it do not complete successfully. This program will store your previous optimisations in a folder called ``previous_opt_files``. 

To run this program,  move into the folder that contains your jobs and  run ``ECCP did_complete`` in the terminal: 

.. code-block:: bash

	cd path/to/gaussian/jobs
	ECCP reset_RE_calc

Note: This program WILL NOT modify any files or folders that have successfully finished geometry optimisations. You can run it from any folder, and it will only modify subdirectories that have not completed their geometry optimisations. For example, you can run the program like this

.. code-block:: bash

	cd Unique_RE_Gaussian_Jobs
	ECCP reset_RE_calc

Once you have done this, you can resubmit your reorganisation jobs using ``ECCP mass_submit``

.. code-block:: bash

	ECCP mass_submit

Processing results of atomic transition charge Gaussian jobs using ``ECCP process_ATC``
***************************************************************************************

To do




Processing results of reorganisation energy Gaussian jobs using ``ECCP process_RE``
***********************************************************************************

To do




Processing results of Electronic Energy Transfer jobs using ``ECCP process_EET``
********************************************************************************

It is possible for this program to process the electronic coupling results from Gaussian jobs and present the results in text and in an excel spreadsheet. If the Gaussian job runs successfully, it will give a ``output.log`` file that contains values for the electronic coupling between the molecules in the dimer using the EET method in Gaussian. To do this, move into your ``Unique_EET_Gaussian_Jobs`` folder and run ``ECCP process_EET`` by typing into the terminal: 

.. code-block:: bash

	cd Unique_EET_Gaussian_Jobs
	ECCP process_EET

This method will go through all the folders in ``Unique_EET_Gaussian_Jobs`` and extract the data from every successfully run ``output.log`` file and 

	1. Place this data into an excel file called ``Unique_EET_Gaussian_Jobs.xlsx``, and two text files called ``Unique_EET_Gaussian_Jobs.txt`` and ``Unique_EET_Gaussian_Jobs_wavenumber.txt``. These are located in the ``EET_Data`` folder that has just been created. 
	2. Also in the newly created ``EET_Data`` folder are text files of the electronic coupling values for particular functionals and basis sets are also be given in the  ``TXT_of_Func_and_basis_sets_Energy`` and ``TXT_of_Func_and_basis_sets_Wavenumber`` folders. These files contain the electron coupling information in meV and in cm :sup:`-1`. 
	3. The ``Individual_EET_Data`` contains electronic coupling values for each dimer in individual text files. 


Processing results of Intermolecular Charge Transfer (ICT) jobs using ``ECCP process_ICT``
******************************************************************************************

It is possible for this program to process the intermolecular charge transfer results from Gaussian jobs and present the results in text and in an excel spreadsheet. If the Gaussian job runs successfully, it will give a ``output.log`` file that matrix data for obtaining intermolecular charge transfer energies, such as hole and electron transfer energies. To do this, move into your ``Unique_Eigendata_Gaussian_Jobs`` folder and run ``ECCP process_ICT`` by typing into the terminal: 

.. code-block:: bash

	cd Unique_Eigendata_Gaussian_Jobs
	ECCP process_ICT

This method will go through all the folders in ``Unique_Eigendata_Gaussian_Jobs`` and extract the data from every successfully run ``output.log`` file and: 

	1. Locate and extract the overlap matrix and molecular orbital (MO) energies and coefficients from the ``output.log`` and save these matrices as txt files called:
		
		* ``orbital_overlap_matrix.txt``: This is the overlap matrix. 
		* ``MO_energies.txt``: These are the energies of the MOs in your monomer/dimer.
		* ``MO_coefficients.txt``: These are the coefficients of the MOs in your monomer/dimer.
		* ``MO_orbital_names.txt``: These are the names and the indices of the MO coefficients that are involved with each atom in your monomer/dimer.
		* ``MO_occupancies.txt``: This file indicates which orbtials are occupied and which orbtials are vacant. 

	2. Remove any matrices from the ``output.log``  files. This is necessary as these matrices can make a ``output.log`` incredibly large (GBs is size). This will reduce the size of the ``output.log`` to a few MBs or less. All the necessary matrix data will be located in txt file as mentioned in (1.). 
	3. Calculate the hole and electron transfer energies and place these values into an excel file called ``Unique_ICT_Gaussian_Jobs.xlsx``, and two text files called ``Unique_ICT_Gaussian_Jobs.txt`` and ``Unique_ICT_Gaussian_Jobs.txt``. These are located in the ``ICT_Data`` folder that has just been created. 
	4. Also in the newly created ``ICT_Data`` folder are text files of the intermolecular charge transfer values for particular functionals and basis sets are also be given in the  ``TXT_of_Func_and_basis_sets_Energy`` and ``TXT_of_Func_and_basis_sets_Wavenumber`` folders. These files contain the intermolecular charge transfer energy values in meV and in cm :sup:`-1`. 
	5. The ``Individual_ICT_Data`` contains intermolecular charge transfer energy values for each dimer in individual text files. 


Processing matrix values from Eigendata jobs using ``ECCP process_Eigendata``
*****************************************************************************

Instead of processing the ICT jobs completely, you may just want to obtain the matrix text files from the Eigendata folder. If you only want to process the matrix data from your successfully run ``output.log`` files, move into your ``Unique_Eigendata_Gaussian_Jobs`` folder and run ``ECCP process_Eigendata`` by typing into the terminal: 

.. code-block:: bash

	cd Unique_Eigendata_Gaussian_Jobs
	ECCP process_Eigendata

This method will go through all the folders in ``Unique_Eigendata_Gaussian_Jobs`` and extract the data from every successfully run ``output.log`` file and: 

	1. Locate and extract the overlap matrix and molecular orbital (MO) energies and coefficients from the ``output.log`` and save these matrices as txt files called:
		
		* ``orbital_overlap_matrix.txt``: This is the overlap matrix. 
		* ``MO_energies.txt``: These are the energies of the MOs in your monomer/dimer.
		* ``MO_coefficients.txt``: These are the coefficients of the MOs in your monomer/dimer.
		* ``MO_orbital_names.txt``: These are the names and the indices of the MO coefficients that are involved with each atom in your monomer/dimer.
		* ``MO_occupancies.txt``: This file indicates which orbtials are occupied and which orbtials are vacant. 

	2. Remove any matrices from the ``output.log``  files. This is necessary as these matrices can make a ``output.log`` incredibly large (GBs is size). This will reduce the size of the ``output.log`` to a few MBs or less. All the necessary matrix data will be located in txt file as mentioned in (1.). 

Remove large and unnecessary files using ``ECCP tidy``
******************************************************

Gaussian produces a number of files that are not needed once the calculation has finished. Many of these calculation are large and do not provide any further necessary information. These include ``.chk``, ``.d2e``, ``.int``, ``.rwf``, and ``.skr`` files. Removing these files saves space and makes data management much easier. 

To use this program, move into the overall path that contains all your Gaussian jobs, and type ``ECCP tidy`` into the terminal:

.. code-block:: bash

	cd path/to/gaussian/jobs
	ECCP tidy

Note that this program will only remove the files of jobs that have successfully finished. ``ECCP`` will check to make sure the job has completed successfully before removing unnecessary files. 









