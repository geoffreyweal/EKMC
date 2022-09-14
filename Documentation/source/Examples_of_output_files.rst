
.. _Examples_of_output_files:

Outputs from the Electronic Crystal Calculation Prep program
############################################################

The Electronic Crystal Calculation Prep program will create three to five folders. These are: 

General files are placed in:

	* ``ECCP_Data``: This contains all the information about molecules and dimers in the crystal, as well as the xyz files of molecules and dimers. 

Atomic Transition Charge (ATC) files are placed in:

	* ``All_ATC_Gaussian_Jobs``: This folder contains the ATC gaussian files of all the molecules in the crystal. These files are created in case you need to look through them, but you don't necessarily need to run these in Gaussian. 
	* ``Unique_ATC_Gaussian_Jobs``: This folder contains the ATC gaussian files of just the unique molecules in the crystal. These are the files you want to run in Gaussian. 

Reorganisation energy (RE) files are placed in:

	* ``All_RE_Gaussian_Jobs``: This folder contains the RE gaussian files of all the molecules in the crystal. These files are created in case you need to look through them, but you don't necessarily need to run these in Gaussian. 
	* ``Unique_RE_Gaussian_Jobs``: This folder contains the RE gaussian files of just the unique molecules in the crystal. These are the files you want to run in Gaussian. 

Electronic Energy Transfer (EET) files are placed in:

	* ``All_EET_Gaussian_Jobs``: This folder contains the EET gaussian files of all the dimers in the crystal. These files are created in case you need to look through them, but you don't necessarily need to run these in Gaussian. 
	* ``Unique_EET_Gaussian_Jobs``: This folder contains the EET gaussian files of just the unique dimers in the crystal. These are the files you want to run in Gaussian. 

Eigendata files that is used to obtain Intermolecular Charge Transfer (ICT) energies are placed in:

	* ``All_Eigendata_Gaussian_Jobs``: This folder contains the gaussian files of all the dimers in the crystal for obtaining molecular orbtial (MO) energies, coefficients, and overlap matrices for dimers and their associated monomers. These files are created in case you need to look through them, but you don't necessarily need to run these in Gaussian. 
	* ``Unique_Eigendata_Gaussian_Jobs``: This folder contains the gaussian files of just the unique dimers in the crystal for obtaining molecular orbtial (MO) energies, coefficients, and overlap matrices for dimers and their associated monomers. These are the files you want to run in Gaussian. 

Files in the ``ECCP_Data`` folder
*********************************

The folder called ``ECCP_Data`` contains all the information about molecules and dimers in the crystal, as well as the xyz files of molecules and dimers. The files included in this folder include: 

* ``Dimer_Information.txt``: A file that contains information about the molecules and dimers that were found in the crystal.
* ``crystal.xyz``: The original crystal in xyz format. Name given will be the same as the crystal file name given to Electronic_Crystal_Calculation_Prep.
* ``human_friendly_crystal_small.xyz``: The crystal in a version that makes it easier to view and understand the crystal packing in the crystal. This is a smaller version of this view. 
* ``human_friendly_crystal_large.xyz``: The crystal in a version that makes it easier to view and understand the crystal packing in the crystal. This is a larger version of this view. 
* ``All_Molecules``: This is a folder containing all the molecules found in the crystal. 
* ``Unique_Molecules``: This is a folder containing all the unique molecules found in the crystal. 
* ``All_Dimers``: This is a folder containing all the dimers found in the crystal. 
* ``Unique_Dimers``: This is a folder containing all the unique dimers found in the crystal. 


Files in the ATC, EET, and Eigendata folders
********************************************

These folders contain two files in them. These are:

* A Gaussian input file (``.gjf``) that contain all the information about the molecule or the dimer to run in Gaussian
* ``submit.sl``: This is the submission file requires to submit the gaussian job to slurm. 


Files in the RE folders
***********************

These folders contain a few files. 


In the ``ground_structure`` folder will be:

	* ``GS_GS.gjf``: The Gaussian file that contain information about how to optimise your molecule to the ground state structure. 
	* ``GS_GS_submit.sl``: File to submit the ``GS_GS.gjf`` Gaussian file to slurm.
	* ``GS_ES_submit.sl``: File to submit the ``GS_ES.gjf`` Gaussian file to slurm.

During the course of calculation, another file will be created:

	* ``GS_ES.gjf``: This Gaussian file contains information for performing a single point calculation of the excited state of your molecule with the ground state structure. A frequency calculation will also be performed.


In the ``excited_structure`` folder will be:

	* ``ES_ES.gjf``: The Gaussian file that contain information about how to optimise your molecule to the excited state structure. 
	* ``ES_ES_submit.sl``: File to submit the ``ES_ES.gjf`` Gaussian file to slurm.
	* ``ES_GS_freq_submit.sl``: File to submit the ``ES_ES_freq.gjf`` Gaussian file to slurm.
	* ``ES_GS_submit.sl``: File to submit the ``ES_GS.gjf`` Gaussian file to slurm.

During the course of calculation, another file will be created:

	* ``ES_ES_freq.gjf``: This Gaussian file contains information for performing a frequency calculation on the excited state structure. 
	* ``ES_GS.gjf``: This Gaussian file contains information for performing a single point calculation of the ground state of your molecule with the excited state structure. 




