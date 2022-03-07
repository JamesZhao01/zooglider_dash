from dash.dependencies import Input, Output
from dash import html, dcc
import os
import json
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
from dash.html.H1 import H1
from dash.html.P import P
from helper import conf

from io import BytesIO
from dash.dependencies import Input, Output, State
from dash import html, dcc
from app import app
import flask

# required to allow callbacks for non-existent ID's
app.config.suppress_callback_exceptions = True


df = px.data.medals_wide(indexed=True)


base = "\\\\zgdata.ucsd.edu\\d_sarafian\zooplankton-pytorch/experiments/resnet152_pretrain_padding_12_21/trial_8"
img_view_dir = "\\\\zgdata.ucsd.edu\\d_sarafian/datasets/UVP5_processed_sep_2021_depadded"
df = pd.read_csv(os.path.join(base, "outputs", "classifications_for_all.csv"))
cm, axis = conf.create_confusion_mat(df)
if os.path.exists("cache.json"):
    with open("cache.json", "r") as f:
        print("Load from Cache")
        obj = json.load(f)
        corr, ground_miss, pred_miss, index = obj[0], obj[1], obj[2], obj[3]
else:
    print("Creating first time")
    corr, ground_miss, pred_miss, index = conf.make_dicts(df)
    with open("cache.json", "w") as f:
        json.dump([corr, ground_miss, pred_miss, index], f)


@app.server.route("/imgview/<path:path><any(png, jpg):extension>")
def serve_image(path, extension):
    '''
    Serves Images from image_directory, accessible through /static route
    '''
    imgname = os.path.basename(path) + extension
    imgpath = os.path.dirname(path)
    return flask.send_from_directory(os.path.join(img_view_dir, imgpath), imgname)


def heatmap():
    # use go.Image, with secondary axes?
    z = [[.1, .3, .5, .7, .9],
         [1, .8, .6, .4, .2],
         [.2, 0, .5, .7, .9],
         [.9, .8, .4, .2, 0],
         [.3, .4, .5, .7, 1]]
    z = cm
    colscal = [[0.0, "rgb(255,0,0)"],
               [0.1, "rgb(255,255,255)"],
               [1.0, "rgb(0,255,0)"]]
    fig = px.imshow(z, text_auto=True,
                    color_continuous_scale=colscal,
                    x=axis, y=axis, height=1200)
    fig.update_xaxes(fixedrange=True)
    fig.update_xaxes(title="Ground Truth")
    fig.update_yaxes(title="Predicted Label")

    fig.update_traces(
        text=z, texttemplate="%{text}"
    )

    return fig


def build_cor(cor_list, clas, bg="bg-success"):
    li = []
    li.append(
        html.Div(children=f"{clas}: ({len(cor_list)})", className=f"h3 {bg} text-white"))
    for v in cor_list:
        url = "/imgview/" + index[v]
        li.append(html.Img(src=url, style={
                  "max-width": "25%"}, className="border border-2 border-info"))
    return li


def build_neg(error_map, title=""):
    li = []
    li.append(html.Div(children=title, className=f"h3 bg-warning text-white"))
    for k, v in error_map.items():
        li += build_cor(v, k, bg="bg-danger")
    return li


@app.callback(
    Output("c1", "children"),
    Output("c2", "children"),
    Output("c3", "children"),
    Input('graph3', 'clickData'))
def display_click_data(clickData):
    if clickData is None:
        return "", "", ""
    pt = clickData["points"][0]
    true, pred, ct = pt["x"], pt["y"], pt["z"]
    c = corr.get(true, [])
    g_miss = ground_miss.get(true, [])
    p_miss = pred_miss.get(pred, [])
    d = {"corr": c, "g_miss": g_miss, "p_miss": p_miss}
    return build_cor(c, true),  \
        build_neg(g_miss, f"False Negatives (Ground Truth {true})"), \
        build_neg(p_miss, f"False Positives (Mispredicted as {true})")


app.layout = html.Div([
    # dcc.Graph(id="graph"),
    # dcc.Graph(id="graph2", figure=heatmap2()),
    dcc.Graph(id="graph3", figure=heatmap()),
    html.Div(id="click-data"),
    dbc.Container(fluid=True, children=[
        dbc.Row(children=[
            dbc.Col(id="c1"),
            dbc.Col(id="c2"),
            dbc.Col(id="c3")
        ])
    ])
])


if __name__ == "__main__":
    app.run_server(debug=True)
