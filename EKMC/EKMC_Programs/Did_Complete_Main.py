'''
Did_Complete_Main.py, Geoffrey Weal, 08/03/2019

This program will determine which of your dimers have been successfully calculated in Gaussian.
'''
import os, sys, subprocess

def tail(f, n, offset=0):
    proc = subprocess.Popen(['tail', '-n', str(n + offset), f], stdout=subprocess.PIPE)
    lines = proc.stdout.readlines()
    return lines

def get_variables_from_run(filepath):
    with open(filepath+'/Run_EKMC.py','r') as RunPY:
        sim_time_limit = None
        for line in RunPY:
            if line.startswith('sim_time_limit = '):
                sim_time_limit = float(eval(line.replace('sim_time_limit = ','')))
                break
    if sim_time_limit is None:
        print('Error')
        print(sim_time_limit)
        import pdb; pdb.set_trace()
        exit('Error')
    return sim_time_limit

problem_simulations = []
def Did_Simulation_finish_successfully(filepath):
    """
    This method will go through the kMC_sim.txt file and see if the simulation completed or not.
 
    Parameters
    ----------
    filepath : str.
        This is the path to the output.log file.

    Returns
    -------
    True if finished successfully. False if not.
    """

    # First, obtain the sim_time_limit fromthe local Run_EKMC.py file.
    sim_time_limit = get_variables_from_run(filepath)

    # Second, if kMC_sim.txt not found, return False, the simulation has not begun.
    if not os.path.exists(filepath+'/kMC_sim.txt'):
        return False
    
    # Third, obtain the last line in the kMC_sim.txt file
    last_lines_in_kMC_simTXT = tail(filepath+'/kMC_sim.txt',1) 
    last_lines_in_kMC_simTXT = last_lines_in_kMC_simTXT[0]
    if isinstance(last_lines_in_kMC_simTXT, bytes):
        last_lines_in_kMC_simTXT = last_lines_in_kMC_simTXT.decode()

    # Fourth, determine if a simulation has begun.
    if last_lines_in_kMC_simTXT.strip() == "":
        return False
    if last_lines_in_kMC_simTXT.startswith('Count:'):
        return False

    # Fifth, obtain the components of the last line in the kMC_sim.txt file.
    try:
        count, molecule, cell_point, time, time_step, hop_distance, energy, sum_kij, _, Dxx, Dyy, Dzz, Dxy, Dxz, Dyz, _ = last_lines_in_kMC_simTXT.rstrip().split()
    except Exception as exception:
        to_string = 'error with '+str(filepath)+'. Error Message\n'+str(exception)
        print(to_string)
        import pdb; pdb.set_trace()
        raise Exception(to_string)

    # Sixth, convert time variable from string to float
    time = float(time)

    # Seventh, return True if time is greater or equal to sim_time_limit (indicating the simulation completed successfully). Otherwise, return False if time < sim_time_limit.
    return (time >= sim_time_limit)

def has_all_simulations_finished(dirpath, dirnames):

    print('Scanning: '+str(dirpath))

    completed_Simulations = []
    incomplete_Simulations = []
    dirnames = [dirname for dirname in dirnames if dirname.startswith('Sim')]
    dirnames.sort(key=lambda dirname: int(dirname.replace('Sim','')))
    number_of_dirnames = len(dirnames)
    for index in range(number_of_dirnames):
        dirname = dirnames[index]
        simulation_no = int(dirname.replace('Sim',''))
        did_simulation_finish_successfully = Did_Simulation_finish_successfully(dirpath+'/'+dirname)
        if did_simulation_finish_successfully:
            completed_Simulations.append(simulation_no)
        else:
            incomplete_Simulations.append(simulation_no)
        ###########
        sys.stdout.write("\r                                                                  ")
        sys.stdout.flush()
        sys.stdout.write("\rScanning Completion: "+str(round((float(index+1)/float(number_of_dirnames)*100.0),2))+" % (Checked "+str(dirname)+").")
        sys.stdout.flush()
        ###########
    completed_Simulations.sort()
    incomplete_Simulations.sort()
    completed_successfully = True if len(incomplete_Simulations) == 0 else False
    return completed_successfully, completed_Simulations, incomplete_Simulations, problem_simulations


