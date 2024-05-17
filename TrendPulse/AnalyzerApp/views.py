from django.shortcuts import render
from .models import Comment
#from product_recommendations_db import get_embedding, cosine_similarity
import numpy as np
import json
import openai 
from dotenv import load_dotenv, find_dotenv
import os
from django.db.models import IntegerField
from django.db.models.functions import Cast 
import matplotlib.pyplot as plt
from django.shortcuts import HttpResponse
import subprocess

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect
from django.urls import reverse

from packaging import version
required_version = version.parse("1.1.1")
current_version = version.parse(openai.__version__)

if current_version < required_version:
    raise ValueError(f"Error: OpenAI version {openai.__version__}"
                     " is less than the required version 1.1.1")
else:
    print("OpenAI version is compatible.")

from openai import OpenAI 

###########################################################################################################################
# FUNCIONES AUXILIARES
###########################################################################################################################
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


###########################################################################################################################


# VISTA QUE MUESTRA TODOS LOS COMENTARIOS DIVIDIDOS EN TRES COLUMNAS (POSITIVOS, NEGATIVOS, NEGATIVOS) Y ORGANIZADOS PO LA CALIFICAION
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



# VISTA DONDE ESTA EL BOTON "COMENZAR" y "ANALIZAR"QUE INICIA EL PORCESO DEL SCRAPPING
def buttons_view(request):
    return render(request, 'buttons.html')


# VISTA PARA RECIBIR LOS DATOS DEL SCRAPING Y GUARDARLOS EN LA BD

@csrf_exempt
def submit_json_view(request):
    if request.method == 'POST':
        
        result = subprocess.run(['python3', './lastHope.py'], capture_output=True, text=True)

        if result.returncode == 0:
            print("Script executed successfully")
            json_file_path = 'AnalyzerApp/ScrapingData.json'
            with open(json_file_path, 'r', encoding='utf-8') as file:
                comments = json.load(file)
            Comment.objects.all().delete()
            for comment in comments:
                Comment.objects.create(
                user_tag=comment.get('user_tag', ''),  # Utiliza get() para manejar claves ausentes en el diccionario
                tweet=comment.get('tweet', ''),
                time=comment.get('time_stamp', ''),
                reply=comment.get('reply', None),  # Si el valor es None, será tratado como nulo
                retweet=comment.get('retweet', None),
                like=comment.get('like', None),
                analysis=comment.get('analysis', ''),  # Si no hay análisis, se asigna una cadena vacía
                clasification=comment.get('clasification', None), # Si no hay clasificación, se asigna None
                )
            print("Datos guardados en la base de datos correctamente.")

        else:
            print(f"Script execution failed with error: {result.stderr}")
        return redirect('comments')
    else:
        return JsonResponse({'status': 'error', 'message': 'Only POST requests are allowed'})
    


# VISTA PARA MOSTRAR TODOS LOS COMENTARIOS RESULTADO DEL SCRAPPING
def resultado_scraping(request):
    # Leer el diccionario desde el archivo JSON
    comments = Comment.objects.all()
    return render(request, 'comments', {'comments': comments})


# VISTA PARA HACER EL ANALISIS Y CALIFICACION DE LOS COMENTARIOS EN LA BD Y ACTUALIZAR LA BD
def hacer_analisis(request):
    if request.method == 'POST':
        comments = Comment.objects.all()
        instruction = "Vas a actuar como un analizador de sentimientos para comentarios extraidos de twitter para un proyecto de social media listening, debes ser capaz de explicar las razones por las se pudo haber escrito el comentario y las posibles razones de las intenciones de este "
        instruction2 = "Vas a actuar como un analizador de sentimientos e intenciones que es capaz de calificar comentarios en una escala numerica del 1 al 10 donde 1 es muy negativo y 10 es muy positivo. Solo puedes dar respuestas numericas y de un solo caracter. Por ejemplo: 4. Es muy importante que tu respuesta sea EXCLUSIVA Y UNICAMENTE UN NUMERO."
        for comment in comments:
            print(f"COMENTRIO A ANALIZAR: {comment.tweet}")
            prompt =  f"{instruction} Has un analisis del comentario {comment.tweet} hecho por el usuario {comment.user_tag}"
            prompt2 = f"{instruction2}califica el comentario {comment.tweet}"
            response = get_completion(prompt)
            response2 = get_completion(prompt2)
            print("-"*30)
            print(response)
    
            print(response2)
            print("-"*30)
            comment.analysis = response
            comment.clasification = response2

            comment.save()
            
        print("Analisis y clasifición guardados en la base de datos correctamente.")

        return redirect('analysis')
    else:
        return JsonResponse({'status': 'error', 'message': 'Only POST requests are allowed'})
    
# VISTA PARA MOSTRAR LOS COMENTAIROS DE LA BASE DE DATOS AHORA CON SU RESPECTIVO ANALISIS Y CALIFICAION
def resultado_analisis(request):
    comments = Comment.objects.all()

    return render(request, 'resultado_analisis.html', {'comments': comments})



def show_index(request):
    return render(request, 'index.html')

def show_login(request):
    return render(request, 'login.html')

def show_register(request):
    return render(request, 'register.html')


#################################################
################################################
###############################################
from plotly.offline import plot
import plotly.graph_objects as go
    
        
def comments_new(request):
    comments = Comment.objects.all()

    return render(request, 'comments.html', {'comments':comments})

def analysis(request):
    comments = Comment.objects.all()
    return render(request, "analysis.html", {'comments':comments})

def charts(request):
    return render(request, "charts.html")

def base(request):
    return render(request, "base.html")