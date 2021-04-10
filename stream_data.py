import dash
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
from plotly.subplots import make_subplots
import plotly.graph_objs as go
import pandas as pd
import webbrowser
from threading import Timer
import feather
import main
import numpy as np


#port
port = 8050



def update_data():
    #return feather.read_dataframe('data/buffer.feather', use_threads=True, memory_map=True)
    #return pd.read_feather('data/buffer.feather')
    return pd.read_pickle('data/buffer.pkl')


def open_browser():
    webbrowser.open_new("http://localhost:{}".format(port))



app = dash.Dash(__name__,
                update_title=None, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = dbc.Container(
    [
        html.Img(src=app.get_asset_url('UofGSoE.PNG')),
        html.Div(['RAMAN Sorting Automation'],
                 style={#'float': 'left',
                        'color': '#003560',     #UofG color code
                        'font-size': '40px',
                        'margin-left': '20px',
                        'display': 'inline-block'}),
        html.Hr(),
        html.Div([dcc.Graph(id='fig1'), dcc.Graph(id='fig2')]),
        dcc.Interval(
            id='interval-component',
            interval=1000,
            n_intervals=0)
    ]
)


@app.callback(
    [Output('fig1', 'figure'),
     Output('fig2', 'figure')],
    [Input('interval-component', 'n_intervals')],
)
def update_graph(n):
    data = update_data()
    sensor_data = make_subplots(rows=1, cols=2,
                                vertical_spacing=0.2,
                                specs=[
                                    [{}, {}]
                                ],
                                subplot_titles=("Signal from 3D chamber (V)", "Signal from beam-break sensor (V)"),
                                x_title='Time (ms)',
                                y_title='Voltage (v)',
                                )
    sensor_data.append_trace({'x': data.index.values, 'y': data['signal_1']}, 1, 1)
    sensor_data.append_trace({'x': data.index.values, 'y': data['signal_2']}, 1, 2)


    processed_data = go.Figure(
        data=[go.Scatter(
            x=data.index.values,
            y=data[col]
        )for col in ['filtered_signal_1', 'filtered_signal_2']
        ],
        layout=go.Layout(
            title='Proccessed Data',
            xaxis={'title': 'Time (ms)'},
            yaxis={'title': 'Strength'},
        )
    )
    return [sensor_data, processed_data]



if __name__ == '__main__':
    Timer(1, open_browser).start()
    app.run_server(debug=False)

#TODO: asthetic changes
# add axis labels
# add save data functionality