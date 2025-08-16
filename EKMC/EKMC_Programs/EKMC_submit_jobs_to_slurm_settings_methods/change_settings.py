

from EKMC.EKMC_Programs.EKMC_submit_jobs_to_slurm_settings_methods.settings_methods import write_submit_settingsTXT_file

def change_settings(args, current_settings):
    """
    This method will allow the user to change the settings in the settings file. 

    Parameters
    ----------
    args : 

    current_settings : 
    """

    raise Exception('Need to write this')
    import pdb; pdb.set_trace()

    if len(args) > 2:
        print('Error in changing submit settings:')
        print('You can only enter at least two arguments after "Adsorber slurm"')
        print('Your input arguments are: '+str(args))
        exit('This program is closing without changing any settings')
    if   args[0] == 'Queue':







        
        write_submit_settingsTXT_file(path_to_settings_txt_file,time_to_wait_before_next_submission_due_to_not_waiting_between_submissions)
    elif args[0] == 'reset':
        write_submit_settingsTXT_file(path_to_settings_txt_file)
    else:
        print('No changes to seegins has been passed through to the EKMC program.')

# =========================================================================================================================================
