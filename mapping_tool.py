import os
import flask
import imagesize
import dash_bootstrap_components as dbc

from dash.dependencies import Input, Output, State, MATCH
from dash import html, dcc
from appsrc import app, config

from components.mappingcomponents import create_ds_type_dd, create_do_sort_dd, create_maxsize_in, create_ds_dd, create_class_dd, create_grid, create_images, default_dd

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
image_directory = config["datasets"]

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


def create_mega_column(idx):
    ds_type_label = f"Dataset {idx} type:"
    # the type of ds to create (UVP, ZG, ZS)
    ds_type_id = {"type": "ds_type", "index": idx}

    ds_size_label = f"Max num of items: "
    # amount of elements to load
    ds_size_id = {"type": "ds_size", "index": idx}

    ds_sel_wrapper_id = {"type": "ds_select_wrapper", "index": idx}
    # wrapper for actual dataset
    ds_sel_label = f"Dataset {idx}: "

    # wrapper for classes
    class_wrapper_id = {"type": "class_wrapper", "index": idx}
    class_label = f"Class {idx}: "

    ds_do_sort_label = f"Sort by Height:"
    ds_do_sort_id = {"type": "do_sort", "index": idx}

    grid_id = {"type": "grid", "index": idx}  # id for the grid

    return dbc.Col(width=4, className="border border-success", children=[
        dbc.Row(children=[
            dbc.Col(width=4, children=[  # ds type (one time)
                html.P(children=ds_type_label),
                create_ds_type_dd(ds_type_id),
            ]),
            dbc.Col(width=4, children=[  # ds size (one time)
                html.P(children=ds_size_label),
                create_maxsize_in(ds_size_id),
            ]),
            dbc.Col(width=4, children=[
                html.P(children=ds_do_sort_label),
                create_do_sort_dd(ds_do_sort_id),  # do sort (one time)
            ]),
        ]),
        dbc.Row(children=[
            dbc.Col(width=6, children=[
                html.P(children=ds_sel_label),
                html.Div(id=ds_sel_wrapper_id, children=[
                    default_dd({"type": "ds_select", "index": int(idx)})
                ])
            ]),
            dbc.Col(width=6, children=[
                html.P(children=class_label),
                html.Div(id=class_wrapper_id, children=[
                    default_dd({"type": "class", "index": int(idx)})
                ]),
            ]),
        ]),
        html.Div(id=grid_id)
    ])


app.layout = html.Div(children=[
    dbc.Container(fluid=True, children=[
        html.H3(children=f"Static File Serving Directory (Hard Coded):"),
        html.P(children=image_directory),
        dbc.Row(children=[create_mega_column(i) for i in range(3)]),
        html.Div(className="d-none",  # creates dummy items
                 children=[html.Div(id={"type": "dummy", "index": a}, children=str(a)) for a in range(3)])
    ]),
])


@app.callback(
    Output({"type": "ds_select_wrapper", "index": MATCH}, "children"),
    Input({"type": "ds_type", "index": MATCH}, "value"),
    State({"type": "dummy", "index": MATCH}, "children"),


)
def callback_ds_type_chosen(ds_type, idx):
    ds_select_id = {"type": "ds_select", "index": int(idx)}
    return create_ds_dd(ds_select_id, ds_type)


@app.callback(
    Output({"type": "class_wrapper", "index": MATCH}, "children"),
    Input({"type": "ds_select", "index": MATCH}, "value"),
    State({"type": "dummy", "index": MATCH}, "children"),
)
def callback_ds_chosen(ds, idx):
    class_id = {"type": "class", "index": int(idx)}
    return create_class_dd(class_id, ds)


@app.callback(
    Output({"type": "grid", "index": MATCH}, "children"),
    Input({"type": "ds_select", "index": MATCH}, "value"),
    Input({"type": "class", "index": MATCH}, "value"),
    Input({"type": "ds_size", "index": MATCH}, "value"),
    State({"type": "dummy", "index": MATCH}, "children")
)
def refresh_grid(ds, classs, size, idx):
    return create_grid(idx, ds, classs, size)


@app.callback(
    Output({"type": "images", "index": MATCH}, "children"),
    Input({"type": "do_sort", "index": MATCH}, "value"),
    Input({"type": "slider", "index": MATCH}, "value"),
    Input({"type": "grid", "index": MATCH}, "children"),
    State({"type": "ds_select", "index": MATCH}, "value"),
    State({"type": "class", "index": MATCH}, "value"),
    State({"type": "dummy", "index": MATCH}, "children")
)
def refresh_images(do_sort, page, _, ds, classs, idx):
    return create_images(idx, ds, classs, page, do_sort)


if __name__ == "__main__":
    app.run_server(debug=True)
