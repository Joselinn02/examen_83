from flask import Flask
import os
from db import db
from routes.alumno_routes import alumno_bp
from routes.auth_routes import auth_bp
from flasgger import Swagger

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    "pool_pre_ping": True,
    "pool_recycle": 280,
    "pool_size": 1,
    "max_overflow": 0,
}

template = {
    "swagger": "2.0",
    "info": {
        "title": "API Alumnos",
        "description": "API REST para gestión de alumnos",
        "version": "1.0"
    }
}
Swagger(app, template=template)
db.init_app(app)

with app.app_context():
    db.create_all()

app.register_blueprint(alumno_bp, url_prefix="/alumnos")
app.register_blueprint(auth_bp, url_prefix="/auth")

if __name__ == "__main__":
    app.run(debug=True)