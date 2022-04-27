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
import name_dict

fig = go.Figure()

def dash_single_analysis(data_path, requests_pathname_prefix="/"):
    single_analysis = SingleAnalysis(data_path)
    app = dash.Dash(__name__, requests_pathname_prefix=requests_pathname_prefix)

    class Ids:
        pass

    app.layout = html.Div(
        children = [
            html.Div(children=[
                html.Label('Virus'),
                dcc.Dropdown(
                    id="vir",
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
            html.Div(children=[
                html.Label('Analysis Metric'),
                dcc.Dropdown(
                    id="metric",
                    value="-log(pos|score)",
                    options=[
                        {'label': 'Negative Score', 'value': 'neg|score'},
                        {'label': 'Positive Score', 'value': 'pos|score'},
                        {'label': '-log of Positive Score', 'value': '-log(pos|score)'},
                        {'label': 'Negative P-Vaue', 'value': 'neg|p-value'},
                        {'label': 'Positive P-Value', 'value': 'pos|p-value'},
                        {'label': 'Negative False Discovery Rate', 'value': 'neg|fdr'},
                        {'label': 'Positive False Discovery Rate', 'value': 'pos|fdr'},
                        {'label': 'Negative Rank', 'value': 'neg|rank'},
                        {'label': 'Positive Rank', 'value': 'pos|rank'},
                        {'label': 'Negative Good sgRNA', 'value': 'neg|goodsgrna'},
                        {'label': 'Positive Good sgRNA', 'value': 'pos|goodsgrna'},
                        {'label': 'Negative Log Fold Change', 'value': 'neg|lfc'},
                        {'label': 'Positive Log Fold Change', 'value': 'pos|lfc'},
                    ],
                ),
            ],
        ),
            html.Div(children=[
                html.Label('Search for Genes'),
                dcc.Dropdown(
                    id="input_genes",
                    value="[]",
                    options=[
                    ],
                    multi = True
                ),
            ],
        ),
            html.Div(children=[
                html.Label('# of Significant Genes'),
                dcc.Dropdown(
                    id="sig_num",
                    value="30",
                    options=[
                    ],
                ),
            ],
        ),
            html.Div(children=[
                html.Label('Hover Metrics'),
                dcc.Dropdown(
                    id="hover_metrics",
                    value="pos|rank",
                    options=[
                        {'label': 'Negative Score', 'value': 'neg|score'},
                        {'label': 'Positive Score', 'value': 'pos|score'},
                        {'label': '-log of Positive Score', 'value': '-log(pos|score)'},
                        {'label': 'Negative P-Vaue', 'value': 'neg|p-value'},
                        {'label': 'Positive P-Value', 'value': 'pos|p-value'},
                        {'label': 'Negative False Discovery Rate', 'value': 'neg|fdr'},
                        {'label': 'Positive False Discovery Rate', 'value': 'pos|fdr'},
                        {'label': 'Negative Rank', 'value': 'neg|rank'},
                        {'label': 'Positive Rank', 'value': 'pos|rank'},
                        {'label': 'Negative Good sgRNA', 'value': 'neg|goodsgrna'},
                        {'label': 'Positive Good sgRNA', 'value': 'pos|goodsgrna'},
                        {'label': 'Negative Log Fold Change', 'value': 'neg|lfc'},
                        {'label': 'Positive Log Fold Change', 'value': 'pos|lfc'},
                    ],
                    multi = True
                ),
            ],
        ),

            html.Div(
                className="graphContainer",
                children=[
                    dcc.Graph(className="graph", id="significance-scatter"),
                ],
            ),
        ],
    )

    @app.callback(
        Output("significance-scatter","figure"),
        Input("vir","value"),
        Input("metric", "value"),
        Input("input_genes", "value"),
        Input("sig_num", "value"),
        Input("hover_metrics", "value")
    )

    def update_figure(vir1, metric, input_genes, sig_num, hover_metrics):
        fig = SingleAnalysis.single_plot(single_analysis, sig_num, metric, input_genes, hover_metrics, vir1)
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
    app.run_server(debug=True, port=8089) 