from flask import Flask, request

app = Flask(__name__)

@app.route('/hello')
def hello():
    """
    Endpoint para saludar al usuario.

    Parametros:
        name (str): Nombre del usuario recibido por URL.

    Retorna:
        str: Mensaje de saludo personalizado.
    """
    name = request.args.get('name', 'mundo')
    return f"Hello, {name}!"

@app.route('/')
def index():
    return "App corriendo. Usa /hello?name=TuNombre"

if __name__ == '__main__':
    app.run(debug=True, port=5000)
