import pandas as pd
import numpy as np
import data_processing
import time
import concurrent.futures

from datetime import datetime
import store


def monitor_detection(transit_time_store, buffer_store, transit_time_threshold, start_time, max_monitor_time = 1000):

    transit_array = pd.read_feather('data/transit_time.pkl', columns=['transit time'], use_threads=True)
    transit_array = list(transit_array['transit time'])
    while (datetime.now() - start_time).total_seconds()*1000 < max_monitor_time:
        b = pd.read_feather('data/buffer.pkl', columns=['filtered_signal_2'], use_threads=True)
        curr_b = list(b['filtered_signal_2'])[-1:]
        if curr_b == [1]:
            window = [(np.mean(transit_array) + transit_time_threshold * np.std(transit_array)),
                      (np.mean(transit_array) - transit_time_threshold * np.std(transit_array))]
            tt = ((datetime.now() - start_time).total_seconds()*1000)
            transit_time_store.add_data(tt, 'transit time')
            print(f'transit time:{tt}')



# TODO: complete readme

if __name__ == "__main__":
    fs = 1000
    buff_len = 1000
    cutoff_low = 0.001
    cutoff_high = 49
    transit_time_threshold = 1

    df = pd.read_csv('Two sets of electric signals.csv')
    df.drop(['Time (s)'], axis=1, inplace=True)
    df = df.apply(pd.to_numeric)
    # df = pd.read_csv('Copy of Electrical signals (Chlorella Vulgaris).csv')
    # df.drop(['Time (ms)'], axis=1, inplace=True)
    # df.drop([50000, 100001], inplace=True)
    # df = df.apply(pd.to_numeric)

    buffer_store = data_processing.input_buffer(buff_len, ['signal_1', 'signal_2', 'filtered_signal_1', 'filtered_signal_2'], 'data/buffer.pkl')
    transit_time_store = data_processing.input_buffer(0, ['transit time'], 'data/transit_time.pkl')
    buffer_store.store_data()
    transit_time_store.store_data()

    a_filter = data_processing.real_time_peak_detection(buff_len, lag=10, threshold=10, influence=1)
    b_filter = data_processing.real_time_peak_detection(buff_len, lag=10, threshold=10, influence=1)


    with concurrent.futures.ProcessPoolExecutor() as executor:
       results = []
       while True:
           '''
           check for input, if not then data = 0 
           '''
           start = time.perf_counter()
           input_a = df.loc[0, 'Signal from 3D chamber (V)']
           input_b = df.loc[0, 'Signal from beam-break sensor (V)']
           # input_a = df.loc[0, 'Electrical signal 1 from 3D detection chamber']
           # input_b = df.loc[0, 'Electrical signal 2 from beam-break sensor']
           df.drop([0], inplace=True)
           df.reset_index(inplace=True, drop=True)

           a_signal, a_peaks = a_filter.thresholding_algo(input_a)
           b_signal, b_peaks = b_filter.thresholding_algo(input_b)

           buffer_store.update_data([a_signal, b_signal, a_peaks, b_peaks],
                                    ['signal_1', 'signal_2', 'filtered_signal_1', 'filtered_signal_2'])





           #if a_peaks[-1] == 1:
           #    start_time = datetime.now()
           #    executor.submit(monitor_detection, transit_time_store, buffer_store,  transit_time_threshold, start_time)


           time.sleep(0.04)
           print((time.perf_counter() - start)*1000)