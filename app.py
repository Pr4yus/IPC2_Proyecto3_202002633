from flask import Flask, request, jsonify
import xml.etree.ElementTree as ET

# from config import config

app = Flask(__name__)


# Estructura de datos para almacenar clientes y bancos
class Cliente:
    def __init__(self, nit, nombre):
        self.nit = nit
        self.nombre = nombre


class Banco:
    def __init__(self, codigo, nombre):
        self.codigo = codigo
        self.nombre = nombre


class Factura:
    def __init__(self, numero_factura, nit_cliente, fecha, valor):
        self.numero_factura = numero_factura
        self.nit_cliente = nit_cliente
        self.fecha = fecha
        self.valor = valor


class Pago:
    def __init__(self, codigo_banco, fecha, nit_cliente, valor):
        self.codigo_banco = codigo_banco
        self.fecha = fecha
        self.nit_cliente = nit_cliente
        self.valor = valor


facturas = []
pagos = []

clientes = {}
bancos = {}


@app.route('/grabarConfiguracion', methods=['POST'])
def grabarConfiguracion():
    try:
        file = request.files['file']
        if file.filename.endswith('xml'):
            tree = ET.parse(file)
            root = tree.getroot()

            for cliente_xml in root.findall('./clientes/cliente'):
                nit = cliente_xml.find('NIT').text
                nombre = cliente_xml.find('nombre').text
                clientes[nit] = Cliente(nit, nombre)

            for banco_xml in root.findall('./bancos/banco'):
                codigo = banco_xml.find('codigo').text
                nombre = banco_xml.find('nombre').text
                bancos[codigo] = Banco(codigo, nombre)

            return jsonify({'message': 'Datos cargados exitosamente'}), 200
        else:
            return jsonify({'error': 'El archivo de tener el formato correcto de XML'}), 400
    except Exception as ex:
        return jsonify({'message': ex})


@app.route('/grabarTransaccion', methods=['POST'])
def grabarTransaccion():
    try:
        file = request.files['file']
        if file.filename.endswith('.xml'):
            tree = ET.parse(file)
            root = tree.getroot()

            for factura_xml in root.findall('./facturas/factura'):
                numero_factura = factura_xml.find('numeroFactura').text
                nit_cliente = factura_xml.find('NITcliente').text
                fecha = factura_xml.find('fecha').text
                valor = factura_xml.find('valor').text
                facturas.append(Factura(numero_factura, nit_cliente, fecha, valor))

            for pago_xml in root.findall('./pagos/pago'):
                codigo_banco = pago_xml.find('codigoBanco').text
                fecha = pago_xml.find('fecha').text
                nit_cliente = pago_xml.find('NITcliente').text
                valor = pago_xml.find('valor').text
                pagos.append(Pago(codigo_banco, fecha, nit_cliente, valor))

            return jsonify({'message': 'Transacciones cargadas exitosamente'}), 200
        else:
            return jsonify({'error': 'El archivo debe tener formato XML'}), 400
    except Exception as ex:
        return jsonify({'message': ex})


@app.route('/devolverEstadoCuenta', methods=['GET'])
def devolverEstadoCuenta():
    nit = request.args.get('nit_cliente')
    # codigo_banco = request.args.get('codigo')
    cliente_info = None
    banco = None
    facturas_info = []
    pagos_info = []
    saldo = 0

    if nit in clientes:
        # if nit in clientes and codigo_banco in bancos:
        cliente_info = clientes[nit]
        # banco = bancos[codigo_banco]
        # return jsonify({'cliente': {'nit': cliente.nit, 'nombre': cliente.nombre}, 'banco': {'codigo': banco.codigo, 'nombre': banco.nombre}})
        total_facturas = 0
        for factura in facturas:
            if factura.nit_cliente == nit:
                factura_info = {
                    'numero_factura': factura.numero_factura,
                    'fecha': factura.fecha,
                    'valor': factura.valor
                }
                facturas_info.append(factura_info)
                total_facturas += float(factura.valor)

        total_pagos = 0
        for pago in pagos:
            if pago.nit_cliente == nit:
                if pago.codigo_banco in bancos:
                    banco = bancos[pago.codigo_banco]
                    pago_info = {
                        'codigo_banco': pago.codigo_banco,
                        'banco': banco.nombre,
                        'fecha': pago.fecha,
                        'valor': pago.valor
                    }
                    pagos_info.append(pago_info)
                    total_pagos += float(pago.valor)

        # Calcular saldo
        saldo = total_facturas - total_pagos

        return jsonify({
            'cliente': {'nit': cliente_info.nit, 'nombre': cliente_info.nombre},
            'cargos': facturas_info,
            'abonos': pagos_info,
            'saldo': saldo,
            'moneda': 'Q'
        })
    else:
        return jsonify({'error': 'Cliente o banco no encontrado'}), 404


@app.route('/devolverResumenPagos', methods=['GET'])
def devolverResumenPagos():
    mes = request.args.get('mes')
    pagos_por_banco = {}

    # Filtrar pagos por el mes especificado
    for pago in pagos:
        if pago.codigo_banco in bancos:
            banco = bancos[pago.codigo_banco]
            fecha_pago = pago.fecha.split('/')[1]
            if fecha_pago == mes:
                if pago.codigo_banco not in pagos_por_banco:
                    pagos_por_banco[banco.nombre] = []

                pago_info = {
                    'fecha': pago.fecha,
                    'codigo_banco': pago.codigo_banco,
                    'banco': banco.nombre,
                    'NIT_cliente': pago.nit_cliente,
                    'monto': pago.valor
                }
                pagos_por_banco[banco.nombre].append(pago_info)

    return jsonify(pagos_por_banco)

@app.route('/borrarDatos', methods=['DELETE'])
def borrarDatos():
    # Asegúrate de que estas son las estructuras de datos correctas que estás utilizando para almacenar tus datos.
    global clientes, facturas, pagos, bancos
    clientes = {}
    facturas = []
    pagos = []
    bancos = {}
    return jsonify({'mensaje': 'Todos los datos han sido borrados.'})

def pagina_no_encontrada(error):
    return "<h1>La página que intentas buscar no existe!!</h1>"


if __name__ == "__main__":
    # app.config.from_object(config['development'])
    app.register_error_handler(404, pagina_no_encontrada)
    app.run(debug=True)
