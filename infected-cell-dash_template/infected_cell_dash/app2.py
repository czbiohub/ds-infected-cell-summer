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

import dual_analysis
from dual_analysis import *

fig = go.Figure()

def configure_app(app: dash.Dash):
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
        l1, l2 = final_comparison(vir1, vir2, tot_vir)
        fig = px.scatter(x=l1, y=l2, labels=dict(x=abbrev[vir1]+' pos|score', y=abbrev[vir2]+' pos|score'), title = 'Comparing pos|score of ' + abbrev[vir1] +  ' and ' + abbrev[vir2])
        return fig

    return app


if __name__ == "__main__":
    app = dash.Dash(__name__)
    configure_app(app)
    app.run_server(debug=True, port=8084)