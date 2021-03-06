from platform import architecture
import ssl
import numpy as np
import pandas as pd
from db import db
import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, dcc, html,State
from SPARQLWrapper import SPARQLWrapper
from utils import image_lib, make_card, make_comparison_table, make_comparison_table_pack_diff, make_comparison_table_pack_sim

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
                dbc.Tab(label="Library", tab_id="library"),
                dbc.Tab(label="Compare", tab_id="compare"),
                dbc.Tab(label="Summary", tab_id="summary"),
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
                    html.P('Introduce the name of a package or the name and the version and the app will return the images that contain that package. Press enter to make your search. ', className="card-text")
                ]),
                dbc.Row([
                html.Br(),
                dbc.Col([
                    dbc.Input(id="PackageName", placeholder="Package Name (for example: log4j)", type="text",debounce=True),
                ]),
                html.Br(),
                dbc.Col([
                    dbc.Input(id="PackageVersion", placeholder="Package Version (for example: 1.2.17)", type="text",debounce=True),
                ]),
            ],
            align="center",
            ),
                html.Br(),
                dbc.ListGroup(id='list-images')
            ])
            ]
            return content
        elif active_tab == "compare":
            content = [html.Div([
                dbc.Row([
                    html.P('Introduce the name of two images and the app will make a comparison of them. Press enter to make your search. ', className="card-text")
                ]),
                dbc.Row([
                    dbc.Card(
                dbc.CardBody(
                    [
                        html.H4("Images in the graph", className="card-title"),
                        html.P(
                            "stain/jena-fuseki:latest, wagoodman/dive:latest, ghcr.io/dgarijo/widoco:latest, python:latest, mysql:latest, neo4j:4.4.5, node:latest, wordpress:latest, python:3.8, pegasus/pegasus:panorama-xenial, amancevice/pandas:latest, mongo:latest, hello-world:latest, pegasus/pegasus:panorama-focal",
                            className="card-text",
                        )
                    ]
                ),
                style={"width": "180rem"},
            )
                ]),
                dbc.Row([
                html.Br(),
                dbc.Col([
                    dbc.Input(id="Image1", placeholder="Image name 1", type="text",debounce=True),
                ]),
                html.Br(),
                dbc.Col([
                    dbc.Input(id="Image2", placeholder="Image name 2", type="text",debounce=True),
                ])   
            ],
            align="center",
            ),
                html.Br(),
                dbc.Button(
                    "Main",
                    id="collapse-button-main",
                    className="mb-3",
                    color="primary",
                    n_clicks=0,
                ),
                dbc.Collapse(dbc.Table(id='compare-images-main'),
                    id="collapse-main",
                    is_open=True,
                ),
                html.Br(),
                dbc.Button(
                    "Same",
                    id="collapse-button-same",
                    className="mb-3",
                    color="success",
                    n_clicks=0,
                ),
                dbc.Collapse(dbc.Table(id='compare-images-same'),
                    id="collapse-same",
                    is_open=True,
                ),
                html.Br(),
                dbc.Button(
                    "Diff",
                    id="collapse-button-diff",
                    className="mb-3",
                    color="warning",
                    n_clicks=0,
                ),
                dbc.Collapse(dbc.Table(id='compare-images-diff'),
                    id="collapse-diff",
                    is_open=True,
                )
                
            
            ])
            ]
            return content
        elif active_tab == "summary":
            content = [html.Div([
                dbc.Row([
                    html.P('Introduce the name of an image and the app will make a summary of its metadata. Press enter to make your search.', className="card-text")
                ]),
                dbc.Row([
                    dbc.Card(
                dbc.CardBody(
                    [
                        html.H4("Images in the graph", className="card-title"),
                        html.P(
                            "stain/jena-fuseki:latest, wagoodman/dive:latest, ghcr.io/dgarijo/widoco:latest, python:latest, mysql:latest, neo4j:4.4.5, node:latest, wordpress:latest, python:3.8, pegasus/pegasus:panorama-xenial, amancevice/pandas:latest, mongo:latest, hello-world:latest, pegasus/pegasus:panorama-focal",
                            className="card-text",
                        )
                    ]
                ),
                style={"width": "180rem"},
            )
                ]),
                dbc.Row([
                html.Br(),
                dbc.Col([
                    dbc.Input(id="ImageTag", placeholder="image Tag", type="text",debounce=True),
                ])   
            ],
            align="center",
            ),
                html.Br(),
                dbc.Card(id='resume_card')
            
            ])
            ]
            return content
    return "No tab selected"

@app.callback(Output("list-images", "children"),
                     Input("PackageName", "value"),
                     Input("PackageVersion", "value")
                     )
def output_image_list(package_name,package_version):
    df = dataBase.name_version_image_finder(package_version,package_name)
    content =[]
    for index, row in df.iterrows():
        identifier = row['id']
        heading = row["tag"]
        content.append(image_lib(heading,identifier))
    return content


@app.callback(Output("resume_card", "children"),
                     Input("ImageTag", "value"),
                     )
def output_image_list(ImageTag):
    df = dataBase.get_card_resume(ImageTag)
    content =[]
    for index, row in df.iterrows():
        architecture = row['architecture']
        tag = row["tag"]
        os = row['osDescription']
        size = row['size']
        packageT = row['packageT']
        total = row['total']
        created = row['created']
        content.append(make_card(tag, architecture, size, os, created, packageT, total))
    return content

@app.callback(
    Output("collapse-main", "is_open"),
    [Input("collapse-button-main", "n_clicks")],
    [State("collapse-main", "is_open")],
)
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open


@app.callback(Output("compare-images-main", "children"),
                     Input("Image1", "value"),
                     Input('Image2', "value")
                     )
def output_image_list(Image1, Image2):
    df = dataBase.get_comparison_meta(Image1, Image2)
    content =[]
    content.append(make_comparison_table(df.set_index('tag')))
    return content

@app.callback(
    Output("collapse-same", "is_open"),
    [Input("collapse-button-same", "n_clicks")],
    [State("collapse-same", "is_open")],
)
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open


@app.callback(Output("compare-images-same", "children"),
                     Input("Image1", "value"),
                     Input('Image2', "value")
                     )
def output_image_list(Image1, Image2):
    _, df2 = dataBase.get_comparison_pack(Image1, Image2)
    content =[]
    content.append(make_comparison_table_pack_diff(df2))
    return content


@app.callback(
    Output("collapse-diff", "is_open"),
    [Input("collapse-button-diff", "n_clicks")],
    [State("collapse-diff", "is_open")],
)
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open


@app.callback(Output("compare-images-diff", "children"),
                     Input("Image1", "value"),
                     Input('Image2', "value")
                     )
def output_image_list(Image1, Image2):
    df1, _ = dataBase.get_comparison_pack(Image1, Image2)
    content =[]
    content.append(make_comparison_table_pack_sim(df1))
    return content


if __name__ == "__main__":
   ssl._create_default_https_context = ssl._create_unverified_context
   app.run_server(debug=False, host="0.0.0.0", port=3000)



   