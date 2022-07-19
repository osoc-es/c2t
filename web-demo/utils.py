from turtle import heading
import dash_bootstrap_components as dbc
from dash import html

def image_lib(heading,identifier):
    content = dbc.ListGroupItem(
            [
                html.Div(
                    [
                        html.H5(heading, className="mb-1")
                    ],
                    className="d-flex w-100 justify-content-between",
                ),
                html.Small(identifier, className="text-muted"),
            ]
        )
    return content