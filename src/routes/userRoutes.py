from flask import Blueprint, jsonify

# Models
from models.usersModel import UserModel


main=Blueprint('user_blueprint', __name__)

@main.route('/')
def get_users():
    try:
        Users = UserModel.get_users()
        return jsonify(Users)
    except Exception as ex:
        return jsonify({'message': str(ex)}),500