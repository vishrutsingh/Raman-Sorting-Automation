import numpy as np
import pandas as pd
from scipy import signal

class buff():
    '''
    A time reversed FIFO Buffer. Input data is always added in forward time.
    Contains function for data manipulation e.g. Normalization, Filtering, Saving, etc.
    '''

    def __init__(self, buff_len):
        self.buff_len = buff_len
        self.signal_1 = 'signal_1'      # signal 1 name
        self.signal_2 = 'signal_2'      # signal 2 name
        self.buff = pd.DataFrame({self.signal_1 : np.zeros(buff_len),
                                  self.signal_2 : np.zeros(buff_len)},
                                 index=np.arange(buff_len),
                                 columns=[self.signal_1, self.signal_2])
        self.index = 0      #insert index

    def add_data(self, input_1, input_2):
        '''
        void, the input date fills up the buffer, until it is full.
        Thereafter the data is inserted at the tail of the buffer.
        :param input_1: signal from 3D detection chamber
        :param input_2: signal from beam breaker sensor
        '''
        if self.index == self.buff_len:
            self.buff.drop([0], inplace=True)
            self.buff.loc[self.index, self.signal_1] = input_1
            self.buff.loc[self.index, self.signal_2] = input_2
            self.buff.reset_index(inplace=True, drop=True)

        else:
            self.buff.loc[self.index, self.signal_1] = input_1
            self.buff.loc[self.index, self.signal_2] = input_2
            self.index += 1

    def filter_data(self, fs, low_cut, high_cut, order=3):
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

        data1= self.buff[self.signal_1].values
        b1, a1 = signal.butter(order, [low, high], analog=False, btype='band')
        zi1 = signal.lfilter_zi(b1, a1)
        za1, _ = signal.lfilter(b1, a1, data1, zi=zi1*data1[0])
        zb1, _ = signal.lfilter(b1, a1, za1, zi=zi1*za1[0])

        data2= self.buff[self.signal_2].values
        b2, a2 = signal.butter(order, [low, high], analog=False, btype='band')
        zi2 = signal.lfilter_zi(b2, a2)
        za2, _ = signal.lfilter(b2, a2, data2, zi=zi2*data2[0])
        zb2, _ = signal.lfilter(b2, a2, za2, zi=zi2*za2[0])

        filt_buff = pd.DataFrame({self.signal_1 : zb1,
                                  self.signal_2 : zb2},
                                 columns=self.buff.columns)

        return filt_buff