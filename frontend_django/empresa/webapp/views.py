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
    url = f'http://localhost:5000/devolverEstadoCuenta/?NIT={nit}'  # Cambia esto por la URL correcta de tu backend Flask
    response = requests.get(url)
    return render(request, 'estado_cuenta.html', response.json(), status=response.status_code)

def devolverResumenPagos(request):
    mes = request.GET.get('mes')
    url = f'http://localhost:5000/devolverResumenPagos?mes={mes}'  # Cambia esto por la URL correcta de tu backend Flask
    response = requests.get(url)
    return render(request, 'resumen_pagos.html', response.json(), status=response.status_code)

def pagina_no_encontrada(request, exception):
    return render(request, '404.html', status=404)
