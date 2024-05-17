import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
from django_plotly_dash import DjangoDash
import pandas as pd
from AnalyzerApp.models import Comment
from datetime import datetime

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# Recuperar comentarios de la base de datos
comments = Comment.objects.all()

# Inicializar diccionarios para conteo por hora
positive_counts = [0] * 24
neutral_counts = [0] * 24
negative_counts = [0] * 24

# Procesar comentarios y clasificarlos por hora
for comment in comments:
    clasification = int(comment.clasification)
    hora = datetime.strptime(comment.time, "%Y-%m-%dT%H:%M:%S.%fZ").hour
    if clasification > 5:
        positive_counts[hora] += 1
    elif clasification == 5:
        neutral_counts[hora] += 1
    else:
        negative_counts[hora] += 1

# Etiquetas para las horas
hours = ['{:02d}:00'.format(i) for i in range(24)]

app = DjangoDash('HoursDiagram', external_stylesheets=external_stylesheets)

app.layout = html.Div([
    dcc.Graph(id='slider-graph', animate=True, style={"backgroundColor": "#1a2d46", 'color': '#ffffff'}),
    dcc.Slider(
        id='slider-updatemode',
        min=0,
        max=23,
        step=1,
        marks={i: '{:02d}:00'.format(i) for i in range(24)},
        value=12,
    ),
])

@app.callback(
    Output('slider-graph', 'figure'),
    [Input('slider-updatemode', 'value')]
)
def display_value(selected_hour):
    filtered_positive = [count if i <= selected_hour else 0 for i, count in enumerate(positive_counts)]
    filtered_negative = [count if i <= selected_hour else 0 for i, count in enumerate(negative_counts)]
    filtered_neutral = [count if i <= selected_hour else 0 for i, count in enumerate(neutral_counts)]

    trace1 = go.Bar(
        x=hours,
        y=filtered_positive,
        name='Positive',
        marker=dict(color='green')
    )
    trace2 = go.Bar(
        x=hours,
        y=filtered_negative,
        name='Negative',
        marker=dict(color='red')
    )
    trace3 = go.Bar(
        x=hours,
        y=filtered_neutral,
        name='Neutral',
        marker=dict(color='grey')
    )

    data = [trace1, trace2, trace3]
    layout = go.Layout(
        paper_bgcolor='#27293d',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        barmode='stack',
        title='Hourly Comments Analysis',
        xaxis=dict(title='Hour of the Day'),
        yaxis=dict(title='Number of Comments')
    )

    return {'data': data, 'layout': layout}