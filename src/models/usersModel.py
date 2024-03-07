import datetime

from flask_jwt_extended import create_access_token
from database.db import get_connection
from werkzeug.security import generate_password_hash, check_password_hash
from models.entities.users import Users

class UserModel:
    @classmethod
    def register_user(cls, username, password):
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

        try:
            connection = get_connection()
            with connection.cursor() as cursor:
                cursor.execute('INSERT INTO login (user, password) VALUES (%s, %s)', (username, hashed_password))
            connection.commit()
            connection.close()
            return True

        except Exception as ex:
            raise Exception(str(ex))

    @classmethod
    def authenticate_user(cls, username, password):
        user = cls.get_user_by_username(username)

        if user and check_password_hash(user.Password, password):
            return True
        else:
            return False


    @classmethod
    def get_user_by_username(cls, username):
        try:
            connection = get_connection()
            with connection.cursor() as cursor:
                cursor.execute('SELECT * FROM login WHERE user = %s', (username,))
                result = cursor.fetchone()
                if result:
                    user = Users(Id_login=result[0], User=result[1], Password=result[2], person_Id_person=result[3])
                    return user
                else:
                    return None
        except Exception as ex:
            raise Exception(str(ex))

    @classmethod
    def get_access_token(cls, username):
        # Obtener el usuario
        user = cls.get_user_by_username(username)

        # Crear un token con tiempo de expiración de 1 hora
        expires = datetime.timedelta(hours=1)
        access_token = create_access_token(identity={'username': user.User}, expires_delta=expires)

        return access_token
