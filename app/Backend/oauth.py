import datetime
import jwt
import ldap
import logging
from config import *

logger = logging.getLogger(__name__)

def create_jwt(username):
    payload = {
        'sub': username,
        'iat': datetime.datetime.utcnow(),
        'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=JWT_EXP_DELTA_SECONDS)
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return token

def authenticate_user(username, password):
    # print(ADMIN_CRED)
    # print(ADMIN_CRED["username"], ADMIN_CRED["password"])
    # print(username, password)

    if ADMIN_CRED["username"]==username  and  ADMIN_CRED["password"]==password:

        return create_jwt(username), None

    conn = ldap.initialize('ldap://DC01.nullbyte.exe') 
    conn.protocol_version = 3
    conn.set_option(ldap.OPT_REFERRALS, 0)

    try:
        conn.simple_bind_s(username, password)
        logger.info("Authentication successful.")
        return create_jwt(username)
    except ldap.INVALID_CREDENTIALS:
        logger.warning("Invalid credentials for user: %s", username)
        return None, 'Invalid username or password'
    except ldap.LDAPError as e:
        logger.error("LDAP error: %s", str(e))
        return None, 'LDAP authentication error'
    except Exception as e:
        logger.error("An unexpected error occurred: %s", str(e))
        return None, 'An unexpected error occurred'
    finally:
        conn.unbind()
