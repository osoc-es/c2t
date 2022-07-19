import numpy as np
import pandas as pd
from db import db
import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, dcc, html
from SPARQLWrapper import SPARQLWrapper
from utils import image_lib

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP]) #[dark,light], [CYBORG,BOOTSTRAP]
dataBase = db(SPARQLWrapper("https://demo.c2t.linkeddata.es/sparql"))
app.layout = dbc.Container(
    [
        dcc.Store(id="store"),
        html.Br(),
        html.H1("Containers to triples"),
        html.Hr(),
        dbc.Tabs(
            [
                dbc.Tab(label="Libreria", tab_id="library"),
                dbc.Tab(label="Comparación", tab_id="compare"),
                dbc.Tab(label="Resumen", tab_id="resume"),
            ],
            id="tabs",
            active_tab="library",
        ),
        html.Div(
            id="tab-content",
            className="p-4",
            ),

    ]
)
@app.callback(
    Output("tab-content", "children"),
    Input("tabs", "active_tab")
)
def render_tab_content(active_tab):
    """
    This callback takes the 'active_tab' property as input, as well as the
    stored graphs, and renders the tab content depending on what the value of
    'active_tab' is.
    """
    if active_tab is not None:
        # we have the entire option-simple tab here
        if active_tab == "library":
            content = [html.Div([
                dbc.Row([
                html.Br(),
                dbc.Col([
                    dbc.Input(id="PackageName", placeholder="Package Name", type="text"),
                ]),
                html.Br(),
                dbc.Col([
                    dbc.Input(id="PackageVersion", placeholder="Package Version", type="text"),
                ])   
            ],
            align="center",
            ),
                html.Br(),
                dbc.ListGroup(id='list-images')
            
            ])
            ]
            return content
        elif active_tab == "compare":
            content=[
            html.Div([
            ],
            style={'text-align': 'center', 'margin':'auto'}
            ),
            
            ]
            return content
        elif active_tab == "resume":
            content = [html.Div([

                
            ],style={'width': '90%','text-align': 'center', 'margin':'auto'})]
            return content
    return "No tab selected"

@app.callback(Output("list-images", "children"),
                     Input("PackageName", "value"),
                     Input("PackageVersion", "value")
                     )
def output_image_list(package_name,package_version):
    df = dataBase.name_version_image_finder(package_version,package_name)
    content =[]
    for i in df.iterrows():
        identifier = i.id
        heading = i.tag
        content.append(image_lib(heading,identifier))
    return content


if __name__ == "__main__":
   app.run_server(debug=True, host="0.0.0.0", port=3000)