# This is a script designed to concatenate all of the files in a folder
import numpy as np
from bin_time import read_and_bin_profile
import glob
import os
from astropy.time import Time
from psrfits_analysis import psrfits_data

def combine_thread(folder, pulse_motion, time_array, adjust=None):
    """"Combine all of the pulsar fits file in the folder
    @param folder: str of the folder whose files to combine
    @param timebins: int of the number of time bins in the combined profile
    """
    # Combine all the files
    profile, time, freq = concatenate_files(folder,pulse_motion, adjust)
    # Adjust the time
    profile, time = read_and_bin_profile(profile, time, time_array)
    return profile, time, freq


def concatenate_files(folder, pulse_motion, shift=None):
    """Combines all the pulsar fits files into the folders, but does not adjust the time.
    Designed to be used as a helper method"""
    time = np.array([], dtype='float')
    freq = np.array([], dtype='float')
    profile = None
    os.chdir(folder)
    files=np.sort(glob.glob('*.ar'))
    for i in range(len(files)):
        scan = files[i][:-2] # Thread
        print(scan)
        print('File_Name: {}, File_Number: {}, Total_Files: {}'.format(files[i], i,len(files)))
        # Roll frequencies
        pfits = psrfits_data(files[i], remove_dispersion=True)
        freq = pfits.freq
        time = np.r_[time, Time(pfits.time).value]
        data = pfits.data
        if type(shift) != type(None):
            data = adjust(data, shift[i])
        # Adjust for pulse movement
        data = np.roll(data, int(np.round(pulse_motion[i])), axis=-1)
        # On the very first loop
        if i == 0:
            profile = data
        else:
            profile = np.r_[profile, data]
    os.chdir("..")
    return profile, time, freq
        
def adjust(arr, shift):
    rolls = np.linspace(0, shift, arr.shape[0])
    copy = arr.copy()
    for i in range(arr.shape[0]):
        copy[i,:,:] = np.roll(copy[i,:,:], int(np.round(rolls[i])), axis=1)
    return copy


def adjust_frequencies(array, freq_rolls):
    """Adjust the frequencies in the array. Only to be used when error in 
    dedispersion occursed. Of the dataset, this should only be used on the 
    Arecibo data"""
    for i in range(data.shape[1]):
        data[:,i,:] = np.roll(data[:,i,:], int(freq_rolls[i]))
    return data
    
