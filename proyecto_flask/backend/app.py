from flask import Flask, request, jsonify
import xml.etree.ElementTree as ET

app = Flask(__name__)

class Cliente:
    def __init__(self, nit, nombre):
        self.nit = nit
        self.nombre = nombre

    def to_dict(self):
        return {
            "nit": self.nit,
            "nombre": self.nombre
        }

class Banco:
    def __init__(self, codigo, nombre):
        self.codigo = codigo
        self.nombre = nombre

    def to_dict(self):
        return {
            "codigo": self.codigo,
            "nombre": self.nombre
        }

class Factura:
    def __init__(self, numero_factura, nit_cliente, fecha, valor):
        self.numero_factura = numero_factura
        self.nit_cliente = nit_cliente
        self.fecha = fecha
        self.valor = valor

    def to_dict(self):
        return {
            "numero_factura": self.numero_factura,
            "nit_cliente": self.nit_cliente,
            "fecha": self.fecha,
            "valor": self.valor
        }

class Pago:
    def __init__(self, codigo_banco, fecha, nit_cliente, valor):
        self.codigo_banco = codigo_banco
        self.fecha = fecha
        self.nit_cliente = nit_cliente
        self.valor = valor

    def to_dict(self):
        return {
            "codigo_banco": self.codigo_banco,
            "fecha": self.fecha,
            "nit_cliente": self.nit_cliente,
            "valor": self.valor
        }

# Listas para almacenar objetos
clientes = []
bancos = []
facturas = []
pagos = []

@app.route('/grabarConfiguracion', methods=['POST'])
def grabar_configuracion():
    try:
        xml_data = request.data
        root = ET.fromstring(xml_data)
        
        for cliente in root.findall('./clientes/cliente'):
            nit = cliente.find('NIT').text
            nombre = cliente.find('nombre').text
            clientes.append(Cliente(nit, nombre).to_dict())

        for banco in root.findall('./bancos/banco'):
            codigo = banco.find('codigo').text
            nombre = banco.find('nombre').text
            bancos.append(Banco(codigo, nombre).to_dict())

        return jsonify({"message": "Configuración procesada y grabada correctamente"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/grabarTransaccion', methods=['POST'])
def grabar_transaccion():
    try:
        xml_data = request.data
        root = ET.fromstring(xml_data)
        
        for factura_elem in root.findall('./facturas/factura'):
            numero_factura = factura_elem.find('numeroFactura').text
            nit_cliente = factura_elem.find('NITcliente').text
            fecha = factura_elem.find('fecha').text
            valor = float(factura_elem.find('valor').text)
            facturas.append(Factura(numero_factura, nit_cliente, fecha, valor).to_dict())

        for pago_elem in root.findall('./pagos/pago'):
            codigo_banco = pago_elem.find('codigoBanco').text
            fecha = pago_elem.find('fecha').text
            nit_cliente = pago_elem.find('NITcliente').text
            valor = float(pago_elem.find('valor').text)
            pagos.append(Pago(codigo_banco, fecha, nit_cliente, valor).to_dict())

        return jsonify({"message": "Transacciones procesadas y grabadas correctamente"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/limpiarDatos', methods=['POST'])
def limpiar_datos():
    try:
        # Limpiar datos
        del facturas[:]
        del pagos[:]
        return jsonify({"message": "Datos limpiados correctamente"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/devolverEstadoCuenta', methods=['GET'])
def devolver_estado_cuenta():
    # Lógica para devolver el estado de cuenta
    #estado_cuenta = 
    return jsonify({"estado_cuenta": estado_cuenta})

@app.route('/devolverResumenPagos', methods=['GET'])
def devolver_resumen_pagos():
    # Lógica para devolver el resumen de pagos
    #resumen_pagos 
    return jsonify({"resumen_pagos": resumen_pagos})

if __name__ == '__main__':
    app.run(debug=True)
