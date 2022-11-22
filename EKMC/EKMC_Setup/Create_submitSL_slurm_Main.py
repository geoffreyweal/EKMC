'''
Geoffrey Weal, Create_submitSL_slurm_Main.py, 10/02/2021

This program is designed to create the various forms of submit.sl/mass_submit.sl files that could be used to submit exciton KMC simulations.ß
'''
from itertools import count

Run_EKMC_filename = 'Run_EKMC.py'
max_no_of_arrayjobs_in_a_mass_submit_file = 1000

# ----------------------------------------------------------------------------------------------------------------------------------------

def make_submitSL(local_path,project=None,time='0-01:00',nodes=1,ntasks_per_node=1,mem=None,mem_per_cpu=None,partition='parallel',constraint=None,email='',python_version='python/3.8.1'):
    """

    """
    # create name for job
    #print("creating submit.sl for "+str(local_path))
    name = local_path.replace('/','_')
    # writing the submit.sl script
    with open("ekmc_submit.sl", "w") as submitSL:
        submitSL.write('#!/bin/bash -e\n')
        submitSL.write('#SBATCH -J ' + str(name) + '\n')
        if project is not None:
            submitSL.write('#SBATCH -A ' + str(project) + '         # Project Account\n')
        submitSL.write('#SBATCH --partition=' + str(partition) + '\n')
        if constraint is not None:
            submitSL.write('#SBATCH --constraint=' + str(constraint) + '\n')
        submitSL.write('\n')
        submitSL.write('#SBATCH --time=' + str(time) + '     # Walltime\n')
        submitSL.write('#SBATCH --nodes=' + str(nodes) + '\n')
        submitSL.write('#SBATCH --ntasks-per-node=' + str(ntasks_per_node) + '\n')
        add_mem_to_submitSL(submitSL,mem=mem,mem_per_cpu=mem_per_cpu)
        submitSL.write('\n')
        submitSL.write('#SBATCH --output=slurm-%j.out      # %x and %j are replaced by job name and ID'+'\n')
        submitSL.write('#SBATCH --error=slurm-%j.err'+'\n')
        if not email == '':
            submitSL.write('#SBATCH --mail-user=' + str(email) + '\n')
            submitSL.write('#SBATCH --mail-type=ALL\n')
        submitSL.write('\n')
        submitSL.write('module load '+str(python_version)+'\n')
        submitSL.write('python3 '+str(Run_EKMC_filename)+'\n')

# ----------------------------------------------------------------------------------------------------------------------------------------

def make_mass_submitSL_full(local_path,general_temp_folder_path,job_name,project=None,no_of_simulations=10,time='0-01:00',nodes=1,ntasks_per_node=1,mem=None,mem_per_cpu=None,partition='parallel',constraint=None,email='',python_version='python/3.8.1'):
    """

    """
    # First, determine the initial low and high job number
    low_job_number = 1
    if no_of_simulations < max_no_of_arrayjobs_in_a_mass_submit_file:
        high_job_number = no_of_simulations
    else:
        high_job_number = max_no_of_arrayjobs_in_a_mass_submit_file

    # Second, get all the mass_submit.sl files for the exciton kMC simulations for this crystal.
    for mass_submit_counter in count(1):
        # 2.1: Make mass_submit.sl
        make_single_mass_submitSL_file_full(mass_submit_counter,general_temp_folder_path,low_job_number,high_job_number,local_path,job_name,project=project,time=time,nodes=nodes,ntasks_per_node=ntasks_per_node,mem=mem,mem_per_cpu=mem_per_cpu,partition=partition,constraint=constraint,email=email,python_version=python_version)
        
        # 2.2: Get the number of jobs that have now been recorded into slurm
        jobs_recorded_in_slurm = ((mass_submit_counter-1)*max_no_of_arrayjobs_in_a_mass_submit_file + high_job_number)

        # 2.2: Determine if to break out of loop.
        if jobs_recorded_in_slurm == no_of_simulations:
            break

        number_of_jobs_to_recorded_to_slurm = no_of_simulations - jobs_recorded_in_slurm

        # 2.3: Increase mass_submit_counter, low_job_number, and high_job_number
        if number_of_jobs_to_recorded_to_slurm < max_no_of_arrayjobs_in_a_mass_submit_file:
            high_job_number = number_of_jobs_to_recorded_to_slurm
        else:
            high_job_number = max_no_of_arrayjobs_in_a_mass_submit_file

def make_single_mass_submitSL_file_full(mass_submit_counter,general_temp_folder_path,low_job_number,high_job_number,local_path,job_name,project=None,time='0-01:00',nodes=1,ntasks_per_node=1,mem=None,mem_per_cpu=None,partition='parallel',constraint=None,email='',python_version='python/3.8.1'):
    """

    """
    # create name for job
    #print("creating mass_submit.sl for "+str(job_name))
    name = job_name.replace('/','_')
    # writing the mass_submit.sl script
    with open(local_path+'/'+"ekmc_mass_submit"+(('_'+str(mass_submit_counter)) if (mass_submit_counter >= 2) else '')+".sl", "w") as submitSL:
        submitSL.write('#!/bin/bash -e\n')
        submitSL.write('#SBATCH -J ' + str(name) + '_ArrayJob_Set_' + str(mass_submit_counter) + '\n')
        if project is not None:
            submitSL.write('#SBATCH -A ' + str(project) + '         # Project Account\n')
        submitSL.write('#SBATCH --partition='+str(partition)+'\n')
        if constraint is not None:
            submitSL.write('#SBATCH --constraint=' + str(constraint) + '\n')
        submitSL.write('\n')
        submitSL.write('#SBATCH --array='+str(low_job_number)+'-'+str(high_job_number)+'\n')
        submitSL.write('\n')
        submitSL.write('#SBATCH --time=' + str(time) + '     # Walltime\n')
        submitSL.write('#SBATCH --nodes=' + str(nodes) + '\n')
        submitSL.write('#SBATCH --ntasks-per-node=' + str(ntasks_per_node) + '\n')
        add_mem_to_submitSL(submitSL,mem=mem,mem_per_cpu=mem_per_cpu)
        submitSL.write('\n')
        submitSL.write('#SBATCH --output=arrayJob_%A_%a.out'+'\n')
        submitSL.write('#SBATCH --error=arrayJob_%A_%a.err'+'\n')
        if not email == '':
            submitSL.write('#SBATCH --mail-user=' + str(email) + '\n')
            submitSL.write('#SBATCH --mail-type=ALL\n')
        submitSL.write('\n')
        submitSL.write('######################\n')
        submitSL.write('# Begin work section #\n')
        submitSL.write('######################\n')
        submitSL.write('\n')
        submitSL.write("# Print this sub-job's task ID\n")
        submitSL.write('echo "My SLURM_ARRAY_JOB_ID: "${SLURM_ARRAY_JOB_ID}\n')
        submitSL.write('echo "My SLURM_ARRAY_TASK_ID: "${SLURM_ARRAY_TASK_ID}\n')
        submitSL.write('\n')
        submitSL.write('# Get the simulation number for this simulation\n')
        submitSL.write('arrayjobset='+str(mass_submit_counter)+'\n')
        submitSL.write('sim_name=$(( $(( $(( ${arrayjobset} - 1 )) * '+str(max_no_of_arrayjobs_in_a_mass_submit_file)+' )) + ${SLURM_ARRAY_TASK_ID} ))\n')
        submitSL.write('\n')
        submitSL.write('# Load python\n')
        submitSL.write('module load '+str(python_version)+'\n')
        submitSL.write('\n')
        submitSL.write('# Make the folder to run the simulation from.\n')
        submitSL.write('if [ ! -d Sim${sim_name} ]; then\n')
        submitSL.write('    mkdir Sim${sim_name}\n')
        submitSL.write('fi\n')
        submitSL.write('\n')
        submitSL.write('# Copy KMC python script into Sim folder\n')
        submitSL.write('cp '+str(Run_EKMC_filename)+' Sim${sim_name}\n')
        submitSL.write('\n')
        submitSL.write('# Move into the Sim folder, run the KMC program, and move out of it.\n')
        submitSL.write('cd Sim${sim_name}\n')
        if general_temp_folder_path is not None:
            submitSL.write('python3 -u '+str(Run_EKMC_filename)+' "'+str(general_temp_folder_path)+'/J${SLURM_ARRAY_JOB_ID}_T${SLURM_ARRAY_TASK_ID}"\n')
        else:
            submitSL.write('python3 -u '+str(Run_EKMC_filename)+'\n')
        submitSL.write('cd ..\n')
        submitSL.write('\n')
        submitSL.write('# Move output and error file to KMC folder.\n')
        submitSL.write('mv arrayJob_${SLURM_ARRAY_JOB_ID}_${SLURM_ARRAY_TASK_ID}.out Sim${sim_name}\n')
        submitSL.write('mv arrayJob_${SLURM_ARRAY_JOB_ID}_${SLURM_ARRAY_TASK_ID}.err Sim${sim_name}\n')
        submitSL.write('\n')
        submitSL.close()

# ----------------------------------------------------------------------------------------------------------------------------------------

def make_mass_submitSL_packets(local_path,general_temp_folder_path,job_name,project=None,no_of_simulations=10,no_of_packets_to_make=1,time='0-01:00',nodes=1,ntasks_per_node=1,mem=None,mem_per_cpu=None,partition='parallel',constraint=None,email='',python_version='python/3.8.1'):
    """

    """
    # make sure that no_of_packets_to_make is a value and no_of_simulations is divisible by it. 
    if not isinstance(no_of_packets_to_make,int):
        print('Error in def make_mass_submitSL_packets, in Create_submitSL_slurm_Main.py')
        print('no_of_packets_to_make needs to be give as a int')
        print('no_of_packets_to_make = '+str(no_of_packets_to_make))
        exit('Check this. The algorithm will finish here.')
    if not (float(no_of_simulations)%float(no_of_packets_to_make)) == 0.0:
        print('Error in def make_mass_submitSL_packets, in Create_submitSL_slurm_Main.py')
        print('no_of_simulations needs to be divisible by no_of_packets_to_make')
        print('no_of_simulations = '+str(no_of_simulations))
        print('no_of_packets_to_make = '+str(no_of_packets_to_make))
        exit('Check this. The algorithm will finish here.')
    number_of_divides = int(float(no_of_simulations)/float(no_of_packets_to_make))
    # create name for job
    #print("creating mass_submit.sl for "+str(job_name))
    name = job_name.replace('/','_')
    # writing the mass_submit.sl script
    with open(local_path+'/'+"ekmc_mass_submit.sl", "w") as submitSL:
        submitSL.write('#!/bin/bash -e\n')
        submitSL.write('#SBATCH -J ' + str(name) + '\n')
        if project is not None:
            submitSL.write('#SBATCH -A ' + str(project) + '         # Project Account\n')
        submitSL.write('#SBATCH --partition='+str(partition)+'\n')
        if constraint is not None:
            submitSL.write('#SBATCH --constraint=' + str(constraint) + '\n')
        submitSL.write('\n')
        submitSL.write('#SBATCH --array=1-'+str(no_of_packets_to_make)+'\n')
        submitSL.write('\n')
        submitSL.write('#SBATCH --time=' + str(time) + '     # Walltime\n')
        submitSL.write('#SBATCH --nodes=' + str(nodes) + '\n')
        submitSL.write('#SBATCH --ntasks-per-node=' + str(ntasks_per_node) + '\n')
        add_mem_to_submitSL(submitSL,mem=mem,mem_per_cpu=mem_per_cpu)
        submitSL.write('\n')
        submitSL.write('#SBATCH --output=arrayJob_%A_%a.out'+'\n')
        submitSL.write('#SBATCH --error=arrayJob_%A_%a.err'+'\n')
        if not email == '':
            submitSL.write('#SBATCH --mail-user=' + str(email) + '\n')
            submitSL.write('#SBATCH --mail-type=ALL\n')
        submitSL.write('\n')
        submitSL.write('######################\n')
        submitSL.write('# Begin work section #\n')
        submitSL.write('######################\n')
        submitSL.write('\n')
        submitSL.write("# Print this sub-job's task ID\n")
        submitSL.write('echo "My SLURM_ARRAY_JOB_ID: "${SLURM_ARRAY_JOB_ID}\n')
        submitSL.write('echo "My SLURM_ARRAY_TASK_ID: "${SLURM_ARRAY_TASK_ID}\n')
        submitSL.write('\n')
        submitSL.write("# Perform each simulation in a for loop\n")
        submitSL.write('number_of_divides='+str(number_of_divides)+'\n')
        submitSL.write('for i in $( eval echo {1..${number_of_divides}} ); do\n')
        submitSL.write('\n')
        submitSL.write('# Get the simulation number for this simulation\n')
        submitSL.write('Sim_no=$(( $(( $(( ${SLURM_ARRAY_TASK_ID} - 1)) * ${number_of_divides} )) + $i ))\n')
        submitSL.write('echo Currently performing caluclation on Sim: $Sim_no\n')
        submitSL.write('\n')
        submitSL.write('# Load python\n')
        submitSL.write('module load '+str(python_version)+'\n')
        submitSL.write('\n')
        submitSL.write('# Make the folder to run the simulation from.\n')
        submitSL.write('if [ ! -d Sim${Sim_no} ]; then\n')
        submitSL.write('    mkdir Sim${Sim_no}\n')
        submitSL.write('fi\n')
        submitSL.write('\n')
        submitSL.write('# Copy KMC python script into Sim folder\n')
        submitSL.write('cp '+str(Run_EKMC_filename)+' Sim${Sim_no}\n')
        submitSL.write('\n')
        submitSL.write('# Write starting message to output and error files.\n')
        submitSL.write("echo '=============================================================================='\n")
        submitSL.write("echo 'Running Sim'${Sim_no}\n")
        submitSL.write("echo '=============================================================================='\n")
        submitSL.write("1>&2 echo '=============================================================================='\n")
        submitSL.write("1>&2 echo 'Running Sim'${Sim_no}\n")
        submitSL.write("1>&2 echo '=============================================================================='\n")
        submitSL.write('\n')
        submitSL.write('# Move into the Sim folder, run the KMC program, and move out of it.\n')
        submitSL.write('cd Sim${Sim_no}\n')
        if general_temp_folder_path is not None:
            submitSL.write('python3 -u '+str(Run_EKMC_filename)+' "'+str(general_temp_folder_path)+'/J${SLURM_ARRAY_JOB_ID}_T${SLURM_ARRAY_TASK_ID}"\n')
        else:
            submitSL.write('python3 -u '+str(Run_EKMC_filename)+'\n')
        submitSL.write('cd ..\n')
        submitSL.write('\n')
        submitSL.write('# Write ending message to output and error files.\n')
        submitSL.write("echo '=============================================================================='\n")
        submitSL.write("1>&2 echo '=============================================================================='\n")
        submitSL.write('\n')
        submitSL.write('# Move output and error file to KMC folder.\n')
        submitSL.write('cp arrayJob_${SLURM_ARRAY_JOB_ID}_${SLURM_ARRAY_TASK_ID}.out Sim${Sim_no}/arrayJob_${SLURM_ARRAY_JOB_ID}_${Sim_no}.out\n')
        submitSL.write('cp arrayJob_${SLURM_ARRAY_JOB_ID}_${SLURM_ARRAY_TASK_ID}.err Sim${Sim_no}/arrayJob_${SLURM_ARRAY_JOB_ID}_${Sim_no}.err\n')
        submitSL.write('echo -n "" > arrayJob_${SLURM_ARRAY_JOB_ID}_${SLURM_ARRAY_TASK_ID}.out\n')
        submitSL.write('echo -n "" > arrayJob_${SLURM_ARRAY_JOB_ID}_${SLURM_ARRAY_TASK_ID}.err\n')
        submitSL.write('\n')
        submitSL.write('done\n')
        submitSL.write('\n')
        submitSL.close()

# ----------------------------------------------------------------------------------------------------------------------------------------

def add_mem_to_submitSL(submitSL,mem=None,mem_per_cpu=None):
    """

    """
    if (mem is None) and not (mem_per_cpu is None):
        submitSL.write('#SBATCH --mem-per-cpu=' + str(mem_per_cpu) + '\n')
    elif not (mem is None) and (mem_per_cpu is None):
        submitSL.write('#SBATCH --mem=' + str(mem) + '\n')
    else:
        print('===================================')
        print('Error during making the submit.sl file.')
        if (mem is None) and (mem_per_cpu is None):
            print('You have not included any values for either "mem" or "mem-per-cpu"')
            print('Enter a value for either  "mem" or "mem-per-cpu" and rerun this program')
        elif not (mem is None) and not (mem_per_cpu is None):
            print('You have included values for both "mem" or "mem-per-cpu"')
            print('Enter a value for only either  "mem" or "mem-per-cpu" and rerun this program')
        print('This program will finish without completing.')
        print('===================================')
        exit()

# ----------------------------------------------------------------------------------------------------------------------------------------




