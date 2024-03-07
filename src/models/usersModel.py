import datetime
from flask_jwt_extended import create_access_token
from database.db import get_connection
from werkzeug.security import generate_password_hash, check_password_hash
from models.entities.users import Users

class UserModel:
    @classmethod
    def register_user(cls, user_data):
        hashed_password = generate_password_hash(user_data['Password'], method='pbkdf2:sha256')

        try:
            connection = get_connection()
            with connection.cursor() as cursor:
                cursor.execute('INSERT INTO person (Name, Address, Mail, UserName, Password, Age, Img) VALUES (%s, %s, %s, %s, %s, %s, %s)',
                            (user_data['Name'], user_data['Address'], user_data['Mail'], user_data['UserName'],
                            hashed_password, user_data['Age'], user_data['Img']))
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
                cursor.execute('SELECT * FROM person WHERE UserName = %s', (username,))
                result = cursor.fetchone()
                if result:
                    user = Users(Id_person=result[0], Name=result[1], Address=result[2], Mail=result[3],
                                UserName=result[4], Password=result[5], Age=result[6], Img=result[7])
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
        access_token = create_access_token(identity={'username': user.UserName}, expires_delta=expires)

        return access_token
