import numpy as np
from astropy.time import Time

def get_tbinned(t, num):
    start = Time(t[0], format='mjd').value
    end = Time(t[-1], format='mjd').value
    new_time = np.linspace(start, end, num)
    return Time(new_time, format='mjd')

def read_and_bin_profile(I, t_init, t_new):
    t_old = Time(t_init, format='mjd')
    Ibinned = np.zeros((len(t_new),I.shape[1], I.shape[2]))
    for i in range(I.shape[0]):
        idx = np.searchsorted(t_new.mjd,t_old[i].mjd)
        Ibinned[idx-1,:]+=I[i,:,:]
    return Ibinned, t_new.value


def read_and_bin_file(fname,tbinned):
    gpu = np.load(fname)
    t = gpu['t']
    I = gpu['I']
    f = gpu['f']
    
    if type(t) != np.ndarray:
        for i in range (len(t)):
            t[i] = np.float(t[i].value)
    t = np.array(t, dtype=float)
    t = Time(t,format='mjd')

    Ibinned = np.zeros((len(tbinned),I.shape[1], I.shape[2]))
    for i in range(I.shape[0]):
        idx = np.searchsorted(tbinned.mjd,t[i].mjd)
        Ibinned[idx-1,:]+=I[i,:,:]
    #Ibinned = Ibinned/Ibinned.mean(axis=1,keepdims=True)
    return Ibinned,f, tbinned


# OLD CODE
def read_and_bin(fname,tbinned):
    gpu = np.load(fname)
    t = gpu['time']
    I = gpu['I']
    f = gpu['freq']

    t = Time(t,format='mjd')

    Ibinned = np.zeros((len(tbinned),I.shape[1]))
    for i in range(I.shape[0]):
        idx = np.searchsorted(tbinned.mjd,t[i].mjd)
        Ibinned[idx-1,:]+=I[i,:]
    Ibinned = Ibinned/Ibinned.mean(axis=1,keepdims=True)
    return Ibinned,f, tbinned
