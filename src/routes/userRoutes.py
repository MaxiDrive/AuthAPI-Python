from flask import Blueprint, jsonify

# Models
from models.usersModel import UserModel
from models.personModel import PersonModel


main=Blueprint('user_blueprint', __name__)

@main.route('/')
def get_users():
    try:
        Users = UserModel.get_users()
        return jsonify(Users)
    except Exception as ex:
        return jsonify({'message': str(ex)}),500
    

@main.route('/person')
def get_person():
    try:
        person = PersonModel.get_person()
        return jsonify({person})
    except Exception as ex:
        return jsonify({'message':str(ex)}); 500
    