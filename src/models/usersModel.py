import base64
import datetime
import os
from flask_jwt_extended import create_access_token
from database.db import get_connection
from werkzeug.security import generate_password_hash, check_password_hash
from models.entities.users import Users
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = "C:\imgPruebas"  # Asegúrate de usar barras diagonales hacia adelante para la ruta

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

class UserModel:
    @classmethod
    def register_user(cls, user_data):
        hashed_password = generate_password_hash(user_data['Password'], method='pbkdf2:sha256')

        try:
            connection = get_connection()
            with connection.cursor() as cursor:
                img_filename = None
                if user_data.get('Img'):
                    file = user_data['Img']
                    if file and cls.allowed_file(file.filename):
                        filename = secure_filename(file.filename)
                        file.save(os.path.join(UPLOAD_FOLDER, filename))
                        img_filename = os.path.join(UPLOAD_FOLDER, filename)  # Guardar la ruta completa
                    else:
                        raise Exception('Formato de archivo no permitido o no se ha seleccionado ningún archivo')

                # Guardar la referencia en la base de datos
                cursor.execute('INSERT INTO person (Name, Address, Mail, UserName, Password, Age, Img) VALUES (%s, %s, %s, %s, %s, %s, %s)',
                            (user_data['Name'], user_data['Address'], user_data['Mail'], user_data['UserName'],
                            hashed_password, user_data['Age'], img_filename))
            connection.commit()
            connection.close()
            return True

        except Exception as ex:
            raise Exception(str(ex))

    @staticmethod
    def allowed_file(filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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
                    user = Users(
                        Id_person=result[0],
                        Name=result[1],
                        Address=result[2],
                        Mail=result[3],
                        UserName=result[4],
                        Password=result[5],
                        Age=result[6],
                        Img=result[7]  # Asegúrate de que la clase Users acepte este argumento en su constructor
                    )

                    img_path = result[7]
                    if img_path:
                        with open(img_path, 'rb') as img_file:
                            img_binary = img_file.read()
                        user.Img = base64.b64encode(img_binary).decode('utf-8')
                    else:
                        user.Img = None
                    
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
