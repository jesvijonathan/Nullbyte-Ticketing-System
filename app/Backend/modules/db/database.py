import os
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy import engine as sengine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from google.cloud.sql.connector import Connector
import pymysql
from time import sleep
from config import * 

for _ in range(2):
    try:
        if useCloudSql:
            print("Connecting to Cloud SQL...")
            unix_socket_path = f"/cloudsql/{CLOUD_SQL_CONNECTION_NAME}"
            print(f"Unix socket path: {unix_socket_path}")

            connector = Connector()
            connection = connector.connect(CLOUD_SQL_CONNECTION_NAME, "pymysql", user=DATABASE_USER, password=DATABASE_PASSWORD, db='information_schema')

            with connection.cursor() as cursor:
                cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DATABASE_NAME}")
                print(f"Database '{DATABASE_NAME}' created or already exists.")

            engine = create_engine(
                sengine.url.URL.create(
                    drivername="mysql+pymysql",
                    username=DATABASE_USER,
                    password=DATABASE_PASSWORD,
                    database=DATABASE_NAME,
                    query={"unix_socket": unix_socket_path}
                ),
                pool_size=20,
                max_overflow=0,
                pool_timeout=30
            )
        else:
            print("Connecting to local database...")
            connection = pymysql.connect(
                host=DATABASE_HOST,
                port=int(DATABASE_PORT),
                user=DATABASE_USER,
                password=DATABASE_PASSWORD
            )
            with connection.cursor() as cursor:
                cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DATABASE_NAME}")
                print(f"Database '{DATABASE_NAME}' created or already exists.")
            engine = create_engine(DATABASE_URL,pool_size=20,max_overflow=0,pool_timeout=30)

        Base = declarative_base()
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        db_session = scoped_session(Session)
        print("Database connection established successfully")
        break

    except pymysql.MySQLError as e:
        print(f"MySQL error: {e}")
    except Exception as e:
        print(f"Database connection failed: {e}")

    print("Retrying in 3 seconds...")
    sleep(5)
else:
    raise Exception("Failed to connect to the database after multiple attempts")
