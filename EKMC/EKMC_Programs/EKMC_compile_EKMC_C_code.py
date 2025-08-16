'''
Geoffrey Weal, Run_ekmc_mass_submitSL_slurm.py, 10/05/2023

This program is designed to submit all sl files called submit.sl to slurm.
'''
import os, sys
import subprocess
from EKMC import __version__

# Get the path to the settings script.
this_scripts_path = os.path.dirname(os.path.abspath(__file__))
path_to_C_code = '../EKMC/KMC_algorithm'
full_path_to_C_code1 = this_scripts_path+'/'+path_to_C_code

class CLICommand:
    """Compile the EKMC C code for running kinetic Monte-Carlo simulations. 
    """

    @staticmethod
    def add_arguments(parser):
        pass

    @staticmethod
    def run(args_submit):
        Run_method()

def Run_method():
    '''
    This method will run the makefile to compile the C++ code. 
    '''

    # First, print that the C++ code will be compiled and indicate what version of EKMC is being used.
    print('Compiling C++ code for EKMC: Version '+str(__version__))
    print('This may take a little bit of time to compile.')

    # Second, Run the makefile 
    original_path = os.getcwd()
    os.chdir(full_path_to_C_code1)
    proc = subprocess.run(['make'])
    os.chdir(original_path)

    # Third, print if there was an issue or not
    if proc.returncode == 0:
        print('EKMC C++ code compiled successfully')
    else:
        print('EKMC C++ code DID NOT compiled successfully')
        toString  = 'Check the errors give above for more info.\n'
        toString += 'If no errors were given, not sure what the issue is.\n\n'
        toString += 'If any problem arises, check what version of GCC and GCCcore you are using. Make sure check you are using a version of GCC that runs c++20. This should be included in GCC 10 and above.'
        print(toString)