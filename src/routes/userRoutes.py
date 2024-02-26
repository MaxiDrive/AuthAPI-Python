from flask import Blueprint, jsonify
from models.userModel import userModel

main = Blueprint('movie_blueprint',__name__)

@main.route('/')
def get_users():
    try:
        users = userModel.get_users()
        return jsonify(users)
    except Exception as ex:
        return jsonify({'message': str(ex)}),500
    
@main.route('/<id>')
def get_user(id):
    try:
        user=userModel.get_user(id)
        if user != None:
            return jsonify(user)
        else:
            return jsonify({}),404
    except Exception as ex:
        return jsonify({'message': str(ex)}), 500