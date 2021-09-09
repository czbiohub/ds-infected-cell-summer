from typing import Optional

import dash
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate
import dash_core_components as dcc
import dash_html_components as html

import pandas as pd

import plotly.express as px

HAV_df = pd.read_csv('/Users/jacklyn.luu/Desktop/ds-infected-cell-summer/test_data/HAV_compare.txt', delimiter = ",")
fig = px.scatter(HAV_df, x="Dataset 1", y="Dataset 2", hover_data=['id'])

def configure_app(app: dash.Dash):
    class Ids:
        pass

    app.layout = html.Div(
        children=[
            dcc.Location(id="url"),
            # TODO: add figures
            html.H1(children='NF pipeline compared to Wang paper data'),

            html.Div(children='''Nextflow pipeline was adapted by Fred Hutchinson's lab '''),
            
            dcc.Graph( id='example-graph', figure=fig)
        ]
    )

    # TODO: add callbacks here


def run():
    app = dash.Dash(__name__)

    configure_app(app)

    app.run_server(debug=True)
