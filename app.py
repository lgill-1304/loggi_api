from flask import Flask, request, jsonify, abort
import sqlite3
from datetime import datetime
from autenticacion import verificar_token
from base_datos import obtener_conexion_bd, crear_tabla


app = Flask(__name__)

# Función para conectarse a la base de datos SQLite
def obtener_conexion_bd():
    conexion = sqlite3.connect('logs.db')
    conexion.row_factory = sqlite3.Row
    return conexion

# Crear la tabla de logs si no existe
crear_tabla()

# Endpoint o punto de acceso para recibir logs
@app.route('/logs', methods=['POST'])
def recibir_log():
    log = request.json
    
    verificar_token() #verificar autenticacion de token
    log = request.json

    # Validar los campos necesarios
    if not all(key in log for key in ("timestamp", "nombre_servicio", "nivel_log", "mensaje", "detalles", "received_at")):
        return jsonify({"error": "Faltan campos obligatorios"}), 400
    
    # Fecha de recepción del log
    fecha_recepcion = datetime.utcnow().isoformat() + "Z"
    
    # Insertar el log en la base de datos
    conexion = obtener_conexion_bd()
    conexion.execute('''
        INSERT INTO logs (timestamp, nombre_servicio, nivel_log, mensaje, detalles,received_at)
        VALUES (?, ?, ?, ?, ?)
    ''', (
        log['timestamp'],
        log['nombre_servicio'],
        log['nivel_log'],
        log['mensaje'],
        str(log.get('detalles')),
        log['received_at'] #guarda la fecha de recepcion
    ))
    conexion.commit()
    conexion.close()
    
    return jsonify({"estado": "Log almacenado con éxito"}), 201

# Endpoint para consultar logs (opcional, para verificar)
@app.route('/logs', methods=['GET'])
def obtener_logs():
    consulta = "SELECT * FROM logs WHERE 1=1"
    parametros = []
    
    nombre_servicio = request.args.get('nombre_servicio')
    nivel_log = request.args.get('nivel_log')
    tiempo_inicio = request.args.get('tiempo_inicio')
    tiempo_fin = request.args.get('tiempo_fin')
    recepcion_inicio = request.args.get('recepcion_inicio')
    recepcion_fin = request.args.get('recepcion_fin')

    if nombre_servicio:
        consulta += " AND nombre_servicio = ?"
        parametros.append(nombre_servicio)
    
    if nivel_log:
        consulta += " AND nivel_log = ?"
        parametros.append(nivel_log)
    
    if tiempo_inicio and tiempo_fin:
        consulta += " AND timestamp BETWEEN ? AND ?"
        parametros.extend([tiempo_inicio, tiempo_fin])

    # Filtrar por rango de fechas de recepción
    if recepcion_inicio and recepcion_fin:
        consulta += " AND received_at BETWEEN ? AND ?"
        parametros.extend([recepcion_inicio, recepcion_fin])
    
    # Ordenar por fecha de recepción, de más reciente a más antiguo
    consulta += " ORDER BY received_at DESC"
    conexion = obtener_conexion_bd()
    logs = conexion.execute(consulta, parametros).fetchall()
    conexion.close()
    
    # Convertir los resultados a una lista de diccionarios
    lista_logs = [dict(log) for log in logs]
    
    return jsonify(lista_logs)

if __name__ == '__main__':
    app.run(host='localhost', port= 5000, debug=True)

