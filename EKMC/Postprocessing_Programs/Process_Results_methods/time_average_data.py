"""
time_average_data.py, Geoffrey Weal, 30/8/22

This script is designed to collect the time average data for simulations
"""
import numpy as np
import scipy.stats

def time_average_data(times, average_energies_over_time, diffusion_over_time, diffusion_tensor_over_time, eigenvalues_of_diffusion_tensor_over_time, begin_recording_time):
    """
    This method is designed to obtain the time average data for various data.

    Parameters
    ----------
    times : list
        These are the times that were sampled across all simulations for this system.

    average_energies_over_time
        This is the list of energy values of the ensemble over sampled time.
    diffusion_over_time
        This is the list of diffusion coefficient values of the ensemble over sampled time.
    diffusion_tensor_over_time
        This is the list of diffusion tensor values of the ensemble over sampled time.
    """

    for beginning_index in range(len(times)):
        if times[beginning_index] >= begin_recording_time:
            break
    else:
        raise Exception('Error.')

    time_average_energy    = np.mean(average_energies_over_time[beginning_index::])
    time_average_energy_sd = np.std (average_energies_over_time[beginning_index::])
    time_average_energy_ci = mean_confidence_interval(average_energies_over_time[beginning_index::], confidence=0.95)

    time_average_diffusion    = np.mean(diffusion_over_time[beginning_index::])
    time_average_diffusion_sd = np.std (diffusion_over_time[beginning_index::])
    time_average_diffusion_ci = mean_confidence_interval(diffusion_over_time[beginning_index::], confidence=0.95)

    measured_diffusion_tensor = diffusion_tensor_over_time[beginning_index::]
    time_average_diffusion_tensor    = np.mean(measured_diffusion_tensor, axis=0)
    time_average_diffusion_tensor_sd = np.std (measured_diffusion_tensor, axis=0)
    time_average_diffusion_tensor_ci = mean_confidence_interval(measured_diffusion_tensor, confidence=0.95, axis=0)

    measured_eigenvalues_of_diffusion_tensor = eigenvalues_of_diffusion_tensor_over_time[beginning_index::]
    time_average_eigenvalues_of_diffusion_tensor    = np.mean(measured_eigenvalues_of_diffusion_tensor, axis=0)
    time_average_eigenvalues_of_diffusion_tensor_sd = np.std (measured_eigenvalues_of_diffusion_tensor, axis=0)
    time_average_eigenvalues_of_diffusion_tensor_ci = mean_confidence_interval(measured_eigenvalues_of_diffusion_tensor, confidence=0.95, axis=0)

    return time_average_energy, time_average_energy_sd, time_average_energy_ci, time_average_diffusion, time_average_diffusion_sd, time_average_diffusion_ci, time_average_diffusion_tensor, time_average_diffusion_tensor_sd, time_average_diffusion_tensor_ci, time_average_eigenvalues_of_diffusion_tensor, time_average_eigenvalues_of_diffusion_tensor_sd, time_average_eigenvalues_of_diffusion_tensor_ci

def mean_confidence_interval(data, confidence=0.95, axis=None):
    a = 1.0 * np.array(data)
    if axis is None:
        n  = len(a)
        se = scipy.stats.sem(a)
    else:
        n  = np.ma.size(a, axis=axis)
        se = scipy.stats.sem(a, axis=axis)
    h = se * scipy.stats.t.ppf((1 + confidence) / 2., n-1)
    return h


