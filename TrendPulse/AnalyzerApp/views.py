from django.shortcuts import render
from .models import Product
#from product_recommendations_db import get_embedding, cosine_similarity
import numpy as np
import json
from openai import OpenAI 
from dotenv import load_dotenv, find_dotenv
import os

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

def analyze_comments(request):
    instruction = "Vas a actuar como un analizador de sentimientos para comentarios extraidos de twitter para un proyecto de social media listening, debes ser capaz de explicar las razones por las se pudo haber escrito el comentario y las posibles razones de las intenciones de este "
    
    return render()
