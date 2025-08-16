'''
Geoffrey Weal, update_to_submission_settings.py, 30/09/2023

This program is designed to allow the program to update itself if the submit_settings.txt file is changed by the user. 
'''
from EKMC.EKMC_Programs.EKMC_submit_jobs_to_slurm_settings_methods.settings_methods import check_submit_settingsTXT, read_submit_settingsTXT_file

def update_to_submission_settings(path_to_settings_txt_file, Max_total_jobs_in_queue_at_any_one_time, Max_jobs_running_in_queue_from_EKMC_mass_submit, Max_jobs_pending_in_queue_from_EKMC_mass_submit, wait_between_submissions, time_to_wait_before_next_submission, time_to_wait_max_queue, number_of_consecutive_error_before_exitting, time_to_wait_due_to_submission_error):
    """
    This method will update the ``EKMC submit`` program settings if they were changed while this program was running. 
    """

    # First, make a check on the subission settings
    check_submit_settingsTXT(path_to_settings_txt_file)

    # Second, get any updated variables from the settings text file.
    updated_Max_total_jobs_in_queue_at_any_one_time, updated_Max_jobs_running_in_queue_from_EKMC_mass_submit, updated_Max_jobs_pending_in_queue_from_EKMC_mass_submit, updated_wait_between_submissions, updated_time_to_wait_before_next_submission, updated_time_to_wait_max_queue, updated_number_of_consecutive_error_before_exitting, updated_time_to_wait_due_to_submission_error = read_submit_settingsTXT_file(path_to_settings_txt_file)

    # Third, determine which settings have been updated.
    did_update_Max_total_jobs_in_queue_at_any_one_time         = not (updated_Max_total_jobs_in_queue_at_any_one_time         == Max_total_jobs_in_queue_at_any_one_time)
    did_update_Max_jobs_running_in_queue_from_EKMC_mass_submit = not (updated_Max_jobs_running_in_queue_from_EKMC_mass_submit == Max_jobs_running_in_queue_from_EKMC_mass_submit)
    did_update_Max_jobs_pending_in_queue_from_EKMC_mass_submit = not (updated_Max_jobs_pending_in_queue_from_EKMC_mass_submit == Max_jobs_pending_in_queue_from_EKMC_mass_submit)
    did_update_wait_between_submissions                        = not (updated_wait_between_submissions                        == wait_between_submissions)
    did_update_time_to_wait_before_next_submission             = not (updated_time_to_wait_before_next_submission             == time_to_wait_before_next_submission)
    did_update_time_to_wait_max_queue                          = not (updated_time_to_wait_max_queue                          == time_to_wait_max_queue)
    did_update_number_of_consecutive_error_before_exitting     = not (updated_number_of_consecutive_error_before_exitting     == number_of_consecutive_error_before_exitting)
    did_update_time_to_wait_due_to_submission_error            = not (updated_time_to_wait_due_to_submission_error            == time_to_wait_due_to_submission_error)

    # Fourth, print to terminal any updates that have been made:
    if did_update_Max_total_jobs_in_queue_at_any_one_time or did_update_Max_jobs_running_in_queue_from_EKMC_mass_submit or did_update_Max_jobs_pending_in_queue_from_EKMC_mass_submit or did_update_wait_between_submissions or did_update_time_to_wait_before_next_submission or did_update_time_to_wait_max_queue or did_update_number_of_consecutive_error_before_exitting or did_update_time_to_wait_due_to_submission_error:
        print('Update made to settings')
        if did_update_Max_total_jobs_in_queue_at_any_one_time:
            print('Max_total_jobs_in_queue_at_any_one_time: '        +str(Max_total_jobs_in_queue_at_any_one_time)        +' --> '+str(updated_Max_total_jobs_in_queue_at_any_one_time))
        if did_update_Max_jobs_running_in_queue_from_EKMC_mass_submit:
            print('Max_jobs_running_in_queue_from_EKMC_mass_submit: '+str(Max_jobs_running_in_queue_from_EKMC_mass_submit)+' --> '+str(updated_Max_jobs_running_in_queue_from_EKMC_mass_submit))
        if did_update_Max_jobs_pending_in_queue_from_EKMC_mass_submit:
            print('Max_jobs_pending_in_queue_from_EKMC_mass_submit: '+str(Max_jobs_pending_in_queue_from_EKMC_mass_submit)+' --> '+str(updated_Max_jobs_pending_in_queue_from_EKMC_mass_submit))
        if did_update_wait_between_submissions:
            print('wait_between_submissions: '                       +str(wait_between_submissions)                       +' --> '+str(updated_wait_between_submissions))
        if did_update_time_to_wait_before_next_submission:
            print('time_to_wait_before_next_submission: '            +str(time_to_wait_before_next_submission)            +' --> '+str(updated_time_to_wait_before_next_submission))
        if did_update_time_to_wait_max_queue:
            print('time_to_wait_max_queue: '                         +str(time_to_wait_max_queue)                         +' --> '+str(updated_time_to_wait_max_queue))
        if did_update_number_of_consecutive_error_before_exitting:
            print('number_of_consecutive_error_before_exitting: '    +str(number_of_consecutive_error_before_exitting)    +' --> '+str(updated_number_of_consecutive_error_before_exitting))
        if did_update_time_to_wait_due_to_submission_error:
            print('time_to_wait_due_to_submission_error: '           +str(time_to_wait_due_to_submission_error)           +' --> '+str(updated_time_to_wait_due_to_submission_error))

    # Fifth, return updated settngs
    return updated_Max_total_jobs_in_queue_at_any_one_time, updated_Max_jobs_running_in_queue_from_EKMC_mass_submit, updated_Max_jobs_pending_in_queue_from_EKMC_mass_submit, updated_wait_between_submissions, updated_time_to_wait_before_next_submission, updated_time_to_wait_max_queue, updated_number_of_consecutive_error_before_exitting, updated_time_to_wait_due_to_submission_error, updated_Max_jobs_running_in_queue_from_EKMC_mass_submit
