import requests
import time
import json

TOKEN = "token_servicio_2"
URL = "http://127.0.0.1:5000/logs"

def generar_log():
    log = {
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "nombre_servicio": "servicio_2",
        "nivel_log": "INFO",
        "mensaje": "Este es un mensaje de log del servicio 2",
        "detalles": "Detalles adicionales"
    }
    return log

def enviar_log(log):
    headers = {
        "Authorization": f"Bearer {TOKEN}",
        "Content-Type": "application/json"
    }
    response = requests.post(URL, headers=headers, data=json.dumps(log))
    print(f"Respuesta del servidor: {response.status_code} - {response.text}")

if __name__ == "__main__":
    while True:
        log = generar_log()
        enviar_log(log)
        time.sleep(10)  # Esperar 10 segundos antes de enviar el siguiente log
