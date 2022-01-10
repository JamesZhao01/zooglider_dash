from dash import dcc
from utils.path_utils import has_classification
import os


def ds_dd(path):
    try:
        return dcc.Dropdown(
            id="ds",
            options=[{"label": "None", "value": "_"}] + [{"label": f, "value": os.path.join(
                path, "datasets", f)} for f in os.listdir(os.path.join(path, "datasets")) if os.path.isdir(os.path.join(path, "datasets", f))],
            value="_"
        )
    except:
        return dcc.Dropdown(
            id="ds",
            disabled=True
        )


def exp_dd(path):
    try:
        truepath = os.path.join(path, "zooplankton-pytorch", "experiments")
        li = []
        for exp in os.listdir(truepath):
            exp_path = os.path.join(truepath, exp)
            if os.path.isdir(exp_path):
                for trial in os.listdir(exp_path):
                    if not has_classification(os.path.join(exp_path, trial)):
                        break
                    li.append((f"{exp[:20]} ({trial})",
                               os.path.join(exp_path, trial)))
        return dcc.Dropdown(
            id='exp',
            options=[{"label": "None", "value": "_"}] +
            [{"label": lab, "value": val} for lab, val in li],
            value="_"
        )
    except:
        return dcc.Dropdown(
            id="exp",
            disabled=True
        )
