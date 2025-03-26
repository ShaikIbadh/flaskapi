from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from app.models import get_db_cursor

auth_bp = Blueprint('auth', __name__)

# Register route
@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({'error': 'Username and password are required'}), 400

    username = data['username']
    password = data['password']

    cursor = get_db_cursor()
    cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
    existing = cursor.fetchone()
    
# If user exists, return 409 Conflict
    if existing:
        cursor.close()
        return jsonify({'error': 'User already exists'}), 409
        
# Hash password and insert new user
    hashed_pw = generate_password_hash(password)
    cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, hashed_pw))
    cursor.connection.commit()
    cursor.close()

    return jsonify({'message': 'User registered successfully'}), 201
    
# Login route
@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({'error': 'Username and password are required'}), 400

    username = data['username']
    password = data['password']

    cursor = get_db_cursor()
    cursor.execute("SELECT id, username, password FROM users WHERE username = %s", (username,))
    user = cursor.fetchone()
    cursor.close()

    if not user:
        return jsonify({'error': 'Invalid username or password'}), 401
        
# Check password hash
    user_id, user_name, password_hash = user
    if not check_password_hash(password_hash, password):
        return jsonify({'error': 'Invalid username or password'}), 401
        
# Generate JWT token
    token = create_access_token(identity=str(user_id))
    return jsonify({'access_token': token}), 200
