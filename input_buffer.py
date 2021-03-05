import numpy as np
import pandas as pd
from scipy import signal


'''
A time reversed FIFO Buffer. Input data is always added in forward time.
Contains function for data manipulation e.g. Normalization, Filtering, Saving, etc.
'''
buff_len = 500
signal_1 = 'signal_1'      # signal 1 name
signal_2 = 'signal_2'      # signal 2 name
buff = pd.DataFrame({signal_1: np.zeros(buff_len),
                     signal_2: np.zeros(buff_len)},
                    index=np.arange(buff_len),
                    columns=[signal_1, signal_2])

global_max_1 = 0
global_max_2 = 0

index = 0


def add_data(input_1, input_2, normalize = False):
    global index
    global global_max_1
    global global_max_2
    '''
    void, the input date fills up the buffer, until it is full.
    Thereafter the data is inserted at the tail of the buffer.
    :param input_1: signal from 3D detection chamber
    :param input_2: signal from beam breaker sensor
    '''
    if normalize:
        if input_1 > global_max_1:
            global_max_1 = input_1
        if input_2 > global_max_2:
            global_max_2 = input_2
        input_1 = input_1/global_max_1
        input_2 = input_2/global_max_2

    if index == buff_len:
        buff.drop([0], inplace=True)
        buff.loc[index, signal_1] = input_1
        buff.loc[index, signal_2] = input_2
        buff.reset_index(inplace=True, drop=True)
    else:
        buff.loc[index, signal_1] = input_1
        buff.loc[index, signal_2] = input_2
        index += 1


def filter_data(fs, low_cut, high_cut, order=3):
    '''
    void, filters the buffer values using band pass filter
    :param fs: sample rate
    :param low_cut: low cutoff in frequency domain
    :param high_cut: high cutoff in frequency domain
    :param order: order of the bandpass filter
    '''
    nyq = 0.5 * fs
    low = low_cut / nyq
    high = high_cut / nyq

    data1 = buff[signal_1].values
    b1, a1 = signal.butter(order, [low, high], analog=False, btype='band')
    zi1 = signal.lfilter_zi(b1, a1)
    za1, _ = signal.lfilter(b1, a1, data1, zi=zi1*data1[0])
    #zb1, _ = signal.lfilter(b1, a1, za1, zi=zi1*za1[0])

    data2 = buff[signal_2].values
    b2, a2 = signal.butter(order, [low, high], analog=False, btype='band')
    zi2 = signal.lfilter_zi(b2, a2)
    za2, _ = signal.lfilter(b2, a2, data2, zi=zi2*data2[0])
    #zb2, _ = signal.lfilter(b2, a2, za2, zi=zi2*za2[0])

    buff['filtered_signal_1'] = za1
    buff['filtered_signal_2'] = za2


def max_scale():
    global buff
    print(buff[signal_1])
    if buff.iloc[index, signal_1] > global_max[signal_1].value:
        global_max[signal_1] = buff[signal_1].max()
    if buff.iloc[index, signal_2] > global_max[signal_1].value:
        global_max[signal_2] = buff[signal_2].max()

    buff = buff/global_max

