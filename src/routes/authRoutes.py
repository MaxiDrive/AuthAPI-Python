import base64
import os
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.usersModel import UserModel

auth_blueprint = Blueprint('auth_blueprint', __name__)

@auth_blueprint.route('/register', methods=['POST'])
def register_user():
    data = request.form
    img_file = request.files.get('img') if 'img' in request.files else None

    user_data = {
        'Name': data.get('name'),
        'Address': data.get('address'),
        'Mail': data.get('mail'),
        'UserName': data.get('username'),
        'Password': data.get('password'),
        'Age': data.get('age'),
        'Img': img_file
    }

    if not all(user_data.values()):
        return jsonify({'message': 'Faltan datos obligatorios'}), 400

    try:
        UserModel.register_user(user_data)
        return jsonify({'message': 'Usuario registrado exitosamente'}), 201

    except Exception as ex:
        return jsonify({'message': str(ex)}), 500

@auth_blueprint.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'message': 'Falta nombre de usuario o contraseña'}), 400

    if UserModel.authenticate_user(username, password):
        access_token = UserModel.get_access_token(username)
        return jsonify(access_token=access_token), 200
    else:
        return jsonify({'message': 'Credenciales incorrectas'}), 401

@auth_blueprint.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    try:
        current_user = get_jwt_identity()
        user = UserModel.get_user_by_username(current_user['username'])

        if user:
            user_info = user.to_JSON()

            img_path = user_info.get('Img')
            if img_path and os.path.exists(img_path):
                with open(img_path, 'rb') as img_file:
                    img_binary = img_file.read()
                img_base64 = base64.b64encode(img_binary).decode('utf-8')
                user_info['Img'] = img_base64

            return jsonify(user_info), 200
        else:
            return jsonify(message="Usuario no encontrado"), 404

    except Exception as e:
        return jsonify(error=str(e)), 500
