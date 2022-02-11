from __future__ import generator_stop
from typing import Optional
from black import out

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

from single_analysis import SingleAnalysis

fig = go.Figure()

def dash_single_analysis(output_path):
    single_analysis = SingleAnalysis(output_path)
    app = dash.Dash(__name__)

    class Ids:
        pass

    app.layout = html.Div(
        children = [
            html.Div(children=[
                html.Label('Virus 1'),
                dcc.Dropdown(
                    id="selected-vir",
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
                    dcc.Graph(className="graph", id="my_scatter"),
            ],
            )
        ],
        )

    @app.callback(
        Output("my_scatter","figure"),
        Input("selected-vir","value"),
    )

    def update_figure(vir1):
        fig = single_analysis.single_plot(vir1, single_analysis.abbrev)
        return fig

    return app

def prod(output_path):
    app = dash_single_analysis(output_path)
    return app.server

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("output_path", type=str)
    args = parser.parse_args()

    app = dash_single_analysis(args.output_path)
    app.run_server(debug=True, port=8083)