from base64 import encode
from flask import Flask, request, jsonify, make_response, send_file
from sqlalchemy import false
from  werkzeug.security import generate_password_hash, check_password_hash
import jwt
from datetime import datetime, timedelta
from functools import wraps
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from app.src.data.catalog import get_catalog, get_paises
from app.src.data.jugador import get_jugador, insert_jugador, update_jugador
from app.src.data.valoracion import get_valoracion, insert_valoracion, soft_delete_valoracion
from app.src.utils.mapper import Mapper
from app.src.utils.pdf import JugadorInforme
from app.src.utils.utils import Utils
import os
import warnings
import app.src.utils.constants as c
from app.src.data.orm import Equipo, Perfil, Pie, Posicion, Seguimiento, Somatotipo, User, Visualizacion

# Quitar warnings innecesarios de la salida
warnings.filterwarnings('ignore')

# -*- coding: utf-8 -*-
application = Flask(__name__)
application.config['JSON_SORT_KEYS'] = False
application.config[c.SECRET_KEY] = os.environ[c.SECRET_KEY]
application.config[c.SQLALCHEMY_DATABASE_URI] = os.environ[c.SQLALCHEMY_DATABASE_URI]
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(application)
CORS(application)


# usando el decorador @app.route para gestionar los enrutadores (Método GET)
@application.route('/', methods=['GET'])
def root():
    """
        Función para gestionar la salida de la ruta raíz.

        Returns:
           dict.  Mensaje de salida
    """
    return "{'Proyecto':'Futbol'}"


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        # jwt is passed in the request header
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        # return 401 if token is not passed
        if not token:
            return jsonify({'message' : 'Token no encontrado'}), 401
  
        try:
            # decoding the payload to fetch the stored details
            data = jwt.decode(token, application.config['SECRET_KEY'])
            current_user = db.session.query(User)\
                .filter_by(username = data['username'])\
                .first()
        except:
            return jsonify({
                'message' : 'Token invalido'
            }), 401
        # returns the current logged in users contex to the routes
        return  f(current_user, *args, **kwargs)
  
    return decorated


# route for logging user in
@application.route('/api/auth/login', methods =['POST'])
def login():
    # creates dictionary of form data
    auth = request.get_json()
  
    if not auth or not auth.get('email') or not auth.get('password'):
        # returns 401 if any email or / and password is missing
        return make_response(
            'No se ha podido verificar. Login es necesario',
            401,
            {'WWW-Authenticate' : 'Basic realm ="Login es necesario"'}
        )
  
    user = db.session.query(User)\
        .filter_by(email = auth.get('email'))\
        .first()
  
    if not user:
        # returns 401 if user does not exist
        return make_response(
            'Usuario no existe',
            401,
            {'WWW-Authenticate' : 'Basic realm ="Usuario no existe"'}
        )
  
    if check_password_hash(user.password, auth.get('password')):
        # generates the JWT Token
        token = jwt.encode({
            'username': user.username,
            'exp' : datetime.utcnow() + timedelta(minutes = 120)
        }, application.config['SECRET_KEY'])
  
        return make_response(jsonify({'auth-token' : token.decode('UTF-8'),
                                        'auth-user': {
                                            'id_user': user.id_user,
                                            'username': user.username,
                                            'role': user.role.name
                                        }}), 201)
    # returns 403 if password is wrong
    return make_response(
        'Password incorrecta',
        403,
        {'WWW-Authenticate' : 'Basic realm ="Password incorrecta"'}
    )
  
# signup route
@application.route('/api/auth/signup', methods =['POST'])
def signup():
    # creates a dictionary of the form data
    data = request.get_json()
  
    # gets username, email and password
    username, email = data.get('username'), data.get('email')
    password = data.get('password')
  
    # checking for existing user
    user = db.session.query(User)\
        .filter_by(email = email)\
        .first()
    if not user:
        # database ORM object
        user = User(
            username = username,
            email = email,
            password = generate_password_hash(password),
            id_role = 1
        )
        # insert user
        db.session.add(user)
        db.session.commit()

        return make_response('Usuario registrado correctamente.', 201)
    else:
        # returns 202 if user already exists
        return make_response('Usuario ya existe. Por favor Log in.', 202)



@application.route('/jugador', methods=['GET', 'POST', 'PUT','DELETE'])
def jugador():
    if request.method == 'GET':
        args = request.args.to_dict()
        return Mapper().map_jugador_as_json(get_jugador(db, args))
    if request.method == 'POST':
        return insert_jugador(db, request.get_json())
    if request.method == 'PUT':
        return update_jugador(db, request.get_json())

@application.route('/valoracion', methods=['GET', 'POST', 'DELETE'])
@token_required
def valoracion(current_user):
    if request.method == 'GET':
        args = request.args.to_dict()
        return Mapper().map_valoracion_as_json(get_valoracion(db, current_user, args))
    if request.method == 'POST':
        return insert_valoracion(db, request.get_json())
    if request.method == 'DELETE':
        args = request.args.to_dict()
        if c.URL_PARAM_ID_VALORACION in args:
            return soft_delete_valoracion(db, args[c.URL_PARAM_ID_VALORACION])
        else:
            return make_response('Prametro requerido: id_valoracion', 403)
    
@application.route('/informe', methods=['GET'])
@token_required
def get_informe(current_user):
    args = request.args.to_dict()
    if c.URL_PARAM_ID_JUGADOR in args:
        args[c.URL_PARAM_ID] = args[c.URL_PARAM_ID_JUGADOR]
        jugador = get_jugador(db, args)
        valoracion = get_valoracion(db, current_user, args)
        pdf = JugadorInforme().create_informe(current_user, jugador, valoracion)
        
        response = make_response(pdf.output(dest='S').encode('latin1'));
        response.mimetype = 'application/pdf'
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = \
            'inline; filename={}-{}.pdf'.format(jugador.nombre,datetime.now().strftime("%d-%m-%Y_%H:%M:%S"))
        return response
    else:
        return make_response('Prametro requerido: id_jugador', 403)


@application.route('/catalog/equipo', methods=['GET'])
def get_equipo():
    """
        Función para obtener los equipos.

        Returns:
           json. {
                id: id_equipo (numeric),
                descripcion: nombre del equipo (string)
                }
    """
    args = request.args.to_dict()
    return get_catalog(db, Equipo, 'id_equipo', args)
        


@application.route('/catalog/perfil', methods=['GET'])
def get_perfil():
    """
        Función para obtener los perfiles.

        Returns:
           json. {
                id: id_perfil (numeric),
                descripcion: nombre del perfil (string)
                }
    """
    args = request.args.to_dict()
    return get_catalog(db, Perfil, 'id_perfil', args)

@application.route('/catalog/pie', methods=['GET'])
def get_pie():
    """
        Función para obtener los pies.

        Returns:
           json. {
                id: id_pie (numeric),
                descripcion: pie (string)
                }
    """
    args = request.args.to_dict()
    return get_catalog(db, Pie, 'id_pie', args)


@application.route('/catalog/posicion', methods=['GET'])
def get_posicion():
    """
        Función para obtener las posiciones.

        Returns:
           json. {
                id: id_posicion (numeric),
                descripcion: nombre de la posicion (string)
                }
    """
    args = request.args.to_dict()
    return get_catalog(db, Posicion, 'id_posicion', args)


@application.route('/catalog/seguimiento', methods=['GET'])
def get_seguimiento():
    """
        Función para obtener los seguimientos.

        Returns:
           json. {
                id: id_seguimiento (numeric),
                descripcion: nombre del seguimiento (string)
                }
    """
    args = request.args.to_dict()
    return get_catalog(db, Seguimiento, 'id_seguimiento', args)


@application.route('/catalog/somatotipo', methods=['GET'])
def get_somatotipo():
    """
        Función para obtener los somatotipos.

        Returns:
           json. {
                id: id_somatotipo (numeric),
                descripcion: nombre del somatotipo (string)
                }
    """
    args = request.args.to_dict()
    return get_catalog(db, Somatotipo, 'id_somatotipo', args)


@application.route('/catalog/visualizacion', methods=['GET'])
def get_visualizacion():
    """
        Función para obtener los tipo de visualizacion.

        Returns:
           json. {
                id: id_visualizacion (numeric),
                descripcion: nombre de la visualizacion (string)
                }
    """
    args = request.args.to_dict()
    return get_catalog(db, Visualizacion, 'id_visualizacion', args)

@application.route('/catalog/pais', methods=['GET'])
def get_pais():
    """
        Función para obtener los paises.

        Returns:
           json. {
                id: id_pais (numeric),
                nombre: nombre del pais (string)
                codigoISO2: codigoISO2 (string)
                codigoISO3: codigoISO3 (string)
                }
    """
    args = request.args.to_dict()
    return get_paises(db, args)

# main
if __name__ == '__main__':
    # ejecución de la app
    application.run(host='0.0.0.0', port=os.environ[c.APP_PORT], debug=False)
