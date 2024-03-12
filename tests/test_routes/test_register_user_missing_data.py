import json
from flask import Flask
from flask_jwt_extended import JWTManager
from unittest.mock import patch
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

def test_register_user_missing_data(client):
    data = {
        'Name': 'John Doe',
        'Address': '123 Main St',
        'Mail': 'john@example.com',
        'UserName': 'john_doe',
        'Age': 25,
        'Img': 'profile.jpg'
    }

    response = client.post('/register', json=data)
    assert response.status_code == 400
