"""
This app contains is a demo of a volcano plot 

Run this app:
- Ensure a sample data (virus.gene_summary.txt) is in path (Look to line 56)
- Run `python volcano_plot_app.py` in terminal
- Visit http://127.0.0.1:8050/ in your web browser.
""" 

import pandas as pd
import dash
from dash.dependencies import Input, Output
from dash import html, dcc, dash_table

import plotly.express as px
import numpy as np

app = dash.Dash(__name__)


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
        legend_title="Color Legend"
    )
    return fig

# TO DO: path to example gene_summary.txt data should be inserted here
df_raw = pd.read_csv('data/Broeckel_SARS-CoV1/rra/Broeckel_SARS-CoV1_Gecko_.gene_summary.txt', sep="\t")
df = filter_df(df_raw)

############################################
app.layout = html.Div(children = [
    
    html.Div([
        # LFC slider
        html.Div(children=[
            dcc.RangeSlider(
                id='lfc range',
                min=-6,
                max=8,
                step=0.1,
                marks={i: {'label': str(i)} for i in range(-6, 8)},
                value=[-0.5, 1]
            ), 
        ], style={'display': 'inline-block', 'width': '45%'}),
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
            ], style={'display': 'inline-block', 'width': '43%'}),

            # Table container
            html.Div(children=[
                html.Label("Table of Significant and Enriched Genes"),
                dash_table.DataTable(
                    id='sig_table',
                    data=get_sig_df(df).to_dict('records'),
                    columns=[{"name": i, "id": i} for i in df.columns],
                    style_table={'height': 400, 'overflowX': 'auto'},
                    export_format="csv",
                    page_size=12,
                )
            ], style={'display': 'inline-block', 'width': '43%'})
        ]),
    ]),
])

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


if __name__ == '__main__':
    app.run_server(debug=True)