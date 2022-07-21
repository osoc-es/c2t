from turtle import heading
import dash_bootstrap_components as dbc
from dash import html
import pandas as pd

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


def generate_table(packageT, total):
    table_header = [
        html.Thead(html.Tr([html.Th("Package Type"), html.Th("Number of packages")]))
    ]
    print(packageT)
    rows = []
    for i in range (0, len(packageT)):
        row = html.Tr([html.Td(packageT[i]), html.Td(str(total[i]))])
        rows += [row]

    table_body = [html.Tbody(rows)]
    print(table_body)
    table = dbc.Table(table_header + table_body, bordered=True)
    print(table)
    return table


def make_card(tag, architecture, size, osDescription, created, packageT, total):
    card = dbc.Card(
        [
            dbc.CardHeader(tag, className="card-title"),
            dbc.CardBody(
                [
                    html.P('Architecture: '+architecture, className="card-text"),
                    html.P('Size: '+str(size), className="card-text"),
                    html.P('Operative system: '+osDescription, className="card-text"),
                    html.P('Creation time: '+str(created), className="card-text")
                ]
            ),
            generate_table(packageT, total)
        ]
    )
    return card


def make_differences():

    return 


def make_comparison_table(df:pd.DataFrame):
    df = df.transpose()
    df.insert(0,'tags',['architecture', 'size', 'osDescription', 'created'])
    df.set_index('tags')
    table = dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True)
    return table


def make_comparison_table_pack_sim(df:pd.DataFrame):
    df = df.transpose()
    table = dbc.Table.from_dataframe(df.transpose(), dark = True ,striped=True, bordered=True, hover=True)
    return table


def make_comparison_table_pack_diff(df:pd.DataFrame):
    df = df.transpose()
    table = dbc.Table.from_dataframe(df.transpose(), striped=True, bordered=True, hover=True)
    return table