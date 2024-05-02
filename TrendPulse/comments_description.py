#importar librerías
import os
import openai
from openai import OpenAI
import json
from dotenv import load_dotenv, find_dotenv

_ = load_dotenv('../openAI.env')
client = OpenAI(
    api_key=os.environ.get('openAI_api_key'),
)

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


instruction = "Vas a actuar como un analizador de sentimientos para comentarios extraidos de twitter para un proyecto de social media listening, debes ser capaz de explicar las razones por las se pudo haber escrito el comentario y las posibles razones de las intenciones de este "


for i in range(len(comments)):
    prompt =  f"{instruction} Has un analisis del comentario {comments[i]['tweet']} hecho por el usuario {comments[i]['user_tag']}"
    prompt2 = f"{instruction}clasifica el comentario (exclusivamente reponde el numero de la clasificacion, ejemplo: 4) {comments[i]['tweet']} hecho por el usuario {comments[i]['user_tag']} en una escala de los numeros entre el 0 y 10 donde 0 es muy negativo, 10 es muy positivo, y da como respuesta solo la clasificacion del 1 al 10, por ejemplo: 4"
    response = get_completion(prompt)
    response2 = get_completion(prompt2)
    print("-"*30)
    print(response)
    
    print(response2)
    print("-"*30)
    comments[i]['analysis'] = response
    comments[i]['clasification'] = response2

file_path1 = "AnalyzerApp/management/commands/comments_db.json"

with open(file_path1, 'w') as json_file:
    json.dump(comments, json_file, indent=4)  # The 'indent' parameter is optional for pretty formatting

print(f"Data saved to {file_path}")



