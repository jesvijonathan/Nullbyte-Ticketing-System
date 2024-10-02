import os
import secrets
from dotenv import load_dotenv

load_dotenv()

LDAP_SERVER = os.getenv("LDAP_SERVER", "ldap://DC01.nullbyte.exe") 
JWT_SECRET = os.getenv("JWT_SECRET") or secrets.token_urlsafe(32)

if not JWT_SECRET:
    raise ValueError("JWT_SECRET must be set in the environment variables")

JWT_ALGORITHM = 'HS256'
JWT_EXP_DELTA_SECONDS = 36000

# Admin Creds
ADMIN_CRED = dict({
    'username': os.getenv('SVC_ACC', 'administrator@nullbyte.exe'),
    'password': os.getenv('SVC_ACC_PASS', 'rasmiaboobuckerr')
})

# Database configuration
DATABASE_HOST = os.getenv("DATABASE_HOST", "localhost")
DATABASE_PORT = os.getenv("DATABASE_PORT", "3306")
DATABASE_USER = os.getenv("DATABASE_USER", "nullbyteadmin")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD", "rootpassword")
DATABASE_NAME = os.getenv("DATABASE_NAME", "nullbyte")
DATABASE_URL = f"mysql+pymysql://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}"
