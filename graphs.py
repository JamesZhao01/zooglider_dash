from re import M
from dash import callback_context
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from dash.dependencies import Input, Output, State
from dash import html, dcc
from app import app
import pandas as pd
# required to allow callbacks for non-existent ID's
app.config.suppress_callback_exceptions = True

df = pd.read_csv("./assets/all_deployments_summary.csv")
dep_df = pd.read_csv(
    "./assets/2015_11_Scripps_Canyon_2_engineering_summary.csv")
# print(df.columns)
# print(len(df))


def graph():
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.04, specs=[
                        [{"secondary_y": True}], [{}]],
                        subplot_titles=["Images Acquired per Deployment", "Average ROI per frame"])

    fig.add_trace(
        go.Bar(x=df['Unnamed: 0'], y=df['frame_count'],
               name="Frames", offsetgroup=1),
        row=1, col=1, secondary_y=False)

    fig.add_trace(
        go.Bar(x=df['Unnamed: 0'], y=df['roi_count'],
               name="ROIs", offsetgroup=2),
        row=1, col=1, secondary_y=True)
    tr1 = go.Scatter(x=df['Unnamed: 0'], y=df['roi_count'] /
                     df['frame_count'], mode='lines+markers', name='ROI/FRAME',
                     )
    fig.add_trace(tr1, row=2, col=1)

    fig.update_layout(height=1200)
    fig.update_xaxes(title_text="Deployment Name",  row=2, col=1)
    fig.update_yaxes(title_text="ROI / Frame",  row=2, col=1)
    fig.update_yaxes(title_text="# Frames",  row=1, col=1, secondary_y=False)
    fig.update_yaxes(title_text="# ROIS", row=1, col=1, secondary_y=True)

    return fig


def graph2(show=["legendonly"] * 23):
    fig = make_subplots(rows=3, cols=1, shared_xaxes=True, vertical_spacing=0.04, specs=[
                        [{"secondary_y": True}], [{}], [{}]],
                        subplot_titles=["Images Acquired per Dive",
                        "Average ROI per frame for HEHEXD", "Missing XMP values in HEHEXD"])

    fig.add_trace(
        go.Bar(x=dep_df['Dive Number'], y=dep_df['Frame Count'],
               name="Frames", offsetgroup=1),
        row=1, col=1, secondary_y=False,
    )

    fig.add_trace(
        go.Bar(x=dep_df['Dive Number'], y=dep_df['ROI count'],
               name="ROIs", offsetgroup=2),
        row=1, col=1, secondary_y=True
    )

    tr_roi_per_frame = go.Scatter(
        x=dep_df['Dive Number'],
        y=dep_df['ROI count'] /
        dep_df['Frame Count'],
        mode='lines+markers', name='ROI/FRAME'
    )
    fig.add_trace(tr_roi_per_frame, row=2, col=1, )
    xmp_keys = ['Frames missing Pressure', 'ROIs without frames', 'Sv_200kHz_vres_1m', 'Sv_1000kHz_vres_1m', 'Sv_Delta_vres_1m', 'Pressure_dbar', 'ECD_mm', 'Latitude', 'Longitude',
                'Pressure_dbar', 'Local_Time', 'Local_Date', 'Feret_Diam_mm', 'ECD_mm', 'Major_Axis_Len_mm', 'Minor_Axis_Len_mm', 'Temp_deg_C', 'Salinity', 'Rho_kg_m-3', 'Fluor', 'Pitch_deg', 'Roll_deg']

    for x, t in zip(xmp_keys, show):
        tr_missing = go.Scatter(
            x=dep_df['Dive Number'],
            y=dep_df[x],
            mode='lines+markers', name=x, visible=t
        )
        fig.add_trace(tr_missing, row=3, col=1)

    fig.update_layout(height=1000)
    fig.update_xaxes(title_text="Dive Number",  row=3, col=1)
    fig.update_yaxes(title_text="# of Missing Values",  row=3, col=1)
    fig.update_yaxes(title_text="ROI / Frame",  row=2, col=1)
    fig.update_yaxes(title_text="# Frames",  row=1, col=1, secondary_y=False)
    fig.update_yaxes(title_text="# ROIS", row=1, col=1, secondary_y=True)

    return fig


@app.callback(
    Output("graph2", "figure"),
    Input("hide", "n_clicks"),
    Input("show", "n_clicks"),
)
def handle(hide, show):
    changed_id = [p['prop_id'] for p in callback_context.triggered][0]
    if "hide" in changed_id:
        return graph2(["legendonly"] * 23)
    else:
        return graph2([None] * 23)


app.layout = html.Div([
    html.P("Hello World!"),
    dcc.Graph(id="graph", figure=graph()),
    dcc.Graph(id="graph2", figure=graph2()),
    html.Button(id="show", children="SHOW"), html.Button(
        id="hide", children="HIDE")

])


if __name__ == "__main__":
    app.run_server(debug=True)
