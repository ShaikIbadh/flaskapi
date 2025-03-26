from flask import Flask, jsonify
import pymysql
pymysql.install_as_MySQLdb()
from flask_mysqldb import MySQL
from flask_jwt_extended import JWTManager
from app.config import Config

mysql = MySQL()
jwt = JWTManager()

# Application factory pattern
def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
# Initialize MySQL and JWT with app context
    mysql.init_app(app)
    jwt.init_app(app)

    # JWT Error Handlers
    @jwt.unauthorized_loader
    def unauthorized_callback(error):
        return jsonify({'error': 'Missing or invalid token'}), 401

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return jsonify({'error': 'Invalid token'}), 401

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return jsonify({'error': 'Token has expired'}), 401

     # General HTTP Error Handlers
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({'error': 'Bad request'}), 400

    @app.errorhandler(401)
    def unauthorized(error):
        return jsonify({'error': 'Unauthorized'}), 401

    @app.errorhandler(403)
    def forbidden(error):
        return jsonify({'error': 'Forbidden'}), 403

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Resource not found'}), 404

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({'error': 'Internal server error'}), 500

    # Register Blueprints
    from app.auth import auth_bp
    from app.routes import main_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)

    return app
