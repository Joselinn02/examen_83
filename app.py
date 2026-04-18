from flask import Flask
from dotenv import load_dotenv
import os
from sqlalchemy import create_engine, text
from db import db
from routes.alumno_routes import alumno_bp
from routes.auth_routes import auth_bp
from flasgger import Swagger

# Cargar variables de entorno
load_dotenv()

app = Flask(__name__)

# Configuración de base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    "pool_pre_ping": True,
    "pool_recycle": 280,
    "pool_size": 1,
    "max_overflow": 0,
}

# Configuración de Swagger
template = {
    "swagger": "2.0",
    "info": {
        "title": "API Alumnos",
        "description": "API REST para gestión de alumnos",
        "version": "1.0"
    },
    "securityDefinitions": {
        "Bearer": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header",
            "description": "JWT Token - Ingresa: Bearer {token}"
        }
    },
    "security": [{"Bearer": []}],
    "tags": [
        {"name": "Alumnos", "description": "Operaciones con alumnos"},
        {"name": "Auth", "description": "Autenticación"}
    ]
}

swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": 'apispec_1',
            "route": '/apispec_1.json',
            "rule_filter": lambda rule: True,
            "model_filter": lambda tag: True,
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/apidocs/",
    "swagger_ui_config": {
        "docExpansion": "list",
        "filter": True,
        "showRequestHeaders": True,
        "apisSorter": "alpha",
        "operationsSorter": "alpha",
        "displayRequestDuration": True,
        "deepLinking": True
    }
}

swagger = Swagger(app, template=template, config=swagger_config)

# Inicializar extensión DB
db.init_app(app)

# --- BLOQUE DE CREACIÓN AUTOMÁTICA DE BASE DE DATOS ---
def setup_database():
    uri = app.config['SQLALCHEMY_DATABASE_URI']
    # Obtenemos la conexión base al servidor sin la DB específica
    base_uri = uri.rsplit('/', 1)[0] + '/'
    db_name = uri.rsplit('/', 1)[1]
    
    engine = create_engine(base_uri)
    with engine.connect() as conn:
        conn.execute(text(f"CREATE DATABASE IF NOT EXISTS {db_name};"))
        conn.commit()
    print(f"Base de datos '{db_name}' verificada/creada correctamente.")

with app.app_context():
    setup_database() # Crear la DB si no existe
    db.create_all()  # Crear las tablas

# Registrar Blueprints
app.register_blueprint(alumno_bp, url_prefix="/alumnos")
app.register_blueprint(auth_bp, url_prefix="/auth")

if __name__ == "__main__":
    app.run(debug=True)