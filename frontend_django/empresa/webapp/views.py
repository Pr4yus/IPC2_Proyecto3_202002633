from django.http import JsonResponse, FileResponse
from django.shortcuts import render
from django.http import FileResponse
from reportlab.lib.pagesizes import letter
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, Paragraph
from io import BytesIO
from reportlab.pdfgen import canvas
from io import BytesIO
# Create your views here.
# frontend/views.py
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from django.http import FileResponse
import requests
import matplotlib.pyplot as plt
from PIL import Image
from io import BytesIO
import base64
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
########################################
def devolverEstadoCuenta(request):
    nit = request.GET.get('nit_cliente')
    url = f'http://localhost:5000/devolverEstadoCuenta?nit_cliente={nit}'  # Cambia esto por la URL correcta de tu backend Flask
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()

        # Crear el PDF en memoria
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)

        # Crear las tablas para los cargos y abonos
        cargos = [['Fecha', 'Número de Factura', 'Valor']] + [[c['fecha'], c['numero_factura'], c['valor']] for c in data['cargos']]
        abonos = [['Banco', 'Código de Banco', 'Fecha', 'Valor']] + [[a['banco'], a['codigo_banco'], a['fecha'], a['valor']] for a in data['abonos']]

        # Dibujar los datos en el PDF
        elements = []
        elements.append(Paragraph(f"Cliente: {data['cliente']['nombre']}"))
        elements.append(Paragraph(f"NIT: {data['cliente']['nit']}"))
        elements.append(Paragraph("Cargos:"))
        elements.append(Table(cargos))
        elements.append(Paragraph("Abonos:"))
        elements.append(Table(abonos))
        elements.append(Paragraph(f"Saldo: {data['saldo']} {data['moneda']}"))

        doc.build(elements)

        # Crear una respuesta de archivo con el PDF
        buffer.seek(0)
        return FileResponse(buffer, as_attachment=True, filename='estado_cuenta.pdf')
    else:
        return render(request, 'estado_cuenta.html', {'error': 'Cliente o banco no encontrado'})



    ########################################

def devolverResumenPagos(request):
    mes = request.GET.get('mes')
    url = f'http://localhost:5000/devolverResumenPagos?mes={mes}'  # Cambia esto por la URL correcta de tu backend Flask
    response = requests.get(url)
    data = response.json()

    # Crear la gráfica con Matplotlib
    plt.figure(figsize=(10, 6))
    for banco, pagos in data.items():
        plt.bar(banco, sum([float(pago['monto']) for pago in pagos])/1000)  # Dividir por 1000 para convertir a miles
    plt.xlabel('Banco')
    plt.ylabel('Monto (en miles de quetzales)')
    plt.title('Resumen de Pagos')

    # Guardar la gráfica en un archivo
    plt.savefig('grafica.png')

    # Crear el PDF
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    c.setFont("Helvetica", 16)
    c.drawString(30, 750, "Resumen de Pagos")
    c.setFont("Helvetica", 11)
    y = 730
    for banco, pagos in data.items():
        c.drawString(30, y, f"El banco es {banco}")
        y -= 15
        for pago in pagos:
            c.drawString(50, y, f"Fecha: {pago['fecha']} - NIT: {pago['NIT_cliente']} - Monto: Q. {pago['monto']}")
            y -= 15
    c.drawImage('grafica.png', 30, y-200, width=500, height=200)
    c.save()

    # Enviar el PDF como respuesta
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='resumen_pagos.pdf')

def borrarDatos(request):
    url = 'http://localhost:5000/borrarDatos'  # Cambia esto por la URL correcta de tu backend Flask
    response = requests.delete(url)
    if response.status_code == 200:
        return JsonResponse({'mensaje': 'Todos los datos han sido borrados.'})
    else:
        return JsonResponse({'error': 'Hubo un error al intentar borrar los datos.'}, status=400)


def ayuda(request):
    url = 'http://localhost:5000/ayuda'  # Cambia esto por la URL correcta de tu backend Flask
    response = requests.get(url)
    return render(request, 'ayuda.html', {'data': response.json()})

def pagina_no_encontrada(request, exception):
    return render(request, '404.html', status=404)
