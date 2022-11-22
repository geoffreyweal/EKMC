
.. _Setting_Up_The_EKMC_Program:

How To Setup The Exciton kinetic Monte Carlo (EKMC) Program
###########################################################

The Exciton kinetic Monte Carlo (EKMC) program is run in two stages:

	1. The EKMC simulations are first setup using the ``setup_EKMC_sims.py`` script.
	2. This makes several ``Run_EKMC.py`` that run your exciton kinetic Monte Carlo simulation. 

We will begin by describing how to use the ``setup_EKMC_sims.py`` script to create and setup all the files needed to run your excitonic kinetic Monte Carlo simulations. 

The ``setup_EKMC_sims.py`` script contains all the information required to setup your excitonic kinetic Monte Carlo simulations for all of the crystals you wish to perform simulations upon. The ``EKMC`` program will use the information to obtain information necessary for performing kinetic Monte Carlo simulations, such as the rate constants for excitons moving from one molecule to another molecule throughout your crystal. 

.. _setup_EKMC_sims_py_example:

An example of the ``setup_EKMC_sims.py`` script is shown below. General recommendation for settings are given in :ref:`Recommendation_For_Settings`. 

.. code-block:: python

	"""
	setup_EKMC_sims.py, Geoffrey Weal, 17/9/22

	This script is designed to setup your excitonic kinetic Monte Carlo files for running multiple simulations.
	"""
	from math import pi
	from copy import deepcopy
	from EKMC import EKMC_Multi_Setup

	h_bar = 6.582119569 * (10.0 ** -16.0) # eV s
	plancks_constant = h_bar * 2.0 * pi # eVs
	speed_of_light = 29979245800 # cms-1

	# -----------------------------------------------------------------------------------------------
	# First: Give general settings.

	functional_and_basis_set = 'F_wB97XD_B_6_31plusGd_p'
	kinetic_model = 'Marcus'

	frequency_wavenumber = 1500 # cm-1
	Wang_number = plancks_constant * speed_of_light * frequency_wavenumber

	temperature = 300

	general_temp_folder_path = '/tmp/wealge/'

	# -----------------------------------------------------------------------------------------------
	# Second: Give settings for each crystal and electronic settings.

	crystal_names = ['Y6', 'EH-IDTBR', 'ITIC', 'itic-2cl-g', 'itic-2cl-y', 'ITIC-4F']

	energetic_disorders = {'Y6': 56, 'IDIC': 34, 'ITIC': 53, 'itic-2cl-g': 45, 'itic-2cl-y': 45, 'ITIC-4F': 39, 'EH-IDTBR': 48}
	for crystal_shortname in energetic_disorders.keys():
		energetic_disorders[crystal_shortname] = energetic_disorders[crystal_shortname] / 1000.0

	relative_permittivities = {'Y6': 5, 'IDIC': 4, 'ITIC': 5, 'itic-2cl-g': 4, 'itic-2cl-y': 4, 'ITIC-4F': 4, 'EH-IDTBR': 4}
	huang_rhys_factors      = {'Y6': 0.294, 'IDIC': None, 'ITIC': None, 'itic-2cl-g': 0.5291, 'itic-2cl-y': 0.4798, 'ITIC-4F': 0.6591, 'EH-IDTBR': 0.5819}
	reorganisation_energies = {'Y6': 0.26623, 'IDIC': None, 'ITIC': None, 'itic-2cl-g': 0.41139443, 'itic-2cl-y': 0.316988, 'ITIC-4F': 0.311641, 'EH-IDTBR': 0.38139}

	# -----------------------------------------------------------------------------------------------
	# Third, obtain all the settings for all the EKMC simulations you would like to perform.

	all_EKMC_settings = []
	for crystal_name in crystal_names:
		for coupling_disorder in range(0,55,5):

			molecules_path  = 'Electronic_Calculations_Results/ECCP_Data/ECCP_Information/'+crystal_name
			ATC_folder_path = 'Electronic_Calculations_Results/ECCP_Data/Unique_ATC_Gaussian_Jobs/'+crystal_name

			Individual_EET_folder_path = 'Electronic_Calculations_Results/ECCP_Data/Unique_EET_Gaussian_Jobs'
			dimer_couplings = {'Use_non_atc_model_for_dimers': True, 'path_to_dimer_information_file': Individual_EET_folder_path}

			kinetics_details = {}
			kinetics_details['energetic_disorder'] = energetic_disorders[crystal_name]
			coupling_disorder = str(float(coupling_disorder))+'%'
			kinetics_details['coupling_disorder'] = coupling_disorder
			kinetics_details['relative_permittivity'] = relative_permittivities[crystal_name]
			huang_rhys_factor = huang_rhys_factors[crystal_name]
			reorganisation_energy = reorganisation_energys[crystal_name]
			kinetics_details['classical_reorganisation_energy'] = reorganisation_energy - huang_rhys_factor*Wang_number
			kinetics_details['temperature'] = temperature

			neighbourhood_rCut = 40.0 # A
			sim_time_limit = 1000 # ps
			max_no_of_steps = 'inf'

			store_data_in_databases = False
			no_of_molecules_at_cell_points_to_store_on_RAM = None

			crystal_settings = {'folder_name': crystal_name+'/'+str(coupling_disorder), 'general_temp_folder_path': general_temp_folder_path'molecules_path': molecules_path, 'ATC_folder_path': ATC_folder_path, 'functional_and_basis_set': functional_and_basis_set, 'kinetic_model': kinetic_model, 'dimer_couplings': dimer_couplings, 'kinetics_details': kinetics_details, 'neighbourhood_rCut': neighbourhood_rCut, 'sim_time_limit': sim_time_limit, 'max_no_of_steps': max_no_of_steps, 'store_data_in_databases': store_data_in_databases, 'no_of_molecules_at_cell_points_to_store_on_RAM': no_of_molecules_at_cell_points_to_store_on_RAM}

			all_EKMC_settings.append(crystal_settings)

	# -----------------------------------------------------------------------------------------------
	# Fourth, obtaining the dictionary that will add tags to your ekmc_mass_submit.sl files

	mass_submission_information = {}
	mass_submission_information['ntasks_per_node'] = 1
	mass_submission_information['mem'] = '4GB'
	mass_submission_information['time'] = '0-08:00'
	mass_submission_information['partition'] = 'parallel'
	mass_submission_information['constraint'] = 'AVX'
	mass_submission_information['email'] = 'geoffreywealslurmnotifications@gmail.com'
	mass_submission_information['python_version'] = 'python/3.8.1'

	mass_submission_information['submission_type'] = 'full'
	mass_submission_information['no_of_simulations'] = 2000
	#mass_submission_information['no_of_packets_to_make'] = 100

	all_mass_submission_information = [deepcopy(mass_submission_information)]*len(all_EKMC_settings)

	# -----------------------------------------------------------------------------------------------
	# Fifth, setup all your excitonic kinetic Monte Carlo simulations!

	EKMC_Multi_Setup(all_EKMC_settings=all_EKMC_settings, all_mass_submission_information=all_mass_submission_information)

	# -----------------------------------------------------------------------------------------------


The first set of parameters involves providing general settings for your EKMC simulations that will be the same for each system. These are:

	* ``functional_and_basis_set`` (*str.*): This is the functional and basis set that you perform DFT calculations with to obtain atomic transition charges (ATC), electronic energy transfer (EET) values, reorganisation energies, and other parameters. 
	* ``kinetic_model`` (*str.*): This is the kinetic model you would like to use. There are two options available; ``'Marcus'``: Use Marcus theory, ``'MLJ'``: Use Marcus-Levich-Jortner theory. See https://doi.org/10.1063/1.4920945 for more information. 
	* ``temperature`` (*float.*): This is the temperature of the system of interest. 
	* ``general_temp_folder_path`` (*str.*/None): This is the path to place files as the KMC file is running for temporary storage. This is not vital for running a simulation. If set to None, no temporary folder will be created. Dafault: ``None`` 

There are another two parameters that have been given in this example, called ``frequency_wavenumber`` and ``Wang_number``. The ``frequency_wavenumber`` is the XXX, while the Wang's number is the XXX. These are used in this example to obtain the classical component of the reorganisation energy. See later in this documentation page. 


The second set of parameters involves obtaining the settings that are specific for each crystal given. These include: 

	* ``energetic_disorders`` (*dict.* of *floats*): These are the disorder values that are assigned to the energies of the molecules in each crystal. This is used to obtain the energies of molecules in a crystal that has some disorder assigned to them, due to manufacturing of the crystal and the temperature of the system. The energy of a molecule in a crystal is given currently as a Gaussian (normal) probability distribution, where the mean is given as 0.0 eV, and the standard deviation is given by the ``energetic_disorders`` value for that crystal. See https://en.wikipedia.org/wiki/Normal_distribution for more information about the Gaussian (normal) probability distribution. 
	* ``coupling_disorders`` (*dict.* of *floats*): These are the disorder values that are assigned to each coupling energy (obtained by the EET/ATC calculations) in each crystal. This is used to obtain the coupling energies that indicate how easy it is for an exciton to hop from molecule to molecule in the crystal that has some disorder assigned to them, due to manufacturing of the crystal and the temperature of the system. The energy of a molecule in a crystal is given currently as a Gaussian (normal) probability distribution, where the mean is given as the coupling energy between two molecules in the crystal, and the standard deviation is given by the ``coupling_disorders`` value for that crystal. See https://en.wikipedia.org/wiki/Normal_distribution for more information about the Gaussian (normal) probability distribution. 
	* ``relative_permittivities`` (*dict.* of *floats*): This is the relative permittivity for the crystal. This is used when the ATC coupling energy is used to obtain the coupling energy for molecules that are far away from each other in the crystal, which contain other molecules inbetween them, essentially electronically insulating those two molecules and making it harder for an exciton to hop between two molecules. 

There are two other parameters that have been given in this example, called ``huang_rhys_factors`` and ``reorganisation_energies``. The ``huang_rhys_factors`` is the XXX, while ``reorganisation_energies`` is the XXX. These are used in this example to obtain the classical component of the reorganisation energy. See later in this documentation page. 


The third set of parameters involves obtaining the EKMC settings for each crystal of interest. These are placed in the ``crystal_settings`` dictionary. These EKMC settings are:

	* ``'folder_name'`` (*str.*): This is the path that you want to save the ``EKMC`` files for running the ``EKMC`` algorithm to.
	* ``'molecules_path'`` (*str.*): This is the path to the crystal folder in the ``ECCP_Information`` folder, as obtained by the ``ECCP`` program. 
	* ``'ATC_folder_path'`` (*str.*): This is the path to all the unique molecules in the crystal. These are obtained using the ``ECCP`` program. 
	* ``'dimer_couplings'`` (*dict.*): This is a dictionary that indicates if you want to use a non-ATC model to obtain the electronic coupling values between molecules in the crystal that are close to each other (neighbouring). This is for example using the values obtained from electronic energy transfer (EET) values. This dictionary requires the given inputs:

		* ``'Use_non_atc_model_for_dimers'`` (*bool.*): This indicates if you want to use the coupling energy values from another model to close-range coupling (between neighbouring molecules). 
		* ``'path_to_dimer_information_file'`` (*str.*): If you have set ``'Use_non_atc_model_for_dimers'`` to ``True``, this variable is needed to direct the ``EKMC`` algorithm to the files that contain the coupling energies for close-range coupling. For example, this is where the electronic energy transfer (EET) values would be placed. 

	* ``'kinetics_details'`` (*dict.*): This dictionary contains various details required for obtaining exciton hopping rates from molecule to molecule in the crystal. The details contained in this dictionary are:

		* ``'energetic_disorder'`` (*float*): See the ``energetic_disorders`` details above.
		* ``'coupling_disorder'`` (*float*): See the ``coupling_disorders`` details above.
		* ``'relative_permittivity'`` (*float*): See the ``relative_permittivities`` details above.
		* ``'classical_reorganisation_energy'`` (*float*): This is the classical component of the reorganisation energy for a molecule in the crystal. 
		* ``'temperature'`` (*float*): This is the temperature of the system. 

	* ``'neighbourhood_rCut'`` (*float.*): This is the distance from the exciton molecule to surrounding molecules that will have electronic coupling energies attach to them. Within this rCut distance, the coupling energy will be assigned to the molecule-molecule pair, which is calculated using either the atomic transition charge (ATC) method, or another method, such as the electronic energy transfer (EET) energy. 
	* ``'sim_time_limit'`` (*float.* or *str.*): This is the maximum time you would like to simulate the exciton hopping over. If you would like this to be unlimited, set this to ``'inf'``. The time is given in picoseconds. For example, to simulate 1ns, set this to ``1000.0``. 
	* ``'max_no_of_steps'`` (*int.* or *str.*): This is the maximum number of excitonic hops you would like to simulate. If you would like this to be unlimited, set this to ``'inf'``.
	* ``'store_data_in_databases'`` (*bool.*): If you would like to store the data from the simulation, such as the molecule energies and coupling energies (including disorder), set this to ``True``. Otherwise, set this to ``False``. This is useful to set to ``True`` if you would like to extend a simulation if the future. 
	* ``'no_of_molecules_at_cell_points_to_store_on_RAM'`` (*int.*): To do. 


The fourth set of parameters involves inputting the settings of the ``ekmc_mass_submit.sl`` file that is used to submit all the repeated EKMC simulations to slurm. These are placed in the ``mass_submission_information`` dictionary. These mass submission settings are:

	* ``'ntasks_per_node'`` (*int*): This is the number of cpus you would like assigned to each simulation. This should always be set to ``1``. 
	* ``'mem'`` (*str.*): This is the amount of memory to give each simulation when run in slurm. For example, if you want to assign 4 GBs to a job, set this to ``'4GB'``. This is given as a string to include the memory time (e.g. MB: megabytes, GB: gigabytes)
	* ``'time'`` (*str.*): This is the amount of time to give to each simulation when running in slurm. Set this as ``'D-HH:MM'``, where D: Days, HH: Hours, MM: Minutes. 
	* ``'partition'`` (*str.*): This is the partition to run this job on in slurm. This is specific to the computer cluster you are using. 
	* ``'email'`` (*str.*): This is the email address to send information to about the running of your slurm jobs. 
	* ``'python_version'`` (*str.*): This is the version of Python 3 you want to use. On your computer cluster system, write in ``module avail python`` to see what versions of python are available on your computer cluster. 

As well as the amove slurm settings, we also indicate in this dictionary the number of simulations we would like to run.

	* ``'no_of_simulations'`` (*int*): This is the number of repeated simulation you would like to perform. 

If your simulations finish within 5 minutes, it is adviced for some computer clusters to run 10 or so KMC simulations together in the same slurm job. This is because slurm is often not good if lots of jobs do not have long to run and finish at similar times, and slurm can break in some cases. The following parameters allow you to packet some of these KMC simulations into the same slurm job if necessary:

	* ``'submission_type'`` (*str.*): If this is set to ``'full'``, each simulation is run individually. If this is set to ``'packets'``, A number of consecutive simulations will be run in packets one after the other. 
	* ``'no_of_packets_to_make'`` (*int*): If ``'submission_type'`` is set to ``'packets'``, this is the number of simulations to packet together in the same slurm submission. 


Once these settings are all sorted, you are ready to run this python script by running in the terminal

.. code-block:: bash

	python setup_EKMC_sims.py


What will ``setup_EKMC_sims.py`` do
-----------------------------------

See :ref:`What_will_setup_EKMC_sims_py_do` for the full explanation of the files that will be created by this script. 















