import csv
import time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import signal
from scipy.signal import butter
from sklearn.preprocessing import MinMaxScaler
from buff import buff


class read_API():
    def __init__(self):
        self.reader = csv.reader(open('Copy of Electrical signals (Chlorella Vulgaris).csv', 'r'))

    def read(self):
        next(self.reader)
        for row in self.reader:
            if row[0] == 'Time (ms)':
                time.sleep(10)
                continue
            time.sleep(0.001)
            return float(row[1]), float(row[2])




def csv_file(csvfile, skip_data):
    with open(csvfile, 'r') as f:
        reader = csv.reader(f)
        for lines in range(skip_data):
            headers = next(reader)
        data = {h: [] for h in headers}
        for row in reader:
            if row[0] == 'Time (ms)':
                break
            data['Time (ms)'].append(int(row[0]))
            data['Electrical signal 1 from 3D detection chamber'].append(float(row[1]))
            data['Electrical signal 2 from beam-break sensor'].append(float(row[2]))
    return data

def butter_band(data, lowcut, highcut, fs, order=3):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = signal.butter(order, [low, high], analog=False, btype='band')
    zi = signal.lfilter_zi(b, a)
    z, _ = signal.lfilter(b, a, data, zi=zi*data[0])
    z2, _ = signal.lfilter(b, a, z, zi=zi*z[0])
    return z2

def plot_2(x, y1=None, y2=None):
    plt.figure(figsize=(10, 8))
    plt.title('Voltage/Time', fontsize=20)
    plt.ylabel('Voltage', fontsize=15)
    plt.xlabel('Time (ms)', fontsize=15)
    if y1 is not None: plt.plot(x, y1, 'r')
    if y2 is not None: plt.plot(x, y2, 'b')
    plt.show()

def plot_power_spectrum( fs, data_x, data_y1=None, data_y2=None):
    plt.figure(figsize=(10, 8))
    plt.title('Power Spectrum Density', fontsize=20)
    plt.ylabel('Intensity', fontsize=15)
    plt.xlabel('Frequency', fontsize=15)
    time = np.fft.fftfreq(len(data_x), 1/fs)
    cut = time > 0
    if data_y1 is not None:
        signal_1 = np.abs(np.fft.fft(data_y1))**2
        plt.plot(time[cut], signal_1[cut], 'r')
    if data_y2 is not None:
        signal_2 = np.abs(np.fft.fft(data_y2))**2
        plt.plot(time[cut], signal_2[cut], 'b')
    plt.show()




if __name__ == "__main__":
    fs = 1000
    buff_len = 500
    cutoff_low = 0.001
    cutoff_high = 40

    df = pd.read_csv('Copy of Electrical signals (Chlorella Vulgaris).csv')
    df.drop(['Time (ms)'], axis=1, inplace=True)
    df.drop([50000, 100001], inplace=True)
    df = df.apply(pd.to_numeric)

    buffer = buff(buff_len)

    plt.ion()
    fig, ax = plt.subplots()
    index = 0
    while True:
        input_a = df.loc[0, 'Electrical signal 1 from 3D detection chamber']
        input_b = df.loc[0, 'Electrical signal 2 from beam-break sensor']
        df.drop([0], inplace=True)
        df.reset_index(inplace=True, drop=True)

        buffer.add_data(input_a, input_b)
        filt_buffer = buffer.filter_data(fs, cutoff_low, cutoff_high)
        filt_buffer = (filt_buffer-filt_buffer.min())/(filt_buffer.max()-filt_buffer.min())      #minmax normalization

        ax.clear()
        filt_buffer.signal_1.plot(ax=ax,  style='r-')
        filt_buffer.signal_2.plot(ax=ax,  style='b-')
        plt.draw()
        plt.pause(0.001)







