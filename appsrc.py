import dash
import json
import dash_bootstrap_components as dbc

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], external_scripts=[
                "https://cdn.plot.ly/plotly-2.8.3.min.js"])

with open("config.json", "r") as f:
    config = json.load(f)
