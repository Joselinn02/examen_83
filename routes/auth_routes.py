from flask import Blueprint, request, jsonify
from controllers.authController import login
import jwt
import os
from datetime import datetime, timedelta

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login_route():
    """
    Login de usuario y obtención de token JWT
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
            token:
              type: string
            user:
              type: string
    """
    data = request.json

    if not data:
        return jsonify({"error": "Datos requeridos"}), 400

    result = login(data)

    if not result:
        return jsonify({"error": "Credenciales incorrectas"}), 401

    # Generar token JWT 
    token = jwt.encode({
        'usuario_id': result.get('id', 1),
        'username': result.get('username', data.get('username')),
        'exp': datetime.utcnow() + timedelta(hours=24)
    }, os.getenv('SECRET_KEY'), algorithm='HS256')

    return jsonify({
        "msg": "Login exitoso",
        "token": token,
        "user": result.get('username', data.get('username'))
    }), 200