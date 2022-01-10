import os
from dash.html.H1 import H1
from dash.html.P import P
import flask
import csv

from io import BytesIO

import plotly.express as px

from dash.dependencies import Input, Output, State
from dash import html, dcc
import dash_bootstrap_components as dbc
from appsrc import app

# required to allow callbacks for non-existent ID's
app.config.suppress_callback_exceptions = True

# The absolute path directory to serve files from. Assumes file architecture as follows:
# datasets
# -- dataset1
# -- -- Acantharian
# -- -- -- IMG_2016_blahblah_000.png
# -- -- -- IMG_2016_blahblah_001.png
# -- -- Comets
# -- -- -- IMG_2018_blahblah_054.png
# -- -- -- IMG_2017_blahblah_234.png
# -- dataset2
image_directory = "\\\\zgdata.ucsd.edu\\d_sarafian\\datasets"
# Absolute max number of viewable files because some categories are HUGEEEE
ABSOLUTE_MAX = 5000


@app.server.route("/static/<path:path><any(png, jpg):extension>")
def serve_image(path, extension):
    '''
    Serves Images from image_directory, accessible through /static route
    '''
    imgname = os.path.basename(path) + extension
    imgpath = os.path.dirname(path)
    return flask.send_from_directory(os.path.join(image_directory, imgpath),
                                     imgname)


def get_ds_dropdown(id):
    '''
    Creates a dropdown for all datasets using the hardcoded image directory
    '''
    default = [{"label": "None", "value": "_"}]
    return dcc.Dropdown(
        id=id,
        value="_",
        options=default + [{
            "label": f,
            "value": f
        } for f in os.listdir(image_directory)
            if os.path.isdir(os.path.join(image_directory, f))],
    )


app.layout = html.Div(children=[
    dbc.Container(children=[
        html.H3(children=f"Static File Serving Directory (Hard Coded):"),
        html.P(children=image_directory),
        dbc.Row(children=[
            dbc.Col(
                width=6,
                children=[
                    html.P(children="Dataset 1:"),
                    get_ds_dropdown("ds1"),
                ],
            ),
            dbc.Col(
                width=6,
                children=[
                    html.P(children="Dataset 2:"),
                    get_ds_dropdown("ds2"),
                ],
            ),
        ]),
        dbc.Row(children=[
            dbc.Col(width=6, children=[
                html.P(children="Class for DS 1"),
                html.Div(id="class-sel-1")
            ]),
            dbc.Col(width=6, children=[
                html.P(children="Class for DS 2"),
                html.Div(id="class-sel-2")
            ]),
        ]),
        dbc.Row(children=[
            dbc.Col(width=6, id="grid1"),
            dbc.Col(width=6, id="grid2"),
        ]),
        dbc.Row(id="grid"),
    ]),
])

files = [[], []]
ct_per = 50


@app.callback(
    Output("grid1", "children"),
    Input("class-1-dd", "value"),
    State("ds1", "value")
)
def class1_body(label, ds):
    '''
    Renders a slider to select ranges of images for a certain dataset + label combination, as well 
    as the body to render the images
    '''
    if not label or not ds or label == "_" or ds == "_":
        files[0] = []
        return ""
    files[0] = list(os.listdir(os.path.join(image_directory, ds, label)))[
        :ABSOLUTE_MAX]
    slider = dcc.Slider(id='class1-slider', min=0,
                        max=len(files[0]) // ct_per, step=1, value=0)
    return [dbc.Row(children=slider), html.P(id="class1-label"), dbc.Row(children=html.Div(id="class1-body"))]


@app.callback(
    Output("class1-label", "children"),
    Output("class1-body", "children"),
    Input("class1-slider", "value"),
    State("ds1", "value"),
    State("class-1-dd", "value")
)
def class1_slider(page, ds1, class1):
    '''
    Renders the actual images, as well as a "[0, 49] / 5000" range indictator 
    '''
    if not ds1 or ds1 == "_" or not class1 or class1 == "_":
        return ""
    left = page*ct_per
    right = (page + 1) * ct_per
    subset = files[0][left: right]
    return f"[{left}, {right - 1}] / {len(files[0])}", \
        html.Div(style={"height": "100vh"}, className="overflow-auto", children=[html.Img(src=f"static/{ds1}/{class1}/{f}", title=f,
                                                                                          style={"max-width": "500px", "border": "1px solid cyan"}) for f in subset])


@app.callback(
    Output("grid2", "children"),
    Input("class-2-dd", "value"),
    State("ds2", "value")
)
def class2_body(label, ds):
    '''
    Renders a slider to select ranges of images for a certain dataset + label combination, as well 
    as the body to render the images
    '''
    if not label or not ds or label == "_" or ds == "_":
        files[1] = []
        return ""
    files[1] = list(os.listdir(os.path.join(image_directory, ds, label)))[
        :ABSOLUTE_MAX]
    slider = dcc.Slider(id='class2-slider', min=0,
                        max=len(files[1]) // ct_per, step=1, value=0)
    return [dbc.Row(children=slider), html.P(id="class2-label"), dbc.Row(children=html.Div(id="class2-body"))]


@app.callback(
    Output("class2-label", "children"),
    Output("class2-body", "children"),
    Input("class2-slider", "value"),
    State("ds2", "value"),
    State("class-2-dd", "value")
)
def class2_slider(page, ds, clas):
    '''
    Renders the actual images, as well as a "[0, 49] / 5000" range indictator 
    '''
    if not ds or ds == "_" or not clas or clas == "_":
        return ""
    left = page*ct_per
    right = (page + 1) * ct_per
    subset = files[1][left: right]
    # return [html.P(children=f) for f in subset]
    return f"[{left}, {right - 1}] / {len(files[1])}", \
        html.Div(style={"height": "100vh"}, className="overflow-auto", children=[html.Img(src=f"static/{ds}/{clas}/{f}", title=f,
                                                                                          style={"max-width": "500px", "border": "1px solid cyan"}) for f in subset])


@app.callback(
    Output("class-sel-1", "children"),
    Input("ds1", "value")
)
def ds1_selected(val):
    '''
    Creates class dropdown when a dataset is selected for column 1
    '''
    if val == "_":
        return dcc.Dropdown(id="class-1-dd", disabled=True)
    default = [{"label": "None", "value": "_"}]
    path = os.path.join(image_directory, val)
    dd = dcc.Dropdown(
        id="class-1-dd",
        value="_",
        options=default + [{
            "label": f,
            "value": f
        } for f in os.listdir(path)
            if os.path.isdir(os.path.join(path, f))],
    )
    return dd


@app.callback(
    Output("class-sel-2", "children"),
    Input("ds2", "value")
)
def ds2_selected(val):
    '''
    Creates class dropdown when a dataset is selected for column 2
    '''
    if val == "_":
        return dcc.Dropdown(id="class-2-dd", disabled=True)
    default = [{"label": "None", "value": "_"}]
    path = os.path.join(image_directory, val)
    dd = dcc.Dropdown(
        id="class-2-dd",
        value="_",
        options=default + [{
            "label": f,
            "value": f
        } for f in os.listdir(path)
            if os.path.isdir(os.path.join(path, f))],
    )
    return dd


if __name__ == "__main__":
    app.run_server(debug=True)
