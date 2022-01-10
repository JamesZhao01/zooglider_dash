# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from inspect import classify_class_attrs
import dash
import os
import base64
import flask
import csv
from PIL import Image

from io import BytesIO

import plotly.express as px
# import pandas as pd

from dash.dependencies import Input, Output, State
from dash import html, dcc
import dash_bootstrap_components as dbc
# from components.table import generate_table
from appsrc import app
from components.vis import getdropdown
from components.exp_dropdown import exp_dd, ds_dd
from utils.path_utils import has_classification


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

image_directory = 'C:/Users/James/Desktop/quicklocate/2022/sampleimgs'
image_directory = "\\\\zgdata.ucsd.edu\\d_sarafian\\datasets"
static_image_route = '/static/'

app.layout = html.Div(
    style={'backgroundColor': colors['background']},
    children=[
        html.H1(children='Hello Dash', style={"color": "white"}),
        # dcc.Graph(
        #     id='example-graph',
        #     figure=fig
        # ),
        dbc.Container(children=[
            dbc.Row(children=[
                dbc.Col(width=4, children=[
                    html.P(children="Root Address: "),
                    dcc.Input(
                        id="exp-path",
                        className="w-100",
                        placeholder="Input root path",
                        value="\\\\zgdata.ucsd.edu\\d_sarafian",
                    )]
                ),
                dbc.Col(width=4, children=[
                    html.P(children="Experiment (Trial):"),
                    html.Div(id="exp-dd-wrap")
                ]),
                dbc.Col(width=4, children=[
                    html.P(children="Dataset:"), html.Div(className="d-flex flex-row", children=[
                        html.Div(id="ds-dd-wrap", className="flex-grow-1"),
                        html.Button("🗘", id="refresh")]
                    )]
                ),
            ]),
            dbc.Row(children=[
                dbc.Col(width=6, id="class-sel-1"),
                dbc.Col(width=6, id="class-sel-2")
            ]),
            dbc.Row(id="grid")
        ]),
        dbc.Container(children=[
            dbc.Row(children=[
                dbc.Col(children="ASDF", width=4),
                dbc.Col(children="ASDF", width=4),
                dbc.Col(children="ASDF", width=4),
            ])
        ])
    ])


@app.server.route('/static/<path:path>.png')
def serve_image(path):
    imgname = os.path.basename(path) + ".png"
    imgpath = os.path.dirname(path)
    return flask.send_from_directory(os.path.join(image_directory, imgpath), imgname)


c1_page = 0
c2_page = 0
class1_imgs = []
class2_imgs = []
exp_data = []


@app.callback(
    Output("grid", "children"),
    Input("class-sel-1-dd", "value"),
    Input("class-sel-2-dd", "value"),
    State("ds", "value"),
    State("exp", "value")
)
def update_class_selection(class1, class2, ds, exp):
    if class1 == "_" or class2 == "_":
        return ""
    ds_name = os.path.basename(ds)
    static_class_root = os.path.join("static", ds_name, class1)
    fs_class_path = os.path.join(ds, class1)
    files = os.listdir(fs_class_path)[:2]
    # print(pil_to_b64(os.path.join(classpath, t)))
    return html.Div(className="d-flex flex-row flex-wrap",
                    children=[html.Img(src=os.path.join(static_class_root, f)) for f in files])


@ app.callback(
    Output("exp-dd-wrap", "children"),
    Output("ds-dd-wrap", "children"),
    Input("refresh", "n_clicks"),
    State("exp-path", "value")
)
def update_dd(n_cli, path):
    return exp_dd(path), ds_dd(path)


@ app.callback(
    Output("class-sel-1", "children"),
    Output("class-sel-2", "children"),
    Input("exp", "value"),
    Input("ds", "value")
)
def experiment_selected(exp_path, ds_path):
    '''
    exp_path = \\zgdata.ucsd.edu\\zooplankton-pytorch\\experiments\\<exp_name>\\<trial#>
    '''
    if exp_path == "_" or ds_path == "_":
        return "", ""
    dd1 = dcc.Dropdown(id="class-sel-1-dd", options=[{"label": "None", "value": "_"}] + [{"label": f, "value": f} for f in os.listdir(ds_path) if os.path.isdir(os.path.join(ds_path, f))],
                       value="_")
    dd2 = dcc.Dropdown(id="class-sel-2-dd", options=[{"label": "None", "value": "_"}] + [{"label": f, "value": f} for f in os.listdir(ds_path) if os.path.isdir(os.path.join(ds_path, f))],
                       value="_")
    print(exp_path)
    # classification csv file
    classification_csv = has_classification(exp_path)
    if not classification_csv:
        print("DOES NOT EXIST")
        return "DOES NOT EXIST", "DOES NOT EXIST"
    with open(classification_csv, newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        next(spamreader)
        exp_data = []
        for row in spamreader:
            exp_data.append(row)
    # print([f for f in os.listdir(os.path.join(exp_path, "outputs"))])
    return html.Div(children=["Class 1: ", dd1]), html.Div(children=["Class 2: ", dd2])


@ app.callback(
    Output("out", "children"),
    Input("example-graph", "clickData")
)
def fn(data):
    if data is None:
        return ""
    return f"data: {data['points'][0]['label']}, {data['points'][0]['value']}"


if __name__ == '__main__':
    app.run_server(debug=True)
