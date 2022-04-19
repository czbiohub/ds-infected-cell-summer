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
import utils 

from single_analysis import SingleAnalysis

fig = go.Figure()

def dash_single_analysis(data_path, requests_pathname_prefix="/"):
    virus_list = utils.list_gene_summary_files(data_path)

    single_analysis = SingleAnalysis(data_path)
    app = dash.Dash(__name__, requests_pathname_prefix=requests_pathname_prefix)

    app.layout = html.Div(
        children = [
            html.Div(children=[
                html.Label('Virus'),
                dcc.Dropdown(
                    id="selected-vir",
                    value=virus_list[0]["value"],
                    options=virus_list,
                ),
            ],
        ),
            html.Div(
                className="graphContainer",
                children=[
                    dcc.Graph(className="graph", id="significance-scatter"),
                ],
            )
        ],
    )

    # Update significance scatterplot based on selected virus
    @app.callback(
        Output("significance-scatter", "figure"),
        Input("selected-vir", "value"),
    )
    def update_figure(virus_path):
        virus_name = utils.getFileNameWoExt(virus_path)
        fig = single_analysis.single_plot(virus_path, virus_name)
        return fig

    return app

def prod(data_path, requests_pathname_prefix="/"):
    app = dash_single_analysis(data_path, requests_pathname_prefix)
    return app.server

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("data_path", type=str)
    args = parser.parse_args()

    app = dash_single_analysis(args.data_path)
    app.run_server(debug=True, port=8083)