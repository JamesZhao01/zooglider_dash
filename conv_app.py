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
from appsrc import app, config
from components.vis import getdropdown
from components.dropdowns import experiment_dropdown, trial_dropdown

app.config.suppress_callback_exceptions = True

image_directory = os.path.join(config["datasets"])
experiment_directory = os.path.join(config["experiments"])
static_image_route = '/static/'
confusion_image_route = "/confusion/"


@app.server.route(f"{static_image_route}<path:path><any(png, jpg):extension>")
def serve_dataset_image(path, extension):
    '''
    Serves Images from image_directory, accessible through /static route
    '''
    imgname = os.path.basename(path) + extension
    imgpath = os.path.dirname(path)
    return flask.send_from_directory(os.path.join(image_directory, imgpath), imgname)


@app.server.route(f"{confusion_image_route}<path:path><any(png, jpg):extension>")
def serve_confusion_image(path, extension):
    '''
    Serves Confusion Matrices
    '''
    imgname = os.path.basename(path) + extension
    imgpath = os.path.dirname(path)
    return flask.send_from_directory(os.path.join(experiment_directory, imgpath), imgname)


app.layout = html.Div(
    children=[
        html.H1(children='Hello Dash', style={"color": "white"}),
        dbc.Container(children=[
            dbc.Row(children=[
                dbc.Col(width=6, children=[
                    html.P(children="Experiment:"),
                    experiment_dropdown("experiment-dropdown")
                ]),
                dbc.Col(width=6, children=[
                    html.P(children="Dataset:"),
                    html.Div(id="trial-dropdown-wrapper")
                ]),
            ]),
            dbc.Row(children=[
                dbc.Col(width=6, id="class-sel-1"),
                dbc.Col(width=6, id="class-sel-2")
            ]),
        ]),
        dbc.Container(id="experiment-body")
    ])


@app.callback(
    Output("trial-dropdown-wrapper", "children"),
    Input("experiment-dropdown", "value")
)
def update_trial_dropdown(experiment):
    return trial_dropdown("trial-dropdown", experiment)


def render_confusion(exp_id, trial_num):
    return html.Img(src=f"/confusion/{exp_id}/{trial_num}/outputs/confusion_matrix_for_all.png", style={"max-width": "100%"})


@app.callback(
    Output("experiment-body", "children"),
    Input("trial-dropdown", "value"),
    State("experiment-dropdown", "value")
)
def render_body(trial, experiment):
    if trial == "None" or experiment == "None":
        return ""
    trial_num, exp_id = os.path.basename(trial), os.path.basename(experiment)
    return [
        dbc.Row(children=render_image(exp_id, trial_num)),
        dbc.Row(children=[

        ])
    ]


# @app.callback(
#     Output("grid", "children"),
#     Input("class-sel-1-dd", "value"),
#     Input("class-sel-2-dd", "value"),
#     State("ds", "value"),
#     State("exp", "value")
# )
# def update_class_selection(class1, class2, ds, exp):
#     if class1 == "_" or class2 == "_":
#         return ""
#     ds_name = os.path.basename(ds)
#     static_class_root = os.path.join("static", ds_name, class1)
#     fs_class_path = os.path.join(ds, class1)
#     files = os.listdir(fs_class_path)[:2]
#     # print(pil_to_b64(os.path.join(classpath, t)))
#     return html.Div(className="d-flex flex-row flex-wrap",
#                     children=[html.Img(src=os.path.join(static_class_root, f)) for f in files])
# @ app.callback(
#     Output("class-sel-1", "children"),
#     Output("class-sel-2", "children"),
#     Input("exp", "value"),
#     Input("ds", "value")
# )
# def experiment_selected(exp_path, ds_path):
#     '''
#     exp_path = \\zgdata.ucsd.edu\\zooplankton-pytorch\\experiments\\<exp_name>\\<trial#>
#     '''
#     if exp_path == "_" or ds_path == "_":
#         return "", ""
#     dd1 = dcc.Dropdown(id="class-sel-1-dd", options=[{"label": "None", "value": "_"}] + [{"label": f, "value": f} for f in os.listdir(ds_path) if os.path.isdir(os.path.join(ds_path, f))],
#                        value="_")
#     dd2 = dcc.Dropdown(id="class-sel-2-dd", options=[{"label": "None", "value": "_"}] + [{"label": f, "value": f} for f in os.listdir(ds_path) if os.path.isdir(os.path.join(ds_path, f))],
#                        value="_")
#     print(exp_path)
#     # classification csv file
#     classification_csv = has_classification(exp_path)
#     if not classification_csv:
#         print("DOES NOT EXIST")
#         return "DOES NOT EXIST", "DOES NOT EXIST"
#     with open(classification_csv, newline='') as csvfile:
#         spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
#         next(spamreader)
#         exp_data = []
#         for row in spamreader:
#             exp_data.append(row)
#     # print([f for f in os.listdir(os.path.join(exp_path, "outputs"))])
#     return html.Div(children=["Class 1: ", dd1]), html.Div(children=["Class 2: ", dd2])
# @ app.callback(
#     Output("out", "children"),
#     Input("example-graph", "clickData")
# )
# def fn(data):
#     if data is None:
#         return ""
#     return f"data: {data['points'][0]['label']}, {data['points'][0]['value']}"
if __name__ == '__main__':
    app.run_server(debug=True)
