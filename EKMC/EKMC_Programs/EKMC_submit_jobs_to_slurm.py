'''
Geoffrey Weal, Run_ekmc_mass_submitSL_slurm.py, 10/05/2023

This program is designed to submit all sl files called submit.sl to slurm.
'''
import os, sys, math, getpass
import argparse, textwrap
import time, tqdm
from time import sleep
from subprocess import run as subprocess_run
from subprocess import PIPE, TimeoutExpired

from EKMC.EKMC.Run_EKMC_setup_files.get_EKMC_version                                                    import get_EKMC_version
from EKMC.EKMC_Programs.EKMC_submit_jobs_to_slurm_settings_methods.settings_methods                     import check_submit_settingsTXT, read_submit_settingsTXT_file
from EKMC.EKMC_Programs.EKMC_submit_jobs_to_slurm_settings_methods.change_settings                      import change_settings
from EKMC.EKMC_Programs.EKMC_submit_jobs_to_slurm_settings_methods.print_settings                       import print_settings
from EKMC.EKMC_Programs.EKMC_submit_jobs_to_slurm_methods.update_to_submission_settings                 import update_to_submission_settings
from EKMC.EKMC_Programs.EKMC_submit_jobs_to_slurm_methods.check_max_jobs_in_queue_after_next_submission import check_max_jobs_in_queue_after_next_submission
from EKMC.EKMC_Programs.EKMC_submit_jobs_to_slurm_methods.check_max_jobs_in_queue_after_next_submission import get_number_to_trials_that_will_be_submitted_by_ekmc_mass_submitSL
from EKMC.EKMC_Programs.EKMC_submit_jobs_to_slurm_methods.wait_for_slurmjob_queue_decrease              import wait_for_slurmjob_queue_decrease
from EKMC.EKMC_Programs.EKMC_submit_jobs_to_slurm_methods.countdown                                     import countdown

# Get the path to the settings script.
this_scripts_path = os.path.dirname(os.path.abspath(__file__))
submit_settings_name = 'EKMC_submit_jobs_to_slurm_settings_methods/submit_settings.txt'
path_to_settings_txt_file = this_scripts_path+'/'+submit_settings_name

class CLICommand:
    """Submit EKMC jobs to slurm. See ``EKMC submit --help`` for more information.
    """

    @staticmethod
    def add_arguments(parser):
        parser.add_argument('-P', '--print-settings', action='store_true', help='Print your settings without submitting EKMC jobs.')
        parser.add_argument('new_settings', nargs='*', help='This contains the settings that you would like to change. Use ``EKMC submit -P`` to determine all the settings you can change, and see what they currently are.')

    @staticmethod
    def run(args_submit):

        # First, use this method to create a settings.txt file if it doesn't already exist, and check that the current settings.txt file can be read without problems.
        current_settings = check_submit_settingsTXT(path_to_settings_txt_file)

        # Second, obtain the list of settings to be changed in EKMC submit
        new_settings = args_submit.new_settings

        if args_submit.print_settings:

            # 3.1: Print the current settings for EKMC submit
            print_settings(current_settings)

        elif len(new_settings) > 0:

            # 2.2: Change the settings for the ``EKMC submit`` program.s
            change_settings(new_settings, current_settings)

        else:

            # 2.3: Run EKMC submit program
            Run_method()

# ================================================================================================

def is_sim_folder_in_directory(dirpath, dirnames):
    """
    This method is designed to determine if a EKMC simulation folder exists in the dirpath directory
    """
    for dirname in dirnames:
        if os.path.exists(dirpath+'/'+dirname) and os.path.isdir(dirpath+'/'+dirname):
            return True
    return False

force_submit = True
def Run_method():
    '''
    Geoffrey Weal, Run_Adsorber_submitSL_slurm.py, 16/06/2021

    This program is designed to submit all sl files called submit.sl to slurm

    '''
    print('---------------------------------------------------------')
    print('---------------------------------------------------------')
    print('-------- MASS SUBMITTING EXCITON KMC SIMULATIONS --------')
    version_no = get_EKMC_version()
    version_string = 'Version '+str(version_no)
    space_no = math.floor((57 - len(version_string))/2.0)
    print(' '*space_no+str(version_string))
    print()
    print('This program is designed to submit all your submit.sl scripts appropriately to slurm.')
    print()
    print('---------------------------------------------------------')
    print('---------------------------------------------------------')

    # First, get user changable variables from the settings file.
    Max_total_jobs_in_queue_at_any_one_time, Max_jobs_running_in_queue_from_EKMC_mass_submit, Max_jobs_pending_in_queue_from_EKMC_mass_submit, wait_between_submissions, time_to_wait_before_next_submission, time_to_wait_max_queue, number_of_consecutive_error_before_exitting, time_to_wait_due_to_submission_error = read_submit_settingsTXT_file(path_to_settings_txt_file)

    # Second, print the submission settings to the terminal
    print_settings((Max_total_jobs_in_queue_at_any_one_time, Max_jobs_running_in_queue_from_EKMC_mass_submit, Max_jobs_pending_in_queue_from_EKMC_mass_submit, wait_between_submissions, time_to_wait_before_next_submission, time_to_wait_max_queue, number_of_consecutive_error_before_exitting, time_to_wait_due_to_submission_error))
    print('***************************************************************************')

    # Third, create the list to store informations about EKMC jobs that are currently running and pending in the slurm queue. 
    running_slurm_jobs_queue = []
    pending_slurm_jobs_queue = []

    # Fourth, indicate if there will be a small wait between jobs.
    if wait_between_submissions == True:
        print('This program will wait between submitting jobs.')
    else:
        print('This program will not wait between submitting jobs.')
    print('Will begin to search for submit.sl and other .sl files.')
    print('***************************************************************************')

    # Fifth, time to submit all the GA scripts! Lets get this stuff going!
    if not wait_between_submissions:
        max_consec_counter = 100
        consec_counter = 0
    errors_list = []
    error_counter = 0
    path = os.getcwd()

    # Sixth, check to make sure the array line in all ekmc_mass_submit.sl scripts is there and that none of the mass_submission script submit more than Max_total_jobs_in_queue_at_any_one_time into the queue. 
    print('-----------------------------------------------')
    print('Checking to make sure that the array line in all ekmc_mass_submit.sl scripts is there and that none of the mass_submission script submit more than Max_total_jobs_in_queue_at_any_one_time into the queue.')
    number_of_jobs_to_process = 0
    pbar = tqdm.tqdm(os.walk(path))
    for (dirpath, dirnames, filenames) in pbar:
        pbar.set_description(dirpath)
        dirnames.sort()
        if 'ekmc_mass_submit.sl' in filenames:
            no_of_trials_that_will_be_submitted = get_number_to_trials_that_will_be_submitted_by_ekmc_mass_submitSL(dirpath)
            if no_of_trials_that_will_be_submitted > Max_total_jobs_in_queue_at_any_one_time:
                print('Issue: The number of Trials that you want to submit is greater the number of trials you are allowed to submit at any one time.')
                print('Number of jobs that will be submitted by '+str(dirpath)+'/ekmc_mass_submit.sl: '+str(no_of_trials_that_will_be_submitted))
                print('Maximum number of trials that can be submitted into slurm: '+str(Max_total_jobs_in_queue_at_any_one_time))
                print('Consider doing either:')
                print('    1) Using the scripts Create_submitSL_slurm.py and Run_submitSL_slurm.py to run your jobs. This will submit your jobs individually and has better control over submitting this large number of trials within slurm without causing issues with slurm.')
                print('    2) Contact your slurm technical support about increasing the maximum number of jobs that can be found in the queue at any one time.')
                print('This program will exit without doing anything.')
                exit()
            number_of_jobs_to_process += 1
            dirnames[:] = []
            filenames[:] = []
    print('All clear to submit your ekmc_mass_submit.sl scripts.')
    print('-----------------------------------------------')
    print('*****************************************************************************')
    print('*****************************************************************************')
    print('Submitting ekmc_mass_submit.sl scripts to slurm.')
    print()
    print('*****************************************************************************')

    # Seventh, time to submit all the GA scripts! Lets get this stuff going!
    job_submission_counter = 0
    error_counter = 0
    for (dirpath, dirnames, filenames) in os.walk(path):
        dirnames.sort()
        if 'ekmc_mass_submit.sl' in filenames:
            
            # 7.1: Get updated user changable variables from the settings file.
            Max_total_jobs_in_queue_at_any_one_time, Max_jobs_running_in_queue_from_EKMC_mass_submit, Max_jobs_pending_in_queue_from_EKMC_mass_submit, wait_between_submissions, time_to_wait_before_next_submission, time_to_wait_max_queue, number_of_consecutive_error_before_exitting, time_to_wait_due_to_submission_error, Max_jobs_running_in_queue_from_EKMC_mass_submit = update_to_submission_settings(path_to_settings_txt_file, Max_total_jobs_in_queue_at_any_one_time, Max_jobs_running_in_queue_from_EKMC_mass_submit, Max_jobs_pending_in_queue_from_EKMC_mass_submit, wait_between_submissions, time_to_wait_before_next_submission, time_to_wait_max_queue, number_of_consecutive_error_before_exitting, time_to_wait_due_to_submission_error)
            
            # 7.2: Determine if this submission script has already been submitted.
            # This is best practise to prevent slurm from being overloaded with successful jobs (as they have already run completely) that end immediately.
            # Submit any jobs where some simulations have already begun by hand to prevent slurm breaking issues.
            if (not force_submit) and is_sim_folder_in_directory(dirpath, dirnames):
                print('Found Sim folders in '+str(dirpath)+', indicating this has already been submitted. Will continue on.')
                print('If you need to submit these jobs, it is best to do this by hand and submit only the ekmc_mass_submit.sl files that you need to submit.')
                print('This is because if many of your simulations have already completed, they finish immediately.')
                print('Slurm is not good with dealling with hundreds of jobs finishing quickly and at the same time.')
                print('Submit the simulations you want to perform by hand in order to minimise this issue arising.')
                print('*****************************************************************************')
                dirnames[:] = []
                filenames[:] = []
                continue
            
            # 7.3: Determine if it is the right time to submit jobs
            print('*****************************************************************************')
            Max_total_jobs_in_queue_at_any_one_time, Max_jobs_running_in_queue_from_EKMC_mass_submit, Max_jobs_pending_in_queue_from_EKMC_mass_submit, wait_between_submissions, time_to_wait_before_next_submission, time_to_wait_max_queue, number_of_consecutive_error_before_exitting, time_to_wait_due_to_submission_error, Max_jobs_running_in_queue_from_EKMC_mass_submit = update_to_submission_settings(path_to_settings_txt_file, Max_total_jobs_in_queue_at_any_one_time, Max_jobs_running_in_queue_from_EKMC_mass_submit, Max_jobs_pending_in_queue_from_EKMC_mass_submit, wait_between_submissions, time_to_wait_before_next_submission, time_to_wait_max_queue, number_of_consecutive_error_before_exitting, time_to_wait_due_to_submission_error)
            reached_max_jobs, number_in_queue = check_max_jobs_in_queue_after_next_submission(dirpath, Max_total_jobs_in_queue_at_any_one_time)
            if reached_max_jobs:
                print('-----------------------------------------------------------------------------')
                print('You can not have any more jobs in the queue before submitting the mass_sub (Max queue number: '+str(Max_total_jobs_in_queue_at_any_one_time)+'). Will wait a bit of time for some of them to complete')
                print('Number of Jobs in the queue = '+str(number_in_queue))
                while True:
                    Max_total_jobs_in_queue_at_any_one_time, Max_jobs_running_in_queue_from_EKMC_mass_submit, Max_jobs_pending_in_queue_from_EKMC_mass_submit, wait_between_submissions, time_to_wait_before_next_submission, time_to_wait_max_queue, number_of_consecutive_error_before_exitting, time_to_wait_due_to_submission_error, Max_jobs_running_in_queue_from_EKMC_mass_submit = update_to_submission_settings(path_to_settings_txt_file, Max_total_jobs_in_queue_at_any_one_time, Max_jobs_running_in_queue_from_EKMC_mass_submit, Max_jobs_pending_in_queue_from_EKMC_mass_submit, wait_between_submissions, time_to_wait_before_next_submission, time_to_wait_max_queue, number_of_consecutive_error_before_exitting, time_to_wait_due_to_submission_error)
                    reached_max_jobs, number_in_queue = check_max_jobs_in_queue_after_next_submission(dirpath, Max_total_jobs_in_queue_at_any_one_time)
                    if not reached_max_jobs:
                        break
                    sleep(time_to_wait_max_queue)
                print('The number of jobs in the queue is now less than the Maximum job number ('+str(Max_total_jobs_in_queue_at_any_one_time)+')')
                print('The number of jobs in the queue currently is: '+str(number_in_queue))
            
            # 7.4: Submit the jobs
            os.chdir(dirpath)
            name = dirpath.replace(path, '').split('/', -1)[1:]
            name = "_".join(str(x) for x in name)
            job_submission_counter += 1
            print("Submitting " + str(name) + " to slurm (submission "+str(job_submission_counter)+" of "+str(number_of_jobs_to_process)+").")
            print('Submission .sl file found in: '+str(os.getcwd()))
            ekmc_mass_submit_files = [filename for filename in filenames if (filename.startswith('ekmc_mass_submit') and filename.endswith('.sl'))]
            ekmc_mass_submit_files.sort(key=lambda x: 1 if (x.replace('ekmc_mass_submit','').replace('.sl','') == '') else int(x.replace('ekmc_mass_submit_','').replace('.sl','')))
            error_counter = 0
            for ekmc_mass_submit_filename in ekmc_mass_submit_files:
                submitting_command = ['sbatch', str(ekmc_mass_submit_filename)]
                while True:
                    if error_counter == number_of_consecutive_error_before_exitting:
                        break
                    else:
                        try:
                            proc = subprocess_run(submitting_command, stdout=PIPE, stderr=PIPE, timeout=(2*60))
                            if (proc.returncode == 0): 
                                # Submission successful, report this and move on.
                                job_number = int(proc.stdout.decode("utf-8").replace('Submitted batch job',''))
                                print("Submitted " + str(name) + " to slurm: "+str(job_number))
                                # Add the current job_number (including all arrayjobs) from the just submitted EKMC job to the pending_slurm_jobs_queue queue
                                add_job_number_to_queue(pending_slurm_jobs_queue, job_number)
                                # Wait until this ``EKMC submit`` program's running and pending queues are ready 
                                update_to_submission_settings_inputs = (path_to_settings_txt_file, Max_total_jobs_in_queue_at_any_one_time, Max_jobs_running_in_queue_from_EKMC_mass_submit, Max_jobs_pending_in_queue_from_EKMC_mass_submit, wait_between_submissions, time_to_wait_before_next_submission, time_to_wait_max_queue, number_of_consecutive_error_before_exitting, time_to_wait_due_to_submission_error)
                                wait_for_slurmjob_queue_decrease(pending_slurm_jobs_queue, running_slurm_jobs_queue, Max_jobs_pending_in_queue_from_EKMC_mass_submit, Max_jobs_running_in_queue_from_EKMC_mass_submit, update_to_submission_settings_inputs)
                                break
                            else:
                                # A problem occurred during the submission. Report this and wait a bit before trying again.
                                error_counter += 1
                                if error_counter == number_of_consecutive_error_before_exitting:
                                    print('----------------------------------------------')
                                    print('Error in submitting submit script to slurm.')
                                    print('I got '+str(number_of_consecutive_error_before_exitting)+" consecutive errors. Something must not be working right somewhere. I'm going to stop here just in case something is not working.")
                                    print('')
                                    print('The following ekmc_mass_submit.sl scripts WERE NOT SUBMITTED TO SLURM')
                                    print('')
                                else:
                                    print('----------------------------------------------')
                                    print('Error in submitting submit script to slurm. This error was:')
                                    print(proc.stderr)
                                    print('Number of consecutive errors: '+str(error_counter))
                                    print('Run_ekmc_mass_submitSL_slurm.py will retry submitting this job to slurm after '+str(time_to_wait_due_to_submission_error)+' seconds of wait time')
                                    print('----------------------------------------------')
                                    countdown(time_to_wait_due_to_submission_error)
                        except TimeoutExpired:
                            # A problem occurred during the submission, sbatch timedout. Report this and wait a bit before trying again.
                            proc.kill()
                            error_counter += 1
                            if error_counter == number_of_consecutive_error_before_exitting:
                                print('----------------------------------------------')
                                print('Error in submitting submit script to slurm. Job timed-out after 2 minutes.')
                                print('I got '+str(number_of_consecutive_error_before_exitting)+" consecutive errors. Something must not be working right somewhere. I'm going to stop here just in case something is not working.")
                                print('')
                                print('The following submit.sl scripts WERE NOT SUBMITTED TO SLURM')
                                print('')
                            else:
                                print('----------------------------------------------')
                                print('Error in submitting submit script to slurm. Job timed-out after 2 minutes.')
                                print('Number of consecutive errors: '+str(error_counter))
                                print('Run_submitSL_slurm.py will retry submitting this job to slurm after '+str(time_to_wait_before_next_submission_due_to_temp_submission_issue)+' seconds of wait time')
                                print('----------------------------------------------')
                                countdown(time_to_wait_before_next_submission_due_to_temp_submission_issue)

            # 7.5: check that there were any errors, and wait until it is possible to submit another job without going over the maximum limit for this user.
            if error_counter == number_of_consecutive_error_before_exitting:
                print(dirpath)
                errors_list.append(dirpath)
            else:
                if wait_between_submissions:
                    Max_total_jobs_in_queue_at_any_one_time, Max_jobs_running_in_queue_from_EKMC_mass_submit, Max_jobs_pending_in_queue_from_EKMC_mass_submit, wait_between_submissions, time_to_wait_before_next_submission, time_to_wait_max_queue, number_of_consecutive_error_before_exitting, time_to_wait_due_to_submission_error, Max_jobs_running_in_queue_from_EKMC_mass_submit = update_to_submission_settings(path_to_settings_txt_file, Max_total_jobs_in_queue_at_any_one_time, Max_jobs_running_in_queue_from_EKMC_mass_submit, Max_jobs_pending_in_queue_from_EKMC_mass_submit, wait_between_submissions, time_to_wait_before_next_submission, time_to_wait_max_queue, number_of_consecutive_error_before_exitting, time_to_wait_due_to_submission_error)
                    reached_max_jobs, number_in_queue = check_max_jobs_in_queue_after_next_submission(dirpath, Max_total_jobs_in_queue_at_any_one_time)
                    print('The number of jobs in the queue after submitting job currently is: '+str(number_in_queue))
                    countdown(time_to_wait_before_next_submission)
                    print('*****************************************************************************')

            # 7.6: If you are waiting between 
            dirnames[:] = []
            filenames[:] = []
            if not wait_between_submissions:
                if consec_counter >= max_consec_counter:
                    print('----------------------------------------------')
                    print('As you are not waiting between consecutive submissions, it is good practise to wait for a minute at some stage')
                    print(str(max_consec_counter) +' have been submitted consecutively. Will not wait for '+str(time_to_wait_before_next_submission)+' s before continuing')
                    print('----------------------------------------------')
                    countdown(time_to_wait_before_next_submission)
                    consec_counter = 0
                else:
                    consec_counter += 1

    # Eighth, print finishing message and indicate if there was an issue submitting the last job.
    if len(errors_list) > 0:
        print('----------------------------------------------')
        print()
        print('"Run_ekmc_mass_submitSL_slurm.py" will finish WITHOUT HAVING SUBMITTED ALL JOBS.')
        print()
        print('*****************************************************************************')
        print('The following ekmc_mass_submit.sl SCRIPTS WERE NOT SUBMITTED SUCCESSFULLY.')
        print()
        for error_dirpath in errors_list:
            print(error_dirpath)
        print('*****************************************************************************') 
    else:
        print('*****************************************************************************')
        print('*****************************************************************************')
        print('*****************************************************************************')
        print('All ekmc_mass_submit.sl scripts have been submitted to slurm successfully.')
        print('*****************************************************************************')
        print('*****************************************************************************')
        print('*****************************************************************************')

# ======================================================================================================================================================================================

def add_job_number_to_queue(slurm_jobs_queue, job_number):
    """
    This method will add the current job_number (including all arrayjobs) from the just submitted EKMC job to the slurm_jobs_queue queue.

    Parameters
    ----------
    slurm_jobs_queue : list of (int,int/None)
        This is the queue of EKMC submit jobs (either running or pending).
    job_number : int
        This is the slurmjob number (not including arrayjob information).

    """

    # First: run squeue and get the current queue for this job. 
    username = getpass.getuser()
    check_queue_command = ['squeue','-r','-u',username]
    counter = 0
    while True:
        try:
            proc = subprocess_run(check_queue_command, stdout=PIPE, stderr=PIPE, timeout=(2*60))
            if (proc.returncode == 0): 
                break
            else:
                counter += 1
        except TimeoutExpired as tee:
            print('Error: '+str(tee)+': '+str(proc.stderr))
            counter += 1
        if counter >= 10:
            raise Exception('Error: squeue timed out over 10 times.')
        else:
            print('Will try to obtain queue details again')
    output = proc.stdout.decode()

    # Second, determine which of the jobs submitted by this program are still pending or running in the slurm queue.
    for line in output.split('\n')[1:-1:1]:

        # 2.1: Grab the job number from line
        line = line.split()
        full_jn = line[0]

        # 2.2: Get the job number for this job.
        jobset = full_jn.split('_')
        jn = int(jobset[0])

        # 2.3: If jn is not the job number of interest we care about, moving on to the next job in the output. 
        if not (jn == job_number):
            continue

        # 2.4: Get the arrayjob number for this job if this job is an arrayjob.
        if len(jobset) >= 2:
            an = int(jobset[1])
        else:
            an = None

        # 2.5: Make the job set for this job, consisting of (job number, array number)
        jobset = (jn, an)

        # 2.6: Check that this job is not already in the slurm_jobs_queue. It should be if we are wanting to add job_number to slurm_jobs_queue.
        if jobset in slurm_jobs_queue:
            raise Exception('Error: jobset already in slurm_jobs_queue.\nCheck this.\njobset = '+str(jobset)+'\nslurm_jobs_queue = '+str(slurm_jobs_queue))

        # 2.7: Append jobset to slurm_jobs_queue
        slurm_jobs_queue.append(jobset)

    # Third, sort the slurm_jobs_queue by job number
    slurm_jobs_queue.sort()

# ======================================================================================================================================================================================











