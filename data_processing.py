import numpy as np
import pandas as pd
from collections import deque
import feather


class input_buffer():
    '''
    A time reversed FIFO Buffer. Input data is always added in forward time.
    Contains function for data manipulation e.g. Normalization, Filtering, Saving, etc.
    '''

    def __init__(self, buff_len, columns, store):
        self.buff_len = buff_len
        self.buffer = pd.DataFrame(0,
                                   index=np.arange(buff_len),
                                   columns=columns
                                   )
        self.store = store


    def store_data(self):
        self.buffer.to_pickle(self.store)
        #self.buffer.to_feather(self.store)
        #feather.write_dataframe(self.buffer, self.store)

    def add_data(self, data, column):
        temp = self.buffer[column].tolist()
        temp = temp[1:] + [data]
        self.buffer[column] = temp
        print(self.buffer[column])
        self.store_data()

    def update_data(self, data_arrays, columns):
        for i in range(len(columns)):
            self.buffer[columns[i]] = data_arrays[i]
        self.store_data()


class real_time_peak_detection():
    def __init__(self, buffer_length, lag, threshold, influence):
        self.buffer = deque(np.zeros(buffer_length), maxlen=buffer_length)
        self.length = buffer_length
        self.lag = lag
        self.threshold = threshold
        self.influence = influence
        self.signals = deque(np.zeros(buffer_length), maxlen=buffer_length)
        self.filteredY = deque(np.zeros(buffer_length), maxlen=buffer_length)
        self.avgFilter = deque(np.zeros(buffer_length), maxlen=buffer_length)
        self.stdFilter = deque(np.zeros(buffer_length), maxlen=buffer_length)
        self.flag = True

    def thresholding_algo(self, new_value):
        self.buffer.append(new_value)
        self.avgFilter.append(np.mean(list(self.filteredY)[- self.lag:]))
        self.stdFilter.append(np.mean(list(self.filteredY)[- self.lag:]))

        if abs(self.buffer[-1] - self.avgFilter[-2]) > self.threshold * self.stdFilter[-2]:
            if self.flag == True:
                self.signals.append(1)
                self.flag = False
            else:
                self.signals.append(0)
            self.filteredY.append(self.influence * self.buffer[-1] + (1 - self.influence) * self.filteredY[-2])

        else:
            if self.flag == False:
                self.flag = True
            self.signals.append(0)
            self.filteredY.append(self.buffer[-1])

        return list(self.buffer), list(self.signals)






#TODO: min max normalize buffer
# add peak detection functionality
# add standard deviaton class for transit time