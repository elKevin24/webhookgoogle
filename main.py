import functions_framework
from flask import jsonify

@functions_framework.http
def hello_http(request):
    """HTTP Cloud Function compatible con Dialogflow CX."""
    req = request.get_json(silent=True) or {}

    # Caso: viene de Dialogflow CX
    if "fulfillmentInfo" in req:
        params = req.get("sessionInfo", {}).get("parameters", {}) or {}
        nit = params.get("nit", "desconocido")

        # Verifica último dígito numérico
        digitos = "".join(c for c in str(nit) if c.isdigit())
        if digitos:
            ultimo = int(digitos[-1])
            if ultimo % 2 == 0:
                msg = f"El NIT {nit} está OMISO (termina en número par)."
            else:
                msg = f"El NIT {nit} no tiene omisos (termina en número impar)."
        else:
            msg = f"El NIT recibido ({nit}) no contiene dígitos válidos."

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
