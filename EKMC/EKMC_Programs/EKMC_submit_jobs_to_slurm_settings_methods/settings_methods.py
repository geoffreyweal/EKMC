"""
update_settings_methods.py, Geoffrey Weal, 3/1/2023

These methods will allow the user to change settings for this program
"""
import os

# =========================================================================================================================================
# These are the default settings for this program.

# Maximum numbers of jobs in the ``EKMC submit`` queue:
Max_jobs_in_queue_at_any_one_time_DEFAULT = 2000
Max_jobs_running_in_queue_from_EKMC_mass_submit_DEFAULT = None
Max_jobs_pending_in_queue_from_EKMC_mass_submit_DEFAULT = 100

# Wait time to submit consecutives jobs to slurm: 
wait_between_submissions_DEFAULT = False
time_to_wait_before_next_submission_DEFAULT = 10.0

# Wait time to submit jobs if you have reached the maximum ``EKMC submit`` queue:
time_to_wait_max_queue_DEFAULT = 60.0

# Settings that control what happens if there is an error when submitting jobs to slurm: 
number_of_consecutive_error_before_exitting_DEFAULT = 20
time_to_wait_due_to_submission_error_DEFAULT = 20.0

# =========================================================================================================================================

def check_submit_settingsTXT(path_to_settings_txt_file):
    """
    This method will read in the settings for the program. 
    """

    # First, read in the settings file. If this doesnt exist yet.
    # This method will create a new settings file if it doesn't already exist. 
    if not os.path.exists(path_to_settings_txt_file):
        write_submit_settingsTXT_file(path_to_settings_txt_file)
    try:
        settings = read_submit_settingsTXT_file(path_to_settings_txt_file)
    except Exception as ee:
        write_submit_settingsTXT_file(path_to_settings_txt_file)
        settings = read_submit_settingsTXT_file(path_to_settings_txt_file)

    # Second, return the settings. 
    return settings

def read_submit_settingsTXT_file(path_to_settings_txt_file):
    """
    This method will read the settings file.
    """

    # First, read in the settings file.
    variables_found = []
    with open(path_to_settings_txt_file,'r') as submit_settingsTXT:
        for line in submit_settingsTXT:
            if   'Max_jobs_in_queue_at_any_one_time = ' in line:
                line = line.rstrip().replace('Max_jobs_in_queue_at_any_one_time = ','')
                Max_jobs_in_queue_at_any_one_time = int(line)
                variables_found.append('Max_jobs_in_queue_at_any_one_time')

            elif 'Max_jobs_running_in_queue_from_EKMC_mass_submit = ' in line:
                line = line.rstrip().replace('Max_jobs_running_in_queue_from_EKMC_mass_submit = ','')
                Max_jobs_running_in_queue_from_EKMC_mass_submit = 'Not Set' if ((line.lower() == 'None'.lower()) or (line is None)) else int(line)
                variables_found.append('Max_jobs_running_in_queue_from_EKMC_mass_submit')
            elif 'Max_jobs_pending_in_queue_from_EKMC_mass_submit = ' in line:
                line = line.rstrip().replace('Max_jobs_pending_in_queue_from_EKMC_mass_submit = ','')
                Max_jobs_pending_in_queue_from_EKMC_mass_submit = 'Not Set' if ((line.lower() == 'None'.lower()) or (line is None)) else int(line)
                variables_found.append('Max_jobs_pending_in_queue_from_EKMC_mass_submit')

            elif 'wait_between_submissions = ' in line:
                line = line.rstrip().replace('wait_between_submissions = ','')
                if line.lower() == 'true':
                    wait_between_submissions = True
                elif line.lower() == 'false':
                    wait_between_submissions = False
                else:
                    raise Exception('Error: wait_between_submissions must be either True or False. wait_between_submissions = '+str(wait_between_submissions))
                variables_found.append('wait_between_submissions')
            elif 'time_to_wait_before_next_submission = ' in line:
                line = line.rstrip().replace('time_to_wait_before_next_submission = ','')
                time_to_wait_before_next_submission = float(line)
                variables_found.append('time_to_wait_before_next_submission')

            elif 'time_to_wait_max_queue = ' in line:
                line = line.rstrip().replace('time_to_wait_max_queue = ','')
                time_to_wait_max_queue = float(line)
                variables_found.append('time_to_wait_max_queue')

            elif 'number_of_consecutive_error_before_exitting = ' in line:
                line = line.rstrip().replace('number_of_consecutive_error_before_exitting = ','')
                number_of_consecutive_error_before_exitting = int(line)
                variables_found.append('number_of_consecutive_error_before_exitting')
            elif 'time_to_wait_due_to_submission_error = ' in line:
                line = line.rstrip().replace('time_to_wait_due_to_submission_error = ','')
                time_to_wait_due_to_submission_error = float(line)
                variables_found.append('time_to_wait_due_to_submission_error')

    # Second, check that all the variables have been obtained from the settings file. 
    # 2.1: Determine which variables are contained in the settings file. 
    variables_needed = ['Max_jobs_in_queue_at_any_one_time', 'Max_jobs_running_in_queue_from_EKMC_mass_submit', 'Max_jobs_pending_in_queue_from_EKMC_mass_submit', 'wait_between_submissions', 'time_to_wait_before_next_submission', 'time_to_wait_max_queue', 'number_of_consecutive_error_before_exitting', 'time_to_wait_due_to_submission_error']
    variables_you_do_not_have_in_settingsTXT = []
    for variable in variables_needed:
        if not variable in locals():
            variables_you_do_not_have_in_settingsTXT.append(variable)
    if not len(variables_you_do_not_have_in_settingsTXT) == 0:
        print(variables_you_do_not_have_in_settingsTXT)
        import pdb; pdb.set_trace()
        exit('Error')

    # Third, check that no variables have been entered twice:
    if not (len(variables_found) == len(set(variables_found))):
        print(variables_you_do_not_have_in_settingsTXT)
        import pdb; pdb.set_trace()
        exit('Error')

    # Fourth, return all the settings from the settings file.
    return Max_jobs_in_queue_at_any_one_time, Max_jobs_running_in_queue_from_EKMC_mass_submit, Max_jobs_pending_in_queue_from_EKMC_mass_submit, wait_between_submissions, time_to_wait_before_next_submission, time_to_wait_max_queue, number_of_consecutive_error_before_exitting, time_to_wait_due_to_submission_error

def write_submit_settingsTXT_file(path_to_settings_txt_file, Max_jobs_in_queue_at_any_one_time=Max_jobs_in_queue_at_any_one_time_DEFAULT, Max_jobs_running_in_queue_from_EKMC_mass_submit=Max_jobs_running_in_queue_from_EKMC_mass_submit_DEFAULT, Max_jobs_pending_in_queue_from_EKMC_mass_submit=Max_jobs_pending_in_queue_from_EKMC_mass_submit_DEFAULT, wait_between_submissions=wait_between_submissions_DEFAULT, time_to_wait_before_next_submission=time_to_wait_before_next_submission_DEFAULT, time_to_wait_max_queue=time_to_wait_max_queue_DEFAULT, number_of_consecutive_error_before_exitting=number_of_consecutive_error_before_exitting_DEFAULT, time_to_wait_due_to_submission_error=time_to_wait_due_to_submission_error_DEFAULT): 
    """
    This method will write the new settings to the settings file.
    """
    with open(path_to_settings_txt_file,'w') as submit_settingsTXT:
        submit_settingsTXT.write('Max_jobs_in_queue_at_any_one_time = '+str(Max_jobs_in_queue_at_any_one_time)+'\n')
        submit_settingsTXT.write('Max_jobs_running_in_queue_from_EKMC_mass_submit = '+str(Max_jobs_running_in_queue_from_EKMC_mass_submit)+'\n')
        submit_settingsTXT.write('Max_jobs_pending_in_queue_from_EKMC_mass_submit = '+str(Max_jobs_pending_in_queue_from_EKMC_mass_submit)+'\n')
        submit_settingsTXT.write('wait_between_submissions = '+str(wait_between_submissions)+'\n')
        submit_settingsTXT.write('time_to_wait_before_next_submission = '+str(time_to_wait_before_next_submission)+'\n')
        submit_settingsTXT.write('time_to_wait_max_queue = '+str(time_to_wait_max_queue)+'\n')
        submit_settingsTXT.write('number_of_consecutive_error_before_exitting = '+str(number_of_consecutive_error_before_exitting)+'\n')
        submit_settingsTXT.write('time_to_wait_due_to_submission_error = '+str(time_to_wait_due_to_submission_error)+'\n')

# =========================================================================================================================================

