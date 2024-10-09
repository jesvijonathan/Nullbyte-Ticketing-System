from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import pymysql
from time import sleep
from modules.log import *
from config import * 


# Connect to the newly created database
for _ in range(10):
    try:
        # Create the database if it does not exist
        try:
            connection = pymysql.connect(
                host=DATABASE_HOST,
                port=int(DATABASE_PORT),
                user=DATABASE_USER,
                password=DATABASE_PASSWORD
            )
            logger.info(f"Database '{DATABASE_NAME}' created or already exists.")
        except pymysql.MySQLError as e:
            logger.error(f"Error creating database: {e}")
            raise 
        
        engine = create_engine(DATABASE_URL)
        Base = declarative_base()
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        db_session = Session()
        logger.info("Database connection established successfully")
        break
    except Exception as e:
        logger.error(f"Database connection failed: {e}")
        logger.info("Retrying in 3 seconds")
        sleep(5)
else:
    raise Exception("Failed to connect to the database after multiple attempts")