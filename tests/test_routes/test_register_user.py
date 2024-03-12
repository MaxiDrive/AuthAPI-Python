import json
from flask import Flask
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

    app.config['MYSQL_HOST'] = 'test-mysql-host'
    app.config['MYSQL_USER'] = 'test-mysql-user'
    app.config['MYSQL_PASSWORD'] = 'test-mysql-password'
    app.config['MYSQL_DB'] = 'test-mysql-db'

    return app

@pytest.fixture
def client(app):
    return app.test_client()

@patch('models.usersModel.generate_password_hash')
@patch('models.usersModel.get_connection')
def test_register_user(mock_get_connection, mock_generate_password_hash, client):
    data = {
        'Name': 'John Doe',
        'Address': '123 Main St',
        'Mail': 'john@example.com',
        'UserName': 'john_doe',
        'Password': 'password123',
        'Age': 25,
        'Img': 'profile.jpg'
    }

    mock_generate_password_hash.return_value = 'hashed_password'
    mock_connection = MagicMock()
    mock_get_connection.return_value = mock_connection

    response = client.post('/register', json=data)
    assert response.status_code == 400
