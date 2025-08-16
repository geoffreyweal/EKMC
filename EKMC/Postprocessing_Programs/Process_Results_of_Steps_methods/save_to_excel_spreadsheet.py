"""
save_to_excel_spreadsheet.py, Geoffrey Weal, 30/8/22

This script is designed to enter the data from the EKMC simulations to an excel spreadsheet
"""
import numpy as np
from tqdm import tqdm, trange
from datetime import datetime, timedelta
from xlsxwriter import Workbook

kB = 8.617333262145 * (10.0 ** -5.0) # eV K-1
interval_spacing = 15
def save_to_excel_spreadsheet(data_foldername, data_for_excel):
    """
    This method is designed to write the data about EKMC simulation to an excel spreadsheet

    Parameters
    ----------
    data_for_excel : list
        This is the data about the EKMC simulations to save to disk

    """

    if len(data_for_excel) == 0:
        return

    print('------------------------------------------------')
    print(str(datetime.now().strftime("%d/%m/%Y %H:%M:%S"))+' - Making Excel Spreadsheet containing EKMC Data.')

    workbook = Workbook(data_foldername+'/EKMC_data.xlsx')
    worksheet = workbook.add_worksheet('Data_Energy')

    merge_format_mol, merge_format_dimer, merge_format_barrier, table_format, number_format = format_worksheet(workbook)

    floating3_point_bordered = workbook.add_format({'num_format': '#,##0.000'})
    floating6_point_bordered = workbook.add_format({'num_format': '#,##0.000000'})

    for index in tqdm(range(len(data_for_excel))):

        root, time_average_energy, time_average_energy_sd, time_average_energy_ci, time_average_diffusion, time_average_diffusion_sd, time_average_diffusion_ci, time_average_diffusion_tensor, time_average_diffusion_tensor_sd, time_average_diffusion_tensor_ci, time_average_eigenvalues_of_diffusion_tensor, time_average_eigenvalues_of_diffusion_tensor_sd, time_average_eigenvalues_of_diffusion_tensor_ci, begin_recording_time, endtime, temperature, energetic_disorder, coupling_disorder, conformationally_unique_bandgap_energies = data_for_excel[index]

        worksheet.write(0, 0+(interval_spacing*index), str(root))

        worksheet.write(2, 0+(interval_spacing*index), 'Start Recording Time for Averages')
        worksheet.write(2, 1+(interval_spacing*index), str(begin_recording_time)+' ps')
        worksheet.write(3, 0+(interval_spacing*index), 'End Simulation Time')
        worksheet.write(3, 1+(interval_spacing*index), str(endtime)+' ps')

        worksheet.write(5, 1+(interval_spacing*index), 'Time Average')
        worksheet.write(5, 2+(interval_spacing*index), 'Standard Deviation')
        worksheet.write(5, 3+(interval_spacing*index), '95% Confidence Interval')

        worksheet.write(6, 0+(interval_spacing*index), 'Energy (eV)')
        worksheet.write(6, 1+(interval_spacing*index), float(time_average_energy), floating3_point_bordered)
        worksheet.write(6, 2+(interval_spacing*index), float(time_average_energy_sd), floating3_point_bordered)
        worksheet.write(6, 3+(interval_spacing*index), float(time_average_energy_ci), floating3_point_bordered)

        worksheet.write(7, 0+(interval_spacing*index), 'Energy Asympote (eV)')
        worksheet.write(7, 1+(interval_spacing*index), make_energy_asympote_string(conformationally_unique_bandgap_energies, energetic_disorder, temperature)) # float(energy_limit), floating3_point_bordered)

        worksheet.write(9, 0+(interval_spacing*index), 'Diffusion Coefficient (cm2 s−1)')
        worksheet.write(9, 1+(interval_spacing*index), float(time_average_diffusion), floating6_point_bordered)
        worksheet.write(9, 2+(interval_spacing*index), float(time_average_diffusion_sd), floating6_point_bordered)
        worksheet.write(9, 3+(interval_spacing*index), float(time_average_diffusion_ci), floating6_point_bordered)

        worksheet.write(11, 0+(interval_spacing*index), 'Diffusion Tensor (cm2 s−1)')
        worksheet.write(12, 1+(interval_spacing*index), 'Time Average Diffusion Tensor')
        worksheet.write(12, 5+(interval_spacing*index), 'Standard Deviation')
        worksheet.write(12, 9+(interval_spacing*index), '95% Confidence Interval')

        worksheet.write(13, 1+(interval_spacing*index), float(time_average_diffusion_tensor[0][0]), floating6_point_bordered)
        worksheet.write(13, 2+(interval_spacing*index), float(time_average_diffusion_tensor[0][1]), floating6_point_bordered)
        worksheet.write(13, 3+(interval_spacing*index), float(time_average_diffusion_tensor[0][2]), floating6_point_bordered)
        worksheet.write(14, 1+(interval_spacing*index), float(time_average_diffusion_tensor[1][0]), floating6_point_bordered)
        worksheet.write(14, 2+(interval_spacing*index), float(time_average_diffusion_tensor[1][1]), floating6_point_bordered)
        worksheet.write(14, 3+(interval_spacing*index), float(time_average_diffusion_tensor[1][2]), floating6_point_bordered)
        worksheet.write(15, 1+(interval_spacing*index), float(time_average_diffusion_tensor[2][0]), floating6_point_bordered)
        worksheet.write(15, 2+(interval_spacing*index), float(time_average_diffusion_tensor[2][1]), floating6_point_bordered)
        worksheet.write(15, 3+(interval_spacing*index), float(time_average_diffusion_tensor[2][2]), floating6_point_bordered)

        worksheet.write(13, 5+(interval_spacing*index), float(time_average_diffusion_tensor_sd[0][0]), floating6_point_bordered)
        worksheet.write(13, 6+(interval_spacing*index), float(time_average_diffusion_tensor_sd[0][1]), floating6_point_bordered)
        worksheet.write(13, 7+(interval_spacing*index), float(time_average_diffusion_tensor_sd[0][2]), floating6_point_bordered)
        worksheet.write(14, 5+(interval_spacing*index), float(time_average_diffusion_tensor_sd[1][0]), floating6_point_bordered)
        worksheet.write(14, 6+(interval_spacing*index), float(time_average_diffusion_tensor_sd[1][1]), floating6_point_bordered)
        worksheet.write(14, 7+(interval_spacing*index), float(time_average_diffusion_tensor_sd[1][2]), floating6_point_bordered)
        worksheet.write(15, 5+(interval_spacing*index), float(time_average_diffusion_tensor_sd[2][0]), floating6_point_bordered)
        worksheet.write(15, 6+(interval_spacing*index), float(time_average_diffusion_tensor_sd[2][1]), floating6_point_bordered)
        worksheet.write(15, 7+(interval_spacing*index), float(time_average_diffusion_tensor_sd[2][2]), floating6_point_bordered)

        worksheet.write(13, 9 +(interval_spacing*index), float(time_average_diffusion_tensor_ci[0][0]), floating6_point_bordered)
        worksheet.write(13, 10+(interval_spacing*index), float(time_average_diffusion_tensor_ci[0][1]), floating6_point_bordered)
        worksheet.write(13, 11+(interval_spacing*index), float(time_average_diffusion_tensor_ci[0][2]), floating6_point_bordered)
        worksheet.write(14, 9 +(interval_spacing*index), float(time_average_diffusion_tensor_ci[1][0]), floating6_point_bordered)
        worksheet.write(14, 10+(interval_spacing*index), float(time_average_diffusion_tensor_ci[1][1]), floating6_point_bordered)
        worksheet.write(14, 11+(interval_spacing*index), float(time_average_diffusion_tensor_ci[1][2]), floating6_point_bordered)
        worksheet.write(15, 9 +(interval_spacing*index), float(time_average_diffusion_tensor_ci[2][0]), floating6_point_bordered)
        worksheet.write(15, 10+(interval_spacing*index), float(time_average_diffusion_tensor_ci[2][1]), floating6_point_bordered)
        worksheet.write(15, 11+(interval_spacing*index), float(time_average_diffusion_tensor_ci[2][2]), floating6_point_bordered)

        worksheet.write(17, 0+(interval_spacing*index), 'Eigenvalues of the Diffusion Tensior (cm2 s−1)')

        worksheet.write(18, 1+(interval_spacing*index), 'Time Average Diffusion Tensor')
        worksheet.write(18, 2+(interval_spacing*index), 'Standard Deviation')
        worksheet.write(18, 3+(interval_spacing*index), '95% Confidence Interval')
        worksheet.write(19, 0+(interval_spacing*index), 'Major')
        worksheet.write(19, 1+(interval_spacing*index), float(time_average_eigenvalues_of_diffusion_tensor[0]), floating6_point_bordered)
        worksheet.write(19, 2+(interval_spacing*index), float(time_average_eigenvalues_of_diffusion_tensor_sd[0]), floating6_point_bordered)
        worksheet.write(19, 3+(interval_spacing*index), float(time_average_eigenvalues_of_diffusion_tensor_ci[0]), floating6_point_bordered)
        worksheet.write(20, 0+(interval_spacing*index), 'Minor 1')
        worksheet.write(20, 1+(interval_spacing*index), float(time_average_eigenvalues_of_diffusion_tensor[1]), floating6_point_bordered)
        worksheet.write(20, 2+(interval_spacing*index), float(time_average_eigenvalues_of_diffusion_tensor_sd[1]), floating6_point_bordered)
        worksheet.write(20, 3+(interval_spacing*index), float(time_average_eigenvalues_of_diffusion_tensor_ci[1]), floating6_point_bordered)
        worksheet.write(21, 0+(interval_spacing*index), 'Minor 2')
        worksheet.write(21, 1+(interval_spacing*index), float(time_average_eigenvalues_of_diffusion_tensor[2]), floating6_point_bordered)
        worksheet.write(21, 2+(interval_spacing*index), float(time_average_eigenvalues_of_diffusion_tensor_sd[2]), floating6_point_bordered)
        worksheet.write(21, 3+(interval_spacing*index), float(time_average_eigenvalues_of_diffusion_tensor_ci[2]), floating6_point_bordered)

        worksheet.merge_range(0, (interval_spacing-2)+(interval_spacing*index), 21, (interval_spacing-2)+(interval_spacing*index), '', merge_format_barrier)

    # Close files
    workbook.close()

def format_worksheet(workbook):
    '''
    This method is designed to 

    Parameters
    ----------
    workbook : xlsxwriter.Workbook
        This is the workbook you want to add formats too. 

    Returns
    -------
    merge_format_mol : xlsxwriter.format
        This the format for the molecule name title
    merge_format_dimer : xlsxwriter.format
        This the format for the dimer name title
    merge_format_barrier : xlsxwriter.format
        This the format for the barrier between molecule data
    table_format : xlsxwriter.format
        This the format for the row and column names in a table of data
    number_format : xlsxwriter.format
        This is the format for the numbers in each cell.
    '''
    
    merge_format_mol = workbook.add_format({
        'bold':     True,
        #'border':   6,
        'align':    'center',
        'valign':   'vcenter',
        'fg_color': '#D7E4BC',
    })

    merge_format_dimer = workbook.add_format({
        'bold':     True,
        #'border':   6,
        'align':    'center',
        'valign':   'vcenter',
        'fg_color': '#D7E4BC',
    })

    merge_format_barrier = workbook.add_format({
        'bold':     True,
        #'border':   6,
        'align':    'center',
        'valign':   'vcenter',
        'fg_color': '#000000',
    })

    table_format = workbook.add_format({
        'bold':     True,
        'align':    'left',
        'valign':   'vcenter',
    })

    number_format = workbook.add_format({
        'num_format': '0'
    })

    return merge_format_mol, merge_format_dimer, merge_format_barrier, table_format, number_format

# -----------------------------------------------------------------

def make_energy_asympote_string(conformationally_unique_bandgap_energies, energetic_disorder, temperature):
    """
    This method will turn the energy asympotes for the conformationally unique molecules in the crystal.
    """
    energy_asympote_string = ''; counter = 0
    for molname, bandgap_energy in sorted(conformationally_unique_bandgap_energies.items()):
        energy_asympote = bandgap_energy - ((energetic_disorder ** 2.0)/(kB * temperature))
        energy_asympote_string += str(molname)+': '+str(energy_asympote)
        if counter < (len(conformationally_unique_bandgap_energies)-1):
            energy_asympote_string += ', '
    return energy_asympote_string

# -----------------------------------------------------------------


