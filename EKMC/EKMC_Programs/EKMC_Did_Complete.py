'''
Did_Complete.py, Geoffrey Weal, 11/04/2022

This program will determine which of your dimers have been successfully calculated in Gaussian.
'''
import os

from EKMC.EKMC_Programs.Did_Complete_Main import has_all_simulations_finished

class CLICommand:
    """Will determine which EKMC jobs have completed and which ones have not.
    """

    @staticmethod
    def add_arguments(parser):
        pass
        
    @staticmethod
    def run(args):
        Run_method()

def Run_method(time_between_250_cancels=60):
    """
    This method will determine which of your dimers have been successfully calculated in Gaussian.
    """

    path = os.getcwd()

    number_of_simulations = []
    Overall_Simulations_to_check = {}

    all_problem_simulations = []

    for dirpath, dirnames, filenames in os.walk(path):
        dirnames.sort()
        if any([(dirname.startswith('Sim') and dirname.replace('Sim','').isdigit()) for dirname in dirnames]):
            completed_successfully, completed_Simulations, incomplete_Simulations, problem_simulations = has_all_simulations_finished(dirpath, dirnames)
            toString = ''
            toString += '******************************************************************************\n'
            toString += '******************************************************************************\n'
            toString += 'This set of Exciton Kinetic Monte Carlo simulations finished '+('SUCCESSFULLY' if completed_successfully else 'UNSUCCESSFULLY')+'.\n'
            toString += '\n'
            toString += '# Successful Simulations: '+str(len(completed_Simulations))+';\t# Unsuccessful Simulations: '+str(len(incomplete_Simulations))+';\tTotal # of Simulations: '+str(len(completed_Simulations)+len(incomplete_Simulations))+'\n'
            number_of_simulations.append((dirpath,len(completed_Simulations),len(incomplete_Simulations)))
            toString += '\n'
            toString += 'The following Simulations in '+str(dirpath)+' completed or did not complete.\n'
            toString += 'Completed Simulations: '+str(completed_Simulations)+'\n'
            toString += 'Incomplete Simulations: '+str(incomplete_Simulations)+'\n'
            toString += 'There were '+str(len(incomplete_Simulations))+' incomplete simulations.\n'
            toString += '******************************************************************************\n'
            toString += '******************************************************************************\n'
            print(toString)
            with open(dirpath+'/SimulationsCompletionDetails.txt','w') as SimulationsCompletionDetailsTXT:
                SimulationsCompletionDetailsTXT.write(toString)
            dirnames[:] = []
            filenames[:] = []
            if not completed_successfully:
                Overall_Simulations_to_check[dirpath] = incomplete_Simulations
            all_problem_simulations += problem_simulations

    print('########################################################################')
    print('########################################################################')
    number_of_simulations.sort()
    print('Number of Simulations that were performed for each set of simulations:')
    for dirpath, no_of_successful, no_of_unsuccessful in number_of_simulations:
        print(dirpath+': '+str(no_of_successful+no_of_unsuccessful)+'\t(successful: '+str(no_of_successful)+'; unsuccessful: '+str(no_of_unsuccessful)+')')
    print('########################################################################')
    print('########################################################################')
    print('Details of Simulations that did not complete:')
    if len(Overall_Simulations_to_check) == 0:
        print('ALL Simulations completed SUCCESSFULLY')
    else:
        for dirpath, incomplete_Simulations in Overall_Simulations_to_check.items():
            print('path: '+str(dirpath)+'; Simulations to Repeat: '+str(incomplete_Simulations))
    print('########################################################################')
    print('########################################################################')
    if not len(all_problem_simulations) == 0:
        print('There were also a few problem simulations that this Did_Complete.py program had errors with. These should be checked out as something may be wrong with the simulation itself and may just need to be reset.')
        print('This could be for example a file was accidentally deleted')
        print('These problem simulations are:')
        print('')
        for problem_simulation in all_problem_simulations:
            print(str(problem_simulation))
        print('')
        print('########################################################################')
        print('########################################################################')
