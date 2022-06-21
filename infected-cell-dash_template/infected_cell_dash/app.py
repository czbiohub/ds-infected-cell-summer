from typing import Optional

import dash
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate
import dash_core_components as dcc
import dash_html_components as html

import pandas as pd

import plotly.express as px
virus_LFC_path = '/Users/jacklyn.luu/Desktop/ds-infected-cell-summer/infected-cell-portal/public/data/viruses_LFC.csv'
lfc_df = pd.read_csv(virus_LFC_path, delimiter = ",")
viruses = lfc_df.columns[1:]

#fig = px.scatter(HAV_df, x="Dataset 1", y="Dataset 2", hover_data=['id'])

def configure_app(app: dash.Dash):
    class Ids:
        pass

    app.layout = html.Div(
        children=[
            html.Div([
                dcc.Dropdown(
                    id='demo-dropdown',
                    options=viruses,
                    value=viruses[1]
                ),
                html.Div(id='dd-output-container')
            ])
        ]
    )

    # TODO: add callbacks here
    @app.callback(
        dash.dependencies.Output('dd-output-container', 'children'),
        [dash.dependencies.Input('demo-dropdown', 'value')])
        
    def update_output(value):
        return 'You have selected "{}"'.format(value)

    return app

def run():
    app = dash.Dash(__name__)

    configure_app(app)

    app.run_server(debug=True)
