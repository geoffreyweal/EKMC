"""
print_settings.py, Geoffrey Weal, 3/1/2023

These method will print the current settings for EKMC submit
"""
import os

def print_settings(settings):
    """
    This method will print the current ``EKMC submit`` settings.

    Parameters
    ----------
    settings : tuple
        This contains all the settings for ``EKMC submit``.
    """
    Max_jobs_in_queue_at_any_one_time, Max_jobs_in_queue_at_any_one_time_running, Max_jobs_in_queue_at_any_one_time_pending, wait_between_submissions, time_to_wait_before_next_submission, time_to_wait_max_queue, number_of_consecutive_error_before_exitting, time_to_wait_due_to_submission_error = settings
    print('Current EKMC submit settings:')
    print()
    print("Setting Keyword: Value")
    print()
    print('Queue (Max total number of jobs in your slurm queue): '+str(Max_jobs_in_queue_at_any_one_time))
    print()
    print('Running (Max number of EKMC jobs running in the queue, None=Not Max Set): '+str(Max_jobs_in_queue_at_any_one_time_running))
    print('Pending (Max number of EKMC jobs pending in the queue, None=Not Max Set): '+str(Max_jobs_in_queue_at_any_one_time_pending))
    print()
    print('SubWait (Do you want to wait between submissions): '+str(wait_between_submissions))
    print('SubWaitTime ( If SubWait = True, this is the amount of time to wait between submissions): '+str(time_to_wait_before_next_submission))
    print()
    print('QueueWaitTime (This is the amount of time to wait in the queue before trying to submit again): '+str(time_to_wait_max_queue))
    print()
    print('Errors (The number of consecutive errors when trying to submit the same job before this submission program finishes on the spot): '+str(number_of_consecutive_error_before_exitting))
    print('ErrorWaitTime (The time to wait before attempting to submit a job that has had a submission error before): '+str(time_to_wait_due_to_submission_error))
    print()
    print('Note: The names of the variables in the EKMC/EKMC_Programs/EKMC_submit_jobs_to_slurm_settings_methods/submit_settings.txt file that you can modify are:')
    print()
    print('Queue:         Max_total_jobs_in_queue_at_any_one_time')
    print('Running:       Max_jobs_running_in_queue_from_EKMC_mass_submit')
    print('Pending:       Max_jobs_pending_in_queue_from_EKMC_mass_submit')
    print('SubWait:       wait_between_submissions ')
    print('SubWaitTime:   time_to_wait_before_next_submission')
    print('QueueWaitTime: time_to_wait_max_queue')
    print('Errors:        number_of_consecutive_error_before_exitting')
    print('ErrorWaitTime: time_to_wait_due_to_submission_error')
    