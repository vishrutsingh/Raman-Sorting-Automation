import dash
import dash_html_components as html
import dash_core_components as dcc



app = dash.Dash(__name__, update_title=None)
app.layout = html.Div([
    html.Div([
        html.H2('RAMAN Data',
                style={'float': 'left',
                       }),
        ]),
    html.Div(children=html.Div(id='graphs'), className='row'),
    dcc.Interval(
        id='graph-update',
        interval=1),
    ], className="container",style={'width':'98%','margin-left':10,'margin-right':10,'max-width':50000})


@app.callback(
    dash.dependencies.Output('graphs', 'children'),
    [dash.dependencies.Input('graph-update', 'interval')]
    )
def update_graph(input_buffer):
    graphs = []
    for fields in input_buffer.columns():

        data = go.Scatter(
            x=list(times),
            y=list(data_dict[data_name]),
            name='Scatter',
            fill="tozeroy",
            fillcolor="#6897bb"
            )

        graphs.append(html.Div(dcc.Graph(
            id=data_name,
            animate=True,
            figure={'data': [data],'layout' : go.Layout(xaxis=dict(range=[min(times),max(times)]),
                                                        yaxis=dict(range=[min(data_dict[data_name]),max(data_dict[data_name])]),
                                                        margin={'l':50,'r':1,'t':45,'b':1},
                                                        title='{}'.format(data_name))}
            ), className=class_choice))

    return graphs




if __name__ == '__main__':
    app.run_server(mode='external', port = 8069, dev_tools_ui=True, dev_tools_hot_reload =True, threaded=True)


