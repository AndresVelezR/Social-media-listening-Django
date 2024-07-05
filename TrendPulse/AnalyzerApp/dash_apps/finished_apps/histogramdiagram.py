import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
from django_plotly_dash import DjangoDash
from AnalyzerApp.models import Comment
from collections import Counter

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = DjangoDash('HistogramDiagram', external_stylesheets=external_stylesheets)

app.layout = html.Div([
    dcc.Graph(id='slider-graph', animate=True, style={"backgroundColor": "#1a2d46", 'color': '#ffffff'}),
    dcc.Slider(
        id='slider-updatemode',
        min=0,
        max=10,
        step=1,
        value=5,
        marks={i: str(i) for i in range(11)}
    ),
])

@app.callback(
    Output('slider-graph', 'figure'),
    [Input('slider-updatemode', 'value')]
)
def display_value(value):
    comments = Comment.objects.all()
    texto = " ".join([str(comment.tweet) for comment in comments])
    texto_sin_espacios = " ".join(texto.split())
    palabras = texto_sin_espacios.split()
    
    # Contar la frecuencia de cada palabra
    frecuencia_palabras = Counter(palabras)
    
    # Crear listas de palabras y sus frecuencias
    palabras_unicas = list(frecuencia_palabras.keys())
    frecuencias = list(frecuencia_palabras.values())

    graph = go.Bar(
        x=palabras_unicas,
        y=frecuencias,
        name='Frecuencia de Palabras'
    )
    layout = go.Layout(
        paper_bgcolor='#27293d',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        title='Histograma de Frecuencia de Palabras',
        xaxis=dict(title='Palabras'),
        yaxis=dict(title='Frecuencia')
    )
    return {'data': [graph], 'layout': layout}
