.. The EKMC documentation master file, created by
   sphinx-quickstart on Mon Oct  1 08:10:30 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to the Exciton kinetic Monte Carlo (EKMC) documentation!
################################################################

.. image:: https://img.shields.io/pypi/pyversions/EKMC
   :target: https://docs.python.org/3/
   :alt: Python Version


.. image:: https://img.shields.io/github/v/release/geoffreyweal/EKMC
   :target: https://github.com/geoffreyweal/EKMC
   :alt: GitHub release (latest by date)


.. image:: https://img.shields.io/pypi/v/EKMC
   :target: https://pypi.org/project/EKMC/
   :alt: PyPI


.. image:: https://img.shields.io/conda/v/gardengroupuo/ekmc
   :target: https://anaconda.org/geoffreyweal/ekmc
   :alt: Conda


.. image:: https://img.shields.io/github/license/geoffreyweal/EKMC
   :target: https://www.gnu.org/licenses/agpl-3.0.en.html
   :alt: Licence


.. image:: https://img.shields.io/lgtm/grade/python/github/geoffreyweal/EKMC
   :target: https://lgtm.com/projects/g/geoffreyweal/EKMC/context:python
   :alt: LGTM Grade


.. sectionauthor:: Dr. Geoffrey Weal <geoffrey.weal@gmail.com>
.. sectionauthor:: Dr. Josh Sutton
.. sectionauthor:: Dr. Chayanit Wechwithayakhlung
.. sectionauthor:: Dr. Daniel Packwood <dpackwood@icems.kyoto-u.ac.jp>
.. sectionauthor:: Dr. Paul Hume <paul.hume@vuw.ac.nz>
.. sectionauthor:: Prof. Justin Hodgkiss <justin.hodgkiss@vuw.ac.nz>

What is the Exciton kinetic Monte Carlo (EKMC) Program
======================================================

The Exciton kinetic Monte Carlo (EKMC) program is designed to simulate the diffusion of an exciton throughout a crystal structure. Here, an exciton begins on a molecule in the crystal. From there, the exciton hops to another molecule within the extended crystal structure based on probability as well as the excitonic coupling energies between molecules in the crystal. After repeating this process for a given amount of simulation time, and repeating the simulation many times, it is possible to determine the behaviour of excitons in the materials of interest. 

Installation
============

It is recommended to read the installation page before using the EKMC program. See :ref:`Installation: Setting Up EKMC and Pre-Requisites Packages <Installation>` for more information. Note that you can install EKMC through ``pip3`` and ``conda``. 

Guide To Using EKMC
===================

After you have installed EKMC, see :ref:`Guide_To_Using_EKMC` to learn about how to use this program. 

Table of Contents
=================

.. toctree::
   :maxdepth: 2
   
   Installation
   Guide_To_Using_EKMC
   Setting_Up_The_EKMC_Program
   Recommendation_For_Settings
   Running_The_EKMC_Program
   What_will_happen_when_you_run_Run_EKMC_py
   postprocessing_data
   Troubleshooting
   genindex
   py-modindex

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`




