from functools import wraps
import jwt
from flask import Blueprint, request, make_response, jsonify
import datetime
from .ldap_wrapper import Lwrapper
from ..log import logger
from config import *
# from flask import session

auth_ldap = Blueprint('auth', __name__)

@auth_ldap.post('/auth')
def authenticate():
    if request.is_json:
        body = request.json
    else:
        body = request.form
    username = body.get('email')
    password = body.get('password')

    if not username or not password:
        return make_response(jsonify({'error': 'Email and password are required'}), 400)

    logger.info(f"Authenticating user: {username}")

    if Lwrapper().Authenticate(username, password):
        payload = {
            'sub': username,
            'iat': datetime.datetime.now(datetime.timezone.utc),
            'exp': datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=1)
        }
        token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
        if token:
            response = make_response(jsonify({'token': token, 'message': 'Authentication successful'}), 201)
            response.set_cookie('session', token, httponly=True, secure=True)
            if username in users_token:
                del users[users_token[username]]
            users_token[username] = token
            users[token] = {
                'username': username,
                'added': payload.get('iat'),
                'exp': payload.get('exp'),
            }
            logger.info(f"Session user set to: {username} {token}")
            return response
    return make_response(jsonify({'error': 'Invalid credentials'}), 401)

def cleanup_user(token=None, user_id=None):
    if user_id:
        for key, value in users.items():
            if value["username"] == user_id:
                token = key
                break
    if token:
        del users[token]
        del sockets[token]

def jwt_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(" ")[1]
        elif 'session' in request.cookies:
            print("Session Cookie: ", request.cookies['session'])
            token = request.cookies['session']
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401 
        try:
            data = jwt.decode(token, JWT_SECRET, JWT_ALGORITHM)
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired!'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Invalid token!'}), 401

        return f(*args, **kwargs)

    return decorated

def datetime_to_string(data):
    if isinstance(data, dict):
        return {k: datetime_to_string(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [datetime_to_string(i) for i in data]
    elif isinstance(data, datetime.datetime):
        return data.isoformat()
    return data

@auth_ldap.get('/list_users')
def list_users():
    try:
        serializable_users = datetime_to_string(users)
        return jsonify(serializable_users) 
    except Exception as e:
        print(f"Error while listing users: {str(e)}")
        return jsonify({'error': str(e)}), 500