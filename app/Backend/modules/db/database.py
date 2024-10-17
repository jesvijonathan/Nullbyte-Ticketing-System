from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from google.cloud.sql.connector import Connector
import pymysql
from time import sleep
# from modules.log import *
from config import * 


# Connect to the newly created database
for _ in range(10):
    try:
        # Create the database if it does not exist
        try:
            if(useCloudSql):
                print("Connected to cloudsql")
                connection_name = CLOUD_SQL_CONNECTION_NAME
                connector = Connector()
                connection = connector.connect(connection_name,"pymysql",user=DATABASE_USER, password=DATABASE_PASSWORD, db=DATABASE_NAME)
                with connection.cursor() as cursor:
                    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DATABASE_NAME}")

            else:    
                print("Connected to local")
                connection = pymysql.connect(
                host=DATABASE_HOST,
                port=int(DATABASE_PORT),
                user=DATABASE_USER,
                password=DATABASE_PASSWORD
                )
                print(f"Database '{DATABASE_NAME}' created or already exists.")
        except pymysql.MySQLError as e:
            print(f"Error creating database: {e}")
            raise 
        
        engine = create_engine(DATABASE_URL)
        Base = declarative_base()
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        db_session = Session()
        print("Database connection established successfully")
        break
    except Exception as e:
        print(f"Database connection failed: {e}")
        print("Retrying in 3 seconds")
        sleep(5)
else:
    raise Exception("Failed to connect to the database after multiple attempts")