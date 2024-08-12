import sqlite3

def obtener_conexion_bd():
    conexion = sqlite3.connect('logs.db')
    conexion.row_factory = sqlite3.Row
    return conexion

def crear_tabla():
    conexion = obtener_conexion_bd()
    conexion.execute('''
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            nombre_servicio TEXT NOT NULL,
            nivel_log TEXT NOT NULL,
            mensaje TEXT NOT NULL,
            detalles TEXT,
            received_at TEXT NOT NULL
        )
    ''')
    conexion.commit()
    conexion.close()
