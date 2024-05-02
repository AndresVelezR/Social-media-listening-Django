#importar librerías
import os
from openai import OpenAI
import json
from dotenv import load_dotenv, find_dotenv
import requests
from PIL import Image
from io import BytesIO
import numpy as np

#Se lee del archivo .env la api key de openai
_ = load_dotenv('../openAI.env')
client = OpenAI(
    # This is the default and can be omitted
    api_key=os.environ.get('openAI_api_key'),
)

#Se carga la lista de películas de movie_titles.json
with open('AnalyzerApp/management/commands/comments_db.json', 'r') as file:
    file_content = file.read()
    comments = json.loads(file_content)



#Se hace la conexión con la API de generación de imágenes. El prompt en este caso es:
#Alguna escena de la película + "nombre de la película"
response = client.images.generate(
  model="dall-e-3",
  #prompt=f"Alguna escena de la película {comments[np.random.randint(idx_movie)]['title']}",
  prompt = "LOGO QUE REPRESENTE UN COMENTARIO DE TWITTER NEGATIVO",
  size="1024x1024",
  quality="standard",
  style= 'vivid',
  n=1,
)

image_url = response.data[0].url

# La API devuelve la url de la imagen, por lo que debemos generar una función auxiliar que
# descargue la imagen.
def fetch_image(url):
    response = requests.get(url)
    response.raise_for_status()

    # Convert the response content into a PIL Image
    image = Image.open(BytesIO(response.content))
    return(image)

img = fetch_image(image_url)
img.show()
print(image_url)
img.save(f'AnalyzerApp/static/images/test2.jpg')           
            