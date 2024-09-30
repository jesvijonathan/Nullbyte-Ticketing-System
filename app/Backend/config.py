import os
import secrets
import logging

LDAP_SERVER = os.getenv("LDAP_SERVER", "ldap://DC01.nullbyte.exe") 
JWT_SECRET = os.getenv("JWT_SECRET") or secrets.token_urlsafe(32)

if not JWT_SECRET:
    raise ValueError("JWT_SECRET must be set in the environment variables")

JWT_ALGORITHM = 'HS256'
JWT_EXP_DELTA_SECONDS = 36000

# Admin Creds
ADMIN_CRED=dict({
    'username':'Administrator@nullbyte.exe',
    'password':'rasmiaboobuckerr'
})

#logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)