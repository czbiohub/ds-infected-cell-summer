from __future__ import generator_stop
from turtle import title
from typing import Optional

import dash
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate
from dash import dcc
from dash import html
from dash import dash_table

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

############################################
# Filter Data 
def filter_df(curr_df, effect_size=[-1,1], pv=2):
    curr_df.lower_limit = effect_size[0]
    curr_df.upper_limit = effect_size[1]
    curr_df["color"] = np.where((curr_df["pos|lfc"] > curr_df.upper_limit) & (-np.log(curr_df["pos|p-value"]) > pv), "Positive hit: Significant & Enriched", 
        np.where((curr_df["pos|lfc"] < curr_df.lower_limit) & (-np.log(curr_df["pos|p-value"]) > pv), "Negative hit: Significant & Enriched", "Neither"))
    
    ret = curr_df[["id", "pos|p-value", "pos|rank", "pos|lfc", "color"]]
    ret = ret.set_axis(['Gene id', 'P-Value', 'Rank', 'LFC', 'Color'], axis=1, inplace=False)
    return ret 

# Create table of significant and enriched genes 
def get_sig_df(curr_df):
    return curr_df[curr_df.Color.str.endswith("Significant & Enriched")]

# Create Volcano Plot
def volcano_plot(curr_df):
    fig = px.scatter(
                curr_df,
                x= "LFC",
                y= -np.log(curr_df["P-Value"]),
                color="Color",
                color_discrete_sequence=["green", "gray", "red"],
                hover_data=["Gene id", "P-Value", "LFC"]    
            )
    fig.update_layout(
        title="Volcano Plot",
        xaxis_title="Log Fold Change",
        yaxis_title="-Log(p-value)",
        legend_title="Color Legend",
        font_family='Inter'
    )
    return fig

# TO DO: path to example gene_summary.txt data should be inserted here
df_raw = pd.read_csv('/Users/nathaniel.delrosario/Downloads/mageck_nextflow_out/Broeckel_SARS-CoV1_Gecko_/rra/Broeckel_SARS-CoV1_Gecko_.gene_summary.txt', sep="\t")
df = filter_df(df_raw)

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
                                    {'label': 'Ebola Virus (Flint et al.)', 'value': 'EBOV_AB_'},
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
                                multi = True,
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

        html.Div([

            # P value slider
            html.Div(children = [
                html.Div(children = [
                    dcc.Slider(
                        id='pvalue',
                        min=0,
                        max=16,
                        step=0.1,
                        marks={i: {'label': str(i)} for i in range(0, 16)},
                        value=2,
                        vertical=True
                    )
                ], style={'display': 'inline-block'}),

                # Volcano plot 
                html.Div(children = [
                    dcc.Graph(
                        id='volcanoplot',
                        figure=volcano_plot(df)
                    )
                ], style={'display': 'inline-block', 'width': '43%', 'font-family': 'Inter'}),

                # Table container
                html.Div(children=[
                    html.Label("Table of Significant and Enriched Genes"),
                        html.Div("(Click off table to reset filtering)"), 
                    dash_table.DataTable(
                        id='sig_table',
                        data=get_sig_df(df).to_dict('records'),
                        columns=[{"name": i, "id": i} for i in df.columns],
                        style_table={'height': 421.5, 'overflowX': 'auto', 'font-family':'Inter', 'border': '2px solid grey'},
                        style_as_list_view = True,
                        style_header={'border': '2px solid grey'},
                        filter_action = 'native',
                        filter_query = '',
                        sort_action='custom',
                        sort_mode='multi',
                        sort_by=[],
                        export_format="csv",
                        page_size=12,
                        style_cell={'fontSize':14, 
                                    'font-family': 'Inter', 
                                    'textAlign': 'left', 
                                    },
                        style_data={
                            'font-family': 'Inter'
                        }
                    )
                ], style={'display': 'inline-block', 'width': '43%', 'flex': 100, 'padding-top': '50px'}),

                # LFC slider
                html.Div(children=[
                    dcc.RangeSlider(
                        id='lfc range',
                        min=-6,
                        max=8,
                        step=0.1,
                        marks={i: {'label': str(i)} for i in range(-6, 8)},
                        value=[-0.5, 1],
                        vertical = False
                    ), 
                ], style={'display': 'inline-block', 'width': '45%'})
            ]),
        ]),
    ])

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

    def prod(data_path, requests_pathname_prefix="/"):
        app = dash_single_analysis(data_path, requests_pathname_prefix)
        return app.server

    ############################################   

    # Update Volcano Plot
    @app.callback(
        Output('volcanoplot', 'figure'),
        Input('lfc range', 'value'),
        Input('pvalue', 'value')
    )

    def update_volcanoplot(lfc_range, pvalue):
        res_df = filter_df(df_raw, effect_size = lfc_range, pv = pvalue)
        return volcano_plot(res_df)

    # Update table of significant genes for Volcano plot 
    @app.callback(
        Output('sig_table', 'data'),
        Input('lfc range', 'value'),
        Input('pvalue', 'value')
    )

    def update_sig_table(lfc_range, pvalue):
        res_df = filter_df(df_raw, effect_size = lfc_range, pv = pvalue)
        return get_sig_df(res_df).to_dict('records')

    return app

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--data_path", type=str)
    parser.add_argument("--host", type=str, default="localhost")
    args = parser.parse_args()

    app = dash_single_analysis(args.data_path)
    app.run_server(debug=True, port=8089, host=args.host) 
