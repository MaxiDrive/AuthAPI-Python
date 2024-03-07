from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager
from config import config
from routes import authRoutes

app = Flask(__name__)

# Configuración de Flask-JWT-Extended
app.config['JWT_SECRET_KEY'] = config['development'].SECRET_KEY
jwt = JWTManager(app)

def page_not_found(error):
    return "<h1>Not found page</h1>", 404

if __name__ == '__main__':
    app.config.from_object(config['development'])

    # Blueprints
    app.register_blueprint(authRoutes.auth_blueprint, url_prefix='/api/auth')

    # Error handlers
    app.register_error_handler(404, page_not_found)
    app.run()
