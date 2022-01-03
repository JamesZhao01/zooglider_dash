import dash
from dash.dependencies import Input, Output
from dash import html, dcc
from appsrc import app

@app.callback(
    Output('dd-output-container', 'children'),
    Input('demo-dropdown', 'value')
)
def update_output(value):
    print(value)
    return [html.Span(children = f"V:{c}", style={"color": "cyan"}) for c in value]

def getdropdown():
    return html.Div(children = [dcc.Dropdown(
        id=f'demo-dropdown',
        options=[
            {'label': 'New York City', 'value': 'NYC'},
            {'label': 'Montreal', 'value': 'MTL'},
            {'label': 'San Francisco', 'value': 'SF'}
        ],
        value='NYC'
    ),
    html.Div(id = "dd-output-container")
    ])