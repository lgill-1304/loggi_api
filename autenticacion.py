from flask import request, abort

tokens_validos = {
    "servicio_1": "token_servicio_1",
    "servicio_2": "token_servicio_2",
    "servicio_3": "token_servicio_3"
}

def verificar_token():
    encabezado_autenticacion = request.headers.get('Authorization')
    if encabezado_autenticacion is None or not encabezado_autenticacion.startswith("Bearer "):
        abort(401, description="Token no proporcionado o mal formado")
        
    token = encabezado_autenticacion.split(" ")[1]

    if token not in tokens_validos.values():
        abort(403, description="Token inválido")
