import jwt
from datetime import datetime, timedelta

SECRET_KEY = "super_secret_key"  

def login(data):
    if not data:
        return None

    username = data.get("username")
    password = str(data.get("password"))  # normalizamos

    # Usuario hardcodeado (examen)
    if username == "admin" and password == "1234":
        return {
            "msg": "Login exitoso",
            "user": username
        }

    return None