import dash
from dash.dependencies import Input, Output
from dash import html, dcc
from appsrc import app

import os

def ds_dropdown(path):
    try:
        return dcc.Dropdown(
            id="ds",
            options = [{"label": "None", "value": "_"}] + [{"label": f, "value": os.path.join(path, "datasets", f)} for f in os.listdir(os.path.join(path, "datasets"))],
            value = "_"
        )
    except:
        return dcc.Dropdown(
            id="ds",
            disabled=True
        )

def exp_dropdown(path):
    try:
        truepath = os.path.join(path, "zooplankton-pytorch", "experiments")
        li = []
        print(truepath)
        for exp in os.listdir(truepath):
            exp_path = os.path.join(truepath, exp)
            for trial in os.listdir(exp_path):
                li.append((f"{exp[:12]}({trial})", os.path.join(exp_path, trial)))
        print(li)
        return dcc.Dropdown(
            id='exp',
            options = [{"label": "None", "value": "_"}] + [{"label": lab, "value": val} for lab, val in li],
            value = "_"
        )
    except:
        return dcc.Dropdown(
            id="exp",
            disabled=True
        )
    
    html.Div(children=str(os.listdir("\\\\zgdata.ucsd.edu\d_sarafian")))