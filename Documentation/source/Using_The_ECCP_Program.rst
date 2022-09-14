
.. _Using_The_ECCP_Program:

How To Use The Electronic Crystal Calculation Prep Program
##########################################################

The Electronic Crystal Calculation Prep (ECCP) program is run using a script called ``Run_ECCP.py``. This contains information about all the crystals you want to obtain molecules and dimers for, as well as the parameters required to create atomic transition charge (ATC), reorganisation energy (RE), and electronic energy transfer (EET) gaussian input files for those molecules and dimers. 

.. _Run_ECCP_py_example:

An example of this script is shown below. General recommendation for settings are given in :ref:`Recommendation_For_Settings`. 

.. code-block:: python

	"""
	Run_ECCP.py, Geoffrey Weal, 18/2/22

	This script is an example input script for the Electronic Crystal Calculation Prep program.
	"""
	import os
	from ECCP import ECCP

	# --------------------------------------------------------------------------------------------------------------
	# --------------------------------------------------------------------------------------------------------------
	# These are the parameters needed for the dimer method. 
	# See https://github.com/geoffreyweal/ECCP for more information about these parameters

	# This is the method use to reassemble individual molecule from the crystal. 
	make_molecule_method = 'component_assembly_approach'
	# This dictionary include information about determining which molecules are equivalent. Required if you want to perform ATC calculations on molecules.
	molecule_equivalence_method = {'method': 'invariance_method', 'type': 'combination'} 

	# This is the method use to obtain dimers between molecules in the system.
	dimer_method = {'method': 'nearest_atoms_method', 'max_dimer_distance': 5.0}
	# This dictionary provides information for determining which dimers are equivalent
	dimer_equivalence_method = {'method': 'invariance_method', 'type': 'combination'} 

	# This tag indicates if you want to remove solvents from the crystal. This requires the input file to have a reference to which molecules are solvents called "SolventList"
	remove_solvents = False

	# --------------------------------------------------------------------------------------------------------------
	# --------------------------------------------------------------------------------------------------------------
	# The following dictionaries are required if you want to perform Gaussian and Multiwfn jobs on your molecules and dimers

	# --------------------------------------------------------------------------------------------------------------
	# The following dictionaries provide the Gaussian parameters and Submission information required for performing 
	# Atomic Transition Charge (ATC) calculations on your molecules.

	# This dictionary will add tags to your gaussian .gjf file
	gaussian_parameters_for_atomic_transition_charges = {}
	gaussian_parameters_for_atomic_transition_charges['mem']         = '48GB'
	gaussian_parameters_for_atomic_transition_charges['method']      = 'wB97XD'
	gaussian_parameters_for_atomic_transition_charges['basis']       = '6-31+G(d,p)'
	gaussian_parameters_for_atomic_transition_charges['td_settings'] = 'tda(nstates=10)'
	gaussian_parameters_for_atomic_transition_charges['obtain_excitation_amplitudes'] = False
	gaussian_parameters_for_atomic_transition_charges['extra']       = '# maxdisk=2TB'

	# This dictionary will add tags to your submit.sl file for performing Gaussian Calculations to get the initial ATC wfn files and to perofmr EET calculations
	submission_information_for_atomic_transition_charges = {}
	submission_information_for_atomic_transition_charges['cpus_per_task']    = 12
	submission_information_for_atomic_transition_charges['mem']              = '60GB' # This has been set to gaussian_parameters_for_atomic_transition_charges['mem'] + 12 GBs
	submission_information_for_atomic_transition_charges['time']             = '10-00:00'
	submission_information_for_atomic_transition_charges['partition']        = 'parallel'
	submission_information_for_atomic_transition_charges['constraint']       = 'AVX'
	submission_information_for_atomic_transition_charges['email']            = 'your_email@email.com'
	submission_information_for_atomic_transition_charges['gaussian_version'] = 'gaussian/g16'
	submission_information_for_atomic_transition_charges['python_version']   = 'python/3.8.1'

	# This tag indicates if you want to obtain Gaussian input files of molecules for performing ATC calculations. 
	submission_information_for_multiwfn = {}
	submission_information_for_multiwfn['cpus_per_task'] = 12
	submission_information_for_multiwfn['mem']           = '24GB'
	submission_information_for_multiwfn['time']          = '1-00:00'
	submission_information_for_multiwfn['partition']     = 'parallel'
	submission_information_for_multiwfn['constraint']    = 'AVX'
	submission_information_for_multiwfn['email']         = 'your_email@email.com'

	# --------------------------------------------------------------------------------------------------------------
	# The following dictionaries provide the Gaussian parameters and Submission information required for performing 
	# reorganisation energy (RE) calculations on your molecules.

	# This dictionary will add tags to your gaussian .gjf file
	gaussian_parameters_for_reorganisation_energy = {}
	gaussian_parameters_for_reorganisation_energy['mem']         = '96GB'
	gaussian_parameters_for_reorganisation_energy['method']      = gaussian_parameters_for_atomic_transition_charges['method']
	gaussian_parameters_for_reorganisation_energy['basis']       = gaussian_parameters_for_atomic_transition_charges['basis']
	gaussian_parameters_for_reorganisation_energy['td_settings'] = gaussian_parameters_for_atomic_transition_charges['td_settings']
	gaussian_parameters_for_reorganisation_energy['extra']       = '# maxdisk=2TB'

	# This tag indicates if you want to obtain Gaussian input files of molecules for performing ATC calculations. 
	submission_information_for_reorganisation_energy = {}
	submission_information_for_reorganisation_energy['cpus_per_task']    = 24
	submission_information_for_reorganisation_energy['mem']              = '120GB' # This has been set to gaussian_parameters_for_reorganisation_energy['mem'] + 24 GBs
	submission_information_for_reorganisation_energy['time']             = '10-00:00'
	submission_information_for_reorganisation_energy['partition']        = 'parallel'
	submission_information_for_reorganisation_energy['constraint']       = 'AVX'
	submission_information_for_reorganisation_energy['email']            = 'your_email@email.com'
	submission_information_for_reorganisation_energy['gaussian_version'] = 'gaussian/g16'
	submission_information_for_reorganisation_energy['python_version']   = 'python/3.8.1'

	# --------------------------------------------------------------------------------------------------------------
	# The following dictionaries provide the Gaussian parameters and Submission information required for performing 
	# Electronic Energy Transfer (EET) calculations on your molecules.

	# This dictionary will add tags to your gaussian .gjf file
	gaussian_parameters_for_electronic_energy_transfer = {}
	gaussian_parameters_for_electronic_energy_transfer['mem']         = '48GB'
	gaussian_parameters_for_electronic_energy_transfer['method']      = gaussian_parameters_for_atomic_transition_charges['method']
	gaussian_parameters_for_electronic_energy_transfer['basis']       = gaussian_parameters_for_atomic_transition_charges['basis']
	gaussian_parameters_for_electronic_energy_transfer['td_settings'] = gaussian_parameters_for_atomic_transition_charges['td_settings']
	gaussian_parameters_for_electronic_energy_transfer['obtain_excitation_amplitudes'] = False
	gaussian_parameters_for_electronic_energy_transfer['extra']       = '# maxdisk=2TB'

	# This dictionary will add tags to your submit.sl file for performing Gaussian Calculations to get the initial ATC wfn files and to perform EET calculations
	submission_information_for_electronic_energy_transfer = {}
	submission_information_for_electronic_energy_transfer['cpus_per_task']    = 12
	submission_information_for_electronic_energy_transfer['mem']              = '60GB' # This has been set to gaussian_parameters_for_electronic_energy_transfer['mem'] + 12 GBs
	submission_information_for_electronic_energy_transfer['time']             = '10-00:00'
	submission_information_for_electronic_energy_transfer['partition']        = 'parallel'
	submission_information_for_electronic_energy_transfer['constraint']       = 'AVX'
	submission_information_for_electronic_energy_transfer['email']            = 'your_email@email.com'
	submission_information_for_electronic_energy_transfer['gaussian_version'] = 'gaussian/g16'
	submission_information_for_electronic_energy_transfer['python_version']   = 'python/3.8.1'

	# --------------------------------------------------------------------------------------------------------------
	# The following dictionaries provide the Gaussian parameters and Submission information required for obtaining 
	# eigendata (such as overlap orbtials and molecular orbital energies and coefficients).

	# This dictionary will add tags to your gaussian .gjf file
	gaussian_parameters_for_eigendata = dict(gaussian_parameters_for_electronic_energy_transfer)

	# This dictionary will add tags to your submit.sl file for performing Gaussian Calculations to obtain eigendata.
	submission_information_for_eigendata = dict(submission_information_for_electronic_energy_transfer)

	# --------------------------------------------------------------------------------------------------------------
	# These tag provide the information to the ECCP about Gaussian parameters and submission information for performing ATC, RE, and/or EET calculations and/or obtain eigendata (such as overlap orbtials and molecular orbital energies and coefficients).
	# If you dont want to perform a task, set the appropriate take to None. For example: if you don't want to perform ATC calcs, set get_molecule_atcs = None 

	# This tag indicates if you want to obtain Gaussian input files of molecules for performing ATC calculations. 
	get_molecule_atcs = (gaussian_parameters_for_atomic_transition_charges, submission_information_for_atomic_transition_charges, submission_information_for_multiwfn)
	# This tag indicates if you want to obtain Gaussian input files to obtain the disorder energies of the molecules in the crystal.
	get_molecule_res = (gaussian_parameters_for_reorganisation_energy, submission_information_for_reorganisation_energy)
	# This tag indicates if you want to obtain Gaussian input files of dimers for performing EET calculations. 
	get_dimer_eets = (gaussian_parameters_for_electronic_energy_transfer, submission_information_for_electronic_energy_transfer)
	# This tag indicates if you want to obtain Gaussian input files of dimers for obtaining eigendata (such as overlap orbtials and molecular orbital energies and coefficients).
	get_dimer_eigendata = (gaussian_parameters_for_eigendata, submission_information_for_eigendata)

	# --------------------------------------------------------------------------------------------------------------

	# --------------------------------------------------------------------------------------------------------------
	# These are the directories to the crystal files of OPV you would like to analyse with this Dimer Pairer method
	folder = 'editted_crystals'
	files_not_to_examine = [] #['itic-2cl-g.cif', 'itic-2cl-y.cif', 'EH-IDTBR.cif']
	filepaths = sorted([folder+'/'+file for file in os.listdir(folder) if (os.path.isfile(folder+'/'+file) and file.endswith('.xyz') and (file not in files_not_to_examine))])
	#filepaths = [folder+'/'+'Y6_MUPMOC_editted.xyz']
	# --------------------------------------------------------------------------------------------------------------

	# --------------------------------------------------------------------------------------------------------------
	# This will run this method
	for filepath in filepaths:
		ECCP(filepath, make_molecule_method=make_molecule_method, molecule_equivalence_method=molecule_equivalence_method, dimer_method=dimer_method, dimer_equivalence_method=dimer_equivalence_method, remove_solvents=remove_solvents, get_molecule_atcs=get_molecule_atcs, get_molecule_res=get_molecule_res, get_dimer_eets=get_dimer_eets, get_dimer_eigendata=get_dimer_eigendata)
	# --------------------------------------------------------------------------------------------------------------


The first set of parameters involves providing the file path to the crystal file you would like to process with the ECCP program: 

	* ``filepath`` (*str.*): The directory to the crystal file of OPV or chemical system you would like to analyse with this program.

The second set of parameters involves obtaining the individual molecules from the crystal: 

	* ``make_molecule_method`` (*str.*): This is the method you would like to use to reconnect a molecule from a crystal into a more human-friendly form. See :ref:`Make_Molecules_Methods` for more information about the ``make_molecule_method`` methods available. 

The third set of parameters involves determining which molecules are unique and which are equivalent to each other: 

	* ``molecule_equivalence_method`` (*dict.*): This dictionary indicates the method that you want to use to determine which molecules in the crystal are unique (and which ones are equivalent to each other). See :ref:`Determine_Equivalent_Molecules_Methods` for more information about the ``molecule_equivalence_method`` methods available. 
	
The fourth set of parameters involves creating dimers from pairs of molecules from the crystal.

	* ``dimer_method`` (*dict.*): This dictionary contains the information required for determining how dimers are determined/obtained by this program. See :ref:`Make_Dimers_Methods` for more information about the ``dimer_method`` methods available. 

The fifth set of parameters involve determining which dimers are unique and which are equivalent to each other: 

	* ``dimer_equivalence_method`` (*dict.*): This dictionary contains information required for determining which dimers were equivalent and which were unique. See :ref:`Determine_Equivalent_Dimers_Methods` for more information about the ``dimer_equivalence_method`` methods available. 

The sixth set of parameters involve determining if you want to include solvents as monomers in your dimers.

	* ``remove_solvents`` (*bool.*): If ``True``, will include solvents as monomers in your dimers. If ``False``, will not include solvents as monomers in your dimers.

The seventh set of parameters involves indicating which types of Gaussian files you would like to create for the molecules and dimers obtained with the ECCP program.

	* ``get_molecule_atcs``: This variable indicates if you want to write atomic transition charge (ATC) gaussian input files for the molecules found in this crystal. If you would like to perform ATC calculations, see :ref:`get_molecule_atcs` below. If you do not want to perform ATC calculation, set this variable to ``None``. 
	* ``get_molecule_res``: This variable indicates if you want to write reorganisation energy (RE) gaussian input files for the molecules found in this crystal. If you would like to perform ATC calculations, see :ref:`get_molecule_res` below. If you do not want to perform ATC calculation, set this variable to ``None``. 
	* ``get_dimer_eets``: This variable indicates if you want to write electronic energy transfer (EET) gaussian input files for the dimers found in this crystal. If you would like to perform ATC calculations, see :ref:`get_dimer_eets` below. If you do not want to perform ATC calculation, set this variable to ``None``. 
	* ``get_dimer_eigendata``: This variable indicates if you want to write gaussian input files for obtaining eigendata matrices (such as overlap intergral matrices, molecular orbital (MO) energies, and MO coefficients) for the monomers and dimers found in this crystal. These matrices are useful if you would like to perform intermolecular charge transfer (ICT) calculations upon your dimers to study the intermolecular charge transfers betweem monomers (individual molecules) in your crystals. If you would like to perform Gaussian calculations for obtaining eigendata matrices or perform ICT calculations, see :ref:`get_dimer_icts` below. If you do not want to obtain eigendata matrices or perform ICT calculations, set this variable to ``None``. 

.. _get_molecule_atcs:

Dictionaries needed for obtaining atomic transition charge (ATC) input files for Monomers
*****************************************************************************************

If you would like to obtain input files for performing atomic transition charge (ATC) calculations, you will want to provide three dictionaries for the ``get_molecule_atcs`` variable. These are:

	* ``gaussian_parameters_for_atomic_transition_charges`` (*dict.*): This dictionary contains information required for the Gaussian files for performing ATC Gaussian calculations.
	* ``submission_information_for_atomic_transition_charges`` (*dict.*): This dictionary contains information required for making the ``submit.sl`` file for submitting ATC jobs to slurm. 
	* ``submission_information_for_multiwfn`` (*dict.*): This dictionary contains information required for the ``multiwfn_submit.sl`` file. This submit script will run the Multiwfn component of the calculation, where the ``.wfn`` created by Gaussian is used to perform the ATC calculation to obtain the ``.chg`` file of the molecule. This ``.chg`` file contains the atomic transition charges for the molecule. 

If you would like to perform ATC calculations for the molcules, you want to set ``get_molecule_atcs`` as:

.. code-block:: python

	get_molecule_atcs = (gaussian_parameters_for_atomic_transition_charges, submission_information_for_atomic_transition_charges, submission_information_for_multiwfn)

where ``gaussian_parameters_for_atomic_transition_charges`` , ``submission_information_for_atomic_transition_charges``, and ``submission_information_for_multiwfn`` are given :ref:`like in the example above <Run_ECCP_py_example>`. Also see :ref:`Gaussian Parameter Settings <gaussian_parameters_settings>` and :ref:`Submission Information Settings <submission_information_settings>` for more information about what settings you want to include in these dictionaries. 

If you do not want to perform ATC calculations for the molcules, you want to set ``get_molecule_atcs = None``:

.. code-block:: python

	get_molecule_atcs = None


.. _get_molecule_res:

Dictionaries needed for obtaining reorganisation energy (RE) input files for Monomers
*************************************************************************************

If you would like to obtain input files for performing reorganisation energy (RE) calculations, you will want to provide two dictionaries for the ``get_molecule_res`` variable. These are:

	* ``gaussian_parameters_for_reorganisation_energy`` (*dict.*): This dictionary contains information required for the Gaussian files for performing RE Gaussian calculations.
	* ``submission_information_for_reorganisation_energy`` (*dict.*): This dictionary contains information required for making the ``submit.sl`` file for submitting RE jobs to slurm. 

If you would like to perform RE calculations for the dimers, you want to set ``get_molecule_res`` as:

.. code-block:: python

	get_molecule_res = (gaussian_parameters_for_reorganisation_energy, submission_information_for_reorganisation_energy)

where ``gaussian_parameters_for_reorganisation_energy``  and ``submission_information_for_reorganisation_energy`` are given :ref:`like in the example above <Run_ECCP_py_example>`. Also see :ref:`Gaussian Parameter Settings <gaussian_parameters_settings>` and :ref:`Submission Information Settings <submission_information_settings>` for more information about what settings you want to include in these dictionaries. 

If you do not want to perform ATC calculations for the molcules, you want to set ``get_molecule_res = None``:

.. code-block:: python

	get_molecule_res = None


.. _get_dimer_eets:

Dictionaries needed for obtaining electronic energy transfer (EET) input files for Dimers
*****************************************************************************************

If you would like to obtain input files for performing electronic energy transfer (EET) calculations, you will want to provide two dictionaries for the ``get_dimer_eets`` variable. These are:

	* ``gaussian_parameters_for_electronic_energy_transfer`` (*dict.*): This dictionary contains information required for the Gaussian files for performing EET Gaussian calculations.
	* ``submission_information_for_electronic_energy_transfer`` (*dict.*): This dictionary contains information required for making the ``submit.sl`` file for submitting EET jobs to slurm. 

If you would like to perform EET calculations for the dimers, you want to set ``get_dimer_eets`` as:

.. code-block:: python

	get_dimer_eets = (gaussian_parameters_for_electronic_energy_transfer, submission_information_for_electronic_energy_transfer)

where ``gaussian_parameters_for_electronic_energy_transfer``  and ``submission_information_for_electronic_energy_transfer`` are given :ref:`like in the example above <Run_ECCP_py_example>`. Also see :ref:`Gaussian Parameter Settings <gaussian_parameters_settings>` and :ref:`Submission Information Settings <submission_information_settings>` for more information about what settings you want to include in these dictionaries. 

If you do not want to perform EET calculations for the dimers, you want to set ``get_dimer_eets = None``:

.. code-block:: python

	get_dimer_eets = None


.. _get_dimer_icts:

Dictionaries needed for obtaining eigendata that is used to obtain intermolecular charge transfer (ICT) input files for Dimers
******************************************************************************************************************************

Intermolecular charge transfer coupling values can be obtained for charge transfer between monomers (in a dimer) by obtaining the eigendata from Gaussians upon the dimer and the two monomers that are apart of the dimer. This includes obtaining overlap matrices, MO energies, and MO coefficients. 

If you would like to obtain input files for performing intermolecular charge transfer (ICT) calculations, you will want to provide two dictionaries for the ``get_dimer_eigendata`` variable. These are:

	* ``gaussian_parameters_for_eigendata`` (*dict.*): This dictionary contains information required for the Gaussian files for obtaining eigendata from your monomers and dimers. 
	* ``submission_information_for_eigendata`` (*dict.*): This dictionary contains information required for making the ``submit.sl`` file for submitting eigendata gathering jobs to slurm. 

If you would like to perform ICT calculations for the dimers, you want to set ``get_dimer_eigendata`` as:

.. code-block:: python

	get_dimer_eigendata = (gaussian_parameters_for_eigendata, submission_information_for_eigendata)

where ``gaussian_parameters_for_eigendata``  and ``submission_information_for_eigendata`` are given :ref:`like in the example above <Run_ECCP_py_example>`. Also see :ref:`Gaussian Parameter Settings <gaussian_parameters_settings>` and :ref:`Submission Information Settings <submission_information_settings>` for more information about what settings you want to include in these dictionaries. 

If you do not want to perform ICT calculations for the dimers, you want to set ``get_dimer_eigendata = None``:

.. code-block:: python

	get_dimer_eigendata = None


Examples of Input Files
***********************

The folder called ``Examples`` contains all the files that are needed to run the ECCP program. This includes examples of the ``Run_ECCP.py`` file. 




