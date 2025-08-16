"""
check_max_jobs_in_queue_after_next_submission.py, Geoffrey Weal, 4/1/2023

This method will check to make sure that the next job can be submitted and not go over the allocated number of maximum jobs.
"""
import getpass
import subprocess

username = getpass.getuser()
command = "squeue -r -u "+str(username)
def check_max_jobs_in_queue_after_next_submission(dirpath, Max_jobs_in_queue_at_any_one_time):
    """
    This method will check to make sure that the next job can be submitted and not go over the allocated number of maximum jobs.

    Parameters
    ----------
    dirpath : str.
        This is the settings? not needed to be programmed yet.
    Max_jobs_in_queue_at_any_one_time : int
        This is the maximum limit of jobs that can be in the user queue

    Returns
    -------

    """
    while True:
        text = myrun(command)
        nlines = len(text.splitlines())-1
        if not (nlines == -1):
            break
        else:
            print('Could not get the number of jobs in the slurm queue. Retrying to get this value.')
    number_of_trials_to_be_submitted = get_number_to_trials_that_will_be_submitted_by_ekmc_mass_submitSL(dirpath)
    if nlines > (Max_jobs_in_queue_at_any_one_time - number_of_trials_to_be_submitted):
        return True, nlines
    else:
        return False, nlines

def get_number_to_trials_that_will_be_submitted_by_ekmc_mass_submitSL(dirpath):
    path_to_ekmc_mass_submitSL = dirpath+'/ekmc_mass_submit.sl'
    with open(path_to_ekmc_mass_submitSL,'r') as ekmc_mass_submitSL:
        for line in ekmc_mass_submitSL:
            if '#SBATCH --array=' in line:
                trials = line.replace('#SBATCH --array=','')
                no_of_trials_that_will_be_submitted = 0
                worked_successfully = True
                trial_limits_commands = trials.rstrip().split(',')
                for trial_limits in trial_limits_commands:
                    if trial_limits.count('-') == 1:
                        trial_limits = trial_limits.split('-')
                        if len(trial_limits) == 2 and trial_limits[0].isdigit() and trial_limits[1].isdigit():
                            no_of_trials_that_will_be_submitted =+ int(trial_limits[1]) - int(trial_limits[0]) + 1
                        else:
                            worked_successfully = False
                            break
                    elif trial_limits.isdigit():
                        no_of_trials_that_will_be_submitted += 1
                    else:
                        worked_successfully = False
                        break
                if worked_successfully:
                    return no_of_trials_that_will_be_submitted
                else:
                    print('========================================================')
                    print('Error in submitting: '+str(path_to_ekmc_mass_submitSL))
                    print('One of the clusters in the array to be submitted is not a integer or is entered incorrectly.')
                    print()
                    print(line)
                    print()
                    print('Check this line in your submit.sl script')
                    print('This program will now exit')
                    exit ('========================================================')         
    print('Error in def get_number_to_trials_that_will_be_submitted_by_ekmc_mass_submitSL, in Run_ekmc_mass_submitSl_slurm.py script, found in the folder SubsidiaryPrograms in this GA program.')
    print('The ekmc_mass_submit.sl script found in '+str(dirpath)+' does not have the line that starts with "#SBATCH --array=" in the script.')
    print('Just check this script to make sure everything is all good.')
    import pdb; pdb.set_trace()
    print('This program will finish')
    exit()

def myrun(cmd):
    """
    This method will run a task in the terminal/bash.

    Parameters
    ----------
    cmd : str. 
        This is the command you would like to run in the terminal/bash.
    """
    proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout_lines = list(iter(proc.stdout.readline,b''))
    stdout_lines = [line.decode() for line in stdout_lines]
    return ''.join(stdout_lines)

