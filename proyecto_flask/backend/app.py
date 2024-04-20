# backend.py
from flask import Flask, jsonify

app = Flask(__name__)

# Define un endpoint para la API
@app.route('/api/clients', methods=['GET'])
def get_clients():
    # Aquí iría la lógica para obtener los clientes desde la base de datos
    clients = [
        {"NIT": "123456-A", "nombre": "Cliente 1"},
        {"NIT": "654321-B", "nombre": "Cliente 2"}
    ]
    return jsonify(clients)

if __name__ == '__main__':
    app.run(debug=True)

