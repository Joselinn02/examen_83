from models.alumno import Alumno
from db import db
from datetime import datetime

def crear_alumno(data):
    alumno = Alumno(**data)
    db.session.add(alumno)
    db.session.commit()
    return alumno

def obtener_alumnos():
    return Alumno.query.all()

def obtener_por_id(id):
    return Alumno.query.get(id)

def actualizar_alumno(id, data):
    alumno = Alumno.query.get(id)
    if not alumno:
        return None
    
    for key, value in data.items():
        setattr(alumno, key, value)
    
    db.session.commit()
    return alumno

def eliminar_alumno(id):
    alumno = Alumno.query.get(id)
    if not alumno:
        return None
    
    db.session.delete(alumno)
    db.session.commit()
    return True

def alumnos_por_fecha(inicio, fin):
    inicio = datetime.strptime(inicio, "%Y-%m-%d")
    fin = datetime.strptime(fin, "%Y-%m-%d")
    
    return Alumno.query.filter(
        Alumno.fecha_alta.between(inicio, fin)
    ).all()