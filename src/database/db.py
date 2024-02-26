import mysql.connector
from mysql.connector import Error
from decouple import config


def get_connection():
    try:
        return mysql.connector.connect(
            host=config('MYSQL_HOST'),
            user=config('MYSQL_USER'),
            password=config('MYSQL_PASSWORD'),
            database=config('MYSQL_DB')
        )
    except Error as ex:
        print(f"Error during database connection: {ex}")
        return None
