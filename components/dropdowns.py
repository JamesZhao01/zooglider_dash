from dash import dcc
from utils.path_utils import has_classification
import os

from appsrc import config


# def dataset_dropdown(path):
#     try:
#         return dcc.Dropdown(
#             id="dataset_dropdown",
#             options=[{"label": "None", "value": "_"}] + [{"label": f, "value": os.path.join(
#                 path, "datasets", f)} for f in os.listdir(os.path.join(path, "datasets")) if os.path.isdir(os.path.join(path, "datasets", f))],
#             value="_"
#         )
#     except:
#         return dcc.Dropdown(
#             id="ds",
#             disabled=True
#         )


def experiment_dropdown(id):
    try:
        exp_dir = config["experiments"]
        li = [(exp, os.path.join(exp_dir, exp)) for exp in os.listdir(
            exp_dir) if os.path.isdir(os.path.join(exp_dir, exp))]
        return dcc.Dropdown(
            id=id,
            options=[{"label": "None", "value": "None"}] +
            [{"label": lab, "value": val} for lab, val in li],
            value="None"
        )
    except:
        return dcc.Dropdown(
            id=id,
            disabled=True
        )


def trial_dropdown(id, experiment_dir):
    try:
        li = [(trial, os.path.join(experiment_dir, trial)) for trial in os.listdir(
            experiment_dir) if os.path.isdir(os.path.join(experiment_dir, trial))]
        return dcc.Dropdown(
            id=id,
            options=[{"label": "None", "value": "None"}] +
            [{"label": lab, "value": val} for lab, val in li],
            value="None"
        )
    except:
        return dcc.Dropdown(
            id=id,
            disabled=True
        )
