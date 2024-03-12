from unittest.mock import MagicMock, patch
import json
from flask import Flask
from models.usersModel import UserModel

def test_get_user_by_username():
    app = Flask(__name__)

    with app.test_request_context('/user/john_doe'):
        user_data = {
            'Name': 'John Doe',
            'Address': '123 Main St',
            'Mail': 'john@example.com',
            'UserName': 'john_doe',
            'Password': 'password123',
            'Age': 25,
            'Img': 'profile.jpg'
        }

        # Crear un mock para la conexión a la base de datos
        mock_connection = MagicMock()
        
        # Utilizar el decorador patch para sustituir get_connection por el mock_connection
        with patch('models.usersModel.get_connection', return_value=mock_connection):
            # Registrar al usuario antes de la obtención por nombre de usuario
            UserModel.register_user(user_data)

            # Configurar el comportamiento del cursor y fetchone del mock_connection
            mock_cursor = MagicMock()
            mock_cursor.fetchone.side_effect = [(i, *user_data.values())for i in range(1, 6)]
            mock_connection.cursor.return_value.__enter__.return_value = mock_cursor

            # Hacer la solicitud de obtención del usuario por nombre de usuario
            user = UserModel.get_user_by_username('john_doe')

            print(user)

            assert user is not None
            assert user.UserName == 'john_doe'


# Ejecutar la prueba
# pytest -v -o log_cli_level=INFO C:\Users\ASUS\Documents\GitHub\AuthAPI-Python\tests\test_models\test_get_user_by_username.py
# pytest -v -o log_cli_level=INFO C:\Users\ASUS\Documents\GitHub\AuthAPI-Python\tests\test_models\
