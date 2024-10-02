from flask import Blueprint
import datetime
import jwt
from wrapper.ldap_wrapper import Lwrapper;
from flask import request, make_response, jsonify
from config import *
auth_ldap=Blueprint('auth',__name__)

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
    
    if Lwrapper().Authenticate(username,password):
        payload = {
        'sub': username,
        'iat': datetime.datetime.utcnow(),
        'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=JWT_EXP_DELTA_SECONDS)
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    if token:
        return make_response(jsonify({'token': token}), 201)