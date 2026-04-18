from flask import Blueprint, request, jsonify
from controllers.alumnoController import *

alumno_bp = Blueprint('alumnos', __name__)

# CREATE
@alumno_bp.route('/', methods=['POST'])

def create():
    """
    Crear alumno
    ---
    tags:
      - Alumnos
   
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - nombre
            - apellido_paterno
            - apellido_materno
            - matricula
            - correo
          properties:
            nombre:
              type: string
              example: baruc
            apellido_paterno:
              type: string
              example: pineda
            apellido_materno:
              type: string
              example: mejia
            matricula:
              type: string
              example: 222310404
            correo:
              type: string
              example: baruc@email.com
    responses:
      201:
        description: Alumno creado correctamente
      401:
        description: No autorizado (token inválido o no enviado)
    """
    data = request.json

    if not data:
        return jsonify({"error": "Datos requeridos"}), 400

    alumno = crear_alumno(data)

    return jsonify({
        "msg": "Alumno creado",
        "alumno": alumno.to_dict()
    }), 201
# get
@alumno_bp.route('/', methods=['GET'])

def get_all():
    """
    Obtener todos los alumnos
    ---
    tags:
      - Alumnos
   
    responses:
      200:
        description: Lista de alumnos
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: integer
                example: 1
              nombre:
                type: string
              
              apellido_paterno:
                type: string
               
              apellido_materno:
                type: string
            
              matricula:
                type: string
             
              correo:
                type: string
                
              fecha_alta:
                type: string
               
      401:
        description: No autorizado (token inválido o no enviado)
    """
    alumnos = obtener_alumnos()
    return jsonify([a.to_dict() for a in alumnos])

# UPDATE
@alumno_bp.route('/<int:id>', methods=['PUT'])
def update(id):
    """
    Actualizar alumno
    ---
    tags:
      - Alumnos
    parameters:
      - name: id
        in: path
        type: integer
        required: true
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            nombre:
              type: string
            apellido_paterno:
              type: string
            apellido_materno:
              type: string
            matricula:
              type: string
            correo:
              type: string
    responses:
      200:
        description: Actualizado
      400:
        description: Error en datos
      404:
        description: No encontrado
    """

    data = request.json

    if not data:
        return jsonify({"error": "Datos requeridos"}), 400

    alumno = Alumno.query.get(id)

    if not alumno:
        return jsonify({"error": "No encontrado"}), 404

    for key, value in data.items():
        setattr(alumno, key, value)

    return jsonify({
        "msg": "Actualizado",
        "alumno": alumno.to_dict()
    })
# DELETE
@alumno_bp.route('/<int:id>', methods=['DELETE'])

def delete(id):
    """
    Eliminar alumno
    ---
    tags:
      - Alumnos
    
    parameters:
      - name: id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Eliminado
      401:
        description: No autorizado
      404:
        description: No encontrado
    """
    if not eliminar_alumno(id):
        return jsonify({"error": "No encontrado"}), 404

    return jsonify({"msg": "Eliminado"})
# FILTRO POR FECHA
@alumno_bp.route('/fecha', methods=['GET'])

def por_fecha():
    """
    Obtener alumnos por rango de fecha
    ---
    tags:
      - Alumnos
    
    parameters:
      - name: inicio
        in: query
        type: string
        required: true
        example: 2026-03-25
      - name: fin
        in: query
        type: string
        required: true
        example: 2026-03-26
    responses:
      200:
        description: Lista filtrada
      401:
        description: No autorizado
    """
    inicio = request.args.get('inicio')
    fin = request.args.get('fin')

    if not inicio or not fin:
        return jsonify({"error": "Parámetros inicio y fin requeridos"}), 400

    alumnos = alumnos_por_fecha(inicio, fin)

    return jsonify([a.to_dict() for a in alumnos])