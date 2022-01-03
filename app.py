# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash, os

import plotly.express as px
# import pandas as pd

from dash.dependencies import Input, Output, State
from dash import html, dcc
import dash_bootstrap_components as dbc
# from components.table import generate_table
from components.vis import getdropdown
from components.exp_dropdown import exp_dropdown, ds_dropdown
from appsrc import app


app.config.suppress_callback_exceptions = True

colors = {
    'background': 'white',
    'text': '#7FDBFF'
}


# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
# df = pd.DataFrame({
#     "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
#     "Amount": [4, 1, 2, 2, 4, 5],
#     "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]
# })

# fig = px.bar(df, x="Fruit", y="Amount", color="City", barmode="group")

# fig.update_layout(
#     plot_bgcolor=colors['background'],
#     paper_bgcolor=colors['background'],
#     font_color=colors['text']
# )


app.layout = html.Div(
    style={'backgroundColor': colors['background']},
    children=[
    html.H1(children='Hello Dash', style={"color": "white"}),
    # dcc.Graph(
    #     id='example-graph',
    #     figure=fig
    # ),
    dbc.Container(children = [
        dbc.Row(children = 
            dbc.Col(width=12, className="d-flex flex-row", children = 
                [dcc.Input(
                    id="exp-path",
                    placeholder="Input root path",
                    #value="\\\\zgdata.ucsd.edu\d_sarafian",
                    value = "C:\\Users\\James\\Desktop\\quicklocate\\dsarafian_cpy",
                    style={"width": "200px"}
                ),
                html.Div(id="exp-dd-wrap", style={"width": "200px"}),
                html.Div(id="ds-dd-wrap", style={"width": "200px"}),
                html.Button("🗘", id="refresh")
                ]
            )
        ),
        dbc.Row(children = 
            [
                dbc.Col(width=6, id="class-sel-1"),
                dbc.Col(width=6, id="class-sel-2")
            ]
        )
    ]),
    dbc.Container(children = [
        dbc.Row(children = [
            dbc.Col(children = "ASDF", width=4),
            dbc.Col(children = "ASDF", width=4),
            dbc.Col(children = "ASDF", width=4),
        ])
    ]),
    html.Div(id = "hello", children = "Hello", style={"color": "blue"}),
    html.Div(children = "Pog", style={"color": "orange"}, id="out"),
    html.Img(src="./assets/Untitled.png")
])
@app.callback(
    Output("exp-dd-wrap", "children"),
    Output("ds-dd-wrap", "children"),
    Input("refresh", "n_clicks"),
    State("exp-path", "value")
)
def update_dd(n_cli, path):
    return exp_dropdown(path), ds_dropdown(path)

@app.callback(
    Output("hello", "children"),
    Output("class-sel-1", "children"),
    Output("class-sel-2", "children"),
    Input("exp", "value"),
    Input("ds", "value")
)
def experiment_selected(exp_path, ds_path):
    print("exp selected", exp_path, "ds selected", ds_path)
    if exp_path == "_" or ds_path == "_":
        return "Empty", "None", "None"
    print([f for f in os.listdir(os.path.join(exp_path, "outputs"))])
    return exp_path, exp_path, ds_path


@app.callback(
    Output("out", "children"),
    Input("example-graph", "clickData")
)
def fn(data):
    if data is None:
        return ""
    return f"data: {data['points'][0]['label']}, {data['points'][0]['value']}"

if __name__ == '__main__':
    app.run_server(debug=True)