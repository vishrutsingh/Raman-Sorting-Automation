import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

if __name__ == "__main__":
    buff_len = 100
    x = np.random.rand(1000)
    y = np.random.rand(1000)
    df = pd.DataFrame({"x":x, "y":y})

    buff_data = {"x": np.zeros(buff_len), "y": np.zeros(buff_len)}

    df2 = pd.DataFrame(buff_data, index=np.arange(buff_len), columns=df.columns)


    plt.ion()
    fig, ax = plt.subplots()
    index = 0

    while True:

        input_x = df.loc[0, "x"]
        input_y = df.loc[0, "y"]
        df.drop([0], inplace=True)
        df.reset_index(inplace=True, drop=True)

        if index == buff_len:
            df2.drop([0], inplace=True)
            df2.loc[index, 'x'] = input_x
            df2.loc[index, 'y'] = input_y
            df2.reset_index(inplace=True, drop=True)

        else:
            df2.loc[index, 'x'] = input_x
            df2.loc[index, 'y'] = input_y
            index+=1


        ax.clear()
        df2.x.plot(ax=ax,  style='r-')
        df2.y.plot(ax=ax,  style='b-')
        plt.draw()
        plt.pause(0.001)


