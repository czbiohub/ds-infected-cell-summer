from __future__ import generator_stop
from typing import Optional

import dash
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate
import dash_core_components as dcc
import dash_html_components as html

import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import os
from collections import Counter
from plotly.subplots import make_subplots
from pathlib import Path
import argparse

from heatmap import Heatmap

fig = go.Figure()

def dash_heatmaps(output_path, pickle_path):
    heatmap = Heatmap(output_path, pickle_path)
    app = dash.Dash(__name__)

    class Ids:
        pass
    
    app.layout = html.Div(
        children = [
            html.Div(children=[
                html.Label('Virus 1'),
                dcc.Dropdown(
                    id="selected-vir",
                    value="Wang_229E",
                    options=[
                        {'label': 'Dengue', 'value': 'DENV'},
                        {'label': 'Enterovirus', 'value': 'EV'},
                        {'label': 'Hepatitis A', 'value': 'HAV'},
                        {'label': 'Hepatitis C', 'value': 'HCV'},
                        {'label': 'Rhinovirus', 'value': 'RV'},
                        {'label': 'Human Coronavirus 229E', 'value': 'Wang_229E'},
                        {'label': 'Human Coronavirus OC43', 'value': 'Wang_OC43'},
                        {'label': 'SARS-CoV-2', 'value': 'Wang_SARS-CoV2'},
                    ],
                ),
            ],
        ),
                    html.Div(children=[
                html.Label('Virus 2'),
                dcc.Dropdown(
                    id="selected-vir1",
                    value="Wang_OC43",
                    options=[
                        {'label': 'Dengue', 'value': 'DENV'},
                        {'label': 'Enterovirus', 'value': 'EV'},
                        {'label': 'Hepatitis A', 'value': 'HAV'},
                        {'label': 'Hepatitis C', 'value': 'HCV'},
                        {'label': 'Rhinovirus', 'value': 'RV'},
                        {'label': 'Human Coronavirus 229E', 'value': 'Wang_229E'},
                        {'label': 'Human Coronavirus OC43', 'value': 'Wang_OC43'},
                        {'label': 'SARS-CoV-2', 'value': 'Wang_SARS-CoV2'},
                    ],
                ),
            ],
        ),
            html.Div(
                className="graphContainer",
                children=[
                    dcc.Graph(className="graph", id="heatmap"),
            ],
            )
        ],
        )

    @app.callback(
        Output("heatmap","figure"),
        Input("selected-vir","value"),
        Input("selected-vir1","value")
    )

    def update_figure(vir1, vir2):
        final_df, a, combined_df = heatmap.final([vir1, vir2], heatmap.tot_vir)
        if not final_df.empty:
                fig = px.imshow(final_df, labels=dict(x="Viruses", y="Genes", color="Significance (-log[pos score])"),
                y=combined_df['Shared_Genes'][a], x = [heatmap.abbrev[vir1], heatmap.abbrev[vir2]], title=combined_df['Original Name_x'][a])
                return fig
        else:
            data = [go.Heatmap( x=[], y=[], z=[])]
            fig = go.Figure(data=data)

            fig.update_layout(
                title = 'No data to display'
            )
            return fig

    return app

def prod(output_path, pickle_path):
    app = dash_heatmaps(output_path, pickle_path)
    return app.server

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("output_path", type=str)
    parser.add_argument("pickle_path", type=str)
    args = parser.parse_args()

    app = dash_heatmaps(args.output_path, args.pickle_path)
    app.run_server(debug=True, port=8082)