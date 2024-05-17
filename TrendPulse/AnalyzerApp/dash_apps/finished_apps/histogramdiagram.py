import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
from django_plotly_dash import DjangoDash
from AnalyzerApp.models import Comment

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = DjangoDash('HistogramDiagram', external_stylesheets=external_stylesheets)


app.layout = html.Div([
    dcc.Graph(id='slider-graph', animate=True, style={"backgroundColor": "#1a2d46", 'color': '#ffffff'}),
    dcc.Slider(
        id='slider-updatemode'),
])


@app.callback(
               Output('slider-graph', 'figure'),
              [Input('slider-updatemode', 'value')])

def display_value(value):

    comments = Comment.objects.all()
    texto = ""
    for comment in comments:
        twt = str(comment.tweet)
        texto = texto + twt
    
    y = texto.split()

    graph = go.Histogram(
        x=y,
        name='Histogram Graph',
        xbins=dict(
            start=min(y),
            end=max(y),
            size=1
        )
    )
    layout = go.Layout(
        paper_bgcolor='#27293d',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),

    )
    return {'data': [graph], 'layout': layout}
