import csv
import time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import signal
from scipy.signal import butter
from sklearn.preprocessing import MinMaxScaler
import input_buffer as buffer
from datetime import datetime



if __name__ == "__main__":
    fs = 1000
    buff_len = 500
    cutoff_low = 0.001
    cutoff_high = 40

    df = pd.read_csv('Copy of Electrical signals (Chlorella Vulgaris).csv')
    df.drop(['Time (ms)'], axis=1, inplace=True)
    df.drop([50000, 100001], inplace=True)
    df = df.apply(pd.to_numeric)

    plt.ion()
    fig, ax = plt.subplots()
    index = 0
    while True:
        start = datetime.now()
        input_a = df.loc[0, 'Electrical signal 1 from 3D detection chamber']
        input_b = df.loc[0, 'Electrical signal 2 from beam-break sensor']
        df.drop([0], inplace=True)
        df.reset_index(inplace=True, drop=True)

        buffer.add_data(input_a, input_b, normalize=True)
        buffer.filter_data(fs, cutoff_low, cutoff_high)


        ax.clear()
        #ax.set_ylim(0,1)
        buffer.buff.filtered_signal_1.plot(ax=ax,  style='r-')
        buffer.buff.filtered_signal_2.plot(ax=ax,  style='b-')
        plt.draw()
        plt.pause(0.001)


        #end = datetime.now()
        #print((start - end))







