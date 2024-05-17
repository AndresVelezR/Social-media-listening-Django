import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
from django_plotly_dash import DjangoDash
from dash import Dash, html, Input, Output, dash_table
import pandas as pd

data_url = 'https://raw.githubusercontent.com/plotly/datasets/master/2014_usa_states.csv'

data = [
    {"autor": "Juan", "comentario": "Excelente artículo, muy informativo."},
    {"autor": "María", "comentario": "Me gustó mucho la lectura, gracias por compartir."},
    {"autor": "Pedro", "comentario": "Interesante perspectiva, gracias por la reflexión."},
    {"autor": "Laura", "comentario": "Buen contenido, me ayudó a comprender mejor el tema."},
    {"autor": "Carlos", "comentario": "Muy bien redactado, se nota el esfuerzo en la escritura."},
    {"autor": "Ana", "comentario": "Me encantó, voy a compartirlo con mis amigos."},
    {"autor": "Luis", "comentario": "Excelente aporte, me dejó pensando."},
    {"autor": "Sofía", "comentario": "Gran trabajo, me mantuvo interesada de principio a fin."},
    {"autor": "Pablo", "comentario": "Muy instructivo, aprendí cosas nuevas."},
    {"autor": "Elena", "comentario": "Me inspiró, seguiré atenta a tus publicaciones."}
]

keys = list(data[0].keys())

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = DjangoDash('Comments1', external_stylesheets=external_stylesheets)


app.layout = html.Div([
    html.H4('Simple interactive table'),
    html.P(id='table_out'),
    dash_table.DataTable(
        id='table',
        columns=[{"name": i, "id": i} 
                 for i in keys],
        data= data,
        style_cell=dict(textAlign='left'),
        style_header=dict(backgroundColor="paleturquoise"),
        style_data=dict(backgroundColor="lavender")
    ), 
])

@app.callback(
    Output('table_out', 'children'), 
    Input('table', 'active_cell'))


def display_value(active_cell):
    if active_cell:
        cell_data = df.iloc[active_cell['row']][active_cell['column_id']]
        return f"Data: \"{cell_data}\" from table cell: {active_cell}"