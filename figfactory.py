import os
import json
import flask
import time
import yaml
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc
import helper.fig_components as fc
import plotly.graph_objects as go
import plotly.subplots as subplots
from dash.html.H1 import H1
from dash.html.P import P
from helper import conf
import numpy as np
from io import BytesIO
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from dash import html, dcc
from app import app
from helper import parse_logs

# required to allow callbacks for non-existent ID's
app.config.suppress_callback_exceptions = True


experiment_directory = "\\\\zgdata.ucsd.edu\\d_sarafian\\zooplankton-pytorch\\experiments"
img_view_dir = "\\\\zgdata.ucsd.edu\\d_sarafian\\datasets/UVP5_processed_sep_2021_depadded"


@app.server.route("/imgview/<path:path><any(png, jpg):extension>")
def serve_image(path, extension):
    '''
    Serves Images from image_directory, accessible through /static route
    '''
    imgname = os.path.basename(path) + extension
    imgpath = os.path.dirname(path)
    return flask.send_from_directory(os.path.join(img_view_dir, imgpath), imgname)


def build_cor(cor_list, clas, index, display_num, bg="bg-success"):
    li = []
    li.append(
        html.Div(children=f"{clas}: ({display_num:0.2f})", className=f"h3 {bg} text-white"))
    for v in cor_list:
        url = "/imgview/" + index[v]
        li.append(html.Img(src=url, className="border border-2 border-info"))
    return li


def build_neg(error_map, index, key_to_num, title=""):
    li = []
    li.append(html.Div(children=title, className=f"h3 bg-warning text-white"))
    for k, v in error_map.items():
        li += build_cor(v, k, index, key_to_num[k], bg="bg-danger")
    return li


@app.callback(
    Output("c1", "children"),
    Output("c2", "children"),
    Output("c3", "children"),
    Input('graph3', 'clickData'),
    State('session', 'data'))
def display_click_data(clickData, session):
    '''
        Displays clickdata in three columns
    '''
    if clickData is None or session is None or session["conf"] is None:
        return "", "", ""
    pt = clickData["points"][0]

    pred, true, ct = pt["x"][8:], pt["y"][:-7], pt["z"]

    corr, ground_miss, pred_miss, index = session["conf"]["corr"], session["conf"]["ground_miss"], session["conf"]["pred_miss"], session["conf"]["index"]
    vert, horiz, axis = session["conf"]["vert"], session["conf"]["horiz"], session["conf"]["axis"]



    c = corr.get(true, [])
    g_miss = ground_miss.get(true, {})
    p_miss = pred_miss.get(true, {})
    gm2 = dict([(k,len(v)) for k,v in g_miss.items()])
    pm2 = dict([(k,len(v)) for k,v in p_miss.items()])

    return build_cor(c, true, index, horiz[0]),  \
        build_neg(g_miss, index, gm2, f"False Negatives (Ground Truth {true})"), \
        build_neg(p_miss, index, pm2, f"False Positives (Mispredicted as {true})")

@app.callback(
    Output("trial-choice-wrap", "children"),
    Input("exp-choice", "value")
)
def exp_callback(choice):
    '''
        Creates the trials dropdown
    '''
    if choice is None:
        return fc.dd_empty("trial-choice")
    return fc.dir_dd(os.path.join(experiment_directory, choice), "trial-choice", True)

def get_experiment_data(experiment, trial_id):
    '''
        Analyzes an experiment's results and creates 'features' to display on the page. 
    '''
    base = os.path.join(experiment_directory, experiment, trial_id)
    class_csv = os.path.join(base, "outputs", "classifications_for_all.csv")
    logs_path = os.path.join(base, "logs", "train.log")
    cache_path = os.path.join(base, "outputs", "cache.json")
    yaml_path = os.path.join(base, "logs", "args.yaml")
    features = {}
    '''
        Conf:
            Fig: the heatmap
            cm: the np confusion matrix
            cm2: the  
    '''
    if os.path.exists(class_csv):
        df = pd.read_csv(class_csv)
        cm, axis, vert, horiz = conf.create_confusion_mat(df)
        cm2 = conf.modify_mat(cm)
        fig = fc.heatmap(cm, cm2, axis, vert, horiz)
        if os.path.exists(cache_path):
            with open(cache_path, "r") as f:
                print("Load from Cache")
                obj = json.load(f)
                corr, ground_miss, pred_miss, index = obj[0], obj[1], obj[2], obj[3]
        else:
            print(f"Creating first time: {cache_path}")
            corr, ground_miss, pred_miss, index = conf.make_dicts(df)
            with open(cache_path, "w") as f:
                json.dump([corr, ground_miss, pred_miss, index], f)

        features["conf"] = {
            "fig": fig, "cm": cm, "cm2": cm2, 
            "axis": axis, "corr": corr, "ground_miss": ground_miss, 
            "pred_miss": pred_miss, "index": index, 
            "vert": vert, "horiz": horiz
        }
    if os.path.exists(class_csv):  
        with open(logs_path, "r") as f:
            logs = "".join(f.readlines())
            train, res = parse_logs.parse_log_file(logs_path)
            features["logs"] = {
                "logs": logs,
                "train": train,
                "res": res
            }
    if os.path.exists(yaml_path):
        with open(yaml_path, "r") as f:
            raw = "".join(f.readlines())
            f.seek(0)
            obj = yaml.load(f)
            features["config"] = {
                "raw": raw,
                "obj": obj
            }
    return features


def create_logs(session):
    train, res = session["logs"]["train"], session["logs"]["res"]
    thead = [html.Thead(html.Tr([html.Th(k) for k in res.keys()]))]
    tbody = [html.Tr([html.Td(v) for v in res.values()])]
    table = dbc.Table(thead + tbody, bordered=True)
    fig = go.Figure()

    fig.add_trace(go.Scatter(x = [int(e["Epoch"]) for e in train], y = [float(e["train loss:"]) for e in train], mode="lines", name="Train Loss"))
    fig.add_trace(go.Scatter(x = [int(e["Epoch"]) for e in train], y = [float(e["val loss:"]) for e in train], mode="lines", name="Validation Loss"))
    fig.update_layout(title_text="Loss Plots")
    fig.update_xaxes(title_text="Epoch")
    fig.update_yaxes(title_text="Loss")

    return dbc.Container(dbc.Row([
        dcc.Graph(figure=fig),
        table
    ]))

def create_config(session):
    return dbc.Container(dbc.Row(dbc.Textarea(id="config", readonly="true", rows=15, value=session["config"]["raw"])))

def create_conf(session):
    return html.Div(children=[
        dbc.Row(dcc.Graph(id="graph3", figure=session["conf"]["fig"])),
        dbc.Row(children=[
            dbc.Col(id="c1"),
            dbc.Col(id="c2"),
            dbc.Col(id="c3")
        ])
    ])

@app.callback(Output("mega-object-wrap", 'children'),
                Input("session", 'data'),
                State("exp-choice", "value"),
                State("trial-choice", "value"))
def on_session_change(session, exp, trial):
    v = [
        ("logs", "Logs", create_logs),
        ("config", "Configs", create_config),
        ("conf", "Confusion Matrix", create_conf)
    ]
    out = []
    out.append(html.H2(f"Experiment: {exp}, Trial: {trial}"))
    for key, name, fn in v:
        out.append(html.H3(name))
        out.append(html.Hr())
        if key not in session:
            out.append(html.P(f"No definition for {name}. "))
        else:
            out.append(fn(session))
    return dbc.Container(fluid=True, children=out)
    
@app.callback(Output("session", 'data'),
                Input("bam", 'n_clicks'),
                State("exp-choice", "value"),
                State("trial-choice", "value"))
def on_click(n_clicks, exp, trial):
    if n_clicks is None or exp is None or trial is None:
        raise PreventUpdate
    # Give a default data dict with 0 clicks if there's no data.
    data = get_experiment_data(exp, trial)
    return data

app.layout = html.Div([
    # dcc.Graph(id="graph"),
    # dcc.Graph(id="graph2", figure=heatmap2()),
    dbc.Container([
        dbc.Row(html.H3("Choose an experiment and Trial")),
        dbc.Row([
            dbc.Col(fc.dir_dd(experiment_directory, "exp-choice", True), width=5),
            dbc.Col(fc.dd_empty("trial-choice"), id="trial-choice-wrap", width=5),
            dbc.Col(dbc.Button(id="bam", children="Refresh", className="w-100", color="secondary"), width=2)
        ]),
    ]),
    dcc.Loading(id="ls-loading-1", 
        children=[
            dcc.Store(id='session')]
    , type="default"),
    html.Div(id="mega-object-wrap")
])


if __name__ == "__main__":
    app.run_server(debug=True)
