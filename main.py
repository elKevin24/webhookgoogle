import functions_framework
from flask import jsonify

@functions_framework.http
def hello_http(request):
    """HTTP Cloud Function compatible con Dialogflow CX."""
    req = request.get_json(silent=True) or {}

    # Caso: viene de Dialogflow CX
    if "fulfillmentInfo" in req:
        params = req.get("sessionInfo", {}).get("parameters", {}) or {}
        # Recupera parámetro 'nit' si existe, si no usa 'desconocido'
        nit = params.get("nit", "desconocido")
        msg = f"El NIT recibido es: {nit}"
        return jsonify({
            "fulfillment_response": {
                "messages": [
                    {"text": {"text": [msg]}}
                ]
            },
            "sessionInfo": {"parameters": params}
        })

    # Caso: prueba directa (navegador o Postman)
    request_args = request.args
    if req and 'name' in req:
        name = req['name']
    elif request_args and 'name' in request_args:
        name = request_args['name']
    else:
        name = 'World'
    return f'Hello {name}!'
