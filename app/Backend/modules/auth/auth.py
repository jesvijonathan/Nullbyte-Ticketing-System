from functools import wraps
import jwt
from flask import Blueprint, request, make_response, jsonify
import datetime
from .ldap_wrapper import Lwrapper
from modules.log import *
from config import *
# from flask import session

auth_ldap = Blueprint('auth', __name__)
lwrapper=Lwrapper()


@auth_ldap.post('/auth')
def authenticate():
    if request.is_json:
        body = request.json
    else:
        body = request.form

    username = body.get('email')
    password = body.get('password')
    payload = {}

    if not username or not password:
        return make_response(jsonify({'error': 'email and password are required'}), 400)

    logger.info(f"Authenticating user: {username}")

    if username == ADMIN_CRED['username'] and password == ADMIN_CRED['password']:
        payload = {'username': 'Administrator', 'ou': [], 'upn': 'administrator@nullbyte.exe'}
    elif lwrapper.Authenticate(username, password):
        payload = lwrapper.getPayload(username)

    payload['iat'] = datetime.datetime.now(datetime.timezone.utc)
    payload['exp'] = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(seconds=JWT_EXP_DELTA_SECONDS)
    logger.info(payload)

    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

    if token:
        response = make_response(jsonify({'token': token, 'message': 'Authentication successful'}), 201)
        response.set_cookie('session', token, httponly=False, secure=True)
        response.set_cookie('user', username, httponly=False, secure=True)
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
            logging.debug("Session Cookie: %s", request.cookies['session'])
            token = request.cookies['session']
        
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401
        
        try:
            data = jwt.decode(token, JWT_SECRET, JWT_ALGORITHM)
            logging.debug("Decoded JWT data: %s", data)
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired!'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Invalid token!'}), 401

        # Check if the decorated function accepts 'payload' as a keyword argument
        if 'payload' in f.__code__.co_varnames:
            kwargs['payload'] = data  # Store payload in kwargs if the function accepts it

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