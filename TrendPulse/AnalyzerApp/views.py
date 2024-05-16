from django.shortcuts import render
from .models import Comment
#from product_recommendations_db import get_embedding, cosine_similarity
import numpy as np
import json
from openai import OpenAI 
from dotenv import load_dotenv, find_dotenv
import os
from django.db.models import IntegerField
from django.db.models.functions import Cast 
import matplotlib.pyplot as plt

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect
from django.urls import reverse



#Se lee del archivo .env la api key de openai
_ = load_dotenv('../openAI.env')
client = OpenAI(
    # This is the default and can be omitted
    api_key=os.environ.get('openAI_api_key'),
)

#Se carga la lista de películas de movie_titles.json
file_path = 'AnalyzerApp/management/commands/comments_db.json'
with open(file_path, 'r') as file:
    file_content = file.read()
    comments = json.loads(file_content)

def get_completion(prompt, model="gpt-3.5-turbo"):
    messages = [{"role": "user", "content": prompt}]
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0,
    )
    return response.choices[0].message.content

def show_comments(request):
    comments = Comment.objects.annotate(
        classification_int=Cast('clasification', IntegerField())
        ).order_by('classification_int')

    return render(request, 'show_comments.html', {'comments': comments})

def clasification(request):
    comments = Comment.objects.annotate(
        classification_int=Cast('clasification', IntegerField())
        ).order_by('classification_int')

    positive = []
    negative = []
    neutral = []
    for comment in comments:
        clasification = int(comment.clasification)
        if clasification >  5:
            positive.append(comment)
       
        elif clasification == 5:
            neutral.append(comment)
      
        else:
            negative.append(comment)
            

    return render(request, 'stats.html',{'positive': positive, 'neutral': neutral, 'negative': negative})

def show_chart(request):
    comments = Comment.objects.all()
    pos = 0
    neu = 0
    neg = 0
    for comment in comments:
        clasification = int(comment.clasification)
        if clasification >  5:
            pos += 1
       
        elif clasification == 5:
            neu += 1
      
        else:
            neg +=1
    
    x = ['pos', 'neu', 'neg']
    y = [6, 3, 1]
    colors = ['green', 'yellow', 'red']

    plt.subplot(2,2,1)
    plt.bar(x,y, color=colors)
    ruta = 'AnalyzerApp/static/images/matplot2.jpg'
    plt.savefig(ruta)
    plt.close()
    return render(request, 'graph.html')

def index_view(request):
    return render(request, 'index.html')

@csrf_exempt
def submit_json_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        with open('datos.json', 'w') as f:
            json.dump(data, f)
        print("JSON guardado correctamente.")
        # Redirigir a la vista de resultado
        return redirect(reverse('resultado'))
    else:
        return JsonResponse({'status': 'error', 'message': 'Only POST requests are allowed'})

def resultado_view(request):
    # Leer el diccionario desde el archivo JSON
    with open('datos.json', 'r') as f:
        data = json.load(f)
    return render(request, 'sera.html', {'data': data})
        
