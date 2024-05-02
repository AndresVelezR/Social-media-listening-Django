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
    comments = Comment.objects.all()

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
