from __future__ import generator_stop
from turtle import title
from typing import Optional

import dash
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate
from dash import dcc
from dash import html

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
                href="https://fonts.googleapis.com/css?family=Inter:400",
                rel="stylesheet",
            ),
            html.Div(
                className="dropdowns",
                children=[
                    html.Div(
                        className="dropdown",
                        children=[
                            html.Label(children="Virus (Alphabetically)"),
                            dcc.Dropdown(
                                id="vir",
                                options=[
                                    {'label': 'Dengue Virus (Marceau et al.)', 'value': 'Marceau_DENV_'},
                                    {'label': 'Dengue Virus 276RKI (Ooi et al.)', 'value': 'Ooi_DENV1_276RKI_'},
                                    {'label': 'Dengue Virus 429557(Ooi et al.)', 'value': 'Ooi_DENV2_429557_'},
                                    {'label': 'Dengue Virus Philippines H871856 (Ooi et al.)', 'value': 'Ooi_DENV3_Philippines-H871856_'},
                                    {'label': 'Dengue Virus BC287-97 (Ooi et al.)', 'value': 'Ooi_DENV4_BC287-97_'},
                                    {'label': 'Enterovirus (Diep et al.)', 'value': 'Diep_EV_'},
                                    {'label': 'Ebola Virus', 'value': 'EBOV_AB_'},
                                    {'label': 'Kaposi\'s sarcoma-associated Herpesvirus (Carolina Arias et al.)', 'value': 'KSHV_CRISPRi'},
                                    {'label': 'Human Corona Virus 229E (schnieder)', 'value': 'Schneider_HCoV-229E_'},
                                    {'label': 'Human Corona Virus NL63 (schnieder)', 'value': 'Schneider_HCoV-NL63_'},
                                    {'label': 'Human Corona Virus OC43 (schnieder)', 'value': 'Schneider_HCoV-OC43_'},
                                    {'label': 'Hepatitis A Virus (Kulsuptrakul et al.)', 'value': 'Kulsuptrakul_HAV_'},
                                    {'label': 'Hepatitis C Virus (Marceau et al.)', 'value': 'Marceau_HCV_'},
                                    {'label': 'Human Coronavirus 229E (Wang et al.)', 'value': 'Wang_229E'},
                                    {'label': 'Human Coronavirus NL63 (Wang et al.)', 'value': 'Wang_NL63_Gecko_'},
                                    {'label': 'Human Coronavirus OC43 (Wang et al.)', 'value': 'Wang_OC43'},
                                    {'label': 'Influenza A Virus (Han et al.)', 'value': 'Han_InfluenzaA_'},
                                    {'label': 'Lymphocytic Choriomeningitis Virus (Liu et al.)', 'value': 'Liu_LCMV_'},
                                    {'label': 'Middle East Respiratory Syndrome Coronavirus (MERS-CoV)', 'value': 'Flather_MERS_CMK_Gecko_'},
                                    {'label': 'Rhinovirus (Diep et al.)', 'value': 'Diep_RV_'},
                                    {'label': 'SARS-CoV-2 Virus (Wang et al.)', 'value': 'Wang_SARS-CoV2'},
                                    {'label': 'SARS-CoV-2 Virus (Schnieder et al.)', 'value': 'Schneider_SARS-CoV-2_'},
                                    {'label': 'SARS-CoV-1 Virus (Broeckel et al.)', 'value': 'Broeckel_SARS-CoV1_Gecko_'},
                                    {'label': 'SARS-CoV-2 Virus Omicron (Puschnik et al.)', 'value': 'SARS-CoV2-Omicron'},
                                    {'label': 'Yellow Fever Virus (Hofann et al.)', 'value': 'Hoffann_YFV_'},
                                    {'label': 'Zika Virus (Hoffmann et al.)', 'value': 'Hoffmann_ZIKV_' }
                                ],
                                value="Marceau_DENV_",
                                clearable=False,
                                optionHeight=70,
                            ),
                        ],
                    ),
                    html.Div(
                        className="dropdown",
                        children=[
                            html.Label(children="Analysis Metric", style={"right": '80px'}),
                            dcc.Dropdown(
                                id="metric",
                                value="-log(pos|score)",
                                options=[
                                    {'label': '-log of Positive Score', 'value': '-log(pos|score)'},
                                    {'label': 'Positive Log Fold Change', 'value': 'pos|lfc'},
                                ],
                                clearable=False,
                                optionHeight=65
                                #style={"left": '80px'}
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
                                clearable=True,
                                multi = False,
                                optionHeight = 50                      
                            ),
                        ],
                    ),

                    html.Div(
                        className="dropdown",
                        children=[
                            html.Label(children="Search for Genes"),
                            # TODO: Fix init value crashing app
                            dcc.Dropdown(
                                id="search_genes",
                                placeholder="Gene Name",
                                value ="ACER1",
                                options=[
                                    {'label': 'ACER 1', 'value': 'ACER1'} # insert preferred default gene into this dictionary, then replace it in value arg. above
                                ],
                                multi = True,
                                # style={"left": '80px'}
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
                        step=1,
                        #style={"margin-left": '65px'}
                        )
                    ],
                ),
                ],
            ),

            html.Div(
                id = "graph_positioning"
            ),
        ],
    )


    # callback 1
    @app.callback(
        Output("graph_positioning", "className"),
        Input("sig_num", "value")
    )

    #if the user choses a number less than 30 as their num of sig genes, graphs side by side
    #else put the graphs stacked as to not crowd
    #both of these are defined in styles.css (under assets)
    def update_className(sig_num):
        if sig_num < 30:
            return "graphContainer"
        else:
            return "graphStack"

    # callback 2
    # updates graph
    @app.callback(
        Output("graph_positioning","children"),
        Input("vir","value"),
        Input("metric", "value"),
        Input("search_genes", "value"),
        Input("sig_num", "value"),
        Input("hover_metrics", "value")
    )

    def update_figure(vir, metric, input_genes, sig_num, hover_metrics):
        if hover_metrics is None or input_genes is None:
            fig1 = fig2 = {}
        else:
            fig1 = single_analysis.single_plot(data_path, sig_num, metric, input_genes, hover_metrics, vir)
            fig2 = single_analysis.sig_rank(data_path, sig_num, metric, input_genes, hover_metrics, vir)
        return [dcc.Graph(figure = fig1, className="graph"), dcc.Graph(figure = fig2, className="graph")]

    # callback 3
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
    parser.add_argument("--data_path", type=str)
    parser.add_argument("--host", type=str, default="localhost")
    args = parser.parse_args()

    app = dash_single_analysis(args.data_path)
    app.run_server(debug=True, port=8089, host=args.host) 
