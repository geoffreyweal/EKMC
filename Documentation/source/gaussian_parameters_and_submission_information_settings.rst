
.. _gaussian_parameters_and_submission_information_settings:

Gaussian Parameters and Submission Information Settings
#######################################################

The following provide information about the settings and other advice for the Gaussian parameters and submission information dictionaries required for running this program.


.. _gaussian_parameters_settings:

Tags needed for the ``gaussian_parameters`` dictionaries
********************************************************

The ``gaussian_parameters_for_atomic_transition_charges``, ``gaussian_parameters_for_reorganisation_energy``, ``gaussian_parameters_for_electronic_energy_transfer``, and ``gaussian_parameters_for_eigendata`` dictionaries allow you to place the parameters needed for the .gjf file. These include:

* ``'method'`` (*str.*): The level of theory you want to use (i.e. the functional).
* ``'basis'`` (*str.*): The basis set you want to use.
* ``'td_settings'`` (*str.*): This allows you to provide the settings for performing TD-DFT calculations. Default: ``'TD'``
* ``'extra'`` (*str.*): These are any extra tags that you need to add. For example: ``'# maxdisk=2TB'``

Other parameters that can be given in the ``gaussian_parameters_for_atomic_transition_charges``, ``gaussian_parameters_for_electronic_energy_transfer``, and ``gaussian_parameters_for_eigendata`` dictionaries are:

* ``'obtain_excitation_amplitudes'`` (*bool.*): Will include tags in the Gaussian input file for obtaining excitation amplitudes. Default: ``False``

You can also specify where you would like certain files to be placed, particularly if you want to place some of the temporary Gaussian files into a SCRATCH directory. If you want all the temporary files to be placed in a general SCRATCH files, provide a entry for ``'gaussian_scratch_path'`` in ``gaussian_parameters`` dictionary: 

* ``'gaussian_scratch_path'`` (*str.*): This is the path to the SCRATCH directory to place temporary Gaussian files. The default path is the path that your ``.gjf`` file was placed in by this program. 

You can also select specific temporary Gaussian files to be placed in the SCRATCH directory. These are ``'chk'``, ``'rwf'``, ``'int'``, ``'d2e'``, and ``'skr'``. These are given as a boolean where if ``True``, place in the SCRATCH directory you gave in ``gaussian_parameters['gaussian_scratch_path']``, if ``False``, place in the same file as your ``.gjf`` Gaussian input file. Default: ``True``. For example: 

.. code-block:: python

	gaussian_parameters['gaussian_scratch_path'] = '/nfs/scratch2/wealge'
	gaussian_parameters['chk'] = True
	gaussian_parameters['rwf'] = False
	gaussian_parameters['int'] = True
	gaussian_parameters['d2e'] = False
	gaussian_parameters['skr'] = True


Advice for settings for the ``gaussian_parameters`` dictionaries
================================================================

The Gaussian jobs that use the ``gaussian_parameters_for_atomic_transition_charges``, ``gaussian_parameters_for_electronic_energy_transfer``, and ``gaussian_parameters_for_eigendata`` dictionaries perform single point calculations, as well as other calculations for TD-DFT calculations. The Gaussian jobs that use the ``gaussian_parameters_for_reorganisation_energy`` dictionary perform geometry optimisation calculations, which are far more computationally intensive to perform. 

The amount of memory that you will need to use for ``gaussian_parameters_for_reorganisation_energy`` should be double or more needed for ``gaussian_parameters``.


.. _submission_information_settings:

Tags needed for the ``submission_information`` dictionaries
***********************************************************

The ``submission_information_for_atomic_transition_charges``, ``submission_information_for_multiwfn``, ``submission_information_for_reorganisation_energy``, ``submission_information_for_electronic_energy_transfer``, and ``submission_information_for_eigendata`` dictionaries allow you to place the parameters needed for the ``submit.sl`` , ``multiwfn_submit.sl``, and the various reorganisation ``submit.sl`` files. These include:

* ``'cpus_per_task'``: This the the number of CPU's you want to use. This information is also passed on to your .gjf file.
* ``'mem'``: This is the total amount of RAM memory you want to use across all your CPUs. This information is also passed on to your .gjf file.
* ``'time'``: This is the amount of time you want to run this job for. Written HH:MM:SS
* ``'partition'``: This is the name of the partition you want to run your job on.
* ``'constraint'``: This assigns particular nodes to run Gaussian jobs. This is a variable that is needed at Victoria University of Wellington. See ``https://slurm.schedmd.com/sbatch.html`` for more information about this. This is set to ``'AVX'`` on the Rāpoi computer cluster at Victoria University of Wellington. 
* ``'email'``: This is the email you want to use to notify you about this job
* ``'gaussian_version'``: This is the version of gaussian you want to use. For example: ``'g16'``. This setting is required for ``submission_information`` and ``submission_information_for_reorganisation_energy``, as these processes use Gaussian to perform ATC, RE, and EET calculations. This tag is not needed for the ``submission_information_for_multiwfn`` dictionary.
* ``'python_version'``: This is the version of python you want to use. For example: ``'3.8.1'`` for Python 3.8.1. This tag is only needed for the ``submission_information_for_reorganisation_energy`` dictionary, as python is only used here to create single point calculations from the results of the geometrically optimised Gaussian calculations. 

For the ``submission_information_for_multiwfn`` dictionary, you only need to provide the ``'cpus_per_task'``, ``'mem'``, ``'time'``, and ``'partition'`` input parameters (and optionally the ``'constraint'`` and ``'email'`` input parameters). 


Advice for settings for the ``submission_information`` dictionaries
===================================================================

The Gaussian jobs that use the ``submission_information_for_atomic_transition_charges``, ``submission_information_for_electronic_energy_transfer``, and ``submission_information_for_eigendata`` dictionaries perform single point calculations, as well as other calculations for TD-DFT calculations. The Gaussian jobs that use the ``submission_information_for_reorganisation_energy`` dictionary perform geometry optimisation calculations, which are far more computationally intensive to perform. 

The amount of cpus, memory and computational time that you should need to use for ``submission_information_for_reorganisation_energy`` should be double or more needed for ``submission_information_for_atomic_transition_charges`` and ``submission_information_for_electronic_energy_transfer`` dictionaries. 

The Multiwfn program to perform the ATC calculations is not as computationally expensive as Gaussian, and likely will finish within a fraction of time needed for the Gaussian calculation. For this reason, the amount of cpus, memory and computational time ``submission_information_for_multiwfn`` can be the same or less than for ```submission_information_for_atomic_transition_charges``, and ``submission_information_for_electronic_energy_transfer`` dictionaries. 







