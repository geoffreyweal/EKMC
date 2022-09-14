
.. _Guide_To_Using_ECCP:

Guide To Using The Electronic Crystal Calculation Prep (ECCP) Program
#####################################################################

Given a input crystal structure of a OPV or chemical system, the Electronic Crystal Calculation Prep program will obtain all the individual molecules in the crystal, the dimers between neighouring molecules in the crystal, as well as all the unique molecules and dimers in the crystal. Gaussian input files will also be created to run atomic transition charge (ATC) calculations, reorganisation energy (RE) calculations, and excitation energy transfer (EET) calculations upon molecules and dimers in the crystal. You can also obtain eigen-matrices and other data such as overlap intergral matrices, molecular orbital (MO) energies, and MO coefficients. These can be used to obtain other properties of the dimers in your crystal, such as intermolecular charge transfers (ICT) between monomers in your crystal. 

The main component of the ECCP program works as follows:

	1. The ECCP program first takes the input crystal and determines what individual molecules are in the crystal by making a graph of the crystal system, where the nodes are the atoms in the crystal and the edges are the bonds between atoms. From this, the individual molecules can be obtained.

	2. Once the individual molecules are obtained, they may be segmented into a number of components if the molecule is placed through the periodic boundary of the crystal lattice. In the second step, the ECCP program will connect the components of the molecule back together, retaining the positions of the molecule in the original crystal. This will give ``.xyz`` files of molecules that are more user-friendly to observe.

	3. Next, the unique molcules will be determined. Unique molecules are those that are structurally different from one another, including those that are twisted and bent in different ways. This analysis will ignore all hydrogen atoms in the molecules.

	4. The ECCP program will create the files needed to perform ATC and RE calculations if desired.

	5. From the individual molecules, the ECCP program will obtain the dimers of molecules in the crystal (consisting of pairs of neighbouring molecules). 

	6. Some of these dimers will be the same to other dimers that have been located (i.e. will be symmetric to eachother after reflections, translations, or rotations). The ECCP program will remove those dimers that are reflectively, rotationally, and translationally invarient to each other. This analysis will ignore all hydrogen atoms in the molecules/dimers.

	7. The ECCP program will create the files needed to perform EET calculations if desired, as well as calculations to obtain eigen-matrices to perform ICT calculations.

The guide to creating the ECCP file needed to obtain gaussian and slurm files for performing ATC, RE, and EET calcuations and for obtaining eigen-matrices to perform ICT calculations using this program is given in :ref:`Using_The_ECCP_Program`. 

This program will give a number of files and folders that contain information about the molecules and dimers within your crystal, some of which will allow you to perform Gaussian calculations on molecules and dimers. This is given in :ref:`Examples_of_output_files`. 

Once the ECCP program has been run, their are various methods included in the ECCP program to submit ECCP Gaussian jobs to slurm, check if they have completed successfully, and to process results. These additional program will be introduced in :ref:`postprocessing_data`. 