"""
save_time_averaged_data.py, Geoffrey Weal, 10/9/22

This script is designed to enter the time averaged data from the EKMC simulations to a txt file
"""
import os
import numpy as np

from datetime import datetime, timedelta
from xlsxwriter import Workbook

kB = 8.617333262145 * (10.0 ** -5.0) # eV K-1

def save_time_averaged_data(path_to_place_data_in, time_average_energy, time_average_energy_sd, time_average_energy_ci, time_average_diffusion, time_average_diffusion_sd, time_average_diffusion_ci, time_average_diffusion_tensor, time_average_diffusion_tensor_sd, time_average_diffusion_tensor_ci, time_average_eigenvalues_of_diffusion_tensor, time_average_eigenvalues_of_diffusion_tensor_sd, time_average_eigenvalues_of_diffusion_tensor_ci, begin_recording_time, endtime, temperature, energetic_disorder, coupling_disorder, conformationally_unique_bandgap_energies):

    print('Save data and figures to disk.')
    time_averaged_filename = 'Time_Averaged_Data.txt'
    if os.path.exists(path_to_place_data_in+'/'+time_averaged_filename):
        os.remove(path_to_place_data_in+'/'+time_averaged_filename)

    with open(path_to_place_data_in+'/'+time_averaged_filename, 'w') as fileTXT:
        fileTXT.write('Time Averaged Data\n')
        fileTXT.write('\n')
        fileTXT.write('Data given as: Average +- standard deviation (95%'+' confidence interval)\n')
        fileTXT.write('\n')
        fileTXT.write('Taken from '+str(begin_recording_time)+' ps to '+str(endtime)+' ps.\n')
        fileTXT.write('\n')
        fileTXT.write('Time Averaged Energy (eV):\t'+str(time_average_energy)+' +- '+str(time_average_energy_sd)+'\t('+str(time_average_energy_ci)+')\n')
        for molname, bandgap_energy in sorted(conformationally_unique_bandgap_energies.items()):
            energy_limit = bandgap_energy - ((energetic_disorder ** 2.0)/(kB * temperature))
            fileTXT.write('Energy Asympote - Molecule '+str(molname)+' (eV):\t'+str(energy_limit)+'\n')
        fileTXT.write('\n')
        fileTXT.write('Time Averaged Diffusion Coefficient (cm^2 s^-1):\t'+str(time_average_diffusion)+' +- '+str(time_average_diffusion_sd)+'\t('+str(time_average_diffusion_ci)+')\n')
        fileTXT.write('\n')
        fileTXT.write('Time Averaged Diffusion Tensor (cm^2 s^-1):\n')
        fileTXT.write(str(time_average_diffusion_tensor)+'\n')
        fileTXT.write('\n')
        fileTXT.write('+-\n')
        fileTXT.write('\n')
        fileTXT.write(str(time_average_diffusion_tensor_sd)+'\n')
        fileTXT.write('\n')
        fileTXT.write('Confidence interval for Time Averaged Diffusion Tensor (cm^2 s^-1)\n')
        fileTXT.write(str(time_average_diffusion_tensor_ci)+'\n')
        fileTXT.write('\n')
        fileTXT.write('Time Averaged Eigenvalues of the Diffusion Tensor:\n')
        fileTXT.write('Major   (cm^2 s^-1):\t'+str(time_average_eigenvalues_of_diffusion_tensor[0])+' +- '+str(time_average_eigenvalues_of_diffusion_tensor_sd[0])+'\t('+str(time_average_eigenvalues_of_diffusion_tensor_ci[0])+')\n')
        fileTXT.write('Minor 1 (cm^2 s^-1):\t'+str(time_average_eigenvalues_of_diffusion_tensor[1])+' +- '+str(time_average_eigenvalues_of_diffusion_tensor_sd[1])+'\t('+str(time_average_eigenvalues_of_diffusion_tensor_ci[1])+')\n')
        fileTXT.write('Minor 2 (cm^2 s^-1):\t'+str(time_average_eigenvalues_of_diffusion_tensor[2])+' +- '+str(time_average_eigenvalues_of_diffusion_tensor_sd[2])+'\t('+str(time_average_eigenvalues_of_diffusion_tensor_ci[2])+')\n')
        fileTXT.write('\n')


