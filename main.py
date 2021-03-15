import datetime
import pandas as pd
import numpy as np
import data_processing
import matplotlib.pyplot as plt
import time
import tables

fs = 1000
buff_len = 1000
cutoff_low = 0.001
cutoff_high = 49

df = pd.read_csv('Two sets of electric signals.csv')
df.drop(['Time (s)'], axis=1, inplace=True)
df = df.apply(pd.to_numeric)

#df = pd.read_csv('Copy of Electrical signals (Chlorella Vulgaris).csv')
#df.drop(['Time (ms)'], axis=1, inplace=True)
#df.drop([50000, 100001], inplace=True)
#df = df.apply(pd.to_numeric)

buffer = data_processing.input_buffer(buff_len)

#plt.ion()
#fig, ax = plt.subplots()

if __name__ == "__main__":
   while True:
      input_a = df.loc[0, 'Signal from 3D chamber (V)']
      input_b = df.loc[0, 'Signal from beam-break sensor (V)']
      #input_a = df.loc[0, 'Electrical signal 1 from 3D detection chamber']
      #input_b = df.loc[0, 'Electrical signal 2 from beam-break sensor']
      df.drop([0], inplace=True)
      df.reset_index(inplace=True, drop=True)


      buffer.add_data(input_a, input_b)
      buffer.filter_data(fs, cutoff_low, cutoff_high)

      norm = (buffer.buffer - buffer.buffer.mean())/(buffer.buffer.std())
      #norm = (buffer.buffer - buffer.buffer.median())/(buffer.buffer.quantile(0.75) - buffer.buffer.quantile(0.25))
      #store = pd.HDFStore('data/store.h5')

      norm.to_hdf('data/store.h5', 'df', mode='w')
      #print(pd.read_hdf('data/store.h5', 'df'))
      #store.close()

      time.sleep(0.001)

      #ax.clear()
      ##ax.set_ylim(-2, 5)
      #norm.filtered_signal_1.plot(ax=ax,  style='r-')
      #norm.filtered_signal_2.plot(ax=ax,  style='b-')
      #plt.draw()
      #plt.pause(0.001)






