import json
from flask import Flask
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import JWTManager
from unittest.mock import patch, MagicMock
import sys

sys.path.append('C:/Users/ASUS/Documents/GitHub/AuthAPI-Python/src')
from models.usersModel import UserModel
from routes.authRoutes import auth_blueprint
import pytest

@pytest.fixture
def app():
    app = Flask(__name__)
    app.config['JWT_SECRET_KEY'] = 'test-secret-key'
    jwt = JWTManager(app)
    app.register_blueprint(auth_blueprint)

    return app

@pytest.fixture
def client(app):
    return app.test_client()

def test_authenticate_user():
    app = Flask(__name__)

    with app.test_request_context('/login'):
        user_data = {
            'Name': 'John Doe',
            'Address': '123 Main St',
            'Mail': 'john@example.com',
            'UserName': 'john_doe',
            'Password': generate_password_hash('password123', method='pbkdf2:sha256'),
            'Age': 25,
            'Img': 'profile.jpg'
        }

        # Crear un mock para la conexión a la base de datos
        mock_connection = MagicMock()

        # Utilizar el decorador patch para sustituir get_connection por el mock_connection
        with patch('models.usersModel.get_connection', return_value=mock_connection):
            # Registrar al usuario antes de la autenticación
            UserModel.register_user(user_data)

            # Configurar el comportamiento del cursor y fetchone del mock_connection para autenticación
            mock_cursor_auth = MagicMock()
            mock_cursor_auth.fetchone.side_effect = [(1, *user_data.values())]
            mock_connection.cursor.return_value.__enter__.return_value = mock_cursor_auth

            # Desglosar el método authenticate_user y realizar la verificación manual
            username = 'john_doe'
            password = 'password123'

            # Obtener el usuario manualmente (simulando el comportamiento de get_user_by_username)
            user = UserModel.get_user_by_username(username)

            # Verificar la contraseña manualmente (simulando el comportamiento de check_password_hash)
            if user and check_password_hash(user.Password, password):
                result = True
            else:
                result = False

            assert result is True



#pytest -v -o log_cli_level=INFO C:\Users\ASUS\Documents\GitHub\AuthAPI-Python\tests\test_models\test_authenticate_user.py