import dash
import json
import dash_bootstrap_components as dbc

# meta_tags are required for the app layout to be mobile responsive
# external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
external_stylesheets = []

# bootstrap cdn
external_stylesheets += [dbc.themes.BOOTSTRAP]
external_scripts = ["https://cdn.plot.ly/plotly-2.8.3.min.js"]

# app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app = dash.Dash(__name__, suppress_callback_exceptions=True,
                meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0'}],
                external_stylesheets=external_stylesheets,
                external_scripts=external_scripts
                )
app.title = "Zooglider"

# required to allow callbacks for non-existent ID's, added by James
# app.config.suppress_callback_exceptions = True

server = app.server
with open("config.json", "r") as f:
    config = json.load(f)
