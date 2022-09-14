.. _submitting_jobs_to_slurm:

How to submit Gaussian jobs to slurm
####################################

To submit jobs to slurm manually in slurm, go to the directory with the desired Gaussian job you want to submit (which includes a ``.gjf``). You will see that another file called ``submit.sl`` should be there as well. This file contains all the information required for the Gaussian job to be submitted to slurm. To submit this job manually, type into the terminal: 

.. code-block:: bash

	sbatch submit.sl

If you have lots of jobs to submit to slurm in many subfolders, you can also type ``ECCP mass_submit`` that will submit every ``submit.sl`` script that are found as long as a ``.gjf`` file is found alongside the ``submit.sl`` script. This include all the different types of ``submit.sl`` scripts in the RE folders where appropriate. To use this program, change into the directory that contains the Gaussian job you want to submit to slurm. For example, you could change directory into the ``Unique_EET_Gaussian_Jobs`` folder and then type ``ECCP mass_submit`` into the terminal:

.. code-block:: bash

	cd Unique_EET_Gaussian_Jobs
	ECCP mass_submit

Or, you might only want to run a selection of jobs from the ``Unique_EET_Gaussian_Jobs`` folder:

.. code-block:: bash

	cd Unique_EET_Gaussian_Jobs/IDIC_cif
	ECCP mass_submit

``ECCP mass_submit`` will only run jobs that contain both a ``.gjf`` file and a ``submit.sl`` file. ``ECCP mass_submit`` will not run any jobs that also contain a ``.chk``, ``.rwf``, ``.int``, ``.d2e``, ``.skr``, or ``.log`` file. This is because any gaussian job folder that contains any one of these file is likely already running or has already run, so we don't want this job to be submitted to slurm again. If you want to re-run this job from scratch, remove these files from the gaussian job folder before resubmitting. 