"""
save_data_and_plot_figures.py, Geoffrey Weal, 17/8/22

This script is designed to plot
"""
import os
import numpy as np

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

from tqdm import tqdm, trange

from ase import Atoms
from ase.io import read, write

from SUMELF import make_folder, remove_folder

kB = 8.617333262145 * (10.0 ** -5.0) # eV K-1
no_of_atoms = 50
s=5
def save_data_and_plot_figures(path_to_place_data_in, times, positions_at_time, average_displacements_from_initial_position_over_time, average_displacements_squared_from_initial_position_over_time, average_energies_over_time, diffusion_over_time, diffusion_tensor_over_time, eigenvalues_of_diffusion_tensor_over_time, eigenvectors_of_diffusion_tensor_over_time, unit_cell_matrix, temperature, energetic_disorder, coupling_disorder, conformationally_unique_bandgap_energies, path_to_crystal_file=None):
    """
    This method is designed to obtain the displacement vectors and energies for all the simulations over sampled time.

    Parameters
    ----------
    times : list
        These are the times that were sampled across all simulations for this system.

    average_displacements_from_initial_position_over_time : list
        This is the list of displacement values of the ensemble over sampled time.
    average_displacements_squared_from_initial_position_over_time
        This is the list of displacement squared values of the ensemble over sampled time.
    average_energies_over_time
        This is the list of energy values of the ensemble over sampled time.
    diffusion_over_time
        This is the list of diffusion coefficient values of the ensemble over sampled time.
    diffusion_tensor_over_time
        This is the list of diffusion tensor values of the ensemble over sampled time.
    """

    # First, get the name of the folder to save data to, and make this folder. 
    print('Save data and figures to disk.')

    # Second, save the average displacement of the exciton across the ensemble over time.
    plt.scatter(times, average_displacements_from_initial_position_over_time, s=s)
    plt.xlabel('Time (ps)')
    plt.ylabel(r"$\mathregular{\left\langle d \right\rangle  (Å)}$")
    plt.savefig(path_to_place_data_in+'/'+'Disp_Vs_Time.png', dpi=300)
    plt.savefig(path_to_place_data_in+'/'+'Disp_Vs_Time.pdf', dpi=300)
    plt.clf()
    write_plot_data_to_disk_single(times, average_displacements_from_initial_position_over_time, 'Average Displacement (A)', path_to_place_data_in, 'Disp_Vs_Time.txt')

    # Third, save the average displacement squared of the exciton across the ensemble over time.
    plt.scatter(times, average_displacements_squared_from_initial_position_over_time, s=s)
    plt.xlabel('Time (ps)')
    plt.ylabel(r"$\mathregular{\left\langle d^2 \right\rangle  (Å^2)}$")
    plt.savefig(path_to_place_data_in+'/'+'Disp2_Vs_Time.png', dpi=300)
    plt.savefig(path_to_place_data_in+'/'+'Disp2_Vs_Time.pdf', dpi=300)
    plt.clf()
    write_plot_data_to_disk_single(times, average_displacements_squared_from_initial_position_over_time, 'Average Displacement Squared (A^2)', path_to_place_data_in, 'Disp2_Vs_Time.txt')

    # Fourth, save the average energy of the exciton across the ensemble over time.
    for molname, bandgap_energy in sorted(conformationally_unique_bandgap_energies.items()):
        energy_limit = bandgap_energy - ((energetic_disorder ** 2.0)/(kB * temperature))
        plt.axhline(y=energy_limit, color='r', linestyle='--')
    plt.scatter(times, average_energies_over_time, s=s)
    plt.xlabel('Time (ps)')
    plt.ylabel(r"$\mathregular{\left\langle E \right\rangle  (eV)}$")
    plt.savefig(path_to_place_data_in+'/'+'Energy_Vs_Time.png', dpi=300)
    plt.savefig(path_to_place_data_in+'/'+'Energy_Vs_Time.pdf', dpi=300)
    plt.clf()
    write_plot_data_to_disk_single(times, average_energies_over_time, 'Energy (eV)', path_to_place_data_in, 'Energy_Vs_Time.txt')

    # Fifth, save the Diffusion Coefficient of the exciton across the ensemble over time.
    plt.scatter(times, diffusion_over_time, s=s)
    plt.xlabel('Time (ps)')
    plt.ylabel(r"Diffusion Coefficient $\mathregular{(cm^{2} s^{-1})}$")
    plt.savefig(path_to_place_data_in+'/'+'Diffusion_Vs_Time.png', dpi=300)
    plt.savefig(path_to_place_data_in+'/'+'Diffusion_Vs_Time.pdf', dpi=300)
    plt.clf()
    write_plot_data_to_disk_single(times, diffusion_over_time, 'Diffusion Coefficient (cm^2 s^-1)', path_to_place_data_in, 'Diffusion_Vs_Time.txt')

    # Sixth, save each of the components of the diffusion tensor over time.
    diffusion_tensor_xx = []; diffusion_tensor_xy = []; diffusion_tensor_xz = []
    diffusion_tensor_yy = []; diffusion_tensor_yz = []; diffusion_tensor_zz = []
    for diffusion_tensor_at_time in diffusion_tensor_over_time:
        diffusion_tensor_xx.append(diffusion_tensor_at_time[0][0])
        diffusion_tensor_xy.append(diffusion_tensor_at_time[0][1])
        diffusion_tensor_xz.append(diffusion_tensor_at_time[0][2])
        diffusion_tensor_yy.append(diffusion_tensor_at_time[1][1])
        diffusion_tensor_yz.append(diffusion_tensor_at_time[1][2])
        diffusion_tensor_zz.append(diffusion_tensor_at_time[2][2])
    plt.scatter(times, diffusion_tensor_xx, label='xx', s=s)
    plt.scatter(times, diffusion_tensor_xy, label='xy/yx', s=s)
    plt.scatter(times, diffusion_tensor_xz, label='xz/zx', s=s)
    plt.scatter(times, diffusion_tensor_yy, label='yy', s=s)
    plt.scatter(times, diffusion_tensor_yz, label='yz/zy', s=s)
    plt.scatter(times, diffusion_tensor_zz, label='zz', s=s)
    plt.xlabel('Time (ps)')
    plt.ylabel(r"Diffusion Tensor Components $\mathregular{(cm^2 s^{-1})}$")
    plt.legend()
    plt.savefig(path_to_place_data_in+'/'+'Diffusion_Tensor_Vs_Time.png', dpi=300)
    plt.savefig(path_to_place_data_in+'/'+'Diffusion_Tensor_Vs_Time.pdf', dpi=300)
    plt.clf()
    write_plot_data_to_disk_six(times, diffusion_tensor_xx, diffusion_tensor_xy, diffusion_tensor_xz, diffusion_tensor_yy, diffusion_tensor_yz, diffusion_tensor_zz, 'Diffusion Tensor XX Component (cm^2 s^-1)', 'Diffusion Tensor XY Component (cm^2 s^-1)', 'Diffusion Tensor XZ Component (cm^2 s^-1)', 'Diffusion Tensor YY Component (cm^2 s^-1)', 'Diffusion Tensor YZ Component (cm^2 s^-1)', 'Diffusion Tensor ZZ Component (cm^2 s^-1)', path_to_place_data_in, 'Diffusion_Tensor_Vs_Time.txt')

    # Seventh, Obtain the eigenvalues of the tensor matrix and show this over time. 
    major_eigenvalue_of_diffusion_tensor_over_time        = [major  for major, minor1, minor2 in eigenvalues_of_diffusion_tensor_over_time]
    first_minor_eigenvalue_of_diffusion_tensor_over_time  = [minor1 for major, minor1, minor2 in eigenvalues_of_diffusion_tensor_over_time]
    second_minor_eigenvalue_of_diffusion_tensor_over_time = [minor2 for major, minor1, minor2 in eigenvalues_of_diffusion_tensor_over_time]
    plt.scatter(times, major_eigenvalue_of_diffusion_tensor_over_time, label='major', s=s)
    plt.scatter(times, first_minor_eigenvalue_of_diffusion_tensor_over_time, label='first minor', s=s)
    plt.scatter(times, second_minor_eigenvalue_of_diffusion_tensor_over_time, label='second minor', s=s)
    plt.xlabel('Time (ps)')
    plt.ylabel(r"Diffusion Tensor Eigenvalues $\mathregular{(cm^2 s^{-1})}$")
    plt.legend()
    plt.savefig(path_to_place_data_in+'/'+'Eigenvalues_of_Diagonalised_Diffusion_Tensor_Vs_Time.png', dpi=300)
    plt.savefig(path_to_place_data_in+'/'+'Eigenvalues_of_Diagonalised_Diffusion_Tensor_Vs_Time.pdf', dpi=300)
    plt.clf()
    write_plot_data_to_disk_three(times, major_eigenvalue_of_diffusion_tensor_over_time, first_minor_eigenvalue_of_diffusion_tensor_over_time, second_minor_eigenvalue_of_diffusion_tensor_over_time, 'Diffusion Tensor Major Eigenvalue (cm^2 s^-1)', 'Diffusion Tensor Minor Eigenvalue 1 (cm^2 s^-1)', 'Diffusion Tensor Minor Eigenvalue 2 (cm^2 s^-1)', path_to_place_data_in, 'Eigenvalues_of_Diagonalised_Diffusion_Tensor_Vs_Time.txt')

    # Eighth, obtain the visual of the direction of the diagonalised diffusion tensor. 
    if path_to_crystal_file is None:
        crystal_system = Atoms()
    else:
        crystal_system = read(path_to_crystal_file)
    for eigenvalues, eigenvectors in tqdm(zip(eigenvalues_of_diffusion_tensor_over_time, eigenvectors_of_diffusion_tensor_over_time), total=len(eigenvalues_of_diffusion_tensor_over_time), desc="Writing eigenvalues of diffusion tensor over time (diffusion_anisotrophy.xyz)", leave=False):
        eig_major, eig_minor1, eig_minor2 = eigenvalues
        eiv_major, eiv_minor1, eiv_minor2 = eigenvectors
        origin_vector = Atoms('O', [(0,0,0)])
        eigenvectors_at_sampled_time = crystal_system.copy() + origin_vector
        try:
            major_vector  = eig_major  * eiv_major
            minor1_vector = eig_minor1 * eiv_minor1
            minor2_vector = eig_minor2 * eiv_minor2
            major_vector   = Atoms('F' +str(no_of_atoms), [no_of_atoms * major_vector  * (index/no_of_atoms) for index in range(1,no_of_atoms+1)])
            minor1_vector  = Atoms('He'+str(no_of_atoms), [no_of_atoms * minor1_vector * (index/no_of_atoms) for index in range(1,no_of_atoms+1)])
            minor2_vector  = Atoms('H' +str(no_of_atoms), [no_of_atoms * minor2_vector * (index/no_of_atoms) for index in range(1,no_of_atoms+1)])
            eigenvectors_at_sampled_time += minor2_vector + minor1_vector + major_vector
        except:
            pass
        eigenvectors_at_sampled_time.set_cell(unit_cell_matrix)
        write(path_to_place_data_in+'/'+'diffusion_anisotrophy.xyz', eigenvectors_at_sampled_time, append=True)
    write(path_to_place_data_in+'/'+'end_of_simulation_diffusion_anisotrophy.xyz', eigenvectors_at_sampled_time)

    # Ninth, draw the path of the excitons over time
    for time_index in trange(len(positions_at_time[0]), desc="Writing xyz files for the exciton paths over time (exciton_diffusion_over_time.xyz)", leave=False):
        displacements = [positions_at_time[sim_index][time_index] for sim_index in range(len(positions_at_time))]
        excitons      = Atoms(['O']*len(displacements), displacements, cell=unit_cell_matrix)
        write(path_to_place_data_in+'/'+'exciton_diffusion_over_time.xyz', excitons, append=True)
    write(path_to_place_data_in+'/'+'end_of_simulation_exciton_diffusion_over_time.xyz', excitons)


    '''
    final_eigenvector_of_diffusion_tensor = eigenvectors_of_diffusion_tensor_over_time[-1]

    X, Y, Z = np.array((0., 0., 0.))
    U, V, W = zip(*final_eigenvector_of_diffusion_tensor)

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.quiver(X, Y, Z, U, V, W)

    ax.set_xlabel('x axis')
    ax.set_ylabel('y axis')
    ax.set_xlabel('z axis')
    ax.legend()
    plt.savefig(path_to_place_data_in+'/'+'Eigenvectors_of_Diagonalised_Diffusion_Tensor_Vs_Time.png')
    plt.clf()
    '''

def write_plot_data_to_disk_single(times, data_to_save, data_to_save_name, path_to_place_data_in, filename):
    if os.path.exists(path_to_place_data_in+'/'+filename):
        os.remove(path_to_place_data_in+'/'+filename)
    with open(path_to_place_data_in+'/'+filename, 'w') as fileTXT:
        fileTXT.write('Time (ps)\t'+data_to_save_name+'\n')
        for time, datum_to_save in zip(times, data_to_save):
            fileTXT.write(str(time)+'\t'+str(datum_to_save)+'\n')

def write_plot_data_to_disk_six(times, diffusion_tensor_xx, diffusion_tensor_xy, diffusion_tensor_xz, diffusion_tensor_yy, diffusion_tensor_yz, diffusion_tensor_zz, diffusion_tensor_xx_name, diffusion_tensor_xy_name, diffusion_tensor_xz_name, diffusion_tensor_yy_name, diffusion_tensor_yz_name, diffusion_tensor_zz_name, path_to_place_data_in, filename):
    if os.path.exists(path_to_place_data_in+'/'+filename):
        os.remove(path_to_place_data_in+'/'+filename)
    with open(path_to_place_data_in+'/'+filename, 'w') as fileTXT:
        fileTXT.write('Time (ps)\t'+diffusion_tensor_xx_name+'\t'+diffusion_tensor_xy_name+'\t'+diffusion_tensor_xz_name+'\t'+diffusion_tensor_yy_name+'\t'+diffusion_tensor_yz_name+'\t'+diffusion_tensor_zz_name+'\n')
        for time, xx, xy, xz, yy, yz, zz in zip(times, diffusion_tensor_xx, diffusion_tensor_xy, diffusion_tensor_xz, diffusion_tensor_yy, diffusion_tensor_yz, diffusion_tensor_zz):
            fileTXT.write(str(time)+'\t'+str(xx)+'\t'+str(xy)+'\t'+str(xz)+'\t'+str(yy)+'\t'+str(yz)+'\t'+str(zz)+'\n')

def write_plot_data_to_disk_three(times, major_eigenvalue_of_diffusion_tensor_over_time, first_minor_eigenvalue_of_diffusion_tensor_over_time, second_minor_eigenvalue_of_diffusion_tensor_over_time, major_eigenvalue_of_diffusion_tensor_over_time_name, first_minor_eigenvalue_of_diffusion_tensor_over_time_name, second_minor_eigenvalue_of_diffusion_tensor_over_time_name, path_to_place_data_in, filename):
    if os.path.exists(path_to_place_data_in+'/'+filename):
        os.remove(path_to_place_data_in+'/'+filename)
    with open(path_to_place_data_in+'/'+filename, 'w') as fileTXT:
        fileTXT.write('Time (ps)\t'+major_eigenvalue_of_diffusion_tensor_over_time_name+'\t'+first_minor_eigenvalue_of_diffusion_tensor_over_time_name+'\t'+second_minor_eigenvalue_of_diffusion_tensor_over_time_name+'\n')
        for time, major, minor1, minor2 in zip(times, major_eigenvalue_of_diffusion_tensor_over_time, first_minor_eigenvalue_of_diffusion_tensor_over_time, second_minor_eigenvalue_of_diffusion_tensor_over_time):
            fileTXT.write(str(time)+'\t'+str(major)+'\t'+str(minor1)+'\t'+str(minor2)+'\n')








