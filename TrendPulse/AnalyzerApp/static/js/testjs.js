// archivo.js

document.getElementById('tu_boton_id').addEventListener('click', function() {
    // Crear un objeto JSON de ejemplo
    var jsonData = {
        'titulo': 'Título del comentario',
        'contenido': 'Contenido del comentario',
        'retweets': 10
        // Puedes agregar más campos según tus necesidades
    };

    // Enviar el JSON al servidor usando AJAX
    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/ajax/submit_json/', true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.onreadystatechange = function() {
        if (xhr.readyState === 4 && xhr.status === 200) {
            var response = JSON.parse(xhr.responseText);
            if (response.status === 'success') {
                console.log('JSON enviado exitosamente');
                // Aquí puedes realizar más acciones según la respuesta del servidor
            } else {
                console.error('Error al enviar JSON: ' + response.message);
            }
        }
    };
    xhr.send(JSON.stringify(jsonData));
});
