from dash.dependencies import Input, Output
from dash import html, dcc
import dash
import os
import flask
import imagesize
import plotly.express as px
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
from dash.html.H1 import H1
from dash.html.P import P


from io import BytesIO
from dash.dependencies import Input, Output, State
from dash import html, dcc
from appsrc import app

# required to allow callbacks for non-existent ID's
app.config.suppress_callback_exceptions = True


df = px.data.medals_wide(indexed=True)

app.layout = html.Div([
    html.P("Medals included:"),
    dcc.Checklist(
        id='medals',
        options=[{'label': x, 'value': x}
                 for x in df.columns],
        value=df.columns.tolist(),
    ),
    dcc.Graph(id="graph"),
    dcc.Graph(id="graph2"),
])


@app.callback(
    Output("graph", "figure"),
    [Input("medals", "value")])
def filter_heatmap(cols):
    # or any Plotly Express function e.g. px.bar(...)
    fig = go.Figure()

    z = [[.1, .3, .5, .7, .9],
         [1, .8, .6, .4, .2],
         [.2, 0, .5, .7, .9],
         [.9, .8, .4, .2, 0],
         [.3, .4, .5, .7, 1]]
    labels = {
        "x": "True, pre, rec",
        "y": "Pred, pre, rec",
        "color": "xd"
    }
    colscal = [[0.0, "rgb(255,0,0)"],
               [0.5, "rgb(255,255,255)"],
               [1.0, "rgb(0,255,0)"]]
    x = list([chr(ord('a') + i) * 20 for i in range(5)])
    y = list([chr(ord('n') + i) for i in range(5)])
    fig.add_trace(go.Heatmap(z=z, text=z, x=x, y=y, colorscale=colscal))
    # fig.update_layout(yaxis=dict(scaleanchor='x'),
    #                   plot_bgcolor='rgba(0,0,0,0)')
    fig.update_xaxes(tickangle=90)
    fig['layout'].update(scene=dict(aspectmode="data"))
    return fig


@app.callback(
    Output("graph2", "figure"),
    [Input("medals", "value")])
def filter_heatmap2(cols):
    import plotly.figure_factory as ff

    z = [[0.1, 0.3, 0.5, 0.2],
         [1.0, 0.8, 0.6, 0.1],
         [0.1, 0.3, 0.6, 0.9],
         [0.6, 0.4, 0.2, 0.2]]

    x = ['healthy', 'multiple diseases', 'rust', 'scab']
    y = ['healthy', 'multiple diseases', 'rust', 'scab']

    # change each element of z to type string for annotations
    z_text = [[str(y) for y in x] for x in z]

    # set up figure
    fig = ff.create_annotated_heatmap(
        z, x=x, y=y, annotation_text=z_text, colorscale='Viridis')

    # add title
    # fig.update_layout(title_text='<i><b>Confusion matrix</b></i>',
    #                   # xaxis = dict(title='x'),
    #                   # yaxis = dict(title='x')
    #                   )

    # add custom xaxis title
    fig.add_annotation(dict(font=dict(color="black", size=14),
                            x=0.5,
                            y=-0.15,
                            showarrow=False,
                            text="Predicted value",
                            xref="paper",
                            yref="paper"))

    # add custom yaxis title
    fig.add_annotation(dict(font=dict(color="black", size=14), x=-0.35, y=0.5,
                       showarrow=False, text="Real value", textangle=-90, xref="paper", yref="paper"))
    return fig


app.run_server(debug=True)

if __name__ == "__main__":
    app.run_server(debug=True)
