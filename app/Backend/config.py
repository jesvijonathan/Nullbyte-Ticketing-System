import os
import secrets
import logging
from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import time

load_dotenv()

LDAP_SERVER = os.getenv("LDAP_SERVER", "ldap://DC01.nullbyte.exe") 
JWT_SECRET = os.getenv("JWT_SECRET") or secrets.token_urlsafe(32)

if not JWT_SECRET:
    raise ValueError("JWT_SECRET must be set in the environment variables")

JWT_ALGORITHM = 'HS256'
JWT_EXP_DELTA_SECONDS = 36000


# Admin Creds
ADMIN_CRED=dict({
    'username':os.getenv('SVC_ACC','Administrator@nullbyte.exe'),
    'password':os.getenv('SVC_ACC_PASS','rasmiaboobuckerr')

})
#logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Database
DATABASE_URL = 'mysql+pymysql://nullbyteadmin:rootpassword@nullbyte-ticketing-system-sql-1/nullbyte'

for _ in range(10):
    try:
        engine = create_engine(DATABASE_URL)
        Base = declarative_base()
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        session = Session()
        logger.info("Database connection established successfully")
        break
    except Exception as e:
        logger.error(f"Database connection failed: {e}")
        logger.info("Retrying in 3 seconds")
        time.sleep(5)
else:
    raise Exception("Failed to connect to the database after multiple attempts")