from flask import Blueprint, jsonify

main=Blueprint('user_blueprint', __name__)

@main.route('/')
def get_users():
    return jsonify('hola')