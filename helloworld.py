# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash

import plotly.express as px
# import pandas as pd

from dash import html, dcc

app = dash.Dash(__name__)

app.layout = html.Div(
    style={'backgroundColor': "red"},
    children="HelloDash")

if __name__ == '__main__':
    app.run_server(debug=True)