# frontend.py
from django.contrib.sites import requests
from django.http import HttpResponse
from django.shortcuts import render

def index(request):
    # Aquí iría la lógica para obtener los clientes desde la API
    # Supongamos que la API está corriendo en http://localhost:5000/api/clients
    response = requests.get('http://localhost:5000/api/clients')
    clients = response.json()

    # Renderiza la plantilla con los clientes obtenidos
    return render(request, 'index.html', {'clients': clients})
