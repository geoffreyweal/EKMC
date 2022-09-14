# The OPV_Dimer_Pairer Program

[![GitHub release (latest by date)](https://img.shields.io/github/v/release/geoffreyweal/OPV_Dimer_Pairer)](https://github.com/geoffreyweal/OPV_Dimer_Pairer)
[![Licence](https://img.shields.io/github/license/geoffreyweal/OPV_Dimer_Pairer)](https://www.gnu.org/licenses/agpl-3.0.en.html)
[![LGTM Grade](https://img.shields.io/lgtm/grade/python/github/geoffreyweal/OPV_Dimer_Pairer)](https://lgtm.com/projects/g/geoffreyweal/OPV_Dimer_Pairer/context:python)

Authors: Dr. Geoffrey Weal<sup>\*</sup>, Dr. Paul Hume<sup>\*</sup>, Dr. Daniel Packwood<sup>\*\*</sup>, Prof. Justin Hodgkiss<sup>\*</sup>

<sup>\*</sup> Victoria University of Wellington, Wellington, New Zealand; The MacDiarmid Institute for Advanced Materials and Nanotechnology, Wellington, New Zealand. 

<sup>\*\*</sup> Kyoto University, Kyoto, Japan; Institute for Integrated Cell-Material Sciences, Kyoto, Japan.

Group pages: https://people.wgtn.ac.nz/paul.hume/grants, https://www.packwood.icems.kyoto-u.ac.jp/, https://people.wgtn.ac.nz/justin.hodgkiss/grants

## What is OPV_Dimer_Pairer

OPV_Dimer_Pairer is designed to provide information about the molecules in a OPV crystal structure, as well as dimer between individual molecules.

## Installation: Setting Up OPV_Dimer_Pairer and Pre-Requisites Packages

In this article, we will look at how to install the OPV_Dimer_Pairer and all requisites required for this program.

### Pre-requisites

#### Python 3 and ``pip3``

This program is designed to work with **Python 3**. While this program has been designed to work with Python 3.6, it should work with any version of Python 3 that is the same or later than 3.6.

To find out if you have Python 3 on your computer and what version you have, type into the terminal

	python3 --version

If you have Python 3 on your computer, you will get the version of python you have on your computer. E.g.

	geoffreyweal@Geoffreys-Mini Documentation % python3 --version
	Python 3.6.3

If you have Python 3, you may have ``pip3`` installed on your computer as well. ``pip3`` is a python package installation tool that is recommended by Python for installing Python packages. To see if you have ``pip3`` installed, type into the terminal

	pip3 list

If you get back a list of python packages install on your computer, you have ``pip3`` installed. E.g.

	geoffreyweal@Geoffreys-Mini Documentation % pip3 list
	Package                       Version
	----------------------------- ---------
	alabaster                     0.7.12
	asap3                         3.11.10
	ase                           3.20.1
	Babel                         2.8.0
	certifi                       2020.6.20
	chardet                       3.0.4
	click                         7.1.2
	cycler                        0.10.0
	docutils                      0.16
	Flask                         1.1.2
	idna                          2.10
	imagesize                     1.2.0
	itsdangerous                  1.1.0
	Jinja2                        2.11.2
	kiwisolver                    1.2.0
	MarkupSafe                    1.1.1
	matplotlib                    3.3.1
	numpy                         1.19.1
	packaging                     20.4
	Pillow                        7.2.0
	pip                           20.2.4
	Pygments                      2.7.1
	pyparsing                     2.4.7
	python-dateutil               2.8.1
	pytz                          2020.1
	requests                      2.24.0
	scipy                         1.5.2
	setuptools                    41.2.0
	six                           1.15.0
	snowballstemmer               2.0.0
	Sphinx                        3.2.1
	sphinx-pyreverse              0.0.13
	sphinx-rtd-theme              0.5.0
	sphinx-tabs                   1.3.0
	sphinxcontrib-applehelp       1.0.2
	sphinxcontrib-devhelp         1.0.2
	sphinxcontrib-htmlhelp        1.0.3
	sphinxcontrib-jsmath          1.0.1
	sphinxcontrib-plantuml        0.18.1
	sphinxcontrib-qthelp          1.0.3
	sphinxcontrib-serializinghtml 1.1.4
	sphinxcontrib-websupport      1.2.4
	urllib3                       1.25.10
	Werkzeug                      1.0.1
	wheel                         0.33.1
	xlrd                          1.2.0

If you do not see this, you probably do not have ``pip3`` installed on your computer. If this is the case, check out [PIP Installation](https://pip.pypa.io/en/stable/installing/). 

#### Atomic Simulation Environment

OPV_Dimer_Pairer uses the atomic simulation environment (ASE) to create read in the crystal data from various file format, to process the crystals, and to save the molecules and dimers found in the crystal to the preferred file type. 

models of clusters and surfaces that have atoms and moleucles adsorbed to its surface. Read more about [ASE here](https://wiki.fysik.dtu.dk/ase/>). 

The installation of ASE can be found on the [ASE installation page](https://wiki.fysik.dtu.dk/ase/install.html), however from experience if you are using ASE for the first time, it is best to install ASE using pip, the package manager that is an extension of python to keep all your program easily managed and easy to import into your python. 

To install ASE using pip, perform the following in your terminal.

	pip3 install --upgrade --user ase

Installing using ``pip3`` ensures that ASE is being installed to be used by Python 3, and not Python 2. Installing ASE like this will also install all the requisite program needed for ASE. This installation includes the use of features such as viewing the xyz files of structure and looking at ase databases through a website. These should be already assessible, which you can test by entering into the terminal:

	ase gui

This should show a gui with nothing in it, as shown below.

<p align="center">
  <img src="https://github.com/geoffreyweal/OPV_Dimer_Pairer/blob/main/README_images/ase_gui_blank.png?raw=true" alt="This is a blank ase gui screen that you would see if enter ``ase gui`` into the terminal."/>
</p>

However, **in the case that this does not work**, we need to manually add a path to your ``~/.bashrc`` so you can use the ASE features externally outside python. Do the following: first enter the following into the terminal:

	pip3 show ase

This will give a bunch of information, including the location of ase on your computer. For example, when I do this I get:

	Geoffreys-Mini:~ geoffreyweal$ pip show ase
	Name: ase
	Version: 3.20.1
	Summary: Atomic Simulation Environment
	Home-page: https://wiki.fysik.dtu.dk/ase
	Author: None
	Author-email: None
	License: LGPLv2.1+
	Location: /Users/geoffreyweal/Library/Python/3.6/lib/python/site-packages
	Requires: matplotlib, scipy, numpy
	Required-by: 

In the 'Location' line, if you remove the 'lib/python/site-packages' bit and replace it with 'bin'. The example below is for Python 3.6. 

	/Users/geoffreyweal/Library/Python/3.6/bin

This is the location of these useful ASE tools. If you are having issues using the ase tools, for example if ``ase gui`` does not start, you want to put this as a path in your ``~/.bashrc`` as below:

	############################################################
	# For ASE
	export PATH=/Users/geoffreyweal/Library/Python/3.6/bin:$PATH
	############################################################

#### Networkx

``Networkx`` is a python program that is used in OPV_Dimer_Pairer to determine individual molecules in a crystal structure, as well as to help reconstructure molecules in the crystal into more human-friendly versions. The easiest way to install ``Networkx`` is though pip. Type the following into the terminal:

	pip3 install --upgrade --user networkx

#### Packaging

The ``packaging`` program is also used in this program to check the versions of ASE that you are using for compatibility issues. The easiest way to install ``packaging`` is though pip. Type the following into the terminal:

	pip3 install --upgrade --user packaging

#### TQDM

The ``tqdm`` program is used by this program to provide progress bars that are useful for easily monitoring progress during this program. The easiest way to install ``tqdm`` is though pip. Type the following into the terminal:

	pip3 install --upgrade --user tqdm

#### Xlsxwriter

The ``xlsxwriter`` program is used by this program to write the output data from Gaussian jobs to an excel file(s). The easiest way to install ``xlsxwriter`` is though pip. Type the following into the terminal:

	pip3 install --upgrade --user xlsxwriter

### Setting up OPV_Dimer_Pairer

First, download OPV_Dimer_Pairer to your computer. You can do this by cloning a version of this from Github, or obtaining a version of the program from the authors. If you are obtaining this program via Github, you want to ``cd`` to the directory that you want to place this program in on the terminal, and then clone the program from Github through the terminal as well
	
	cd PATH/TO/WHERE_YOU_WANT_OPV_Dimer_Pairer_TO_LIVE_ON_YOUR_COMPUTER
	git clone https://github.com/geoffreyweal/OPV_Dimer_Pairer


Next, add a python path to it in your  ``~/.bashrc`` to indicate its location. Do this by entering into the terminal where you cloned the OPV_Dimer_Pairer program into ``pwd``

	pwd

This will give you the path to the OPV_Dimer_Pairer program. You want to enter the result from ``pwd`` into the ``~/.bashrc`` file. This is done as shown below:

	export PATH_TO_OPV_Dimer_Pairer="<Path_to_OPV_Dimer_Pairer>" 
	export PYTHONPATH="$PATH_TO_OPV_Dimer_Pairer":$PYTHONPATH
	export PATH="$PATH_TO_OPV_Dimer_Pairer"/OPV_Dimer_Pairer/Subsidiary_Programs:$PATH
	export PATH="$PATH_TO_OPV_Dimer_Pairer"/OPV_Dimer_Pairer/Supporting_Programs:$PATH

where ``"<Path_to_OPV_Dimer_Pairer>"`` is the directory path that you place OPV_Dimer_Pairer (Enter in here the result you got from the ``pwd`` command). Once you have run ``source ~/.bashrc``, the OPV_Dimer_Pairer program should be all ready to go!

## What does OPV_Dimer_Pairer do?

Given a input crystal structure of a OPV, the OPV_Dimer_Pairer program will obtain all the individual molecules in the crystal, as well as all the unique, non-symmetric dimers between those individul molecules in the crystal. 

### How does the OPV_Dimer_Pairer obtain the individual molecules and dimers in the molecule:

The OPV_Dimer_Pairer program works as follows:

1. The OPV_Dimer_Pairer program first takes the input crystal and determines what individual molecules are in the crystal by making a graph of the crystal system, where the nodes are the atoms in the crystal and the edges are the bonds between atoms. From this, the individual molecules can be obtained.

2. Once the individual molecules are obtained, they may be segmented into a number of components if the molecule is placed through the periodic boundary of the crystal lattice. In the second step, the OPV_Dimer_Pairer program will connect the components of the molecule back together, retaining the positions of the molecule in the original crystal. This will give xyz files of molecules can are more user-friendly to observe.

3. From these individual molecules, the OPV_Dimer_Pairer program will obtain the dimers of molecules in the crystal (consisting of pairs of neighbouring molecules). 

4. Some of these dimers will be the same to other dimers that have been located (i.e. will be symmetric to eachother after reflections, translations, or rotations). The OPV_Dimer_Pairer program will remove those dimers that are reflectively, rotationally, and translationally invarient to each other. This analysis will ignore all hydrogen atoms in the molecules/dimers.

5. The OPV_Dimer_Pairer program will then record the molecules and dimers found to disk. 

## How to use OPV_Dimer_Pairer

The OPV_Dimer_Pairer is run using a script called ``Run_OPV_Dimer_Pairer.py``. This contains information about all the crystals you want to obtain dimers for, as well as the parameters required to obtain dimers. An example of this script is shown below:

```python
from OPV_Dimer_Pairer import OPV_Dimer_Pairer

# --------------------------------------------------------------------------------------------------------------
# These are the parameters needed for the dimer method. 
# See https://github.com/geoffreyweal/OPV_Dimer_Pairer for more information about these parameters

# This is the method use to reassemble individual molecule from the crystal. 
make_molecule_method = 'component_assembly_approach'
# This is the method use to obtain dimers between molecules in the system.
dimer_method = {'method': 'nearest_atoms_method', 'max_dimer_distance': 5.0}
# This tag will indicate if you want to remove the aliphatic sidegroups from your OPV molecule.
remove_aliphatic_sidegroups = True
# This tag will indicate if you want to add hydrogens to your sp3 carbons that do not have complete hydrogens do to them being missed from the X-Ray. 
add_hydrogens_to_sp3_carbons = True
# This dictionary provides information for determining which dimers are equivalent
#dimer_equivalence_method = {'method': 'atom_distances_method'} # atomic_distance_method # invariance_method
dimer_equivalence_method = {'method': 'invariance_method'} # atom_distances_method # invariance_method # averaging_method

# This dictionary will add tags to your gaussian .gjf file
all_gaussian_parameters = []
methods = ['CAM-B3LYP','wB97XD','LC-wHPBE','B3LYP','M062X']
basises = ['6-31+G(d,p)']
mem = 48 # GB
from itertools import product
for method, basis in product(methods, basises):
	gaussian_parameters = {}
	gaussian_parameters['mem']    = str(mem)+'GB'
	gaussian_parameters['method'] = method
	gaussian_parameters['basis']  = basis
	gaussian_parameters['extra']  = '# td(nstates=1) nosymm maxdisk=1TB'
	all_gaussian_parameters.append(gaussian_parameters)

# This dictionary will add tags to your submit.sl file
submission_information = {}
submission_information['cpus_per_task'] = 12
submission_information['mem'] = str(mem+12)+'GB'
submission_information['time'] = '3-00:00'
submission_information['partition'] = 'parallel'
submission_information['constraint'] = 'AVX'
submission_information['email'] = 'geoffreywealslurmnotifications@gmail.com'
submission_information['gaussian_version'] = 'g16'
# --------------------------------------------------------------------------------------------------------------

# --------------------------------------------------------------------------------------------------------------
# These are the directories to the crystal files of OPV you would like to analyse with this Dimer Pairer method
filepaths = []

filepaths += ["models/Anthracene/Anthracene_1103062.cif"]
filepaths += ["models/Naphthalene/Naphthalene_638506_H_added.cif"]
filepaths += ["models/DCVSN5/DCVSN5_1005541.cif"]
filepaths += ["models/EL86_HB366/EL86_HB366_835848.cif"]

#filepaths += ["poscar_input/it4f_clean.vasp_corrected.xyz"]
# filepaths += ["poscar_input/itic_clean.vasp_corrected.xyz"]
# filepaths += ["poscar_input/itic-2cl-y_clean.vasp"]
# filepaths += ["poscar_input/itic-2cl-y.vasp"]
# filepaths += ["poscar_input/itic-2cl-y.cif"]
# filepaths += ["poscar_input/itic-2cl-g.cif"]
# filepaths += ["poscar_input/itic-4f.cif"]
# filepaths += ["poscar_input/itic.cif"]

# filepaths += ["poscar_input/IDIC.cif"]
# filepaths += ["poscar_input/Y6.cif"]

# filepaths += ["poscar_input/1_sq.cif"]
# filepaths += ["poscar_input/EH-IDTBR.cif"]
# --------------------------------------------------------------------------------------------------------------

# --------------------------------------------------------------------------------------------------------------
# This will run this method
for filepath in filepaths:
	OPV_Dimer_Pairer(filepath, make_molecule_method=make_molecule_method, dimer_method=dimer_method, remove_aliphatic_sidegroups=remove_aliphatic_sidegroups, add_hydrogens_to_sp3_carbons=add_hydrogens_to_sp3_carbons, dimer_equivalence_method=dimer_equivalence_method, gaussian_parameters=all_gaussian_parameters, submission_information=submission_information)
# --------------------------------------------------------------------------------------------------------------
```

The following pameters are:

* ``filepath`` (*str.*): The directory to the crystal file of OPV you would like to analyse with this Dimer Pairer program.
* ``make_molecule_method`` (*str.*): This is the method you would like to use to reconnect a molecule from a crystal into a more human-friendly form. See below for more information about the ``make_molecule_method`` methods available. 
* ``dimer_method`` (*dict.*): This dictionary contains the information required for determining how dimers are determined/obtained by this program. See below for more information about the ``dimer_method`` methods available. 
* ``remove_aliphatic_sidegroups`` (*bool*): This tag indicates if you want to remove aliphatic sidegroups. Note: if you have set ``remove_aliphatic_sidegroups`` to ``True``, ``add_hydrogens_to_sp3_carbons`` will be set to ``True`` in order for it to replace the sidegroup with a H atom in its place.
* ``add_hydrogens_to_sp3_carbons`` (*bool*): This tag indicates if you want to add hydrogens to aliphatic side groups or the carbon left over from the removal of the aliphatic side group to kept them as sp3.
* ``dimer_equivalence_method`` (*dict.*): This dictionary contains information required for determining which dimers were equivalent and which were unique. See below for more information about the ``dimer_equivalence_method`` methods available. 
* ``gaussian_parameters`` (*dict.*): This dictionary contains information required for the Gaussian files, such as the .gjf file. If this is set to ``None``, no Gaussian files will be created. 
* ``submission_information`` (*dict.*): This dictionary contains information required for the ``submit.sl`` file, required for submitting job to slurm. 

### Methods available for ``make_molecule_method``

In order to obtain the individual molecules in the crystal, the molecule may be placed in a position that is crosses from one side of the periodic boundary to the opposite side of the crystal lattice. While this is all fine, it does not make viewing thr molecule very user-friendly. Therefore, the OPV_Dimer_Pairer program will move the segments of the disconnected molecule around so that it is more user-friendly to vuew. There are two approaches for reconstructing the molecule available in OPV_Dimer_Pairer. Ideally, both should give the same results.

#### The Super Lattice Approach

This approach will create a super-lattice consisting of 26 lattices surrounding the origin unit cell. From this, a verison of the complete connected molecule will exist. All partial segments are deleted. This approach is very simple, but it take a bit of time to run.

To use this approach, set ``make_molecule_method = 'super_lattice_approach'`` in your ``Run_OPV_Dimer_Pairer.py`` script. 

#### The Component Assembly Approach

This approach will construct a graph of the components of the molecule across the crystal and use this information to determine which bonds have been disconnected in the molecule. The components are then shifted into place based on the periodic boundary condition so that the two bonds are connected again. This is the recommended approach to use. If this approach fail, report the issue and use the ``'super_lattice_approach'``. 

To use this approach, set ``make_molecule_method = 'component_assembly_approach'`` in your ``Run_OPV_Dimer_Pairer.py`` script. 

### Methods available for ``dimer_method``

In order to identify dimers you need to specify the method for how you want to identify them. There are two methods available for identifying dimers in this program:

#### The Centre of Mass Method

This method identifies dimers by looking at the distance between two molecules centre's of mass. If they are smaller than a predefined maximum dimer distance, then those two molecules are considered dimers. 

To use this method, set ``dimer_method = {'method': 'CM_method', 'max_dimer_distance': 20.0}``, where ``max_dimer_distance`` is a float that is the maximum distance between two molecules centres of mass that you deem for those two molecules to be considered a dimer. 

#### The Average Distance Method

This method identifies dimers by looking at the distances of the non-hydrogen atoms between two molecules. If the average distance between an atom in molecule 1 (or molecule 2) and all non-hydrogen atoms in molecule 2 (molecule 1) is smaller than a predefined maximum dimer distance, then those two molecules are considered dimers. 

To use this method, set ``dimer_method = {'method': 'average_distance_method', 'max_dimer_distance': 5.0}``, where ``max_dimer_distance`` is a float that is the maximum distance between any atom in molecule 1 (or molecule 2) and all non-hydrogen atoms in molecule 2 (molecule 1) for molecule 1 and molecule 2 to be considered a dimer. 

#### The Nearest Atoms Method

This method identifies dimers by looking at the distances of the non-hydrogen atoms between two molecules. If the distance between any two non-hydrogen atoms is smaller than a predefined maximum dimer distance, then those two molecules are considered dimers. 

To use this method, set ``dimer_method = {'method': 'nearest_atoms_method', 'max_dimer_distance': 5.0}``, where ``max_dimer_distance`` is a float that is the maximum distance between any atoms in each molecules from each other for those two molecules to be considered a dimer. 

### Methods available for ``dimer_equivalence_method``

Some of the dimers that will have been obtained will be identical to each other. We would like to know which one of these dimers are equivalent and which ones are unique, as we may not necessarily need to perform Gaussian calculations on equivalent dimer systems. There are three methods available for identifying equivalent dimers in this program:

#### The Atomic Distance Method

This method works by recording the distances in each dimer, from each atom in molecule 1 to every atom in molecule 2 (as well as recording the distances from each atom in molecule 2 to every atom in molecule 1). These distances are then ordered from each atom from shortest to largest distances. If the distances between atoms in dimer 1 are the same as the distance between atoms in dimer 2, the two dimers are considiered equivalent. 

To use this method, set ``dimer_equivalence_method = {'method': 'atomic_distance_method'}``.

#### The Averaging Method

This method works by recording the distances in each dimer, from each atom in molecule 1 to every atom in molecule 2 (as well as recording the distances from each atom in molecule 2 to every atom in molecule 1). All these distances are then averaged to give an average distance. This average distance is then compared between dimers to 2 decimal places. If two dimers have the same average distance, they are considered equivalent. 

To use this method, set ``dimer_equivalence_method = {'method': 'averaging_method'}``.

#### The Invariance Method

This method works by using the Procrustes analysis to determine if two dimers are translationally, rotationally, and reflectively invariant with each other. 

To use this method, set ``dimer_equivalence_method = {'method': 'invariance_method'}``.

### Tags needed for the ``gaussian_parameters`` dictionary

The ``gaussian_parameters`` dictionary allows you to place the parameters needed for the .gjf file. These include:

* ``'method'`` (*str.*): The level of theory you want to use (i.e. the functional).
* ``'basis'`` (*str.*): The basis set you want to use.
* ``'extra'`` (*str.*): These are any extra tags that you need to add. For example: ``'# td(nstates=1) nosymm maxdisk=1TB'``

You can also specify where you would like certain files to be placed, particularly if you want to place some of the temporary Gaussian files into a SCRATCH directory. If you want all the temporary files to be placed in a general SCRATCH files, provide a entry for ``'gaussian_scratch_path'`` in ``gaussian_parameters`` dictionary: 

* ``'gaussian_scratch_path'`` (*str.*): This is the path to the SCRATCH directory to place temporary Gaussian files. The default path is the path that your ``.gjf`` file was placed in by this program. 

You can also select specific temporary Gaussian files to be placed in the SCRATCH directory. These are ``'chk'``, ``'rwf'``, ``'int'``, ``'d2e'``, and ``'skr'``. These are given as a boolean where if ``True``, place in the SCRATCH directory you gave in ``gaussian_parameters['gaussian_scratch_path']``, if ``False``, place in the same file as your ``.gjf`` Gaussian input file. Default: ``True``. For example: 

```python
gaussian_parameters['gaussian_scratch_path'] = '/nfs/scratch2/wealge'
gaussian_parameters['chk'] = True
gaussian_parameters['rwf'] = False
gaussian_parameters['int'] = True
gaussian_parameters['d2e'] = False
gaussian_parameters['skr'] = True
```

### Tags needed for the ``submission_information`` dictionary

The ``submission_information`` dictionary allows you to place the parameters needed for the ``submit.sl`` file needed to submit files to slurm. These include:

* ``'cpus_per_task'``: This the the number of CPU's you want to use. This information is also passed on to your .gjf file.
* ``'mem'``: This is the total amount of RAM memory you want to use across all your CPUs. This information is also passed on to your .gjf file.
* ``'time'``: This is the amount of time you want to run this job for. Written HH:MM:SS
* ``'partition'``: This is the name of the partition you want to run your job on.
* ``'constraint'``: This assigns particular nodes to run Gaussian jobs. This is a variable that is needed at Victoria University of Wellington. See ``https://slurm.schedmd.com/sbatch.html`` for more information about this. This is set to ``'AVX'`` on the Rāpoi computer cluster at Victoria University of Wellington. 
* ``'email'``: This is the email you want to use to notify you about this job
* ``'gaussian_version'``: This is the version of gaussian you want to use. For example: ``'g16'``. 

### Recommendation for settings

to write here.

## Examples of input files

The folder called ``Examples`` contains all the files that are needed to run the OPV_Dimer_Pairer program. This includes examples of the basic run code for OPV_Dimer_Pairer, the ``Run_OPV_Dimer_Pairer.py`` file. 

## Outputs from the OPV_Dimer_Pairer program

The OPV_Dimer_Pairer program will create a folder called ``DimerData`` which will store all the data it produces into. This includes:

* ``Dimer_Information.txt``: A file that contains information about the molecules and dimers that were found in the crystal.
* ``crystal.xyz``: The original crystal in xyz format. Name given will be the same as the crystal file name given to OPV_Dimer_Pairer.
* ``human_friendly_crystal_small.xyz``: The crystal in a version that makes it easier to view and understand the crystal packing in the crystal. This is a smaller version of this view. 
* ``human_friendly_crystal_large.xyz``: The crystal in a version that makes it easier to view and understand the crystal packing in the crystal. This is a larger version of this view. 
* ``Molecules``: This is a folder containing all the molecules found in the crystal. 
* ``All_Dimers``: This is a folder containing all the dimers found in the crystal. 
* ``Unique_Dimers``: This is a folder containing all the unique, non-equivalent dimers found in the crystal. 
* ``All_Gaussian_Jobs``: This is a folder containing all the dimers found in the crystal as Gaussian files that can be submitted to slurm. 

Another folder is also created called ``Unique_Gaussian_Jobs`` that is a folder that contains all the unique, non-equivalent dimers found in the crystal as Gaussian files that can be submitted to slurm. 

## How to submit Gaussian jobs to slurm

To submit jobs to slurm manually in slurm, go to the directory with the desired Gaussian job you want to submit (which includes a ``.gjf``). You will see that another file called ``submit.sl`` should be there as well. This file contains all the information required for the Gaussian job to be submitted to slurm . To submit this job manually, type into the terminal: 

	sbatch submit.sl

If you have lots of jobs to submit to slurm in many subfolders, you can also use the program ``submit_gaussian_jobs_to_slurm.py`` that will submit every ``submit.sl`` script that are found as long as a ``.gjf`` file is found alongside the ``submit.sl`` script. To use this program, change into the directory that contains the Gaussian job you want to submit to slurm. For example, you could change directory into the ``Unique_Gaussian_Jobs`` folder and then run the ``submit_gaussian_jobs_to_slurm.py`` program:

	cd Unique_Gaussian_Jobs
	submit_gaussian_jobs_to_slurm.py

Or, you might only want to run a selection of jobs from the ``Unique_Gaussian_Jobs`` folder:

	cd Unique_Gaussian_Jobs/Anthracene_1103062_cif
	submit_gaussian_jobs_to_slurm.py

``submit_gaussian_jobs_to_slurm.py`` will only run jobs that contain both a  ``.gjf`` file and a ``submit.sl`` file. 

``submit_gaussian_jobs_to_slurm.py`` will also not run any jobs that also contain a ``.out``, ``.chk``, ``.rwf``, ``.int``, ``.d2e``, ``.skr``, or ``.log`` files. This is because any gaussian job folder that contains any one of these file is likely already running or has already run, so we don't want this job to be submitted to slurm again. If you want to rerun this job from scratch, remove these files from the Gaussian job folder before resubmitting. 

## Processing results of Gaussian jobs using the ``processing_OPV_Dimer_data.py`` script

It is possible for this program to process the electronic coupling results from Gaussian jobs and present the results in text for and in an excel spreadsheet. If the Gaussian job runs successfully, it will give a ``output.log`` file that contains values for the electronic coupling between the molecules in the dimer using the EET method in Gaussian. To do this, move into your ``Unique_Gaussian_Jobs`` folder and run the ``processing_OPV_Dimer_data.py`` script by typing into the terminal: 

	cd Unique_Gaussian_Jobs
	processing_OPV_Dimer_data.py

This method will go through all the folders in ``Unique_Gaussian_Jobs`` and extract the data from every successfully run ``output.log`` file and place it into an excel file called ``Unique_Gaussian_Jobs.xlsx``, and two text files called ``Unique_Gaussian_Jobs.txt`` and ``Unique_Gaussian_Jobs_wavenumber.txt``. Thes files contain the electron coupling information in meV and in cm<sup>-1</sup>. 

## Issues

This program is definitely a "work in progress". I have made it as easy to use as possible, but there are always oversights to program development and some parts of it may not be as easy to use as it could be. If you have any issues with the program or you think there would be better/easier ways to use and implement things in OPV_Dimer_Pairer, feel free to email Geoffrey about these (geoffrey.weal@gmail.com). Feedback is very much welcome!

## About

<div align="center">

| Python | [![PyPI - Python Version](https://img.shields.io/pypi/pyversions/OPV_Dimer_Pairer)](https://docs.python.org/3/) | 
|:----------------------:|:-------------------------------------------------------------:|
| Repositories | [![GitHub release (latest by date)](https://img.shields.io/github/v/release/geoffreyweal/OPV_Dimer_Pairer)](https://github.com/geoffreyweal/OPV_Dimer_Pairer) |
| Tests | [![LGTM Grade](https://img.shields.io/lgtm/grade/python/github/geoffreyweal/OPV_Dimer_Pairer)](https://lgtm.com/projects/g/geoffreyweal/OPV_Dimer_Pairer/context:python)
| License | [![Licence](https://img.shields.io/github/license/geoffreyweal/OPV_Dimer_Pairer)](https://www.gnu.org/licenses/agpl-3.0.en.html) |
| Authors | Dr. Geoffrey Weal, Dr. Paul Hume, Dr. Daniel Packwood, Prof. Justin Hodgkiss |
| Group Websites | https://people.wgtn.ac.nz/paul.hume/grants, https://www.packwood.icems.kyoto-u.ac.jp/, https://people.wgtn.ac.nz/justin.hodgkiss/grants |

</div>
