import os
import secrets

LDAP_SERVER = os.getenv("LDAP_SERVER", "ldap://DC01.nullbyte.exe") 
JWT_SECRET = os.getenv("JWT_SECRET") or secrets.token_urlsafe(32)

if not JWT_SECRET:
    raise ValueError("JWT_SECRET must be set in the environment variables")

JWT_ALGORITHM = 'HS256'
JWT_EXP_DELTA_SECONDS = 36000

ADMIN_CRED=dict({
    'username':'admin@nigga.com',
    'password':'nigga'
})