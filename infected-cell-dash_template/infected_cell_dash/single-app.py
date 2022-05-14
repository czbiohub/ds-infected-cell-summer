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

import single_analysis

fig = go.Figure()

def dash_single_analysis(data_path, requests_pathname_prefix="/"):
    app = dash.Dash(__name__, requests_pathname_prefix=requests_pathname_prefix)

    class Ids:
        pass

    app.layout = html.Div(
        children=[
            html.Link(
                href="https://fonts.googleapis.com/css?family=Lato:400",
                rel="stylesheet",
            ),
            html.Div(
                className="dropdowns",
                children=[
                    html.Div(
                        className="dropdown",
                        children=[
                            html.Label(children="Virus"),
                            dcc.Dropdown(
                                id="vir",
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
                                value="DENV",
                                clearable=False,
                            ),
                        ],
                    ),
                    html.Div(
                        className="dropdown",
                        children=[
                            html.Label(children="Analysis Metric"),
                            dcc.Dropdown(
                                id="metric",
                                value="-log(pos|score)",
                                options=[
                                    {'label': '-log of Positive Score', 'value': '-log(pos|score)'},
                                    {'label': 'Positive Log Fold Change', 'value': 'pos|lfc'},
                                ],
                                clearable=False,
                            ),
                        ],
                    ),

                    html.Div(
                        className="dropdown",
                        children=[
                            html.Label(children="Hover Metrics"),
                            dcc.Dropdown(
                                id="hover_metrics",
                                value=['pos|rank'],
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
                                clearable=False,
                                multi = True
                            ),
                        ],
                    ),

                    html.Div(
                        className="dropdown",
                        children=[
                            html.Label(children="Search for Genes"),
                            dcc.Dropdown(
                                id="search_genes",
                                value=['MAGT1'],
                                placeholder="",
                                multi = True
                            ),
                        ],
                    ),

                     html.Div(
                        className="empty_dropdown",
                    ),

                    html.Div(className="dropdown",
                    children=[
                    html.Label(children= "# of Significant Genes"),
                    dcc.Input(
                        id='sig_num',
                        value=15,
                        type='number',
                        min=0,
                        max=2000,
                        step=1)
                    ],
                ),
                ],
            ),

            html.Div(
                id = "graph_positioning"
            ),
        ],
    )

    @app.callback(
        Output("graph_positioning", "className"),
        Input("sig_num", "value")
    )

    def update_className(sig_num):
        if sig_num < 30:
            return "graphContainer"
        else:
            return "graphStack"

    #creating the significance scatter, shows significance of each gene against its alphabetical position
    @app.callback(
        Output("graph_positioning","children"),
        Input("vir","value"),
        Input("metric", "value"),
        Input("search_genes", "value"),
        Input("sig_num", "value"),
        Input("hover_metrics", "value")
    )

    def update_figure(vir, metric, input_genes, sig_num, hover_metrics):
        fig1 = single_analysis.single_plot(data_path, sig_num, metric, input_genes, hover_metrics, vir)
        fig2 = single_analysis.sig_rank(data_path, sig_num, metric, input_genes, hover_metrics, vir)
        return [dcc.Graph(figure = fig1), dcc.Graph(figure = fig2)]

    #making call back so that user can search by gene
    @app.callback(
        Output("search_genes", "options"),
        Input("vir", "value")
    )
    def update_genes_dropdown(vir):
        f1 = single_analysis.file(vir, data_path)
        df1 = pd.read_csv(f1, sep = '\t')
        df1 = df1.rename(columns={'id':'Genes'})
        return [
        {
        "label": df1['Genes'][idx],
        "value": df1['Genes'][idx],
        } for idx in range(len(df1['Genes']))
        ]

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