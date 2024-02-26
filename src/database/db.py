import mysql.connector
from mysql.connector import Error
from decouple import config

def get_connection():
    try:
        return mysql.connector.connect(
            host=config('MYSQL_HOST'),
            port=config('MYSQL_PORT'),
            user=config('MYSQL_USER'),
            password=config('MYSQL_PASSWORD'),
            database=config('MYSQL_DATABASE')
        )
    except Error as ex:
        raise ex
