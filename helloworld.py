# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
import flask
import os

import plotly.express as px
# import pandas as pd

from dash import html, dcc

app = dash.Dash(__name__)

app.layout = html.Div(
    style={'backgroundColor': "red"},
    children=[
        html.Img(src="/static/a2.png"),
        html.Img(src="/static/special/a1.png")
    ])

image_directory = 'C:/Users/James/Desktop/quicklocate/2022/sampleimgs'
static_image_route = '/static/'


@app.server.route('/static/<path:path>.png')
def serve_image(path):
    imgname = os.path.basename(path) + ".png"
    imgpath = os.path.dirname(path)
    return flask.send_from_directory(os.path.join(image_directory, imgpath), imgname)


if __name__ == '__main__':
    app.run_server(debug=True)
