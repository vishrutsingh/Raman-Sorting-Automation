import dash
import dash_html_components as html
import dash_core_components as dcc
from plotly.subplots import make_subplots
import pandas as pd
import tables

def update_data():
    return pd.read_hdf('data/store.h5', 'df', mode='r')



app = dash.Dash(__name__, update_title=None)
app.layout = html.Div(
    html.Div([
        html.H2('RAMAN Data',
            style={'float': 'left',
            }),
        dcc.Graph(id='live-update-graphs', figure='figure'),
        dcc.Interval(
            id='interval-component',
            interval=1000,
            n_intervals=0),
    ])
)


@app.callback(
dash.dependencies.Output('live-update-graphs', 'figure'),
[dash.dependencies.Input('interval-component', 'n_intervals')],
)
def update_graph(n):
    data = update_data()
    fig = make_subplots(rows=3, cols=2,
                                     vertical_spacing=0.2,
                                     specs=[
                                         [{}, {}],
                                         [{"rowspan": 2, "colspan": 2}, None],
                                         [None, None]
                                     ],
                                     subplot_titles=("Signal 1", "Signal 2", "Filtered Signal 1", "Filtered Signal 2"))

    fig.append_trace({'x': data.index.values, 'y': data['signal_1']}, 1, 1)
    fig.append_trace({'x': data.index.values, 'y': data['signal_2']}, 1, 2)
    fig.append_trace({'x': data.index.values, 'y': data['filtered_signal_1']}, 2, 1)
    fig.append_trace({'x': data.index.values, 'y': data['filtered_signal_2']}, 2, 1)
    return fig


if __name__ == '__main__':
    app.run_server(debug=False)


