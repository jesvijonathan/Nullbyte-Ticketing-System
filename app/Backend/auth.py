import jwt
from flask import Blueprint
from wrapper.ldap_wrapper import Lwrapper;
from flask import request, make_response, jsonify
from functools import wraps
from config import *
import datetime
from log import *

auth_ldap=Blueprint('auth',__name__)
lwrapper=Lwrapper()
@auth_ldap.post('/auth')
def authenticate():
    if not request.is_json:
        return make_response(jsonify({'error': 'Request must be JSON'}), 400)
    body = request.json
    username = body.get('email')
    password = body.get('password')

    if not username or not password:
        return make_response(jsonify({'error': 'email and password are required'}), 400)
    logger.info(f"Authenticating user: {username}")  
    if lwrapper.Authenticate(username,password):
        payload=lwrapper.getPayload(username)
        payload['iat']=datetime.datetime.now(datetime.timezone.utc)
        payload['exp']=datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(seconds=JWT_EXP_DELTA_SECONDS)
        logger.info(payload)
        token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
        if token:
            return make_response(jsonify({'token': token}), 201)
    
def jwt_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(" ")[1]
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401

        try:
            data = jwt.decode(token, JWT_SECRET, JWT_ALGORITHM)
            request.user = data['sub']
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired!'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Invalid token!'}), 401

        return f(*args, **kwargs)

    return decorated