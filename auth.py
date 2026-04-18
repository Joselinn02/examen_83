from functools import wraps
from flask import request, jsonify
import jwt

SECRET_KEY = "super_secret_key"

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

      
        if "Authorization" in request.headers:
            auth_header = request.headers["Authorization"]
            parts = auth_header.split(" ")

            if len(parts) == 2 and parts[0] == "Bearer":
                token = parts[1]

        if not token:
            return jsonify({"error": "Token requerido"}), 401

        try:
        
            data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token expirado"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Token inválido"}), 401

        
        return f(data, *args, **kwargs)

    return decorated