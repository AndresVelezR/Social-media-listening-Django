import json

from flask import request

from flask import Flask, render_template

app = Flask(__name__, template_folder='templates')

print("dentro")


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/test', methods=['POST'])
def test():
    output = request.get_json()
    print(output) # This is the output that was stored in the JSON within the browser
    print(type(output))
    result = json.loads(output) #this converts the json output to a python dictionary
    print(result) # Printing the new dictionary
    print("-----------------------------------------------")
    with open('datos.json', 'w') as f:
        json.dump(result, f)
    print("GUARDADO EL JSON DE MANERA EFECTIVA")

    print(type(result))#this shows the json converted as a python dictionary
    return result


if __name__ == '__main__':
    # Inicia el servidor Flask en el puerto 5000 (puedes cambiar el puerto si lo deseas)
    app.run(debug=True, port=5000)