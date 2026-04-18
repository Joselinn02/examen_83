from flask import Blueprint, request, jsonify
from controllers.authController import login

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login_route():
    """
    Login de usuario
    ---
    tags:
      - Auth
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - username
            - password
          properties:
            username:
              type: string
              example: admin
            password:
              type: string
              example: "1234"
    responses:
      200:
        description: Login exitoso
        schema:
          type: object
          properties:
            msg:
              type: string
              example: Login exitoso
            user:
              type: string
              example: admin
      401:
        description: Credenciales incorrectas
      400:
        description: Datos incompletos
    """
    data = request.json

    # Validación básica
    if not data:
        return jsonify({"error": "Datos requeridos"}), 400

    result = login(data)

    if not result:
        return jsonify({"error": "Credenciales incorrectas"}), 401

    return jsonify(result), 200