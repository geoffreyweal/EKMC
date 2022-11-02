import os

class CLICommand:
    """Submit Gaussian+Multiwfn ATC jobs and Gaussian EET jobs to slurm.
    """

    @staticmethod
    def add_arguments(parser):
        parser.add_argument('settings', nargs='*', help='Enter in here a setting for submit that you would like to change.')

    @staticmethod
    def run(args_submit):
        args_submit_settings = args_submit.settings
        check_submit_settingsTXT()
        if len(args_submit_settings) > 0:
            continue_running, wait_between_submissions = change_settings(args_submit_settings)
        else:
            continue_running = True
            wait_between_submissions = False
        if continue_running:
            Run_method(wait_between_submissions)

# ------------------------------------------------------
# These variables can be changed by the user.
this_scripts_path = os.path.dirname(os.path.abspath(__file__))
submit_settings_name = 'submit_settings.txt'
path_to_txt_file = this_scripts_path+'/'+submit_settings_name

Max_jobs_in_queue_at_any_one_time_DEFAULT = 5000
time_to_wait_before_next_submission_DEFAULT = 20.0
time_to_wait_max_queue_DEFAULT = 60.0

time_to_wait_before_next_submission_due_to_temp_submission_issue_DEFAULT = 10.0
number_of_consecutive_error_before_exitting_DEFAULT = 'inf'

time_to_wait_before_next_submission_due_to_not_waiting_between_submissions_DEFAULT = 60.0
# ------------------------------------------------------
# =========================================================================================================================================

def read_submit_settingsTXT_file(path_to_txt_file):
    with open(path_to_txt_file,'r') as submit_settingsTXT:
        for line in submit_settingsTXT:
            if   'Max_jobs_in_queue_at_any_one_time = ' in line:
                line = line.rstrip().replace('Max_jobs_in_queue_at_any_one_time = ','')
                Max_jobs_in_queue_at_any_one_time = int(line)
            elif 'time_to_wait_before_next_submission = ' in line:
                line = line.rstrip().replace('time_to_wait_before_next_submission = ','')
                time_to_wait_before_next_submission = float(line)
            elif 'time_to_wait_max_queue = ' in line:
                line = line.rstrip().replace('time_to_wait_max_queue = ','')
                time_to_wait_max_queue = float(line)
            elif 'time_to_wait_before_next_submission_due_to_temp_submission_issue = ' in line:
                line = line.rstrip().replace('time_to_wait_before_next_submission_due_to_temp_submission_issue = ','')
                time_to_wait_before_next_submission_due_to_temp_submission_issue = float(line)
            elif 'number_of_consecutive_error_before_exitting = ' in line:
                line = line.rstrip().replace('number_of_consecutive_error_before_exitting = ','')
                if 'inf' in line.lower():
                    number_of_consecutive_error_before_exitting = float('inf')
                else:
                    number_of_consecutive_error_before_exitting = int(line)
            elif 'time_to_wait_before_next_submission_due_to_not_waiting_between_submissions = ' in line:
                line = line.rstrip().replace('time_to_wait_before_next_submission_due_to_not_waiting_between_submissions = ','')
                time_to_wait_before_next_submission_due_to_not_waiting_between_submissions = float(line)
    variables_needed = ['Max_jobs_in_queue_at_any_one_time','time_to_wait_before_next_submission','time_to_wait_max_queue','time_to_wait_before_next_submission_due_to_temp_submission_issue','number_of_consecutive_error_before_exitting','time_to_wait_before_next_submission_due_to_not_waiting_between_submissions']
    variables_you_do_not_have_in_settingsTXT = []
    for variable in variables_needed:
        if not variable in locals():
            variables_you_do_not_have_in_settingsTXT.append(variable)
    if not len(variables_you_do_not_have_in_settingsTXT) == 0:
        print('Error')
        print(variables_you_do_not_have_in_settingsTXT)
        import pdb; pdb.set_trace()
        exit('Error')
    return Max_jobs_in_queue_at_any_one_time,time_to_wait_before_next_submission,time_to_wait_max_queue,time_to_wait_before_next_submission_due_to_temp_submission_issue,number_of_consecutive_error_before_exitting,time_to_wait_before_next_submission_due_to_not_waiting_between_submissions

def write_submit_settingsTXT_file(path_to_txt_file,Max_jobs_in_queue_at_any_one_time=Max_jobs_in_queue_at_any_one_time_DEFAULT,time_to_wait_before_next_submission=time_to_wait_before_next_submission_DEFAULT,time_to_wait_max_queue=time_to_wait_max_queue_DEFAULT,time_to_wait_before_next_submission_due_to_temp_submission_issue=time_to_wait_before_next_submission_due_to_temp_submission_issue_DEFAULT,number_of_consecutive_error_before_exitting=number_of_consecutive_error_before_exitting_DEFAULT,time_to_wait_before_next_submission_due_to_not_waiting_between_submissions=time_to_wait_before_next_submission_due_to_not_waiting_between_submissions_DEFAULT):
    with open(path_to_txt_file,'w') as submit_settingsTXT:
        submit_settingsTXT.write('Max_jobs_in_queue_at_any_one_time = '+str(Max_jobs_in_queue_at_any_one_time)+'\n')
        submit_settingsTXT.write('time_to_wait_before_next_submission = '+str(time_to_wait_before_next_submission)+'\n')
        submit_settingsTXT.write('time_to_wait_max_queue = '+str(time_to_wait_max_queue)+'\n')
        submit_settingsTXT.write('time_to_wait_before_next_submission_due_to_temp_submission_issue = '+str(time_to_wait_before_next_submission_due_to_temp_submission_issue)+'\n')
        submit_settingsTXT.write('number_of_consecutive_error_before_exitting = '+str(number_of_consecutive_error_before_exitting)+'\n')
        submit_settingsTXT.write('time_to_wait_before_next_submission_due_to_not_waiting_between_submissions = '+str(time_to_wait_before_next_submission_due_to_not_waiting_between_submissions)+'\n')

def check_submit_settingsTXT():
    if not os.path.exists(path_to_txt_file):
        write_submit_settingsTXT_file(path_to_txt_file)
    try:
        read_submit_settingsTXT_file(path_to_txt_file)
    except Exception as ee:
        write_submit_settingsTXT_file(path_to_txt_file)

def change_settings(args):
    continue_running = False
    wait_between_submissions = False
    if len(args) > 2:
        print('Error in changing submit settings:')
        print('You can only enter at least two arguments after "Adsorber slurm"')
        print('Your input arguments are: '+str(args))
        exit('This program is closing without changing any settings')
    if   args[0] == 'max':
        if len(args) == 1:
            print('Setting Max_jobs_in_queue_at_any_one_time to default ('+str(Max_jobs_in_queue_at_any_one_time_DEFAULT)+')')
            Max_jobs_in_queue_at_any_one_time = Max_jobs_in_queue_at_any_one_time_DEFAULT
        elif not instance(args[1],int):
            print('Error in changing submit sertings:')
            print('You need to enter an int if you want to change the settings for Max_jobs_in_queue_at_any_one_time')
            print('Your input value is: '+str(args[1]))
            exit('This program is closing without changing any settings')
        else:
            Max_jobs_in_queue_at_any_one_time = args[1]
        write_submit_settingsTXT_file(path_to_txt_file,Max_jobs_in_queue_at_any_one_time)
    elif args[0] == 'wait':
        if len(args) == 1:
            print('Setting time_to_wait_before_next_submission to default ('+str(time_to_wait_before_next_submission_DEFAULT)+')')
            time_to_wait_before_next_submission = time_to_wait_before_next_submission_DEFAULT
        elif not instance(args[1],float):
            print('Error in changing submit sertings:')
            print('You need to enter a float if you want to change the settings for time_to_wait_before_next_submission')
            print('Your input value is: '+str(args[1]))
            exit('This program is closing without changing any settings')
        else:
            time_to_wait_before_next_submission = args[1]
        write_submit_settingsTXT_file(path_to_txt_file,time_to_wait_before_next_submission)
    elif args[0] == 'wait_max_queue':
        if len(args) == 2:
            print('Setting time_to_wait_max_queue to default ('+str(time_to_wait_max_queue_DEFAULT)+')')
            time_to_wait_max_queue = time_to_wait_max_queue_DEFAULT
        elif not instance(args[1],float):
            print('Error in changing submit sertings:')
            print('You need to enter a float if you want to change the settings for time_to_wait_max_queue')
            print('Your input value is: '+str(args[1]))
            exit('This program is closing without changing any settings')
        else:
            time_to_wait_max_queue = args[1]
        write_submit_settingsTXT_file(path_to_txt_file,time_to_wait_max_queue)
    elif args[0] == 'wait_error':
        if len(args) == 2:
            print('Setting time_to_wait_before_next_submission_due_to_temp_submission_issue to default ('+str(time_to_wait_before_next_submission_due_to_temp_submission_issue_DEFAULT)+')')
            time_to_wait_before_next_submission_due_to_temp_submission_issue = time_to_wait_before_next_submission_due_to_temp_submission_issue_DEFAULT
        elif not instance(args[1],float):
            print('Error in changing submit sertings:')
            print('You need to enter a float if you want to change the settings for time_to_wait_before_next_submission_due_to_temp_submission_issue')
            print('Your input value is: '+str(args[1]))
            exit('This program is closing without changing any settings')
        else:
            time_to_wait_before_next_submission_due_to_temp_submission_issue = args[1]
        write_submit_settingsTXT_file(path_to_txt_file,time_to_wait_before_next_submission_due_to_temp_submission_issue)
    elif args[0] == 'no_conse_errors':
        if len(args) == 2:
            print('Setting number_of_consecutive_error_before_exitting to default ('+str(number_of_consecutive_error_before_exitting_DEFAULT)+')')
            number_of_consecutive_error_before_exitting = number_of_consecutive_error_before_exitting_DEFAULT
        elif not instance(args[1],int):
            print('Error in changing submit sertings:')
            print('You need to enter a int if you want to change the settings for number_of_consecutive_error_before_exitting')
            print('Your input value is: '+str(args[1]))
            exit('This program is closing without changing any settings')
        else:
            number_of_consecutive_error_before_exitting = args[1]
        write_submit_settingsTXT_file(path_to_txt_file,number_of_consecutive_error_before_exitting)
    elif args[0] == 'wait_mass':
        if len(args) == 2:
            print('Setting time_to_wait_before_next_submission_due_to_not_waiting_between_submissions to default ('+str(time_to_wait_before_next_submission_due_to_not_waiting_between_submissions_DEFAULT)+')')
            time_to_wait_before_next_submission_due_to_not_waiting_between_submissions = time_to_wait_before_next_submission_due_to_not_waiting_between_submissions_DEFAULT
        elif not instance(args[1],float):
            print('Error in changing submit sertings:')
            print('You need to enter a float if you want to change the settings for time_to_wait_before_next_submission_due_to_not_waiting_between_submissions')
            print('Your input value is: '+str(args[1]))
            exit('This program is closing without changing any settings')
        else:
            time_to_wait_before_next_submission_due_to_not_waiting_between_submissions = args[1]
        write_submit_settingsTXT_file(path_to_txt_file,time_to_wait_before_next_submission_due_to_not_waiting_between_submissions)
    elif args[0] == 'reset':
         write_submit_settingsTXT_file(path_to_txt_file)
    elif args[0] in ['t','true']:
        wait_between_submissions = True
        continue_running = True
    elif args[0] in ['f','false']:
        wait_between_submissions = False
        continue_running = True
    else:
        pass
    return continue_running, wait_between_submissions

# =========================================================================================================================================

def is_sim_folder_in_directory(dirpath, dirnames):
    """
    This method is designed to determine if a EKMC simulation folder exists in the dirpath directory
    """
    for dirname in dirnames:
        if os.path.exists(dirpath+'/'+dirname) and os.path.isdir(dirpath+'/'+dirname):
            return True
    return False

# =========================================================================================================================================

def Run_method(wait_between_submissions):
    '''
    Geoffrey Weal, Run_Adsorber_submitSL_slurm.py, 16/06/2021

    This program is designed to submit all sl files called submit.sl to slurm

    '''
    print('###########################################################################')
    print('###########################################################################')
    print('Run_ekmc_mass_submitSL_slurm.py')
    print('###########################################################################')
    print('This program is designed to submit all your submit.sl scripts appropriately to slurm.')
    print('###########################################################################')
    print('###########################################################################')

    import time, sys
    import subprocess

    Max_jobs_in_queue_at_any_one_time,time_to_wait_before_next_submission,time_to_wait_max_queue,time_to_wait_before_next_submission_due_to_temp_submission_issue,number_of_consecutive_error_before_exitting,time_to_wait_before_next_submission_due_to_not_waiting_between_submissions = read_submit_settingsTXT_file(path_to_txt_file)

    if wait_between_submissions == True:
        print('This program will wait one minute between submitting jobs.')
    else:
        print('This program will not wait between submitting jobs.')
    path = os.getcwd()

    def countdown(t):
        print('Will wait for ' + str(float(t)/60.0) + ' minutes, then will resume Slurm submissions.\n')
        while t:
            mins, secs = divmod(t, 60)
            timeformat = str(mins) + ':' + str(secs)
            sys.stdout.write("\r                                                                                   ")
            sys.stdout.flush()
            sys.stdout.write("\rCountdown: " + str(timeformat))
            sys.stdout.flush()
            time.sleep(1)
            t -= 1
        print('Resuming Pan Submissions.\n')

    def myrun(cmd):
        proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout_lines = list(iter(proc.stdout.readline,b''))
        stdout_lines = [line.decode() for line in stdout_lines]
        return ''.join(stdout_lines)

    ###########################################################################################
    ###########################################################################################
    ###########################################################################################

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

    command = "squeue -r -u $USER"
    def check_max_jobs_in_queue_after_next_submission(dirpath):
        while True:
            text = myrun(command)
            nlines = len(text.splitlines())-1
            if not (nlines == -1):
                break
            else:
                print('Could not get the number of jobs in the slurm queue. Retrying to get this value.')
        number_of_trials_to_be_submitted = get_number_to_trials_that_will_be_submitted_by_ekmc_mass_submitSL(dirpath)
        if nlines > Max_jobs_in_queue_at_any_one_time - number_of_trials_to_be_submitted:
            return True, nlines
        else:
            return False, nlines

    ###########################################################################################
    ###########################################################################################
    ###########################################################################################

    # Check to make sure the array line in all ekmc_mass_submit.sl scripts is there and that none of the mass_submission script submit more than Max_jobs_in_queue_at_any_one_time
    # into the queue. 
    print('-----------------------------------------------')
    print('Checking to make sure that the array line in all ekmc_mass_submit.sl scripts is there and that none of the mass_submission script submit more than Max_jobs_in_queue_at_any_one_time into the queue.')
    for (dirpath, dirnames, filenames) in os.walk(path):
        dirnames.sort()
        if 'ekmc_mass_submit.sl' in filenames:
            no_of_trials_that_will_be_submitted = get_number_to_trials_that_will_be_submitted_by_ekmc_mass_submitSL(dirpath)
            if no_of_trials_that_will_be_submitted > Max_jobs_in_queue_at_any_one_time:
                print('Issue: The number of Trials that you want to submit is greater the number of trials you are allowed to submit at any one time.')
                print('Number of jobs that will be submitted by '+str(dirpath)+'/ekmc_mass_submit.sl: '+str(no_of_trials_that_will_be_submitted))
                print('Maximum number of trials that can be submitted into slurm: '+str(Max_jobs_in_queue_at_any_one_time))
                print('Consider doing either:')
                print('    1) Using the scripts Create_submitSL_slurm.py and Run_submitSL_slurm.py to run your jobs. This will submit your jobs individually and has better control over submitting this large number of trials within slurm without causing issues with slurm.')
                print('    2) Contact your slurm technical support about increasing the maximum number of jobs that can be found in the queue at any one time.')
                print('This program will exit without doing anything.')
                exit()
            dirnames[:] = []
            filenames[:] = []
    print('All clear to submit your ekmc_mass_submit.sl scripts.')
    print('-----------------------------------------------')
    print('*****************************************************************************')
    print('*****************************************************************************')
    print('Submitting ekmc_mass_submit.sl scripts to slurm.')
    print()
    print('*****************************************************************************')

    # Time to submit all the GA scripts! Lets get this stuff going!
    error_counter = 0
    for (dirpath, dirnames, filenames) in os.walk(path):
        dirnames.sort()
        if 'ekmc_mass_submit.sl' in filenames:
            # Determine if this submission script has already been submitted.
            # This is best practise to prevent slurm from being overloaded with successful jobs (as they have already run completely) that end immediately.
            # Submit any jobs where some simulations have already begun by hand to prevent slurm breaking issues.
            if is_sim_folder_in_directory(dirpath, dirnames):
                print('Found Sim folders in '+str(dirpath)+', indicating this has already been submitted. Will continue on.')
                print('If you need to submit these jobs, it is best to do this by hand and submit only the ekmc_mass_submit.sl files that you need to submit.')
                print('This is because if many of your simulations have already completed, they finish immediately.')
                print('Slurm is not good with dealling with hundreds of jobs finishing quickly and at the same time.')
                print('Submit the simulations you want to perform by hand in order to minimise this issue arising.')
                print('*****************************************************************************')
                dirnames[:] = []
                filenames[:] = []
                continue
            # determine if it is the right time to submit jobs
            print('*****************************************************************************')
            while True:
                reached_max_jobs, number_in_queue = check_max_jobs_in_queue_after_next_submission(dirpath)
                if reached_max_jobs:
                    print('-----------------------------------------------------------------------------')
                    print('You can not have any more jobs in the queue before submitting the mass_sub. Will wait a bit of time for some of them to complete')
                    print('Number of Jobs in the queue = '+str(number_in_queue))
                    countdown(time_to_wait_before_next_submission)
                    print('-----------------------------------------------------------------------------')
                else:
                    print('The number of jobs in the queue currently is: '+str(number_in_queue))
                    break
            # submit the jobs
            os.chdir(dirpath)
            name = dirpath.replace(path, '').split('/', -1)[1:]
            name = "_".join(str(x) for x in name)
            print("Submitting " + str(name) + " to slurm.")
            print('Submission .sl file found in: '+str(os.getcwd()))
            ekmc_mass_submit_files = [filename for filename in filenames if (filename.startswith('ekmc_mass_submit') and filename.endswith('.sl'))]
            ekmc_mass_submit_files.sort(key=lambda x: 1 if (x.replace('ekmc_mass_submit','').replace('.sl','') == '') else int(x.replace('ekmc_mass_submit_','').replace('.sl','')))
            error_counter = 0
            for ekmc_mass_submit_filename in ekmc_mass_submit_files:
                submitting_command = "sbatch "+ekmc_mass_submit_filename
                while True:
                    if error_counter == number_of_consecutive_error_before_exitting:
                        break
                    else:
                        proc = subprocess.Popen(submitting_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                        if not proc.wait() == 0:
                            error_counter += 1
                            if error_counter == number_of_consecutive_error_before_exitting:
                                print('----------------------------------------------')
                                print('Error in submitting submit script to slurm.')
                                print('I got '+str(number_of_consecutive_error_before_exitting)+" consecutive errors. Something must not be working right somewhere. I'm going to stop here just in case something is not working.")
                                print('')
                                print('The following ekmc_mass_submit.sl scripts WERE NOT SUBMITTED TO SLURM')
                                print('')
                            else:
                                stdout, stderr = proc.communicate()
                                print('----------------------------------------------')
                                print('Error in submitting submit script to slurm. This error was:')
                                print(stderr)
                                print('Number of consecutive errors: '+str(error_counter))
                                print('Run_ekmc_mass_submitSL_slurm.py will retry submitting this job to slurm after '+str(time_to_wait_before_next_submission_due_to_temp_submission_issue)+' seconds of wait time')
                                print('----------------------------------------------')
                                countdown(time_to_wait_before_next_submission_due_to_temp_submission_issue)
                        else:
                            break
            if error_counter == number_of_consecutive_error_before_exitting:
                print(dirpath)
            elif not wait_between_submissions:
                pass # do not wait any time before proceeding to the next submission.
            else:
                reached_max_jobs, number_in_queue = check_max_jobs_in_queue_after_next_submission(dirpath)
                print('The number of jobs in the queue after submitting job is currently is: '+str(number_in_queue))
                #print('Will wait for '+str(time_to_wait_max_queue)+' to give time between consecutive submissions')
                countdown(time_to_wait_max_queue)
                print('*****************************************************************************')
            dirnames[:] = []
            filenames[:] = []

    if error_counter == number_of_consecutive_error_before_exitting:
        print('----------------------------------------------')
        print()
        print('"Run_ekmc_mass_submitSL_slurm.py" will finish WITHOUT HAVING SUBMITTED ALL JOBS.')
        print()
        print('*****************************************************************************')
        print('NOT ALL ekmc_mass_submit.sl SCRIPTS WERE SUBMITTED SUCCESSFULLY.')
        print('*****************************************************************************') 
    else:
        print('*****************************************************************************')
        print('*****************************************************************************')
        print('*****************************************************************************')
        print('All ekmc_mass_submit.sl scripts have been submitted to slurm successfully.')
        print('*****************************************************************************')
        print('*****************************************************************************')
        print('*****************************************************************************')