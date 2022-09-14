
.. _Recommendation_For_Settings:

Recommendation For Settings
############################


The recommended settings for this program are given below in python format. It is also recommended that if there are any side groups on the molecule that you do not want to include in your dimer that you manually remove them, using a program such as Mercury or to custom change the molecules obtained after running this program once again (following the proceedure given in the `Manually removing atoms in molecules in your crystal <https://github.com/geoffreyweal/ECCP#manually-removing-atoms-in-molecules-in-your-crystal>`_ section.

.. code-block:: python

	from ECCP import ECCP

	# This is the method use to reassemble individual molecule from the crystal. 
	make_molecule_method = 'component_assembly_approach'
	# This dictionary include information about determining which molecules are equivalent. Required if you want to perform ATC calculations on molecules.
	molecule_equivalence_method = {'method': 'invariance_method', 'type': 'combination'} 

	# This is the method use to obtain dimers between molecules in the system.
	dimer_method = {'method': 'nearest_atoms_method', 'max_dimer_distance': 8.0}
	# This dictionary provides information for determining which dimers are equivalent
	dimer_equivalence_method = {'method': 'invariance_method', 'type': 'combination'} 