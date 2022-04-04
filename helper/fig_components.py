import plotly.express as px
import os
from dash import dcc
from app import config
from natsort import natsorted

def dd_empty(id):
    return dcc.Dropdown(
            id=id,
            disabled=True
        )

def dir_dd(path, id, onlyDir = True):
    if len(os.listdir(path)) == 0:
        return dcc.Dropdown(
            id=id,
            disabled=True
        )
    else:
        li = [f for f in os.listdir(
            path) if not f.startswith(".") and (True if not onlyDir else os.path.isdir(os.path.join(path, f)))]
        return dcc.Dropdown(
            id=id,
            options= [{"label": f, "value": f} for f in natsorted(li)]
        )

def heatmap(cm, cm2, axis, vert, horiz):
    # use go.Image, with secondary axes?
    z = cm2
    colscal = [[0.0, "rgb(255,0,0)"],
               [1/6, "rgb(255,255,255)"],
               [1.0, "rgb(0,200,0)"]]
    vert = [f"{a} ({b:0.2f})"for (a, b) in zip(axis, vert)]
    horiz = [f"({a:0.2f}) {b}"for (a, b) in zip(horiz, axis)]
    fig = px.imshow(z, text_auto=True,
                    color_continuous_scale=colscal,
                    x=horiz, y=vert, height=1200)
    fig.update_xaxes(fixedrange=True)
    fig.update_xaxes(title="Predicted Label", showline=True, linewidth=1, linecolor='black', mirror=True)
    fig.update_yaxes(title="Ground Truth", showline=True, linewidth=1, linecolor='black', mirror=True)

    fig.update_traces(
        text=cm, texttemplate="%{text}"
    )

    return fig
