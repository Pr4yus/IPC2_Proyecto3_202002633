from flask import Flask, request, jsonify, render_template
import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt
import numpy as np

app = Flask(__name__)

class Cliente:
    def __init__(self, nit, nombre):
        self.nit = nit
        self.nombre = nombre

class Banco:
    def __init__(self, codigo, nombre):
        self.codigo = codigo
        self.nombre = nombre

class Transaccion:
    def __init__(self, tipo, monto):
        self.tipo = tipo
        self.monto = monto

class ProcesadorDatos:
    def __init__(self):
        self.clientes = {}
        self.transacciones = {}

    def procesar_configuracion(self, data):
        try:
            root = ET.fromstring(data)
            for cliente_xml in root.find('clientes').findall('cliente'):
                nit = cliente_xml.find('NIT').text
                nombre = cliente_xml.find('nombre').text
                self.clientes[nit] = Cliente(nit, nombre)

            # No necesitamos procesar los bancos para el estado de cuenta

        except ET.ParseError as e:
            print("Error de análisis XML de configuración:", e)

    def procesar_transacciones(self, data):
        try:
            root = ET.fromstring(data)
            for transaccion_xml in root.find('transacciones').findall('transaccion'):
                nit = transaccion_xml.find('NIT').text
                tipo = transaccion_xml.find('tipo').text
                monto = float(transaccion_xml.find('monto').text)
                if nit in self.transacciones:
                    self.transacciones[nit].append(Transaccion(tipo, monto))
                else:
                    self.transacciones[nit] = [Transaccion(tipo, monto)]
        except ET.ParseError as e:
            print("Error de análisis XML de transacciones:", e)

    def obtener_estado_cuenta(self, nit_cliente):
        # Verificar si el cliente existe en los datos cargados
        if nit_cliente in self.clientes:
            cliente = self.clientes[nit_cliente]
            # Inicializar el saldo actual del cliente
            saldo_actual = 0
            # Inicializar la lista de transacciones del cliente
            transacciones_cliente = []

            # Verificar si hay transacciones asociadas con el cliente
            if nit_cliente in self.transacciones:
                transacciones_cliente = self.transacciones[nit_cliente]
                # Calcular el saldo actual sumando todas las transacciones
                for transaccion in transacciones_cliente:
                    saldo_actual += transaccion.monto

            # Devolver el cliente, el saldo actual y las transacciones
            return cliente, saldo_actual, transacciones_cliente
        else:
            # Si el cliente no existe, devolver None para indicar que no se encontró el cliente
            return None, None, None

procesador_datos = ProcesadorDatos()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/cargarConfiguracion', methods=['POST'])
def cargar_configuracion():
    # Procesar el archivo XML cargado
    archivo_configuracion = request.files['configuracion_file']
    contenido = archivo_configuracion.read()

    procesador_datos.procesar_configuracion(contenido)

    return jsonify({"message": "¡El archivo de configuración se ha cargado correctamente!"})

@app.route('/cargarTransacciones', methods=['POST'])
def cargar_transacciones():
    # Procesar el archivo XML cargado
    archivo_transacciones = request.files['transacciones_file']
    contenido = archivo_transacciones.read()

    procesador_datos.procesar_transacciones(contenido)

    return jsonify({"message": "¡El archivo de transacciones se ha cargado correctamente!"})

@app.route('/consultarEstadoCuenta', methods=['GET'])
def consultar_estado_cuenta():
    nit_cliente = request.args.get('nit_cliente')
    estado_cuenta = procesador_datos.obtener_estado_cuenta(nit_cliente)
    return render_template('estado_cuenta.html', estado_cuenta=estado_cuenta)

def consultar_ingresos(self, mes):
    # Aquí iría la lógica para consultar los ingresos del mes especificado
    # En este ejemplo, simplemente generamos ingresos aleatorios para los últimos 3 meses

    # Meses disponibles (simulación)
    meses = ['enero/2024', 'febrero/2024', 'marzo/2024']

    # Ingresos para los últimos 3 meses (simulación)
    ingresos = [np.random.randint(1000, 5000) for _ in range(3)]

    # Encontrar el índice del mes seleccionado
    try:
        indice_mes = meses.index(mes)
    except ValueError:
        # Si el mes no está en la lista, seleccionamos el último mes por defecto
        indice_mes = 2

    # Obtener los últimos 3 meses y sus ingresos correspondientes
    ultimos_meses = meses[indice_mes::-1]
    ultimos_ingresos = ingresos[indice_mes::-1]

    return ultimos_meses, ultimos_ingresos

# @app.route('/consultarIngresos', methods=['GET'])
# def consultar_ingresos():
#     mes = request.args.get('mes')
#
#     # Consultar los ingresos para el mes especificado
#     meses, ingresos = procesador_datos.consultar_ingresos(mes)
#
#     # Verificar si hay datos disponibles
#     if meses and ingresos:
#         # Generar la gráfica si hay datos
#         plt.barh(meses, ingresos)
#         plt.xlabel('Ingresos')
#         plt.ylabel('Mes')
#         plt.title('Ingresos por mes')
#         plt.tight_layout()
#
#         # Guardar la gráfica en un archivo temporal
#         nombre_archivo = 'ingresos.png'
#         plt.savefig(nombre_archivo)
#
#         # Renderizar la plantilla HTML con la gráfica incrustada
#         return render_template('ingresos.html', nombre_archivo=nombre_archivo, meses=meses, ingresos=ingresos)
#     else:
#         # Si no hay datos disponibles, mostrar un mensaje adecuado
#         mensaje = "No hay datos disponibles"
#         return render_template('ingresos.html', mensaje=mensaje)



if __name__ == '__main__':
    app.run(debug=True)
