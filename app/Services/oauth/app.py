import os
import ldap
import jwt
from flask import Flask, request, make_response, jsonify
import datetime
import logging
import secrets
from flask_cors import CORS


app = Flask(__name__)
CORS(app) # currently allowing all traffic kindly change it in future thank you!!

LDAP_SERVER = "ldap://DC01.nullbyte.exe" # need to change it to env variable in future
JWT_SECRET = os.getenv("JWT_SECRET") or secrets.token_urlsafe(32)
JWT_ALGORITHM = 'HS256'
JWT_EXP_DELTA_SECONDS = 36000

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_jwt(username):
    payload = {
        'sub': username,
        'iat': datetime.datetime.utcnow(),
        'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=JWT_EXP_DELTA_SECONDS)
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return token

@app.route("/sso/auth", methods=["POST"])
def authenticate():
    if not request.is_json:
        return make_response(jsonify({'error':'Request must be Json'}), 400)
    
    body = request.json
    username = body.get('email')
    password = body.get('password')
    
    if not username or not password:
        return make_response(jsonify({'error':'email and password are required'}), 400)
    
    logger.info(f"Authenticating user: {username}")
    
    conn = ldap.initialize(LDAP_SERVER)
    conn.protocol_version = 3
    conn.set_option(ldap.OPT_REFERRALS, 0)
    
    try:
        conn.simple_bind_s(username, password)
        logger.info("Authentication successful.")
        token = create_jwt(username)
        return make_response(jsonify({'token': token}), 201)
    except ldap.INVALID_CREDENTIALS:
        logger.warning("Invalid credentials for user: %s", username)
        return make_response(jsonify({'error': 'Invalid username or password'}), 401)
    except ldap.LDAPError as e:
        logger.error("LDAP error: %s", str(e))
        return make_response(jsonify({'error': 'LDAP authentication error'}), 500)
    except Exception as e:
        logger.error("An unexpected error occurred: %s", str(e))
        return make_response(jsonify({'error': 'An unexpected error occurred'}), 500)
    finally:
        conn.unbind()

if __name__ == '__main__':
    app.run(debug=True)
