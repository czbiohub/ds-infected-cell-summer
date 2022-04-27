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
from app import dash_heatmaps

from dual_analysis import DualAnalysis

fig = go.Figure()

def dash_dual_analysis(output_path, requests_pathname_prefix="/"):
    dual_analysis = DualAnalysis(output_path)
    app = dash.Dash(__name__, requests_pathname_prefix=requests_pathname_prefix)
    
    class Ids:
        pass

    app.layout = html.Div(
        children = [
            html.Div(children=[
                html.Label('Virus 1'),
                dcc.Dropdown(
                    id="selected-vir",
                    value="HAV",
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
                    value="DENV",
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
                    dcc.Graph(className="graph", id="my_compare"),
            ],
            )
        ],
        )

    @app.callback(
        Output("my_compare","figure"),
        Input("selected-vir","value"),
        Input("selected-vir1","value")
    )

    def update_figure(vir1, vir2):
        df1 = dual_analysis.comparo(vir1, vir2, dual_analysis.tot_vir)
        fig = px.scatter(df1, x='col_vir1', y='col_vir2', labels={
        'col_vir1': dual_analysis.abbrev[vir1],
        'col_vir2': dual_analysis.abbrev[vir2]},
        title = 'Comparing Significance of Genes for ' + dual_analysis.abbrev[vir1] +  ' and ' + dual_analysis.abbrev[vir2],
        hover_name="Genes")

        fig.add_trace(go.Scatter(
            x= df1['col_vir1'],
            y=df1['col_vir2'],
            mode="text",
            name="Gene Names",
            text=df1['Genes'],
            textposition="top center"
        ))

        return fig

    return app

def prod(output_path, requests_pathname_prefix="/"):
    app = dash_dual_analysis(output_path, requests_pathname_prefix)
    return app.server

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("output_path", type=str)
    args = parser.parse_args()

    app = dash_dual_analysis(args.output_path)
    app.run_server(debug=True, port=8084)