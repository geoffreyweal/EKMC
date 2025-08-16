"""
wait_for_slurmjob_queue_decrease.py, Geoffrey Weal, 3/1/2023

This method are designed to allow the program to only have a number of jobs in the queue at any one time.

This prevents the queue from being swamped with jobs submitted by this program.
"""
import getpass
from tqdm import tqdm, trange
from time import sleep
from subprocess import Popen, PIPE, TimeoutExpired
from copy import deepcopy
from EKMC.EKMC_Programs.EKMC_submit_jobs_to_slurm_methods.update_to_submission_settings import update_to_submission_settings

def wait_for_slurmjob_queue_decrease(pending_slurm_jobs_queue, running_slurm_jobs_queue, Max_jobs_pending_in_queue_from_EKMC_mass_submit, Max_jobs_running_in_queue_from_EKMC_mass_submit, update_to_submission_settings_inputs):
    """
    This method will use the "check_if_can_submit_next_job" method to wait until the slurm queue is not full.
    
    Parameters
    ----------
    pending_slurm_jobs_queue : list of ints
        This list contains all the EKMC jobs in the pending queue.
    running_slurm_jobs_queue : list of ints
        This list contains all the EKMC jobs in the running queue.
    Max_jobs_pending_in_queue_from_EKMC_mass_submit : int
        This is the maximum number of jobs that we want in the pending queue that were submitted by this program.
    Max_jobs_running_in_queue_from_EKMC_mass_submit : int
        This is the maximum number of jobs that we want in the running queue that were submitted by this program.
    """

    # Third, wait until the number of jobs submitted by this program to slurm that are still pending is less than a given value.
    Max_total_jobs_in_queue_at_any_one_time, Max_jobs_running_in_queue_from_EKMC_mass_submit, Max_jobs_pending_in_queue_from_EKMC_mass_submit, wait_between_submissions, time_to_wait_before_next_submission, time_to_wait_max_queue, number_of_consecutive_error_before_exitting, time_to_wait_due_to_submission_error, Max_jobs_running_in_queue_from_EKMC_mass_submit = update_to_submission_settings(*update_to_submission_settings_inputs)
    is_pending_queue_full, number_of_jobs_in_pending_queue = check_if_can_submit_next_job(pending_slurm_jobs_queue, running_slurm_jobs_queue, Max_jobs_pending_in_queue_from_EKMC_mass_submit, Max_jobs_running_in_queue_from_EKMC_mass_submit, 'pending')
    waited = False
    if is_pending_queue_full:
        waited = True
        print('-----------------------------------------------------------------------------')
        timer = list(range(60,0,-1))
        pbar = tqdm(total=len(timer))
        while True:
            Max_total_jobs_in_queue_at_any_one_time, Max_jobs_running_in_queue_from_EKMC_mass_submit, Max_jobs_pending_in_queue_from_EKMC_mass_submit, wait_between_submissions, time_to_wait_before_next_submission, time_to_wait_max_queue, number_of_consecutive_error_before_exitting, time_to_wait_due_to_submission_error, Max_jobs_running_in_queue_from_EKMC_mass_submit = update_to_submission_settings(*update_to_submission_settings_inputs)
            is_pending_queue_full, number_of_jobs_in_pending_queue = check_if_can_submit_next_job(pending_slurm_jobs_queue, running_slurm_jobs_queue, Max_jobs_pending_in_queue_from_EKMC_mass_submit, Max_jobs_running_in_queue_from_EKMC_mass_submit, 'pending')
            if not is_pending_queue_full:
                break
            for seconds in timer:
                pbar.set_description('Pending Slurm Queue is full (Number of pending jobs: '+str(number_of_jobs_in_pending_queue)+'). Waiting: '+str(seconds)+' s')
                pbar.update()
                sleep(1)
            pbar.set_description('Pending Slurm Queue is full (Number of pending jobs: '+str(number_of_jobs_in_pending_queue)+'). Waiting: 0 s')
            pbar.update()
            pbar.reset()
        pbar.close()
        print('The Pending Slurm Queue is now NOT full. Will submit this job now and continue submitting other jobs.')

    # Fourth, wait until the number of jobs submitted by this program to slurm that are still running is less than a given value.
    Max_total_jobs_in_queue_at_any_one_time, Max_jobs_running_in_queue_from_EKMC_mass_submit, Max_jobs_pending_in_queue_from_EKMC_mass_submit, wait_between_submissions, time_to_wait_before_next_submission, time_to_wait_max_queue, number_of_consecutive_error_before_exitting, time_to_wait_due_to_submission_error, Max_jobs_running_in_queue_from_EKMC_mass_submit = update_to_submission_settings(*update_to_submission_settings_inputs)
    is_running_queue_full, number_of_jobs_in_running_queue = check_if_can_submit_next_job(pending_slurm_jobs_queue, running_slurm_jobs_queue, Max_jobs_pending_in_queue_from_EKMC_mass_submit, Max_jobs_running_in_queue_from_EKMC_mass_submit, 'running')
    if is_running_queue_full:
        if not waited:
            print('-----------------------------------------------------------------------------')
        waited = True
        timer = list(range(60,0,-1))
        pbar = tqdm(total=len(timer))
        while True:
            Max_total_jobs_in_queue_at_any_one_time, Max_jobs_running_in_queue_from_EKMC_mass_submit, Max_jobs_pending_in_queue_from_EKMC_mass_submit, wait_between_submissions, time_to_wait_before_next_submission, time_to_wait_max_queue, number_of_consecutive_error_before_exitting, time_to_wait_due_to_submission_error, Max_jobs_running_in_queue_from_EKMC_mass_submit = update_to_submission_settings(*update_to_submission_settings_inputs)
            is_running_queue_full, number_of_jobs_in_running_queue = check_if_can_submit_next_job(pending_slurm_jobs_queue, running_slurm_jobs_queue, Max_jobs_pending_in_queue_from_EKMC_mass_submit, Max_jobs_running_in_queue_from_EKMC_mass_submit, 'running')
            if not is_running_queue_full:
                break
            for seconds in pbar:
                pbar.set_description('Running Slurm Queue is full (Number of running jobs: '+str(number_of_jobs_in_pending_queue)+'). Waiting: '+str(seconds)+' s')
                pbar.update()
                sleep(1)
            pbar.set_description('Running Slurm Queue is full (Number of running jobs: '+str(number_of_jobs_in_pending_queue)+'). Waiting: 0 s')
            pbar.update()
            pbar.reset()
        pbar.close()
        print('The Running Slurm Queue is now NOT full. Will submit this job now and continue submitting other jobs.')

    if waited:
        print('-----------------------------------------------------------------------------')

# =========================================================================================================================================

def check_if_can_submit_next_job(pending_slurm_jobs_queue, running_slurm_jobs_queue, Max_jobs_pending_in_queue_from_EKMC_mass_submit, Max_jobs_running_in_queue_from_EKMC_mass_submit, list_type_to_check):
    """
    This method is designed to check if there are jobs run by this program currently in the slurm queue.

    If there are "Max_jobs_pending_in_queue_from_EKMC_mass_submit" number of these jobs in the slurm queue, this method will wait until some of the jobs have completed.
    
    Parameters
    ----------
    Max_jobs_pending_in_queue_from_EKMC_mass_submit : int
        This is the maximum number of jobs that we want in the pending queue that were submitted by this program.
    Max_jobs_running_in_queue_from_EKMC_mass_submit : int
        This is the maximum number of jobs that we want in the running queue that were submitted by this program.

    Returns
    -------
    Are the number of jobs pending (submitted by this program) less than Max_jobs_pending_in_queue_from_EKMC_mass_submit
    """

    # First, check to see what jobs of yours are currently in the slurm queue.
    username = getpass.getuser()
    check_queue_command = ['squeue','-r','-u',username]
    while True:
        process = Popen(check_queue_command, stdout=PIPE)
        #process.wait() # 60 seconds
        try:
            out, err = process.communicate(timeout=60) # 60 seconds
            break
        except TimeoutExpired:
            process.kill()
            print('There was an issue in running squeue. Will try again')
    output = out.decode() # Check this because I think it has issues if squeue changes during collection.

    # Second, determine which of the jobs submitted by this program are still pending or running in the slurm queue.
    live_running_queue = []
    live_pending_queue = []
    for line in output.split('\n')[1:-1:1]:

        # 2.1: Grab the job number from line
        line = line.split()
        full_jn = line[0]

        # 2.2: Get the job number for this job.
        jobset = full_jn.split('_')
        jn = int(jobset[0])

        # 2.4: Get the arrayjob number for this job if this job is an arrayjob.
        if len(jobset) >= 2:
            an = int(jobset[1])
        else:
            an = None

        # 2.5: Make the job set for this job, consisting of (job number, array number)
        jobset = (jn, an)

        # 2.2: Check if the job(s) is running or not
        running = line[4]

        # 2.3: Add the job to the running or pending live queue list. 
        if running == 'R':
            live_running_queue.append(jobset)
        if running == 'PD':
            live_pending_queue.append(jobset)
    
    # Third, sort the queues by id number
    if list_type_to_check == 'pending':
        live_pending_queue.sort()
    elif list_type_to_check == 'running':
        live_running_queue.sort()

    # Fourth, return the result depending on if you are wanting to analyse your pending or runnning queue. 
    if list_type_to_check == 'pending':
        return check_pending_queue(live_pending_queue, pending_slurm_jobs_queue, running_slurm_jobs_queue, Max_jobs_pending_in_queue_from_EKMC_mass_submit)
    elif list_type_to_check == 'running':
        return check_running_queue(live_running_queue, running_slurm_jobs_queue, Max_jobs_running_in_queue_from_EKMC_mass_submit)
    else:
        raise Exception('Error: list_type_to_check should be either "pending" or "running". list_type_to_check = '+str(list_type_to_check)+'. Check this out.')

def check_pending_queue(live_pending_queue, pending_slurm_jobs_queue, running_slurm_jobs_queue, Max_jobs_pending_in_queue_from_EKMC_mass_submit):
    """
    This method will compare which of the pending jobs in your slurm queue were submitted by this program.

    Parameters
    ----------
    live_pending_queue : list
        This is the pending queue that is currently in your slurm queue.
    pending_slurm_jobs_queue : list
        These are the pending jobs that were submitted by this program.
    running_slurm_jobs_queue : list
        These are the running jobs that were submitted by this program.
    Max_jobs_pending_in_queue_from_EKMC_mass_submit : int
        This is the maximum number of jobs that you want in your live slurm pending queue.

    Returns
    -------
    If the number of pending jobs is below the limit.
    """

    # First, check the pending_slurm_jobs_queue with the live_pending_queue
    for index in range(len(pending_slurm_jobs_queue)-1,-1,-1):
        job_details = pending_slurm_jobs_queue[index]
        if job_details not in live_pending_queue:
            running_slurm_jobs_queue.append(pending_slurm_jobs_queue.pop(index))

    # Second, determine if the maximum number of pending EKMC submit jobs has been reached
    if (Max_jobs_pending_in_queue_from_EKMC_mass_submit == 'Not Set') or (Max_jobs_pending_in_queue_from_EKMC_mass_submit is None):
        have_reached_maximum_no_of_pending_EKMC_submit_jobs = False
    else:
        have_reached_maximum_no_of_pending_EKMC_submit_jobs = len(pending_slurm_jobs_queue) >= Max_jobs_pending_in_queue_from_EKMC_mass_submit

    # Third, return if the number of pending jobs is below the limit.
    return have_reached_maximum_no_of_pending_EKMC_submit_jobs, len(pending_slurm_jobs_queue)

def check_running_queue(live_running_queue, running_slurm_jobs_queue, Max_jobs_running_in_queue_from_EKMC_mass_submit):
    """
    This method will compare which of the running jobs in your slurm queue were submitted by this program.

    Parameters
    ----------
    live_running_queue : list
        This is the running queue that is currently in your slurm queue.
    running_slurm_jobs_queue : list
        These are the running jobs that were submitted by this program.
    Max_jobs_running_in_queue_from_EKMC_mass_submit : int
        This is the maximum number of jobs that you want in your live slurm running queue.

    Returns
    -------
    If the number of running jobs is below the limit.
    """

    # First, check the running_slurm_jobs_queue with the live_running_queue
    for index in range(len(running_slurm_jobs_queue)-1,-1,-1):
        job_details = running_slurm_jobs_queue[index]
        if job_details not in live_running_queue:
            del running_slurm_jobs_queue[index]

    # Second, determine if the maximum number of pending EKMC submit jobs has been reached
    if Max_jobs_running_in_queue_from_EKMC_mass_submit == 'Not Set' or (Max_jobs_running_in_queue_from_EKMC_mass_submit is None):
        have_reached_maximum_no_of_running_EKMC_submit_jobs = False
    else:
        have_reached_maximum_no_of_running_EKMC_submit_jobs = len(running_slurm_jobs_queue) >= Max_jobs_running_in_queue_from_EKMC_mass_submit

    # Third, return if the number of pending jobs is below the limit.
    return have_reached_maximum_no_of_running_EKMC_submit_jobs, len(running_slurm_jobs_queue)

# =========================================================================================================================================

