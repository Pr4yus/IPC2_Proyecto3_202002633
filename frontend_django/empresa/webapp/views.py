from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
# frontend/views.py

from django.shortcuts import render
import requests

def index(request):
    return render(request, 'index.html')

def grabarConfiguracion(request):
    try:
        file = request.FILES['file']
        url = 'http://localhost:5000/grabarConfiguracion'
        files = {'file': file}
        response = requests.post(url, files=files)
        return render(request, 'cargar_configuracion.html', response.json(), status=response.status_code)
    except Exception as ex:
        return render(request, 'cargar_configuracion.html', {'error': str(ex)}, status=500)

def grabarTransaccion(request):
    try:
        file = request.FILES['file']
        url = 'http://localhost:5000/grabarTransaccion'  # Cambia esto por la URL correcta de tu backend Flask
        files = {'file': file}
        response = requests.post(url, files=files)
        return render(request, 'cargar_transacciones.html', response.json(), status=response.status_code)
    except Exception as ex:
        return render(request, 'cargar_transacciones.html', {'error': str(ex)}, status=500)

def devolverEstadoCuenta(request):
    nit = request.GET.get('nit_cliente')
    url = f'http://localhost:5000/devolverEstadoCuenta?nit_cliente={nit}'  # Cambia esto por la URL correcta de tu backend Flask
    response = requests.get(url)
    if response.status_code == 200:
        return render(request, 'estado_cuenta.html', {'data': response.json()})
    else:
        return render(request, 'estado_cuenta.html', {'error': 'Cliente o banco no encontrado'})

def devolverResumenPagos(request):
    mes = request.GET.get('mes')
    url = f'http://localhost:5000/devolverResumenPagos?mes={mes}'  # Cambia esto por la URL correcta de tu backend Flask
    response = requests.get(url)
    return render(request, 'resumen_pagos.html', {'data': response.json()})

import requests
from django.http import JsonResponse

def borrarDatos(request):
    url = 'http://localhost:5000/borrarDatos'  # Cambia esto por la URL correcta de tu backend Flask
    response = requests.delete(url)
    if response.status_code == 200:
        return JsonResponse({'mensaje': 'Todos los datos han sido borrados.'})
    else:
        return JsonResponse({'error': 'Hubo un error al intentar borrar los datos.'}, status=400)


def pagina_no_encontrada(request, exception):
    return render(request, '404.html', status=404)
